import requests

TTS_SERVER_URL = "http://localhost:5002/api/tts"

headers = {
    "text": 
        "Hello, this is a test of the Coqui TTS system. I am happy that it finally works"
}

response = requests.post(TTS_SERVER_URL, headers=headers)

if response.status_code == 200:
    with open("output.wav", "wb") as f:
        f.write(response.content)
    print("Speech synthesis complete. Saved as output.wav")
else:
    print(f"Error: {response.status_code} - {response.text}")
