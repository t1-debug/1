import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# 1. Define the desired output structure using Pydantic.
# This guarantees Gemini returns clean HTML without markdown code blocks.
class HtmlResponse(BaseModel):
    html_content: str = Field(description="The complete, valid HTML5 code starting with <!DOCTYPE html>")

def generate_project_html():
    # 2. Initialize the client (automatically picks up GEMINI_API_KEY from environment)
    client = genai.Client()

    prompt = """
    Create a modern, responsive landing page for a fictional futuristic coffee shop called "CyberCafé". 
    Include a hero section, a menu grid with 3 items, and a contact form. 
    Use Tailwind CSS via CDN for styling to make it look highly professional.
    """

    print("Sending request to Gemini...")

    try:
        # 3. Configure and call the model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                # Set the persona/role of the AI
                system_instruction="You are an expert frontend developer. Generate clean, valid, and semantic HTML5 code based on the user request.",
                
                # Force the model to reply in JSON matching our Pydantic schema
                response_mime_type="application/json",
                response_schema=HtmlResponse,
                
                temperature=0.7,
            ),
        )

        # 4. Parse the response using the Pydantic schema structure
        # The SDK automatically converts the JSON string into our object
        result = response.parsed
        html_code = result.html_content

        # 5. Save the generated HTML to a file
        file_name = "index.html"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(html_code)

        print(f"\nSuccess! Project configured and HTML generated saved to: {file_name}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_project_html()
