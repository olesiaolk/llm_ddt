import os
import re
import pandas as pd
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# --- Завантаження API ключа ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Зчитування системного prompt ---
with open("prompt/system_prompt.txt") as f:
    system_prompt = f.read()

# --- Зчитування тестових даних ---
df = pd.read_csv("data/test_conversations.csv")
df.columns = df.columns.str.strip()  # обрізаємо пробіли у заголовках

# --- Функція для парсингу рядка атрибутів у словник ---
def parse_attributes(text):
    d = {}
    for p in text.split("|"):
        if ":" in p:
            k, v = p.split(":", 1)
            d[k.strip()] = v.strip()
    return d

# --- Нормалізація телефону ---
def normalize_phone(phone):
    digits = re.sub(r'\D', '', phone)  # залишаємо тільки цифри
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone  # якщо не 10 цифр, повертаємо як є

# --- Нормалізація дати ---
def normalize_date(date_str):
    try:
        dt = datetime.strptime(date_str, "%d-%b-%Y")
        return dt.strftime("%d-%b-%Y")
    except ValueError:
        try:
            dt = datetime.strptime(date_str, "%d/%m/%Y")
            return dt.strftime("%d-%b-%Y")
        except ValueError:
            return date_str  # якщо не вдалось, повертаємо як є

# --- Функція для нормалізації всіх атрибутів ---
def normalize_attributes(d):
    d = d.copy()
    if 'Phone number' in d:
        d['Phone number'] = normalize_phone(d['Phone number'])
    if 'Move date' in d:
        d['Move date'] = normalize_date(d['Move date'])
    return d

actuals, status = [], []

for idx, row in df.iterrows():
    conv = row['chat_history']
    expected = row['expected_attributes']

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": conv}
        ]
    )
    actual = response.choices[0].message.content.strip()
    actuals.append(actual)

    # Парсимо рядки у словники
    actual_dict = normalize_attributes(parse_attributes(actual))
    expected_dict = normalize_attributes(parse_attributes(expected))

    is_match = actual_dict == expected_dict
    status.append(is_match)

    # Друк для дебагу
    print(f"Row {idx+1}: Match={is_match}")
    print("Expected:", expected_dict)
    print("Actual  :", actual_dict)
    print("-"*50)

# --- Збереження результатів ---
df['actual_attributes'] = actuals
df['status'] = status
accuracy = sum(status)/len(status)*100
df['accuracy'] = accuracy
df.to_csv("output/results.csv", index=False)

print(f"Тест завершено. Accuracy: {accuracy:.2f}%")
