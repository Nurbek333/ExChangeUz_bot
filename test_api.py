import requests

# API dan trenddagi valyutalarni olish funksiyasi
def get_trending_cryptos():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    parameters = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False
    }
    
    response = requests.get(url, params=parameters)
    data = response.json()

    # 24 soat ichida eng ko‘p o‘sgan valyutalarni saralash
    top_gainers = sorted(data, key=lambda x: x["price_change_percentage_24h"], reverse=True)[:3]
    top_losers = sorted(data, key=lambda x: x["price_change_percentage_24h"])[:3]

    gainers_text = "🚀 *Eng ko‘p o‘sdi:*\n"
    for coin in top_gainers:
        gainers_text += f"✅ {coin['name']} ({coin['symbol'].upper()}): {round(coin['price_change_percentage_24h'], 2)}%\n"

    losers_text = "\n📉 *Eng ko‘p tushdi:*\n"
    for coin in top_losers:
        losers_text += f"❌ {coin['name']} ({coin['symbol'].upper()}): {round(coin['price_change_percentage_24h'], 2)}%\n"

    return gainers_text + losers_text

# Test qilish
print(get_trending_cryptos())
