from pathlib import Path
import os
from datetime import datetime
from openai import AzureOpenAI

# =====================
# Azure OpenAI client
# =====================
client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
)

DEPLOYMENT_NAME = os.environ["AZURE_OPENAI_DEPLOYMENT"]

# =====================
# Date automation
# =====================
today = datetime.now().strftime("%Y_%m_%d")
today_display = datetime.now().strftime("%Y-%m-%d")

INPUT_FILE = f"input_notes/lesson_{today}.md"
OUTPUT_FILE = f"output_summaries/quiz_{today}.md"

lesson_text = Path(INPUT_FILE).read_text(encoding="utf-8")

# =====================
# Prompt
# =====================
prompt = f"""
あなたは日本語教師です。
以下のレッスンメモを元に小テストを作ってください。

タイトル行を必ず入れる：
# 小テスト ({today_display})

出力形式は必ず固定：

## 【選択問題】
Q1:
Q2:
Q3:
Q4:
Q5:

## 【穴埋め問題】
Q6:
Q7:
Q8:
Q9:
Q10:

## 【単語翻訳問題】
Q11:
Q12:
Q13:
Q14:
Q15:

====================
【答えと解説】
====================

A1:
答え:
解説:

A2:
答え:
解説:

A3:
答え:
解説:

A4:
答え:
解説:

A5:
答え:
解説:

A6:
答え:
解説:

A7:
答え:
解説:

A8:
答え:
解説:

A9:
答え:
解説:

A10:
答え:
解説:

A11:
答え:
解説:

A12:
答え:
解説:

A13:
答え:
解説:

A14:
答え:
解説:

A15:
答え:
解説:

レッスンメモ:
{lesson_text}
"""

# =====================
# LLM call
# =====================
response = client.chat.completions.create(
    model=DEPLOYMENT_NAME,
    messages=[{"role": "user", "content": prompt}],
)

quiz = response.choices[0].message.content

# =====================
# Save file
# =====================
Path(OUTPUT_FILE).write_text(quiz, encoding="utf-8")

print("Quiz generated:", OUTPUT_FILE)
