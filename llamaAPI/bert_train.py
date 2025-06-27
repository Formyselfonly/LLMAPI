from transformers import BertTokenizer, DistilBertForSequenceClassification, TrainingArguments, Trainer
from transformers import DistilBertTokenizer
from datasets import load_dataset
import torch
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import os
import dotenv
from huggingface_hub import login
dotenv.load_dotenv()
os.getenv("HUGGING_FACE_TOKEN")

# 0.Login with HuggingFace
login(token=os.getenv("HUGGING_FACE_TOKEN"))
# ✅ 1. 加载本地 TSV 数据集
dataset = load_dataset('csv', data_files={
    'train': 'train.tsv',
    'test': 'test.tsv'
}, delimiter='\t')

# ✅ 2. 选择 Hugging Face 上公开的 DistilBERT 中文模型
model_name = "distilbert/distilbert-base-uncased"

# ✅ 3. 加载 tokenizer 和模型
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=2)

# ✅ 4. 分词函数
def tokenize_function(example):
    return tokenizer(example["text"], padding="max_length", truncation=True, max_length=128)

# ✅ 5. 数据预处理
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# ✅ 6. 设置训练参数
training_args = TrainingArguments(
    output_dir="../OpenAIAPI/results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_dir="./logs",
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    learning_rate=2e-5,
    load_best_model_at_end=True,
)

# ✅ 7. 定义评估指标
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    acc = accuracy_score(labels, preds)
    return {
        "accuracy": acc,
        "f1": f1,
        "precision": precision,
        "recall": recall
    }

# ✅ 8. 创建 Trainer 实例
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# ✅ 9. 开始训练
trainer.train()

# ✅ 10. 保存模型到本地
trainer.save_model("./sentiment-model-distilbert")
