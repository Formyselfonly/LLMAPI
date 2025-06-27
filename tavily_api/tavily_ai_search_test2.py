import os
from tavily import TavilyClient
from openai import OpenAI
import dotenv
from twisted.python.util import println

dotenv.load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY")
# 初始化客户端
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
deepseek_client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)
openai_client = OpenAI(
    api_key=OPENAI_API_KEY
)

def search_with_tavily(query):
    """使用Tavily SDK进行搜索，返回搜索结果"""
    try:
        response = tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )
        return response.get("results", [])
    except Exception as e:
        print(f"搜索失败：{e}")
        return None

def summary_with_deepseek(search_results):
    """使用DeepSeek SDK处理搜索结果，生成回答"""
    if not search_results:
        return "无搜索结果可处理。"

    # 构造提示词
    prompt = "请根据以下搜索结果生成一个简洁的回答：\n"
    for result in search_results:
        prompt += f"- {result['title']}: {result.get('snippet', '无摘要')}\n"

    try:
        response = deepseek_client.chat.completions.create(
            # deepseek-chat gpt-4o
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"语言处理失败：{e}")
        return "无法生成回答。"

def response_with_searchresult(search_answer,query):
    response = deepseek_client.chat.completions.create(
        # deepseek-chat gpt-4o
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"请根据search_answer:{search_answer}回答我的问题:{query}"}
        ],
        max_tokens=150,
        stream=False
    )
    return response.choices[0].message.content

def keyword_with_deepseek(query):
    response = deepseek_client.chat.completions.create(
        # deepseek-chat gpt-4o
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Here my convert my language into keywords so that I can search by that:{query}.Just give me keywords separate by space,don't give me additional information"}
        ],
        # max_tokens=150,
        stream=False
    )
    return response.choices[0].message.content

def keywords_to_useful(keywords):
    response = deepseek_client.chat.completions.create(
        # deepseek-chat gpt-4o
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant,you need to help add enough context keywords if need so that I can search well"},
            {"role": "user", "content": f"""Here is my keywords{keywords}，Beacuse When searching, there will be some context information that humans already know, such as the current year.
            For example, if I ask who the President of the United States is, and the current year is 2025, then I am asking about the 2025 U.S. President, not the 2024 U.S. President.
            So You need to supplement the relevant contextual information in the keywords. Remember,transfer all of them to useful keywords than give to me!What I need is keywords"""}
        ],
        # max_tokens=150,
        stream=False
    )
    return response.choices[0].message.content

def extract_keywords(useful_keywords):
    response = deepseek_client.chat.completions.create(
        # deepseek-chat gpt-4o
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant,you need to help me extract keywords"},
            {"role": "user", "content": f"""Here is my keywords{useful_keywords}，just extract keywords for me!Don't give other information!"""}
        ],
        # max_tokens=150,
        stream=False
    )
    return response.choices[0].message.content

def math_keywords(keywords_need_match,query):
    response = deepseek_client.chat.completions.create(
        # deepseek-chat gpt-4o
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant,you need to help me extract keywords"},
            {"role": "user", "content": f"""Here is my keywords:"{keywords_need_match}"，Here is my query:"{query}",match my query and keywords,it should based on query,and return keywords that totally match my query,and don't loss the realtime information such as time,all of realtime information keywords should be totallly math with keywords.Just give me keywords,The keywords should be separate by space"""}
        ],
        # max_tokens=150,
        stream=False
    )
    return response.choices[0].message.content

def clear_multiple_keywords(final_keywords):
    response = deepseek_client.chat.completions.create(
        # deepseek-chat gpt-4o
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant,you need to help me extract keywords"},
            {"role": "user", "content": f"Here is my keywords:{final_keywords},Help me delete multiple keywords and just return me unique keywords,don't give me attitional information"}
        ],
        # max_tokens=150,
        stream=False

    )
    return response.choices[0].message.content


def ai_search(query):
    """AI搜索主函数，整合Tavily搜索和DeepSeek语言处理"""
    keywords = keyword_with_deepseek(query)
    if(log_open==True):
        println("keywords",keywords)
    useful_keywords=keywords_to_useful(keywords)
    if(log_open==True):
        println("useful_keywords",useful_keywords)
    keywords_need_match=extract_keywords(useful_keywords)
    if(log_open==True):
        println("keywords_need_match",keywords_need_match)
    final_keywords=math_keywords(keywords_need_match,query)
    if(log_open==True):
        println("final_keywords",final_keywords)
    unique_final_keywords=clear_multiple_keywords(final_keywords)
    if(log_open==True):
        println("unique_final_keywords",unique_final_keywords)
    search_results = search_with_tavily(unique_final_keywords)
    if(log_open==True):
        println("search_results",search_results)
    if search_results:
        search_answer = summary_with_deepseek(search_results)
        answer=response_with_searchresult(search_answer,query)
        return answer
    else:
        return "搜索失败，请检查API密钥或网络连接。"


# 示例使用
if __name__ == "__main__":
    log_open=True
    DEEPSEEK_CHAT="deepseek-chat"
    GPT_4O="gpt-4o"
    model_name=DEEPSEEK_CHAT
    query = "特朗普和马斯克谁儿子多？"
    result = ai_search(query)
    println("------------------------------------------------------------------------")
    print("\n回答：", result)