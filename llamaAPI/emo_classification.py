from transformers import pipeline

# 加载情感分类 pipeline，模型可替换为中文支持的，比如 hfl/chinese-roberta-wwm-ext
classifier = pipeline("sentiment-analysis", model="uer/roberta-base-finetuned-jd-binary-chinese")

# 推理文本
result = classifier("这个产品真的很好用，我非常喜欢！")[0]

# 原始输出格式通常是：
# {'label': 'LABEL_1', 'score': 0.987}

# 标签映射
label_map = {
    "LABEL_0": "neg",
    "LABEL_1": "pos"
}

# 映射结果
final_result = {
    "label": label_map.get(result['label'], result['label']),
    "score": result['score']
}

print(final_result)
