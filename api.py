import requests
import pygame

# LLM Configuration
API_URL = "http://localhost:8081/v1/chat/completions"
MODEL_NAME = "mistral-small-25b-2504-Q6_k_L"  # change this if your model has a specific name
HEADERS = {"Content-Type": "application/json"}


# TTS Config
TTS_SERVER_URL = "http://localhost:5002/api/tts"

# Initial message history with a system prompt
messages = [
    {"role": "system", "content": "You are a helpful and friendly AI assistant. You are not allowed to use emojis"}
]

print("💬 Chat started! Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    # Add user's message to the history
    messages.append({"role": "user", "content": user_input})

    # Send request to llama.cpp server
    response = requests.post(API_URL, json={
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.7
    }, headers=HEADERS)

    # Parse response
    reply = response.json()["choices"][0]["message"]["content"].strip()
    clean_reply = reply.strip().replace("\n", " ").replace("\r", "")

    tts_headers = {"text": clean_reply, "style_wav": "{rate: 4}"}
    tts_payload = {"speed": 2.0}
    tts_response = requests.post(TTS_SERVER_URL, headers=tts_headers)

    if tts_response.status_code == 200:
        with open("output.wav", "wb") as f:
            f.write(tts_response.content)
    else:
        print(f"TTS Error: {tts_response.status_code} - {tts_response.text}")


    # Print assistant's response and add it to history
    print(f"AI: {reply}")

        
    pygame.mixer.init()
    sound = pygame.mixer.Sound("output.wav")
    sound.play()


    # Keep the script alive while playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    messages.append({"role": "assistant", "content": reply.strip()})