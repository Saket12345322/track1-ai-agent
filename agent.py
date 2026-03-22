from groq import Groq
from tavily import TavilyClient
from datetime import datetime
import os
import pytz

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

TIME_PHRASES = ["what time", "current time", "time now", "time in",
    "what is the time", "whats the time", "time is it",
    "what date", "current date", "todays date", "today's date",
    "what day", "current day", "what year", "current year"]

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

def get_all_times() -> str:
    timezones = {
        "India (IST)": "Asia/Kolkata",
        "USA New York (EST/EDT)": "America/New_York",
        "USA Los Angeles (PST/PDT)": "America/Los_Angeles",
        "USA Chicago (CST/CDT)": "America/Chicago",
        "USA Washington DC (EST/EDT)": "America/New_York",
        "UK London (GMT/BST)": "Europe/London",
        "UAE Dubai": "Asia/Dubai",
        "Japan Tokyo": "Asia/Tokyo",
        "Australia Sydney": "Australia/Sydney",
        "Germany Berlin": "Europe/Berlin",
        "France Paris": "Europe/Paris",
        "Singapore": "Asia/Singapore",
        "China Beijing": "Asia/Shanghai",
        "Brazil Sao Paulo": "America/Sao_Paulo",
        "Canada Toronto": "America/Toronto",
    }
    times = {}
    for city, tz in timezones.items():
        tz_obj = pytz.timezone(tz)
        now = datetime.now(tz_obj)
        times[city] = now.strftime("%I:%M %p %Z, %A %B %d, %Y")
    return str(times)

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
    india_tz = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(india_tz).strftime("%I:%M %p IST, %A %B %d, %Y")
    if history is None:
        history = []

    if is_time_question(question):
        all_times = get_all_times()
        prompt = f"""You have access to the EXACT current times for all major cities right now:
{all_times}

The user asked: {question}

Answer using ONLY the times provided above. Be direct and accurate.
If they ask about a city not listed, calculate it from IST (India time is {current_time})."""
        messages = [{"role": "user", "content": prompt}]

    elif is_conversational(question):
        system = f"""You are a friendly AI assistant named "My AI Agent".
Current time in India: {current_time}
You can help with questions, web search, coding, any language, and friendly conversation.
Reply in ONE or TWO short friendly sentences maximum. Be warm and natural."""
        messages = [{"role": "system", "content": system}]
        for h in history:
            messages.append(h)
        messages.append({"role": "user", "content": question})

    else:
        web_results = search_web(question)
        system = f"""You are a helpful AI assistant with live web search access.
Current date and time in India: {current_time}
You can understand and respond in ANY language in the world.
Always match the language the user writes in.

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
