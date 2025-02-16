from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Foydalanuvchilar soni"),
            KeyboardButton(text="Reklama yuborish"),
        ]
        
    ],
   resize_keyboard=True,
   input_field_placeholder="Menudan birini tanlang"
)

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💎 Kriptovalyutalar kursi"),
            KeyboardButton(text="📰 Kripto yangiliklari")
        ],
        [
            KeyboardButton(text="📊 Kripto Kalkulyator"),
            KeyboardButton(text="Valyutalar grafigi")
        ],
        [
            KeyboardButton(text="📈 Valyuta o'sish va pasayish tarixi")
        ]
        
    ],
   resize_keyboard=True,
)

# Kriptovalyuta menyusi tugmalari
crypto_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 24 Soat"), KeyboardButton(text="📈 7 Kun")],
        [KeyboardButton(text="🔙 Orqaga")]
    ],
    resize_keyboard=True
)
