from aiogram.types import Message
from loader import dp,db
from aiogram.filters import CommandStart
from api import get_crypto_prices
from aiogram import F
from keyboard_buttons.admin_keyboard import keyboard, crypto_menu
from api_valyuta_usish import get_trending_cryptos
from crypto_yangiliklar import get_crypto_news

@dp.message(CommandStart())
async def start_command(message:Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    try:
        db.add_user(full_name=full_name,telegram_id=telegram_id) #foydalanuvchi bazaga qo'shildi
        await message.answer(text="Assalomu alaykum, botimizga hush kelibsiz", reply_markup=keyboard)
    except:
        await message.answer(text="Assalomu alaykum", reply_markup=keyboard)


# "Krypto" tugmasi bosilganda
@dp.message(F.text == "💎 Kriptovalyutalar kursi")
async def send_crypto_prices(message: Message):
    prices = get_crypto_prices()
    photo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQROWaSA_9Is9WevWZDRDl3apvNICPhDV6RYfHSNzitOPBav0Q_WwbrNtOh6Zm_mYg9IWc&usqp=CAU"
    
    response_message = (
        f"💰 Bitcoin (BTC): {prices['BTC']['USD']} USD\n\n"
        f"💎 Ethereum (ETH): {prices['ETH']['USD']} USD\n\n"
        f"💲 Tether (USDT): {prices['USDT']['USD']} USD\n\n"
        f"🏆 Binance Coin (BNB): {prices['BNB']['USD']} USD\n\n"
        f"⚡ Solana (SOL): {prices['SOL']['USD']} USD\n\n"
        f"🚀 XRP (XRP): {prices['XRP']['USD']} USD\n\n"
        f"💵 USD Coin (USDC): {prices['USDC']['USD']} USD\n\n"
        f"🐕 Dogecoin (DOGE): {prices['DOGE']['USD']} USD\n\n"
        f"📦 TONCoin (TON): {prices['TON']['USD']} USD\n\n"
        f"🌟 Cardano (ADA): {prices['ADA']['USD']} USD\n\n"
        f"🐶 Shiba Inu (SHIB): {prices['SHIB']['USD']} USD\n\n"
        f"🌎 Avalanche (AVAX): {prices['AVAX']['USD']} USD\n\n"
        f"🔶 TRON (TRX): {prices['TRX']['USD']} USD\n\n"
        f"🔗 Polkadot (DOT): {prices['DOT']['USD']} USD\n\n"
        f"🔍 Litecoin (LTC): {prices['LTC']['USD']} USD\n\n"
        f"🔷 Polygon (MATIC): {prices['MATIC']['USD']} USD\n\n"
    )
    
    await message.answer_photo(photo=photo, caption=response_message, reply_markup=keyboard)


# Trend valyutalar menyusi
@dp.message(F.text == "📈 Valyuta o'sish va pasayish tarixi")
async def send_trending_menu(message: Message):
    await message.answer("📊 Trenddagi kriptovalyutalarni tanlang:", reply_markup=crypto_menu)

# 24 soatlik trendlarni ko‘rsatish
@dp.message(F.text == "📊 24 Soat")
async def send_24h_trending(message: Message):
    trending_data = get_trending_cryptos("24h")
    await message.answer(trending_data, parse_mode="Markdown")

# 7 kunlik trendlarni ko‘rsatish
@dp.message(F.text == "📈 7 Kun")
async def send_7d_trending(message: Message):
    await message.answer("Kechirasiz bu bo'lim hali mavjud emas!", parse_mode="Markdown")

# Orqaga qaytish
@dp.message(F.text == "🔙 Orqaga")
async def go_back(message: Message):
    await message.answer("🔙 Asosiy menyuga qaytdingiz.", reply_markup=keyboard)

@dp.message(F.text == "📰 Kripto yangiliklari")
async def send_crypto_news(message: Message):
    news_data = get_crypto_news()
    await message.answer(news_data, parse_mode="html", disable_web_page_preview=True)
    