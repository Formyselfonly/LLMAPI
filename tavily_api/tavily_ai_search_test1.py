import os
from tavily import TavilyClient
import dotenv
import time
dotenv.load_dotenv()
TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")
DEEPSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY")
from openai import OpenAI




# Initialize Tavily Client with your API key
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


def deep_search(initial_query, max_depth=3, num_results=5):
    """Performs an iterative deep search by refining queries based on retrieved information."""
    explored_queries = set()
    current_query = initial_query
    depth = 0

    while depth < max_depth:
        if current_query in explored_queries:
            print(f"Skipping duplicate query: {current_query}")
            break

        print(f"\n[Depth {depth + 1}] Searching: {current_query}")
        explored_queries.add(current_query)

        # Perform Tavily search
        results = tavily_client.search(query=current_query, search_depth="advanced", max_results=num_results)

        if not results or "results" not in results:
            print("No results found, stopping search.")
            break

        # Print and analyze results
        for i, result in enumerate(results["results"]):
            title = result.get("title", "No Title")
            url = result.get("url", "No URL")
            snippet = result.get("snippet", "No Snippet Available")  # Handle missing snippet safely

            print(f"{i + 1}. {title}")
            print(f"URL: {url}")
            print(f"Snippet: {snippet}\n")

        # Extract new search terms from top results
        new_queries = [result['title'] for result in results["results"][:3] if
                       result.get('title') not in explored_queries]

        if not new_queries:
            print("No new relevant queries found, stopping search.")
            break

        # Choose the next query for deeper search
        current_query = new_queries[0]
        depth += 1
        time.sleep(2)  # Avoid excessive API requests


deepseek_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def deepseek_api_call(input):
    response = deepseek_client.chat.completions.create(
        # deepseek-chat
        # deepseek-reasoner
        model="deepseek-chat",
        max_tokens=8192,
        # response_format={
        #     "type": "json_object"
        # },
        messages=[
            {
                "role": "system",
                "content": "You are my helpful assistant"
            },
            {
                "role": "user",
                "content": input

            },
        ],
        stream=False
    )
    # return response
    return response.choices[0].message.content

def keywords_transfer(query):
    response = deepseek_client.chat.completions.create(
        # deepseek-chat
        # deepseek-reasoner
        model="deepseek-chat",
        max_tokens=8192,
        # response_format={
        #     "type": "json_object"
        # },
        messages=[
            {
                "role": "system",
                "content": "You are my helpful assistant"
            },
            {
                "role": "user",
                "content": f"Here my convert my language into keywords so that I can search by that:{query}.Just give me keywords separate by space,don't give me additional information"

            },
        ],
        stream=False
    )
    # return response
    return response.choices[0].message.content

query="特朗普和马斯克谁儿子多？"
keywords=keywords_transfer(query)
print(keywords)

# Run deep search
deep_search(keywords, max_depth=4)
