from groq import Groq
from tavily import TavilyClient
from datetime import datetime
import os
import pytz

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

TIMEZONE_MAP = {
    "india": "Asia/Kolkata", "mumbai": "Asia/Kolkata", "delhi": "Asia/Kolkata",
    "new york": "America/New_York", "washington": "America/New_York", "washington dc": "America/New_York",
    "los angeles": "America/Los_Angeles", "california": "America/Los_Angeles",
    "chicago": "America/Chicago", "texas": "America/Chicago", "houston": "America/Chicago",
    "london": "Europe/London", "uk": "Europe/London", "england": "Europe/London",
    "paris": "Europe/Paris", "france": "Europe/Paris",
    "berlin": "Europe/Berlin", "germany": "Europe/Berlin",
    "tokyo": "Asia/Tokyo", "japan": "Asia/Tokyo",
    "beijing": "Asia/Shanghai", "china": "Asia/Shanghai", "shanghai": "Asia/Shanghai",
    "dubai": "Asia/Dubai", "uae": "Asia/Dubai",
    "singapore": "Asia/Singapore",
    "sydney": "Australia/Sydney", "australia": "Australia/Sydney",
    "toronto": "America/Toronto", "canada": "America/Toronto",
    "moscow": "Europe/Moscow", "russia": "Europe/Moscow",
    "istanbul": "Europe/Istanbul", "turkey": "Europe/Istanbul",
    "cairo": "Africa/Cairo", "egypt": "Africa/Cairo",
    "johannesburg": "Africa/Johannesburg", "south africa": "Africa/Johannesburg",
    "nairobi": "Africa/Nairobi", "kenya": "Africa/Nairobi",
    "mexico city": "America/Mexico_City", "mexico": "America/Mexico_City",
    "sao paulo": "America/Sao_Paulo", "brazil": "America/Sao_Paulo",
    "buenos aires": "America/Argentina/Buenos_Aires", "argentina": "America/Argentina/Buenos_Aires",
    "seoul": "Asia/Seoul", "south korea": "Asia/Seoul", "korea": "Asia/Seoul",
    "bangkok": "Asia/Bangkok", "thailand": "Asia/Bangkok",
    "jakarta": "Asia/Jakarta", "indonesia": "Asia/Jakarta",
    "karachi": "Asia/Karachi", "pakistan": "Asia/Karachi",
    "dhaka": "Asia/Dhaka", "bangladesh": "Asia/Dhaka",
    "colombo": "Asia/Colombo", "sri lanka": "Asia/Colombo",
    "kathmandu": "Asia/Kathmandu", "nepal": "Asia/Kathmandu",
    "kabul": "Asia/Kabul", "afghanistan": "Asia/Kabul",
    "tehran": "Asia/Tehran", "iran": "Asia/Tehran",
    "riyadh": "Asia/Riyadh", "saudi arabia": "Asia/Riyadh",
    "hong kong": "Asia/Hong_Kong",
    "taipei": "Asia/Taipei", "taiwan": "Asia/Taipei",
    "kuala lumpur": "Asia/Kuala_Lumpur", "malaysia": "Asia/Kuala_Lumpur",
    "manila": "Asia/Manila", "philippines": "Asia/Manila",
    "rome": "Europe/Rome", "italy": "Europe/Rome",
    "madrid": "Europe/Madrid", "spain": "Europe/Madrid",
    "amsterdam": "Europe/Amsterdam", "netherlands": "Europe/Amsterdam",
    "brussels": "Europe/Brussels", "belgium": "Europe/Brussels",
    "vienna": "Europe/Vienna", "austria": "Europe/Vienna",
    "zurich": "Europe/Zurich", "switzerland": "Europe/Zurich",
    "stockholm": "Europe/Stockholm", "sweden": "Europe/Stockholm",
    "oslo": "Europe/Oslo", "norway": "Europe/Oslo",
    "copenhagen": "Europe/Copenhagen", "denmark": "Europe/Copenhagen",
    "helsinki": "Europe/Helsinki", "finland": "Europe/Helsinki",
    "warsaw": "Europe/Warsaw", "poland": "Europe/Warsaw",
    "prague": "Europe/Prague", "czech": "Europe/Prague",
    "budapest": "Europe/Budapest", "hungary": "Europe/Budapest",
    "bucharest": "Europe/Bucharest", "romania": "Europe/Bucharest",
    "athens": "Europe/Athens", "greece": "Europe/Athens",
    "lisbon": "Europe/Lisbon", "portugal": "Europe/Lisbon",
    "miami": "America/New_York", "boston": "America/New_York",
    "seattle": "America/Los_Angeles", "san francisco": "America/Los_Angeles",
    "denver": "America/Denver", "colorado": "America/Denver",
    "phoenix": "America/Phoenix", "arizona": "America/Phoenix",
    "alaska": "America/Anchorage", "hawaii": "Pacific/Honolulu",
    "vancouver": "America/Vancouver",
    "lagos": "Africa/Lagos", "nigeria": "Africa/Lagos",
    "accra": "Africa/Accra", "ghana": "Africa/Accra",
    "addis ababa": "Africa/Addis_Ababa", "ethiopia": "Africa/Addis_Ababa",
    "casablanca": "Africa/Casablanca", "morocco": "Africa/Casablanca",
}

def get_time_for_location(location: str) -> str:
    location_lower = location.lower().strip()
    timezone_str = None
    for key, tz in TIMEZONE_MAP.items():
        if key in location_lower:
            timezone_str = tz
            break
    if timezone_str:
        tz = pytz.timezone(timezone_str)
        now = datetime.now(tz)
        return now.strftime("%I:%M %p, %A %B %d, %Y") + f" ({timezone_str})"
    india_tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india_tz)
    return now.strftime("%I:%M %p IST, %A %B %d, %Y")

def get_india_time() -> str:
    india_tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india_tz)
    return now.strftime("%I:%M %p IST, %A %B %d, %Y")

def is_time_question(question: str) -> bool:
    q = question.lower().strip()
    time_words = ["what time", "current time", "time now", "time is it",
                  "what is the time", "whats the time", "time in", "time at"]
    return any(phrase in q for phrase in time_words)

def is_conversational(question: str) -> bool:
    prompt = f"""Is this message a casual conversation, greeting, or small talk (NOT a research question)?
Message: "{question}"
Answer with only YES or NO."""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=5
    )
    return "YES" in response.choices[0].message.content.strip().upper()

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
        location_time = get_time_for_location(question)
        prompt = f"""The user asked about time. Here is the exact current time for the requested location:
{location_time}
Current IST time for reference: {current_time}
Answer this question directly and confidently: {question}
Just state the time clearly. Do not mention web search or calculations."""
        messages = [{"role": "user", "content": prompt}]

    elif is_conversational(question):
        system = f"""You are a friendly AI assistant named "My AI Agent".
Current time: {current_time}
You can help with: answering questions, web search, coding, summarizing text, any language.
Reply in ONE or TWO short friendly sentences. Be warm and natural."""
        messages = [{"role": "system", "content": system}]
        for h in history:
            messages.append(h)
        messages.append({"role": "user", "content": question})

    else:
        web_results = search_web(question)
        system = f"""You are a helpful AI assistant with live web search.
Current date and time: {current_time}
You can understand and respond in ANY language. Match the user's language.

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
