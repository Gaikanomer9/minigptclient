import openai
import os
from datetime import datetime
import json

openai.api_key = os.getenv("API_KEY")





def send_message(messages: list):
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages)
    try:
        if len(resp.choices) > 1:
            print(f"Received more than one choice: {resp.choices}")
        content = resp.choices[0]["message"]["content"]
    except Exception as e:
        print(e)
        content = ""
    return content

if __name__ == "__main__":
    print("Who would you like to chat with?")
    roles = {
        "1": "Code Assistant",
        "2": "Advisor",
        "3": "Youtube Expert"
    }
    for k, v in roles.items():
        print(f"{k}. {v}")
    role_selection = input("Enter a number: ")
    if not role_selection in roles.keys():
        print("Invalid selection. Exiting.")
        exit()
    role = roles[role_selection]
    messages = [
        {"role": "system", "content": "You are a " + role},
    ]
    print("You are now chatting with " + role)
    print("Enter your message:")
    while True:
        message = input("> ")
        if message == "exit":
            break
        messages.append({"role": "user", "content": message})
        response = send_message(messages)
        messages.append({"role": "system", "content": response})
        print(f"{role}: {response}")

    # Save the chat to a file with date and time as filename
    filename = f"archive/chat_{role}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    with open(filename, "w") as f:
        json.dump(messages, f)