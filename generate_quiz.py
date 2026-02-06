from pathlib import Path
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

INPUT_FILE = "input_notes/lesson_2026_02_05.md"
OUTPUT_FILE = "output_summaries/quiz_2026_02_05.md"

lesson_text = Path(INPUT_FILE).read_text(encoding="utf-8")

prompt = f"""
あなたは日本語教師です。
以下のレッスンメモを元に小テストを作ってください。

選択問題5問
穴埋め問題5問
単語問題5問
解答と解説も含める

{lesson_text}
"""

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": prompt}],
)

quiz = response.choices[0].message.content
Path(OUTPUT_FILE).write_text(quiz, encoding="utf-8")

print("Quiz generated.")
