"""
═══════════════════════════════════════════════════════════════════════
                      TEXT SUMMARIZER  —  UI MODULE
═══════════════════════════════════════════════════════════════════════
This is the user interface (UI) file for a desktop Text Summarizer app.
It is built with Python's Tkinter library and gives users a clean,
green-themed window to interact with an AI summarizer that runs locally
on their computer (using Ollama with the phi3:mini model — fully offline).

MAIN FEATURES THE UI PROVIDES
-----------------------------
  • A LEFT PANEL to paste text or upload .txt / .docx files
  • A RIGHT PANEL that displays the AI-generated summary
  • Buttons to choose summary length — 50, 75, or 100 words
  • A FOLLOW-UP BOX to refine the summary
        (e.g. "make it simpler" or "use bullet points")
  • COPY, CLEAR, and UPLOAD buttons for convenience
  • A live WORD COUNTER and SESSION TRACKER
  • THREADED STREAMING so the summary appears word-by-word
    without freezing the app

This file connects three helper modules:
  • Summariser  → handles AI calls
  • FileReader  → reads uploaded files
  • ChatBot     → stores conversation history
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading

from summariser import Summariser
from file_reader import FileReader
from chatbot import ChatBot

# ─── Colour palette ───────────────────────────────────────────────
HDR_BG   = "#152415"
HDR_LINE = "#4CAF50"
APP_BG   = "#DFE8DC"
PNL_BG   = "#F0F5EE"
PNL_HD   = "#D8E8D4"
PNL_BD   = "#B8D0B2"
INP_BG   = "#0D1F0D"
INP_TXT  = "#FFFFFF"
INP_PH   = "#3A6B3A"
OUT_BG   = "#FFFFFF"
OUT_TXT  = "#1A3A1A"
OUT_PH   = "#5A9E5C"
FLW_BG   = "#0D1F0D"
FLW_TXT  = "#FFFFFF"
FLW_PH   = "#3A6B3A"
BTN_MED  = "#388E3C"
BTN_DRK  = "#2E7D32"
BTN_HVR  = "#1B5E20"
BTN_DIS  = "#81C784"
WHT      = "#FFFFFF"
LBL_HD   = "#1A3A1A"
WC_CLR   = "#5A9E5C"
DIM      = "#6DAF6D"
STS_FG   = "#2E6B2E"
HDR_DIM  = "#7BBF7B"
BADGE_BG = "#4CAF50"


class UIApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.summariser  = Summariser()
        self.file_reader = FileReader()
        self.chatbot     = ChatBot()
        self.word_limit  = tk.IntVar(value=75)
        self.word_btns   = {}
        self._ph_on      = True
        self._fol_ph_on  = True
        self._streaming  = False

        self.title("")
        self.configure(bg=APP_BG)
        self.resizable(True, True)

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        W  = min(1000, sw - 40)
        H  = min(660,  sh - 60)
        self.geometry(f"{W}x{H}+{(sw-W)//2}+{(sh-H)//2}")
        self.minsize(800, 560)

        # ── BUILD ORDER IS CRITICAL ───────────────────────────────
        # Header packs at top.
        # Status bar packs at BOTTOM first — reserves space.
        # Body fills the remaining middle space with expand=True.
        # This ensures buttons are never hidden behind the body.
        self._build_header()
        self._build_statusbar()   # ← must be BEFORE body
        self._build_body()        # ← fills remaining space last

    # ══════════════════════════════════════════════════════════════
    # HEADER
    # ══════════════════════════════════════════════════════════════
    def _build_header(self):
        hdr = tk.Frame(self, bg=HDR_BG, height=56)
        hdr.pack(fill="x", side="top")
        hdr.pack_propagate(False)

        left = tk.Frame(hdr, bg=HDR_BG)
        left.pack(side="left", padx=18)

        tk.Label(left, text="Text Summarizer",
                 bg=HDR_BG, fg=WHT,
                 font=("Segoe UI", 15, "bold")).pack(side="left", pady=15)

        badge = tk.Frame(left, bg=BADGE_BG, padx=12, pady=4)
        badge.pack(side="left", padx=14, pady=18)
        tk.Label(badge, text="AI Powered",
                 bg=BADGE_BG, fg=WHT,
                 font=("Segoe UI", 9, "bold")).pack()

        self.session_var = tk.StringVar(value="0 summaries this session")
        tk.Label(hdr, textvariable=self.session_var,
                 bg=HDR_BG, fg=HDR_DIM,
                 font=("Segoe UI", 10)).pack(side="right", padx=18)

        tk.Frame(self, bg=HDR_LINE, height=3).pack(fill="x", side="top")

    # ══════════════════════════════════════════════════════════════
    # STATUS BAR — packed at BOTTOM before body so it is always visible
    # ══════════════════════════════════════════════════════════════
    def _build_statusbar(self):
        tk.Frame(self, bg=PNL_BD, height=1).pack(fill="x", side="bottom")
        bar = tk.Frame(self, bg=PNL_HD, height=30)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)

        left = tk.Frame(bar, bg=PNL_HD)
        left.pack(side="left", padx=14, pady=8)
        dot = tk.Canvas(left, width=10, height=10,
                        bg=PNL_HD, highlightthickness=0)
        dot.pack(side="left", padx=(0, 7))
        dot.create_oval(1, 1, 9, 9, fill=BADGE_BG, outline="")
        tk.Label(left, text="Ollama  ·  phi3:mini  ·  Local  ·  Offline",
                 bg=PNL_HD, fg=DIM,
                 font=("Segoe UI", 9)).pack(side="left")

        self.status = tk.StringVar(value="Ready")
        tk.Label(bar, textvariable=self.status,
                 bg=PNL_HD, fg=STS_FG,
                 font=("Segoe UI", 9)).pack(side="right", padx=14)

    # ══════════════════════════════════════════════════════════════
    # BODY — fills middle space between header and status bar
    # ══════════════════════════════════════════════════════════════
    def _build_body(self):
        body = tk.Frame(self, bg=APP_BG)
        body.pack(fill="both", expand=True, padx=14, pady=10)
        self._left_panel(body)
        tk.Frame(body, bg=APP_BG, width=12).pack(side="left", fill="y")
        self._right_panel(body)

    # ══════════════════════════════════════════════════════════════
    # LEFT PANEL
    # INPUT TEXT area + Upload File + Clear + Summarise buttons
    # ══════════════════════════════════════════════════════════════
    def _left_panel(self, parent):
        outer = tk.Frame(parent, bg=PNL_BD, padx=1, pady=1)
        outer.pack(side="left", fill="both", expand=True)
        card = tk.Frame(outer, bg=PNL_BG)
        card.pack(fill="both", expand=True)

        # Panel header — INPUT TEXT label + word count
        ph = tk.Frame(card, bg=PNL_HD, height=38)
        ph.pack(fill="x", side="top")
        ph.pack_propagate(False)
        tk.Label(ph, text="  INPUT TEXT",
                 bg=PNL_HD, fg=LBL_HD,
                 font=("Segoe UI", 10, "bold")).pack(side="left", pady=11)
        self.wc_var = tk.StringVar(value="0 words")
        tk.Label(ph, textvariable=self.wc_var,
                 bg=PNL_HD, fg=WC_CLR,
                 font=("Segoe UI", 10, "italic")).pack(side="right", padx=14)
        tk.Frame(card, bg=PNL_BD, height=1).pack(fill="x", side="top")

        # Button bar — packed at BOTTOM of card so it is always visible
        tk.Frame(card, bg=PNL_BD, height=1).pack(fill="x", side="bottom")
        act = tk.Frame(card, bg=PNL_HD, height=76)
        act.pack(fill="x", side="bottom")
        act.pack_propagate(False)

        # UPLOAD FILE button — opens file browser to pick .txt or .docx
        self._gbtn(act, "Upload\nFile",
                   self.upload_file, BTN_MED, w=10, pd=7
                   ).pack(side="left", padx=(12, 8), pady=10)

        # CLEAR button — deletes all text from input box
        self._gbtn(act, "Clear",
                   self.clear_all, BTN_MED, w=8, pd=7
                   ).pack(side="left", pady=10)

        # SUMMARISE button — sends text to AI, streams summary word by word
        self.sum_btn = self._gbtn(act, "Summarise\n  ▶",
                                  self.run_summarise, BTN_DRK, w=14, pd=7)
        self.sum_btn.pack(side="right", padx=12, pady=10)

        # Text input area — user pastes or types their long text here
        self.input_box = scrolledtext.ScrolledText(
            card, wrap="word",
            bg=INP_BG, fg=INP_PH,
            insertbackground=INP_TXT,
            selectbackground=BTN_MED, selectforeground=WHT,
            font=("Segoe UI", 12, "italic"),
            relief="flat", bd=0, highlightthickness=0,
            padx=16, pady=14, undo=True,
        )
        self.input_box.pack(fill="both", expand=True)

        self._PH = (
            "Paste or type your text here...\n\n"
            "You can also click  Upload File  below\n"
            "to load a  .txt  or  .docx  document."
        )
        self.input_box.insert("1.0", self._PH)
        self.input_box.bind("<FocusIn>",    self._ph_in)
        self.input_box.bind("<FocusOut>",   self._ph_out)
        self.input_box.bind("<KeyRelease>", self._update_wc)

    # ══════════════════════════════════════════════════════════════
    # RIGHT PANEL
    # SUMMARY OUTPUT + 50/75/100 word buttons + follow-up + Send
    # ══════════════════════════════════════════════════════════════
    def _right_panel(self, parent):
        outer = tk.Frame(parent, bg=PNL_BD, padx=1, pady=1)
        outer.pack(side="right", fill="both", expand=True)
        card = tk.Frame(outer, bg=PNL_BG)
        card.pack(fill="both", expand=True)

        # Panel header — SUMMARY OUTPUT label + Copy button
        ph = tk.Frame(card, bg=PNL_HD, height=38)
        ph.pack(fill="x", side="top")
        ph.pack_propagate(False)
        tk.Label(ph, text="  SUMMARY OUTPUT",
                 bg=PNL_HD, fg=LBL_HD,
                 font=("Segoe UI", 10, "bold")).pack(side="left", pady=11)
        # COPY button — copies the summary text to clipboard
        self._gbtn(ph, "Copy", self.copy_result,
                   BTN_MED, w=6, pd=4
                   ).pack(side="right", padx=10, pady=6)
        tk.Frame(card, bg=PNL_BD, height=1).pack(fill="x", side="top")

        # Bottom controls — packed at BOTTOM so always visible
        tk.Frame(card, bg=PNL_BD, height=1).pack(fill="x", side="bottom")
        bot = tk.Frame(card, bg=PNL_HD, height=115)
        bot.pack(fill="x", side="bottom")
        bot.pack_propagate(False)

        # WORD COUNT BUTTONS — 50 / 75 / 100 words
        # Click one of these BEFORE clicking Summarise to set the length of words count
        wr = tk.Frame(bot, bg=PNL_HD)
        wr.pack(fill="x", padx=12, pady=(10, 5))
        tk.Label(wr, text="Summary\nlength:",
                 bg=PNL_HD, fg=LBL_HD,
                 font=("Segoe UI", 10, "bold"),
                 justify="left").pack(side="left", padx=(0, 10))
        for w in [50, 75, 100]:
            b = self._gbtn(wr, f"{w}\nwords",
                           lambda ww=w: self.pick_words(ww),
                           BTN_DRK if w == 75 else BTN_MED,
                           w=9, pd=7)
            b.pack(side="left", padx=4)
            self.word_btns[w] = b

        # FOLLOW-UP ROW
        fr = tk.Frame(bot, bg=PNL_HD)
        fr.pack(fill="x", padx=12, pady=(0, 10))

        # INSTRUCTION TEXT PANEL — type a follow-up instruction here
       
        self._FP = "Follow-up — e.g.  bullet points  /  simpler  /  one sentence"
        self.follow = tk.Entry(
            fr,
            bg=FLW_BG, fg=FLW_PH,
            insertbackground=FLW_TXT,
            font=("Segoe UI", 11),
            relief="flat", highlightthickness=0,
        )
        self.follow.insert(0, self._FP)
        self.follow.bind("<FocusIn>",  self._fol_in)
        self.follow.bind("<FocusOut>", self._fol_out)
        self.follow.bind("<Return>",   lambda e: self.run_followup())
        self.follow.pack(side="left", fill="x", expand=True, ipady=9)

        # SEND button — sends instruction to AI to reformat the summary
        self._gbtn(fr, "Send", self.run_followup,
                   BTN_MED, w=7, pd=8
                   ).pack(side="right", padx=(8, 0))

        # Output area — AI summary streams here word by word
        self.output_box = scrolledtext.ScrolledText(
            card, wrap="word",
            bg=OUT_BG, fg=OUT_PH,
            selectbackground=BTN_MED, selectforeground=WHT,
            font=("Segoe UI", 12, "italic"),
            relief="flat", bd=0, state="disabled",
            highlightthickness=0,
            padx=16, pady=14,
            spacing1=4, spacing2=2, spacing3=4,
        )
        self.output_box.pack(fill="both", expand=True)
        self._write_out(
            "Your summary will appear here.\n\n"
            "  1.   Paste text into the left panel\n"
            "  2.   Choose a word count below\n"
            "  3.   Click   Summarise ▶"
        )

    # ══════════════════════════════════════════════════════════════
    # BUTTON FACTORY — solid green button with white text
    # ══════════════════════════════════════════════════════════════
    def _gbtn(self, parent, text, cmd, bg, w=10, pd=7):
        b = tk.Button(
            parent, text=text, command=cmd,
            bg=bg, fg=WHT,
            activebackground=BTN_HVR, activeforeground=WHT,
            font=("Segoe UI", 10, "bold"),
            relief="flat", cursor="hand2",
            width=w, pady=pd, bd=0, justify="center",
        )
        b.bind("<Enter>", lambda e, btn=b:       btn.config(bg=BTN_HVR))
        b.bind("<Leave>", lambda e, btn=b, c=bg: btn.config(bg=c))
        return b

    # ══════════════════════════════════════════════════════════════
    # PLACEHOLDER HANDLERS
    # ══════════════════════════════════════════════════════════════
    def _ph_in(self, _):
        if self._ph_on:
            self.input_box.delete("1.0", "end")
            self.input_box.config(fg=INP_TXT, font=("Segoe UI", 12))
            self._ph_on = False

    def _ph_out(self, _):
        if not self.input_box.get("1.0", "end-1c").strip():
            self.input_box.insert("1.0", self._PH)
            self.input_box.config(fg=INP_PH, font=("Segoe UI", 12, "italic"))
            self._ph_on = True

    def _fol_in(self, _):
        if self._fol_ph_on:
            self.follow.delete(0, "end")
            self.follow.config(fg=FLW_TXT)
            self._fol_ph_on = False

    def _fol_out(self, _):
        if not self.follow.get().strip():
            self.follow.insert(0, self._FP)
            self.follow.config(fg=FLW_PH)
            self._fol_ph_on = True

    # ══════════════════════════════════════════════════════════════
    # HELPERS
    # ══════════════════════════════════════════════════════════════
    def _update_wc(self, _=None):
        if self._ph_on:
            self.wc_var.set("0 words")
            return
        t = self.input_box.get("1.0", "end-1c").strip()
        self.wc_var.set(f"{len(t.split()) if t else 0} words")

    def _get_input(self):
        if self._ph_on:
            return ""
        return self.input_box.get("1.0", "end-1c").strip()

    def _set_busy(self, busy):
        self._streaming = busy
        self.sum_btn.config(
            state="disabled" if busy else "normal",
            bg=BTN_DIS if busy else BTN_DRK
        )

    def _append_token(self, token):
        self.output_box.config(state="normal")
        self.output_box.insert("end", token)
        self.output_box.see("end")
        self.output_box.config(state="disabled")

    def _write_out(self, text):
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", text)
        self.output_box.config(state="disabled")

    def _set_output_font_normal(self):
        self.output_box.config(fg=OUT_TXT, font=("Segoe UI", 12))

    # ══════════════════════════════════════════════════════════════
    # BUTTON ACTIONS
    # ══════════════════════════════════════════════════════════════

    def pick_words(self, w):
        """50 / 75 / 100 WORDS — sets summary length."""
        self.word_limit.set(w)
        for k, b in self.word_btns.items():
            c = BTN_DRK if k == w else BTN_MED
            b.config(bg=c)
            b.bind("<Leave>", lambda e, btn=b, col=c: btn.config(bg=col))

    def upload_file(self):
        """UPLOAD FILE — opens file browser, loads .txt or .docx into input."""
        path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("Supported", "*.txt *.docx"),
                       ("Text", "*.txt"), ("Word", "*.docx")],
        )
        if not path:
            return
        content = self.file_reader.read(path)
        if content.startswith("ERROR"):
            messagebox.showerror("File Error", content)
            return
        self.input_box.config(fg=INP_TXT, font=("Segoe UI", 12))
        self.input_box.delete("1.0", "end")
        self.input_box.insert("1.0", content)
        self._ph_on = False
        self._update_wc()
        self.status.set("Loaded: " + path.replace("\\", "/").split("/")[-1])

    def clear_all(self):
        """CLEAR — removes all text from the input box."""
        self.input_box.config(fg=INP_TXT, font=("Segoe UI", 12))
        self.input_box.delete("1.0", "end")
        self._ph_on = False
        self._update_wc()
        self.input_box.focus_set()

    def copy_result(self):
        """COPY — copies the summary text to clipboard."""
        text = self.output_box.get("1.0", "end-1c").strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.status.set("Copied to clipboard!")
            self.after(2000, lambda: self.status.set("Ready"))

    def run_summarise(self):
        """SUMMARISE — calls AI to summarise text. Streams output word by word."""
        if self._streaming:
            return
        text = self._get_input()
        if not text:
            messagebox.showwarning("No Text",
                "Please paste or type some text in the left panel first.")
            return
        words = self.word_limit.get()
        instr = f"Summarise in {words} words"
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.config(state="disabled")
        self.after(0, self._set_output_font_normal)
        self._set_busy(True)
        self.status.set(f"Summarising  ·  {words} words...")
        threading.Thread(target=self._do_summarise,
                         args=(text, instr), daemon=True).start()

    def _do_summarise(self, text, instr):
        result = self.summariser.summarise_stream(
            text, instr,
            on_token=lambda t: self.after(0, self._append_token, t)
        )
        self.chatbot.add_message("user", text)
        self.chatbot.add_message("assistant", result)
        n = self.chatbot.count() // 2
        self.after(0, self._set_busy, False)
        self.after(0, self.status.set,
                   f"Done  ·  {n} {'summary' if n==1 else 'summaries'} this session")
        self.after(0, self.session_var.set,
                   f"{n} {'summary' if n==1 else 'summaries'} this session")

    def run_followup(self):
        """SEND — sends follow-up instruction to AI to adjust the summary."""
        if self._streaming:
            return
        text  = self._get_input()
        instr = self.follow.get().strip()
        if not text:
            messagebox.showwarning("No Text",
                "Please add text in the left panel first.")
            return
        if self._fol_ph_on or not instr:
            messagebox.showwarning("No Instruction",
                "Please type a follow-up instruction.")
            return
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.config(state="disabled")
        self.after(0, self._set_output_font_normal)
        self._set_busy(True)
        self.status.set("Processing follow-up...")
        threading.Thread(target=self._do_follow,
                         args=(text, instr), daemon=True).start()

    def _do_follow(self, text, instr):
        result = self.summariser.summarise_stream(
            text, instr,
            on_token=lambda t: self.after(0, self._append_token, t)
        )
        self.chatbot.add_message("user", instr)
        self.chatbot.add_message("assistant", result)
        self.after(0, self._set_busy, False)
        self.after(0, self.status.set, "Done")


if __name__ == "__main__":
    app = UIApp()
    app.mainloop()
