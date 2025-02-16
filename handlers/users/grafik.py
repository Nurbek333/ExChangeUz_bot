import logging
import os
from aiogram import types, F
from aiogram.types import FSInputFile
from keyboard_buttons.admin_keyboard import keyboard
from grafik_api import get_crypto_chart
from loader import dp

# Loggingni yoqamiz
logging.basicConfig(level=logging.INFO)

# 📈 Valyuta tarixi menyusi
@dp.message(F.text == "Valyutalar grafigi")
async def send_crypto_menu(message: types.Message):
    await message.answer("📊 Qaysi kripto valyuta tarixini ko‘rishni xohlaysiz?", reply_markup=keyboard)
import logging
import os
import aiohttp
import datetime
from aiogram import types, F
from aiogram.types import FSInputFile
from keyboard_buttons.admin_keyboard import keyboard
from loader import dp
import matplotlib.pyplot as plt

# Loggingni yoqamiz
logging.basicConfig(level=logging.INFO)

# 📈 Valyuta tarixi menyusi
@dp.message(F.text == "Valyutalar grafigi")
async def send_crypto_menu(message: types.Message):
    await message.answer("📊 Qaysi kripto valyuta tarixini ko‘rishni xohlaysiz?", reply_markup=keyboard)

@dp.message()
async def send_crypto_chart(message: types.Message):
    symbol = message.text.lower().strip()
    
    # API'ga jo‘natishdan oldin foydalanuvchi kiritgan ma’lumotni tekshiramiz
    if not symbol.isalpha():
        await message.answer("❌ Iltimos, faqat harflardan iborat valyuta nomini kiriting (masalan: `bitcoin`, `ethereum`).")
        return

    await message.answer(f"⏳ {symbol.upper()} uchun grafik yuklanmoqda...")
    logging.info(f"✅ {symbol.upper()} grafigini yuklash boshlandi...")

    chart_path, values = await get_crypto_chart(symbol)

    if chart_path and os.path.exists(chart_path):
        photo = FSInputFile(chart_path)
        await message.answer_photo(photo=photo, caption=f"📉 {symbol.upper()} ning so‘nggi 7 kunlik tendensiyasi.")

        # 📊 Narx tahlili
        if values:
            min_price = min(values)
            max_price = max(values)
            avg_price = sum(values) / len(values)
            current_price = values[-1]
            price_change = current_price - values[0]
            trend = "📈 O'sish" if price_change > 0 else "📉 Pasayish"

            analysis = (
                f"📊 *{symbol.upper()} Tahlili:*\n"
                f"🔹 *Eng past narx:* ${min_price:.2f}\n"
                f"🔺 *Eng yuqori narx:* ${max_price:.2f}\n"
                f"📉 *O‘rtacha narx:* ${avg_price:.2f}\n"
                f"💰 *Joriy narx:* ${current_price:.2f}\n"
                f"📊 *Umumiy trend:* {trend} ({price_change:+.2f}$)\n"
            )

            await message.answer(analysis, parse_mode="Markdown")

        os.remove(chart_path)

    else:
        await message.answer(f"❌ {symbol.upper()} uchun ma'lumot mavjud emas yoki xato yuz berdi. Iltimos, to‘g‘ri valyuta nomini kiriting.")
    logging.getLogger().handlers.clear()