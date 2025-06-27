from tavily import TavilyClient
import dotenv
import os
from openai import OpenAI
dotenv.load_dotenv()
TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
openai_client=OpenAI(api_key=OPENAI_API_KEY)

def handle_response(response_data):
    if response_data.get('answer'):
        return response_data['answer']
    else:
        results = response_data.get('results', [])
        return [
            {
                'title': r['title'],
                'url': r['url'],
                'content': r['content']
            }
            for r in results
        ]

def llm_with_search_result(query,prompt):
    completions=openai_client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=16384,
        messages=[
            {"role":"assistant","content":"system"},
            {"role":"user","content":f"""
            Here is my search query and result: {final_response}.
            Please help me extract the query and answer only,ignore other information.
            The output format should be 
            <
            Query:{query}
            Answer:Write here
            >
            """}
        ],
        stream=False
    )
    return completions.choices[0].message.content

def translate_into_Chinese(search_result):
    completions=openai_client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=16384,
        messages=[
            {"role":"assistant","content":"system"},
            {"role":"user","content":f"""
            Here is my txt,help me translate into Chinese:{search_result}.
            Don't change the format,Don't add other information
            """}
        ],
        stream=False
    )
    return completions.choices[0].message.content



tavily_client=TavilyClient(api_key=TAVILY_API_KEY)
query="谁是梅西"
response=tavily_client.search(query)
final_response=handle_response(response)
search_result=llm_with_search_result(query,final_response)
cn_search_result=translate_into_Chinese(search_result)
print(cn_search_result,"\n")
