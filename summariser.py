import ollama


class Summariser:
    """
    Calls local Ollama phi3:mini model.
    Uses stream=True for instant word-by-word output.
    Optimised for low RAM laptops (2.3 GB only).
    """

    MODEL = "phi3:mini"  

    SYSTEM = (
        "You are a fast text summarization assistant. "
        "Summarise the given text clearly and accurately. "
        "Use bullet points starting with •. "
        "Be concise. Go straight to the summary — no introductions."
    )

    FORMATS = {
        "bullet":    "Use bullet points. Each starts with •.",
        "bullets":   "Use bullet points. Each starts with •.",
        "numbered":  "Use a numbered list: 1. 2. 3.",
        "paragraph": "Write as one clear paragraph.",
        "simple":    "Use very simple English a school student understands.",
        "plain":     "Use very simple English a school student understands.",
        "sentence":  "Write as ONE single sentence only.",
        "short":     "Maximum 2 sentences only.",
        "academic":  "Use formal academic English.",
    }

    def _fmt(self, instruction: str) -> str:
        low = instruction.lower()
        for kw, fmt in self.FORMATS.items():
            if kw in low:
                return fmt
        return "Use bullet points. Each starts with •."

    def _wc(self, instruction: str) -> str:
        for t in instruction.split():
            c = t.strip(".,!?")
            if c.isdigit():
                return c
        return "75"

    def _build_prompt(self, text: str, instruction: str) -> str:
        fmt   = self._fmt(instruction)
        words = self._wc(instruction)
        return (
            f"Summarise in {words} words. {fmt} "
            f"Include 4-6 key points. Be accurate.\n\n"
            f"TEXT:\n{text}"
        )

    # ── STREAMING — text appears word by word instantly ───────────
    def summarise_stream(self,
                         text: str,
                         instruction: str = "",
                         on_token=None) -> str:
        """
        Streams the response token by token.
        Calls on_token(token) for each piece received.
        Returns the full completed text.
        """
        if not text or not text.strip():
            msg = "ERROR: No text provided."
            if on_token:
                on_token(msg)
            return msg

        if not instruction:
            instruction = "Summarise in 75 words"

        prompt = self._build_prompt(text, instruction)
        full   = []

        try:
            stream = ollama.chat(
                model=self.MODEL,
                messages=[
                    {"role": "system", "content": self.SYSTEM},
                    {"role": "user",   "content": prompt},
                ],
                stream=True,
                options={
                    "temperature":    0.1,
                    "top_p":          0.8,
                    "num_predict":    300,
                    "num_ctx":        2048,
                    "repeat_penalty": 1.1,
                },
            )

            for chunk in stream:
                token = chunk["message"]["content"]
                if token:
                    full.append(token)
                    if on_token:
                        on_token(token)

            result = "".join(full).strip()

            # Remove accidental filler phrases
            for phrase in ["Here is", "Sure!", "Of course!", "Summary:"]:
                if result.startswith(phrase):
                    result = result[len(phrase):].lstrip(": \n").strip()

            return result

        except Exception as e:
            msg = (
                "Could not connect to Ollama.\n\n"
                "Please check:\n"
                "  1.  Ollama is installed  (ollama.com/download)\n"
                "  2.  Ollama app is open and running\n"
                "  3.  phi3:mini downloaded  (ollama pull phi3:mini)\n\n"
                f"Error: {e}"
            )
            if on_token:
                on_token(msg)
            return msg

    # ── Non-streaming fallback ────────────────────────────────────
    def summarise(self, text: str, instruction: str = "") -> str:
        if not text or not text.strip():
            return "ERROR: No text provided."
        if not instruction:
            instruction = "Summarise in 75 words"
        prompt = self._build_prompt(text, instruction)
        try:
            resp = ollama.chat(
                model=self.MODEL,
                messages=[
                    {"role": "system", "content": self.SYSTEM},
                    {"role": "user",   "content": prompt},
                ],
                options={
                    "temperature":    0.1,
                    "top_p":          0.8,
                    "num_predict":    300,
                    "num_ctx":        2048,
                    "repeat_penalty": 1.1,
                },
            )
            return resp["message"]["content"].strip()
        except Exception as e:
            return (
                "Could not connect to Ollama.\n\n"
                "  1.  Ollama installed  (ollama.com/download)\n"
                "  2.  Ollama app open\n"
                "  3.  ollama pull phi3:mini\n\n"
                f"Error: {e}"
            )
