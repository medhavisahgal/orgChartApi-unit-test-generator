import os
import yaml
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
refine_prompt_path = "prompts/_refine.yaml"
with open(refine_prompt_path, "r") as f:
    prompt_config = yaml.safe_load(f)
test_path = "tests/initial/test_orgController.cpp"
if not os.path.exists(test_path):
    print(f"Test file not found at {test_path}")
    exit(1)

with open(test_path, "r") as f:
    test_code = f.read()
full_prompt = f"""
{prompt_config['task']}

Here is the unit test file:
```cpp
{test_code}
Instructions:
{prompt_config['output']['format']}

Constraints:
{chr(10).join('- ' + c for c in prompt_config['constraints'])}

Other Notes:
{prompt_config['notes'][0]}
"""

try:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a strict C++ unit test reviewer."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.2,
        max_tokens=2000
    )
    refined_test_code = response['choices'][0]['message']['content']
    output_dir = "tests/refined"
    os.makedirs(output_dir, exist_ok=True)
    refined_path = os.path.join(output_dir, "test_orgController_refined.cpp")

    with open(refined_path, "w") as f:
        f.write(refined_test_code)

    print(f"Refined test saved to: {refined_path}")
except Exception as e:
    print("Error during refinement:")
    print(str(e))