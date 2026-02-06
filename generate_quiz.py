from pathlib import Path
import os
from datetime import datetime
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
)

DEPLOYMENT_NAME = os.environ["AZURE_OPENAI_DEPLOYMENT"]

# ←ここが新しい部分
today = datetime.now().strftime("%Y_%m_%d")

INPUT_FILE = f"input_notes/lesson_{today}.md"
OUTPUT_FILE = f"output_summaries/quiz_{today}.md"

lesson_text = Path(INPUT_FILE).read_text(encoding="utf-8")

prompt = f"""
あなたは日本語教師です。
以下のレッスンメモを元に小テストを作ってください。

出力形式は必ず固定：
- 選択問題 5問
- 穴埋め問題 5問
- 単語翻訳問題 5問
- 答えと解説は最後にまとめる

レッスンメモ:
{lesson_text}
"""

response = client.chat.completions.create(
    model=DEPLOYMENT_NAME,
    messages=[{"role": "user", "content": prompt}],
)

quiz = response.choices[0].message.content
Path(OUTPUT_FILE).write_text(quiz, encoding="utf-8")

print("Quiz generated:", OUTPUT_FILE)
