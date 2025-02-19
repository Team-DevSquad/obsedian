

import requests
import json
import ast

# Define the API endpoint and headers
api_url = "https://9ff4-58-146-97-91.ngrok-free.app/v1/chat/completions"
headers = {
    "Content-Type": "application/json"
}

# Read the source code from a file
file_path = "vulnerable-llm-example.py"  # Replace with your file path
with open(file_path, "r") as file:
    source_code = file.read()

# Parse the source code into an AST
tree = ast.parse(source_code)

# Extract all functions from the AST
functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

# Function to send code to the API and get vulnerabilities
def scan_code_for_vulnerabilities(code):
    payload = {
        "model": "lily-cybersecurity-7b-v0.2",
        "messages": [
            {"role": "user", "content": f"Scan the following source code for security vulnerabilities and generate fixes. Return the results in the following format:\n\n"
                                        "- Vulnerability ID: <ID>\n"
                                        "- Title: <Title>\n"
                                        "- Severity: <Severity>\n"
                                        "- Location: <Location>\n"
                                        "- Description: <Description>\n"
                                        "- Recommendation: <Recommendation>\n\n"
                                        "Show the vulnerable code snippet and the fixed code snippet. Ensure that the fixes address the vulnerabilities described.\n\n"
                                        f"Source Code:\n{code}"}
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    else:
        return f"Failed to get a response from the API. Status code: {response.status_code}"

# Iterate through each function and scan for vulnerabilities
for func in functions:
    func_code = ast.unparse(func)  # Convert the function node back to code
    print(f"\nScanning function: {func.name}...\n")
    
    # Send the function code to the API for scanning
    result = scan_code_for_vulnerabilities(func_code)
    
    # Print the results
    print(result)
    print("-" * 80)  # Separator for readability