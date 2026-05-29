import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found. Please check your .env file.")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def get_response(self, prompt: str) -> dict:
        """
        Send prompt to Groq and return parsed JSON result.
        Returns a dict with keys: meaning, causes, fix, example
        """
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are IRIS AI, an expert Python debugger. "
                        "Analyze the given Python error or traceback and respond ONLY with a valid JSON object. "
                        "No markdown fences, no preamble, no explanation outside the JSON. "
                        "The JSON must have exactly these four keys:\n"
                        "{\n"
                        '  "meaning": "Clear 1-2 sentence explanation of what the error means",\n'
                        '  "causes": ["cause 1", "cause 2", "cause 3"],\n'
                        '  "fix": "Concrete fix recommendation in 1-2 sentences",\n'
                        '  "example": "# Corrected Python code snippet"\n'
                        "}"
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=self.model,
            temperature=0.3,
            max_tokens=1024,
        )

        raw = chat_completion.choices[0].message.content.strip()

        # Strip accidental markdown fences
        raw = raw.replace("```json", "").replace("```", "").strip()

        return json.loads(raw)
