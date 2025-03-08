import os
import openai  
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")

# API kalitni client yaratishda beramiz
client = openai.OpenAI(api_key=API_KEY)

def analyze_book_summary(book_text: str) -> str:
    """Kitob tahlilini AI orqali qaytaradi (openai>=1.0.0 versiyasi uchun)."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Sen kitob tahlil qiluvchi yordamchi botsan. Javoblarni O'zbek tilida ber."},
                {"role": "user", "content": f"Quyidagi kitob haqida qisqacha tahlil ber: {book_text}"}
            ]
        )
        return response.choices[0].message.content  # Natijani olish
    except Exception as e:
        return f"⚠️ Xatolik yuz berdi: {e}"


def recommend_books(genre: str) -> str:
    """AI yordamida kitob tavsiyalarini qaytaradi."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Sen kitob tavsiya qiluvchi yordamchi botsan. Javoblarni O'zbek tilida ber."},
                {"role": "user", "content": f"Menga {genre} janridagi 3 ta kitob tavsiya qil: kitob nomi, muallifi, janri va varaqlar soni bilan."}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Xatolik yuz berdi: {e}"
    

def chat_books(question: str) -> str:
    """AI yordamida foydalanuvchining kitob haqidagi savoliga javob beradi."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Sen kitoblar bo'yicha bilimli yordamchi botsan. Javoblarni O'zbek tilida ber."},
                {"role": "user", "content": f"{question}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Xatolik yuz berdi: {e}"
    