def parse_llm_output(output: str, path: str):
    output = output.replace("```json", "")
    output = output.replace("```", "")
    output = output.strip()

    try:
        parsed = json.loads(output)

        parsed["file"] = path

        finding = ReviewFinding(**parsed)

        return finding.model_dump()

    except Exception as e:
        return {
            "file": path,
            "error": str(e),
            "raw_output": output
        }