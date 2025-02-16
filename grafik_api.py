import matplotlib.pyplot as plt
import aiohttp
import datetime
import logging

# 📌 Kripto valyutalar ro‘yxati (avval API'dan olib kelinadi)
available_cryptos = {}

# 🔵 Mavjud kripto valyutalarni olish (faqat bir marta yuklanadi)
async def load_available_cryptos():
    global available_cryptos
    if not available_cryptos:  # Agar ro‘yxat bo‘sh bo‘lsa, API chaqiramiz
        url = "https://api.coingecko.com/api/v3/coins/list"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    available_cryptos = {coin["symbol"]: coin["id"] for coin in data}
                    logging.info("✅ Kripto ro‘yxati yuklandi!")
                else:
                    logging.error(f"❌ API xatosi: {response.status}")

# 🔵 API orqali kripto tarixi olish va grafik yaratish
async def get_crypto_chart(symbol):
    await load_available_cryptos()  # 🔹 Mavjud kripto valyutalarni yuklab olamiz
    symbol = symbol.lower().strip()
    symbol_id = available_cryptos.get(symbol)  # 🔹 Endi mavjud bo‘lgan valyutalarni ishlatamiz

    if not symbol_id:
        logging.warning(f"❌ {symbol.upper()} uchun mos kripto topilmadi!")
        return None, None

    url = f"https://api.coingecko.com/api/v3/coins/{symbol_id}/market_chart?vs_currency=usd&days=7"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()

                if "prices" not in data:
                    return None, None

                prices = data["prices"]
                times = [datetime.datetime.fromtimestamp(p[0] / 1000) for p in prices]
                values = [p[1] for p in prices]

                plt.figure(figsize=(8, 4))
                plt.plot(times, values, label=f"{symbol.upper()} narxi", color="blue")
                plt.xlabel("Vaqt")
                plt.ylabel("Narx ($)")
                plt.title(f"{symbol.upper()} O‘sish/Pasayish Tarixi (7 kun)")
                plt.legend()
                plt.grid()
                plt.xticks(rotation=45)

                chart_path = f"{symbol}_trend.png"
                plt.savefig(chart_path)
                plt.close()

                return chart_path, values  # 🔹 Endi ikkita qiymat qaytadi
            else:
                logging.error(f"❌ API xatosi: {response.status}")
                return None, None
