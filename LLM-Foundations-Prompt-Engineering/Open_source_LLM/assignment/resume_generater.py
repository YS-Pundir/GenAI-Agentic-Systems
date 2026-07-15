import os
from datetime import datetime
import requests
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# --- Set your model names ---
LOCAL_MODEL = "qwen2.5:0.5b"   # 0.5B or 1B only; must match `ollama list`
GROQ_MODEL = "llama-3.3-70b-versatile"  # check console.groq.com for available models

CANDIDATE = {
    "name": "Aarav Mehta",
    "email": "aarav.mehta@example.com",
    "phone": "+91-98765-43210",
    "location": "Roorkee, Uttarakhand",
    "education": "B.Tech Computer Science, IIT Roorkee (expected 2026), CGPA 8.4",
    "skills": ["Python", "REST APIs", "SQL", "Git", "Basic ML"],
    "experience": "Summer intern at TechBridge Labs (Jun–Aug 2025): built internal dashboards with FastAPI and PostgreSQL.",
    "projects": "Hostel Room Booking CLI (Python) — 200+ active users on campus.",
}

RESUME_PROMPT = f"""You are a professional resume writer. Create a complete, single-page resume in valid HTML only.

Rules:
- Return ONLY HTML starting with <!DOCTYPE html> — no markdown fences, no explanation before or after.
- Do not invent employers, degrees, or facts not listed below.

Layout (required):
- Use a **two-column** layout for the main body (e.g. CSS flexbox or CSS grid with two columns).
- **Left column (narrower, ~30–35%):** contact block, Skills, Education.
- **Right column (wider, ~65–70%):** Experience, Projects.
- **Full-width header** above the columns: candidate name (large), one-line title or tagline, email / phone / location on one line.

Styling (use a <style> block in <head> — make it look polished):
- Font: a clean sans-serif stack (e.g. Arial, Helvetica, or system-ui).
- **Accent color:** one professional color (e.g. #2563eb blue or #0f766e teal) for headings, section titles, and subtle borders.
- Section headings: uppercase or small-caps, accent color, bottom border or left border.
- Consistent spacing: padding inside columns, margin between sections, readable line-height (1.4–1.6).
- Skills: show as a neat list or small pill/tag style — not a plain comma-separated paragraph.
- Page: max-width ~900px, centered on screen; light background (#f8fafc) with white column areas or a white card look.
- Print-friendly: avoid horizontal scroll; keep everything on one screen-height page if possible.

Candidate data:
Name: {CANDIDATE['name']}
Email: {CANDIDATE['email']}
Phone: {CANDIDATE['phone']}
Location: {CANDIDATE['location']}
Education: {CANDIDATE['education']}
Skills: {', '.join(CANDIDATE['skills'])}
Experience: {CANDIDATE['experience']}
Projects: {CANDIDATE['projects']}
"""


def save_resume_html(html_text: str, mode: str) -> str:
    """
    Save model output to an HTML file. USE THIS FUNCTION AS-IS — do not change the logic.

    File name pattern:
      Local  -> Local_Resume_YYYYMMDD_HHMMSS.html
      Groq   -> Groq_Resume_YYYYMMDD_HHMMSS.html
    """
    prefix = "Local" if mode == "local" else "Groq"
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_Resume_{stamp}.html"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_text)

    print(f"Saved {filename}")
    return filename


def ask_llm(mode: str, prompt_text: str) -> str:
    if mode == "groq":
        # Check standard environment variable naming convention
        api_key = os.getenv("GROQ_API_KEY") or os.getenv("api_key")

        if not api_key:
            raise ValueError("Groq API key not found in environment variables.")
        
        client = Groq(api_key=api_key)

        # Pass the formatted prompt text cleanly as a string payload
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt_text
                }
            ]
        )
        return response.choices[0].message.content

    elif mode == "local":
        url = "http://localhost:11434/api/chat"
        payload = {
            "model": LOCAL_MODEL,
            "messages": [{"role": "user", "content": prompt_text}],
            "stream": False
        }
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["message"]["content"]
    
    else:
        raise ValueError("Invalid mode configuration selected.")


def generate_resume_html(mode: str) -> str:
    """Call the LLM, then save HTML using save_resume_html (do not change this function)."""
    html_from_model = ask_llm(mode, RESUME_PROMPT)
    
    # Strip accidental markdown code blocks if the model fails to follow instructions
    clean_html = html_from_model.replace("```html", "").replace("```", "").strip()
    return save_resume_html(clean_html, mode)


if __name__ == "__main__":
    print("Generating local resume...")
    try:
        generate_resume_html("local")
    except Exception as e:
        print(f"Local run failed or skipped: {e}")

    print("Generating Groq resume...")
    try:
        generate_resume_html("groq")
    except ValueError as e:
        print(f"Groq skipped: {e}")
    except Exception as e:
        print(f"Groq run failed: {e}")

    print("Open both HTML files in your browser and compare quality.")

# Local resume quality: Structural integrity is weak; often skips the two-column grid specifications entirely and renders raw markdown blocks inside plain HTML wrapper elements.
# Groq resume quality: Excellent execution; creates a highly clean Flexbox layout, renders skill pills cleanly with modern CSS border-radii, and correctly observes single-page sizing constraints.