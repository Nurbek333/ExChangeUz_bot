import requests

# API dan trenddagi valyutalarni olish funksiyasi
def get_trending_cryptos(timeframe="24h"):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    parameters = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,  # 20 ta top coin olish
        "page": 1,
        "sparkline": False
    }
    
    response = requests.get(url, params=parameters)
    data = response.json()

    # Vaqt oralig‘iga qarab saralash
    if timeframe == "24h":
        top_gainers = sorted(data, key=lambda x: x["price_change_percentage_24h"], reverse=True)[:5]
        top_losers = sorted(data, key=lambda x: x["price_change_percentage_24h"])[:5]
    elif timeframe == "7d":
        top_gainers = sorted(data, key=lambda x: x["price_change_percentage_7d_in_currency"], reverse=True)[:5]
        top_losers = sorted(data, key=lambda x: x["price_change_percentage_7d_in_currency"])[:5]
    
    gainers_text = "🚀 *Eng ko‘p o‘sdi:*\n"
    for coin in top_gainers:
        gainers_text += f"✅ {coin['name']} ({coin['symbol'].upper()}): {round(coin['price_change_percentage_24h' if timeframe == '24h' else 'price_change_percentage_7d_in_currency'], 2)}%\n"

    losers_text = "\n📉 *Eng ko‘p tushdi:*\n"
    for coin in top_losers:
        losers_text += f"❌ {coin['name']} ({coin['symbol'].upper()}): {round(coin['price_change_percentage_24h' if timeframe == '24h' else 'price_change_percentage_7d_in_currency'], 2)}%\n"

    return gainers_text + losers_text
