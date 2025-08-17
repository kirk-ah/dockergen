import os
from google import genai
from dotenv import load_dotenv

# Load .env if you keep GOOGLE_API_KEY there
load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_prompt(requirements: str) -> str:
    return f"""Given the following Python packages:
{requirements}

Generate a Dockerfile RUN command for Ubuntu 24.04 that installs ONLY the system and development packages strictly required to satisfy these Python packages. 
- Include each package on a separate line with backslashes for continuation.
- Start the command with RUN.
- Do NOT include optional packages, recommendations, comments, explanations, or markdown formatting.
"""


def call_gemini(prompt: str) -> str:
    """Send a prompt to Gemini and return its response text."""
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=prompt
    )
    return response.text.strip()

def strip_markdown_fences(text: str) -> str:
    # remove triple backticks (with or without language tag like 'dockerfile')
    lines = text.strip().splitlines()
    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines)

def generate_from_reqs_file(requirements_filepath: str) -> str:
    """Generate combined apt-get command for all packages in requirements.txt."""
    prompt = generate_prompt(requirements_filepath)
    run_step = call_gemini(prompt)
    formatted_run_step = strip_markdown_fences(run_step)
    return f"""
# Install system deps for pip requirements
{formatted_run_step}
"""