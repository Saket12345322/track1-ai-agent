from groq import Groq
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

def search_web(query: str) -> str:
    results = tavily.search(query=query, max_results=3)
    context = ""
    for r in results["results"]:
        context += f"Source: {r['title']}\n{r['content']}\n\n"
    return context

def summarize_text(text: str) -> str:
    prompt = f"Please summarize the following text in 3-4 sentences:\n\n{text}"
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def ask_question(question: str) -> str:
    web_results = search_web(question)
    prompt = f"""You are a helpful AI assistant with access to live web search results.

Web Search Results:
{web_results}

Based on the above real-time information, answer this question:
{question}

Give a clear, accurate answer using the web results provided."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

Save with Ctrl+S.

---

## Step 5: Test it locally first
```
python main.py
```

Then in second PowerShell window:
```
Invoke-WebRequest -Uri "http://127.0.0.1:8080/ask" -Method POST -ContentType "application/json" -Body '{"question": "What is the latest news in AI today?"}' -UseBasicParsing