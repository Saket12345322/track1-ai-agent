import requests

print("=================================")
print("   Your AI Agent - Chat Mode")
print("=================================")
print("Type your question and press Enter")
print("Type 'exit' to quit")
print("=================================")

while True:
    question = input("\nYou: ")
    if question.lower() == "exit":
        print("Goodbye!")
        break
    
    response = requests.post(
        "http://127.0.0.1:8080/ask",
        json={"question": question}
    )
    answer = response.json().get("answer", "No response")
    print(f"\nAI: {answer}")
