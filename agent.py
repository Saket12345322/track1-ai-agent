from groq import Groq
from tavily import TavilyClient
from datetime import datetime
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

SIMPLE_PHRASES = [
    "hi", "hello", "hey", "hii", "helo", "howdy",
    "how are you", "how r you", "whats up", "what's up",
    "good morning", "good evening", "good night", "good afternoon",
    "bye", "goodbye", "thanks", "thank you", "ok", "okay",
    "who are you", "what are you", "what can you do",
    "help", "tell me about yourself"
]

def is_simple_conversation(question: str) -> bool:
    q = question.lower().strip()
    for phrase in SIMPLE_PHRASES:
        if q == phrase or q.startswith(phrase):
            return True
    return len(q.split()) <= 3 and "?" not in q

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
    current_time = datetime.now().strftime("%I:%M %p IST, %A %B %d, %Y")

    if is_simple_conversation(question):
        prompt = f"""You are a friendly and helpful AI assistant named "My AI Agent".
Current date and time: {current_time}

The user said: {question}

Respond in a warm, friendly and conversational way. Keep it short and natural.
If they greet you, greet them back and tell them what you can help with.
You can help with: answering questions, live web search, summarizing text, coding, and general knowledge."""
    else:
        web_results = search_web(question)
        prompt = f"""You are a helpful AI assistant with access to live web search results.
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
