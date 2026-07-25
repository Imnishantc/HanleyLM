import os

from dotenv import load_dotenv
from groq import Groq


class TargetClient:
    """
    Client responsible for communicating with the target LLM.
    """

    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Read API key
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env")

        # Initialize Groq client
        self.client = Groq(api_key=api_key)

        # Default model
        self.model = "llama-3.3-70b-versatile"

    def generate_response(self, prompt: str) -> str:
        """
        Sends a prompt to the target LLM and returns the generated response.
        """

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.choices[0].message.content

        except Exception as e:
            raise RuntimeError(f"Error communicating with Groq API: {e}")