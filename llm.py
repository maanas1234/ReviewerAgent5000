from openai import OpenAI
import json
# Direct the client to your local Ollama server
client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama'  # A placeholder key is required but ignored locally
)


def review_file(file_path:str, code:str):
    filePath = r"C:\Users\Maanas\OneDrive\Desktop\PROJECTSS\Ai-Code-Review Agent\repodumps\India-Air-Quality-Analysis_20260609_114148.json"
chat_completion = client.chat.completions.create(
    model='llama3.2:3b',  # Specify your locally pulled model
    messages=[
        {'role': 'user', 'content': 'Explain local inference in one sentence.'}
    ]
)
filePath = r"C:\Users\Maanas\OneDrive\Desktop\PROJECTSS\Ai-Code-Review Agent\repodumps\India-Air-Quality-Analysis_20260609_114148.json"
print(chat_completion.choices[0].message.content)

with open(filePath,'r',encoding='utf-8') as f:
    repo_files = json.load(f)
    print(type(repo_files))
    print(len(repo_files))
    for path,code in repo_files.items():
        print("="*50)
        print(path)
        print(code)
        chat_completion = client.chat.completions.create(
        model='llama3.2:3b',  # Specify your locally pulled model
        messages=[
                {
                    "role": "system",
                    "content": "You are a senior code reviewer."
                },
                {
                    "role": "user",
                    "content": f"""
            File Path:
            {path}

            Analyze this code.

            Look for:
            - Bugs
            - Security issues
            - Performance issues
            - Maintainability issues
            - Missing edge cases

            Return ONLY JSON.

            Code:
            {code}
            """
                }
            ]
    )
        print(chat_completion.choices[0].message.content)
