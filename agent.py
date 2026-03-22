from groq import Groq
from tavily import TavilyClient
from datetime import datetime
import os
import pytz

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

TIME_PHRASES = ["what time", "current time", "time now", "time in india",
    "what is the time", "whats the time", "time is it",
    "what date", "current date", "todays date", "today's date",
    "what day", "current day"]

def is_time_question(question: str) -> bool:
    q = question.lower().strip()
    return any(phrase in q for phrase in TIME_PHRASES)

def is_conversational(question: str) -> bool:
    conversational_prompt = f"""Is this message a casual conversation, greeting, or small talk (NOT a question needing research)?
Message: "{question}"
Answer with only YES or NO."""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": conversational_prompt}],
        max_tokens=5
    )
    answer = response.choices[0].message.content.strip().upper()
    return "YES" in answer

def get_india_time() -> str:
    india_tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india_tz)
    return now.strftime("%I:%M %p IST, %A %B %d, %Y")

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

def ask_question(question: str, history: list = None) -> str:
    current_time = get_india_time()
    if history is None:
        history = []

    if is_time_question(question):
        prompt = f"""The current exact time in India right now is: {current_time}
Answer this directly and confidently: {question}
Just give the time. Do not mention web search."""
        messages = [{"role": "user", "content": prompt}]

    elif is_conversational(question):
        system = f"""You are a friendly AI assistant named "My AI Agent".
Current time: {current_time}
You can:
- Answer any question
- Search the web for live information
- Summarize text
- Help with coding
- Detect and respond in any language
- Have friendly conversations
Reply in ONE or TWO short friendly sentences maximum."""
        messages = [{"role": "system", "content": system}]
        for h in history:
            messages.append(h)
        messages.append({"role": "user", "content": question})

    else:
        web_results = search_web(question)
        system = f"""You are a helpful AI assistant with live web search access.
Current date and time: {current_time}
You can understand and respond in ANY language in the world.
If the user writes in Hindi, reply in Hindi.
If the user writes in French, reply in French.
Always match the language of the user.

Web Search Results:
{web_results}"""
        messages = [{"role": "system", "content": system}]
        for h in history:
            messages.append(h)
        messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )
    return response.choices[0].message.content
