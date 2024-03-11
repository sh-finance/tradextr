from service.llm import extract_keywords_for_search


res = extract_keywords_for_search(
    [
        {"role": "user", "content": "小米汽车怎么样了?"},
        {"role": "assistant", "content": "小米汽车大概下半年发布"},
        {"role": "user", "content": "大概多少钱"},
    ]
)
print(res)
