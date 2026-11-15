# 🩺 Doctor AI Chat Bot

**aiogram** va **FastAPI** asosida qurilgan shifokor-AI Telegram boti. Foydalanuvchi ro'yxatdan o'tadi va AI shifokor bilan suhbatlashadi.

---

## ✨ Imkoniyatlar

- 🌐 **Ko'p tilli:** o'zbek, rus, ingliz
- 📝 **Ro'yxatdan o'tish:** ism, familiya, yosh, jins, telefon, parol
- 🤖 **AI suhbat:** shifokor rolidagi AI javoblari
- 💾 **Ma'lumotlar bazasi:** foydalanuvchi va suhbatlar saqlanadi
- 🔒 **Parol himoyasi:** suhbat tarixi parol bilan

---

## 🛠 Texnologiyalar

| Texnologiya | Maqsad |
|---|---|
| **Python 3.12+** | Asosiy til |
| **aiogram 3.x** | Telegram bot |
| **FastAPI** | Backend API |
| **SQLAlchemy** | Ma'lumotlar bazasi |
| **aiohttp** | HTTP so'rovlar |

---

## ⚙️ O'rnatish

```bash
git clone https://github.com/dastonbek8747/Doctor_AI_chat_bot.git
cd Doctor_AI_chat_bot
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

`.env` fayl yarating:

```env
BOT_TOKEN=123456:ABC...
DATABASE_URL=postgresql://user:pass@localhost/db
```

> 🔒 `.env` git'ga qo'shilmaydi.

---

## ▶️ Ishga tushirish

```bash
cd Bot && python main.py
```

---

## 📁 Loyiha tuzilishi

```
Doctor_AI_chat_bot/
├── Bot/
│   ├── main.py         # Bot ishga tushirish
│   ├── handlers.py     # Handler'lar va tillar
│   └── pyproject.toml
└── backend/
    ├── main.py         # FastAPI app
    └── ai_model/       # AI modeli va promptlar
```

---

## 📄 Litsenziya

Litsenziya ko'rsatilmagan.
