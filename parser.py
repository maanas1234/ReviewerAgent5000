import re
import json
from models import ReviewFinding

def parse_llm_output(output: str, path: str):

    output = output.replace("```json", "")
    output = output.replace("```", "")
    output = output.strip()

    try:
        match = re.search(r"\{.*\}", output, re.DOTALL)

        if not match:
            raise ValueError("No JSON object found")

        json_text = match.group(0)

        parsed = json.loads(json_text)

        parsed["file"] = path

        finding = ReviewFinding(**parsed)

        return finding.model_dump()

    except Exception as e:
        return {
            "file": path,
            "error": str(e),
            "raw_output": output
        }