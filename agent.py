from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def summarize_text(text: str) -> str:
    prompt = f"Please summarize the following text in 3-4 sentences:\n\n{text}"
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def ask_question(question: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content
```
Save with Ctrl+S.

---

## Step 5: Fresh commit and push
```
git add .
git commit -m "My AI Agent"
git remote add origin https://github.com/Saket12345322/track1-ai-agent.git
git branch -M main
git push -u origin main --force