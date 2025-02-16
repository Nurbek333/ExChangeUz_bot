import requests
from googletrans import Translator

API_KEY = "6176ee5cf8f7ceb907947a1be9688da1a460fdf4"
translator = Translator()

def get_crypto_news():
    url = "https://cryptopanic.com/api/v1/posts/"
    params = {
        "auth_token": API_KEY,
        "public": "true",
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data:
        return "❌ Xatolik: API'dan yangiliklarni olish imkoni bo‘lmadi."

    news_list = data["results"][:5]  # Faqat eng so‘nggi 5 ta yangilikni olish

    result = "📰 **Eng so‘nggi kripto yangiliklar**:\n\n"
    for idx, news in enumerate(news_list, 1):
        title_uz = translator.translate(news["title"], dest="uz").text  # Tarjima qilish
        result += f"🔹 {title_uz}\n🔗 [Batafsil]({news['url']})\n\n"

    return result
