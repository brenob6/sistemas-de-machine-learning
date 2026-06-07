from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

api_key = os.environ["GEMINI_API_KEY"]

if (not api_key) or api_key == "":
    raise Exception("API_KEY environment variable is not set.")


class GeminiModel:
    def __init__(self, contract: type[BaseModel]):
        self.semantic_structure = contract

    def prompt(self, contents: str) -> str | None:
        client = genai.Client(api_key=api_key)

        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                config=genai.types.GenerateContentConfig(
                    system_instruction=f"Your job are to analyze markdown tables and extract the information in a structured format. You should return the information in a JSON format, with the following structure:{self.semantic_structure.model_json_schema()}",
                    response_schema=self.semantic_structure,
                    response_mime_type="application/json",
                ),
                contents=contents,
            )

            return response.text
        except Exception as e:
            print(f"Error generating content: {e}")
            return None
