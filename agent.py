from groq import Groq
from tavily import TavilyClient
from datetime import datetime
import os
import pytz

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

SIMPLE_PHRASES = [
    "hi", "hello", "hey", "hii", "helo", "howdy",
    "how are you", "how r you", "whats up", "what's up",
    "good morning", "good evening", "good night", "good afternoon",
    "bye", "goodbye", "thanks", "thank you", "ok", "okay",
    "who are you", "what are you", "what can you do",
    "help", "tell me about yourself""can we have conversation", "can we talk", "can we chat",
    "lets talk", "let's talk", "lets chat", "let's chat",
    "i want to talk", "talk to me", "chat with me"
]

TIME_PHRASES = [
    "what time", "current time", "time now", "time in india",
    "what is the time", "whats the time", "time is it",
    "what date", "current date", "todays date", "today's date",
    "what day", "current day"
]

def is_simple_conversation(question: str) -> bool:
    q = question.lower().strip()
    for phrase in SIMPLE_PHRASES:
        if q == phrase or q.startswith(phrase):
            return True
    return len(q.split()) <= 3 and "?" not in q

def is_time_question(question: str) -> bool:
    q = question.lower().strip()
    for phrase in TIME_PHRASES:
        if phrase in q:
            return True
    return False

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

def ask_question(question: str) -> str:
    current_time = get_india_time()

    if is_time_question(question):
        prompt = f"""The current time in India is exactly: {current_time}
Answer this question directly using only this time: {question}
Be direct and confident. Do not search the web."""

    elif is_simple_conversation(question):
        prompt = f"""You are a friendly AI assistant named "My AI Agent".
Current time: {current_time}
The user said: {question}
Respond warmly and briefly. Tell them you can help with questions, web search, summarizing text and coding."""

    else:
        web_results = search_web(question)
        prompt = f"""You are a helpful AI assistant with live web search access.
Current date and time: {current_time}

Web Search Results:
{web_results}

Answer this question: {question}
Give a clear and accurate answer."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

