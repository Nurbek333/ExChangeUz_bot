from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from loader import dp
from kalkulyator_api import get_crypto_price, get_usd_to_uzs

# Kripto qiymatini hisoblash funksiyasi
def calculate_crypto_value(amount, crypto, currency="USD"):
    price = get_crypto_price(crypto, "USD")  # Kripto -> USD kursi
    if price is None:
        return "❌ Xatolik: Kripto kursini olish imkoni bo‘lmadi."

    if currency == "USD":
        total_value = amount * price
        return f"💰 {amount} {crypto} ≈ {total_value:,.2f} USD"
    
    elif currency == "UZS":
        usd_to_uzs = get_usd_to_uzs()  # USD -> UZS kursini olish
        if usd_to_uzs is None:
            return "❌ Xatolik: USD kursini olish imkoni bo‘lmadi."

        total_value = amount * price * usd_to_uzs
        return f"💰 {amount} {crypto} ≈ {total_value:,.0f} UZS"
    
    else:
        return "❌ Xatolik: Noto‘g‘ri valyuta turi."

# Foydalanuvchi ma'lumotlarini saqlash uchun FSM
class CryptoCalculator(StatesGroup):
    amount = State()
    crypto_type = State()
    currency_type = State()

# Kripto kalkulyatorni ishga tushirish
@dp.message(F.text == "📊 Kripto Kalkulyator")
async def start_calculator(message: types.Message, state: FSMContext):
    await message.answer("🧮 Qancha kriptovalyuta sotib olmoqchisiz?\n\n" 
                         "Masalan: `3.5` yoki `1.2`")
    await state.set_state(CryptoCalculator.amount)

# Foydalanuvchidan miqdorni olish
@dp.message(CryptoCalculator.amount)
async def get_crypto_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        await state.update_data(amount=amount)
        await message.answer("🔹 Qaysi kriptovalyutani hisoblaymiz?\n\n"
                             "Masalan: `BTC`, `ETH`, `SOL`, `DOGE`, `TON`...")
        await state.set_state(CryptoCalculator.crypto_type)
    except ValueError:
        await message.answer("❌ Iltimos, miqdorni to‘g‘ri kiriting. (Masalan: `2.5`)")

# Foydalanuvchidan kripto turini olish
@dp.message(CryptoCalculator.crypto_type)
async def get_crypto_type(message: types.Message, state: FSMContext):
    crypto = message.text.upper()
    await state.update_data(crypto=crypto)
    await message.answer("💵 Qaysi valyutaga o‘giramiz?\n\n"
                         "Variantlar: `USD` yoki `UZS`")
    await state.set_state(CryptoCalculator.currency_type)

# Valyutani tanlash va hisob-kitob qilish
@dp.message(CryptoCalculator.currency_type)
async def get_currency_type(message: types.Message, state: FSMContext):
    currency = message.text.upper()
    
    if currency not in ["USD", "UZS"]:
        await message.answer("❌ Iltimos, `USD` yoki `UZS` ni tanlang!")
        return
    
    data = await state.get_data()
    amount = data["amount"]
    crypto = data["crypto"]
    
    result = calculate_crypto_value(amount, crypto, currency)
    
    await message.answer(f"✅ {result}\n\n🔄 Yangi hisob-kitob qilish uchun 📊 Kripto Kalkulyator ni bosing!")
    await state.clear()
