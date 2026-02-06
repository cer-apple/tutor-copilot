from pathlib import Path
import os
from datetime import date
from openai import AzureOpenAI

# -------------------------
# Azure OpenAI client
# -------------------------
client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
)

DEPLOYMENT_NAME = os.environ["AZURE_OPENAI_DEPLOYMENT"]

# -------------------------
# File paths
# -------------------------
today = date.today().strftime("%Y-%m-%d")

INPUT_FILE = "input_notes/lesson_2026_02_05.md"
OUTPUT_FILE = f"output_summaries/quiz_{today}.md"

lesson_text = Path(INPUT_FILE).read_text(encoding="utf-8")

# -------------------------
# Prompt
# -------------------------
prompt = f"""
あなたは日本語教師です。
以下のレッスンメモを元に小テストを作ってください。

重要なルール：
・問題と答えは分離する
・問題セクションには答えを書かない
・最後に「解答・解説」セクションを作る
・Markdown形式で出力する

出力フォーマット：

# 小テスト（{today}）

## 問題

### 選択問題（5問）
### 穴埋め問題（5問）
### 単語翻訳問題（5問）

---

## 解答・解説
Q1〜Q15の答えと解説を書く

---

レッスンメモ:
{lesson_text}
"""

# -------------------------
# Call model
# -------------------------
response = client.chat.completions.create(
    model=DEPLOYMENT_NAME,
    messages=[{"role": "user", "content": prompt}],
)

quiz = response.choices[0].message.content

Path(OUTPUT_FILE).write_text(quiz, encoding="utf-8")

print("Quiz generated:", OUTPUT_FILE)
