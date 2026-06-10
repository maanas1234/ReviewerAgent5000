from openai import OpenAI
import json
from typing import List
# Direct the client to your local Ollama server
from pydantic import BaseModel
from parser import parse_llm_output

class ReviewFinding(BaseModel):
    file: str
    issue_type: str
    severity: str
    confidence: float
    reason: str
    suggested_fix: str
    line_start: int
    line_end: int



client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama'  # A placeholder key is required but ignored locally
)


def review_single_file(path:str,code:str):
            numbered_code = "\n".join(
            f"{i+1}: {line}"
            for i, line in enumerate(code.splitlines())
    )


            print("="*50)
            print(f"Reviewing: {path}")
            #print(code)
            chat_completion = client.chat.completions.create(
            model='gemma2:2b',
            response_format={"type":"json_object"}, # Specify your locally pulled model
            messages=[
                    {
                        "role": "system",
                        "content": "You are a senior code reviewer."
                    },
                    {
    "role": "user",
    "content": f"""
You are reviewing ONE Python file.

FILE:
{path}

TASK:
Find the SINGLE most important issue in this file.

Allowed issue types:
- bug
- security
- performance
- maintainability
- missing_edge_case

IMPORTANT RULES:

1. If no significant issue exists, return:

{{
    "file": "{path}",
    "issue_type": "none",
    "severity": "low",
    "confidence": 1.0,
    "reason": "No significant issue found.",
    "suggested_fix": "",
    "line_start": 1,
    "line_end": 1
}}

2. Do NOT invent problems.

3. Do NOT suggest improvements unless they are actual issues.

4. Use only issue types from the allowed list.

5. confidence must be a number between 0 and 1.

6. line_start and line_end must refer to actual lines in the file.

7. Return ONLY valid JSON.

8. Do NOT use markdown.

CODE:

{numbered_code}
"""
}
                ]
        )
            Final_Output = chat_completion.choices[0].message.content

            result = parse_llm_output(
                Final_Output,
                path
            )
            return result


filePath = r"C:\Users\Maanas\OneDrive\Desktop\PROJECTSS\Ai-Code-Review Agent\repodumps\India-Air-Quality-Analysis_20260609_114148.json"
def review_file(jsonPath:str):
    all_results = []
    with open(jsonPath,'r',encoding='utf-8') as f:
        repo_files = json.load(f)
        print(type(repo_files))
        print(len(repo_files))
        for path,code in repo_files.items():
            result = review_single_file(path,code)
            all_results.append(result)
            review_report = {
                "repository": "India-Air-Quality-Analysis",
                "total_files": len(all_results),
                "reviews": all_results
            }

            with open("review_results.json", "w", encoding="utf-8") as f:
                json.dump(review_report, f, indent=4)

        return all_results
   



results = review_file(jsonPath=filePath)

print(results)