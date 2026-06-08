from openai import OpenAI

# Direct the client to your local Ollama server
client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama'  # A placeholder key is required but ignored locally
)

chat_completion = client.chat.completions.create(
    model='llama3.2:3b',  # Specify your locally pulled model
    messages=[
        {'role': 'user', 'content': 'Explain local inference in one sentence.'}
    ]
)

print(chat_completion.choices[0].message.content)
