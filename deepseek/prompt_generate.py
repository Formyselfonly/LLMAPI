from random import choice

from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
PROMPT_PREFIX="""
Given a task description or existing prompt, produce a detailed system prompt to guide a language model in completing the task effectively.
# Guidelines
- Understand the Task: Grasp the main objective, goals, requirements, constraints, and expected output.
- Minimal Changes: If an existing prompt is provided, improve it only if it's simple. For complex prompts, enhance clarity and add missing elements without altering the original structure.
- Reasoning Before Conclusions**: Encourage reasoning steps before any conclusions are reached. ATTENTION! If the user provides examples where the reasoning happens afterward, REVERSE the order! NEVER START EXAMPLES WITH CONCLUSIONS!
    - Reasoning Order: Call out reasoning portions of the prompt and conclusion parts (specific fields by name). For each, determine the ORDER in which this is done, and whether it needs to be reversed.
    - Conclusion, classifications, or results should ALWAYS appear last.
- Examples: Include high-quality examples if helpful, using placeholders [in brackets] for complex elements.
   - What kinds of examples may need to be included, how many, and whether they are complex enough to benefit from placeholders.
- Clarity and Conciseness: Use clear, specific language. Avoid unnecessary instructions or bland statements.
- Formatting: Use markdown features for readability. DO NOT USE ``` CODE BLOCKS UNLESS SPECIFICALLY REQUESTED.
- Preserve User Content: If the input task or prompt includes extensive guidelines or examples, preserve them entirely, or as closely as possible. If they are vague, consider breaking down into sub-steps. Keep any details, guidelines, examples, variables, or placeholders provided by the user.
- Constants: DO include constants in the prompt, as they are not susceptible to prompt injection. Such as guides, rubrics, and examples.
- Output Format: Explicitly the most appropriate output format, in detail. This should include length and syntax (e.g. short sentence, paragraph, JSON, etc.)
    - For tasks outputting well-defined or structured data (classification, JSON, etc.) bias toward outputting a JSON.
    - JSON should never be wrapped in code blocks (```) unless explicitly requested.
The final prompt you output should adhere to the following structure below. Do not include any additional commentary, only output the completed system prompt. SPECIFICALLY, do not include any additional messages at the start or end of the prompt. (e.g. no "---")

"""

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def prompt_generator(aim,step,rule,constrain,example):
    response = client.chat.completions.create(
        # deepseek-chat
        # deepseek-reasoner
        model="deepseek-reasoner",
        max_tokens=8192,
        # response_format={
        #     "type": "json_object"
        # },
        messages=[
            {
                "role": "system",
                "content": "You are my Prompt master which can help me generator useful and wonderful Prompt!"
            },
            {
                "role": "user",
                "content": f"""
                {PROMPT_PREFIX}
                
                Here is my require,and you need to generate a useful and wonderful and well-format and well structured prompt for me.
                # Aim
                {aim}
                # Step
                {step}
                # Rule
                {rule}
                # Constrain
                {constrain}
                # Example 
                {example}
                
                """
            },
        ],
        stream=False
    )
    # return response
    return response.choices[0].message.content

prompt_for_translate=prompt_generator(
    aim="我想要实现多语言翻译的功能，无论什么语言，都为我翻译为中文",
    step="1.识别用户输入的语言 2.将用户输入的语言精确的翻译为中文",
    rule="请确保翻译的准确性，在语境和意境都要完美翻译",
    constrain="不要增加多余的内容，只为我翻译内容即可",
    example="userinput:Who are u?  outputbyyu:你是谁？"
)
print(prompt_for_translate)



