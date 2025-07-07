import os
import yaml
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
prompt_file_path = "prompts/_generate.yaml"
if not os.path.exists(prompt_file_path):
    print(f"Prompt file not found: {prompt_file_path}")
    exit(1)

with open(prompt_file_path, "r") as f:
    prompt_config = yaml.safe_load(f)
input_cpp_file = "src/orgChartApi/controllers/JobsController.cc"
if not os.path.exists(input_cpp_file):
    print(f"C++ file not found: {input_cpp_file}")
    exit(1)
with open(input_cpp_file, "r") as f:
    cpp_code = f.read()
full_prompt = f"""
{prompt_config['task']}

Here is the C++ file content:
```cpp
{cpp_code}
Instructions:
{prompt_config['output']['format']}

Constraints:
{chr(10).join('- ' + c for c in prompt_config['constraints'])}

Notes:
{prompt_config['notes'][0]}
"""
try:
    response = openai.ChatCompletion.create(
        model="gpt-4", 
        messages=[
            {"role": "system", "content": "You are an expert in generating unit tests for C++ using Google Test."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.2,
        max_tokens=2000
    )
    generated_test_code = response['choices'][0]['message']['content']
    output_dir = "tests/initial"
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, "test_orgController.cpp")

    with open(output_file_path, "w") as f:
        f.write(generated_test_code)

    print(f"Unit test generated and saved to: {output_file_path}")
except Exception as e:
    print("Error while generating unit test:")
    print(str(e))