# bot.py

import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# --- Car Database ---
# Images are in the same folder as bot.py
car_database = {
    "budget": [
        {"name": "Toyota Corolla", "price": 20000, "type": "Sedan", "market_price_range": "$19,000 - $21,000", "image": "corolla.jpg"},
        {"name": "Honda Civic", "price": 22000, "type": "Sedan", "market_price_range": "$21,000 - $23,000", "image": "civic.jpg"},
    ],
    "mid_range": [
        {"name": "BMW 3 Series", "price": 40000, "type": "Sedan", "market_price_range": "$39,000 - $42,000", "image": "bmw3.jpg"},
        {"name": "Audi A4", "price": 42000, "type": "Sedan", "market_price_range": "$41,000 - $44,000", "image": "a4.jpg"},
    ],
    "luxury": [
        {"name": "Rolls Royce Ghost", "price": 300000, "type": "Luxury", "market_price_range": "$310,000 - $350,000", "image": "ghost.jpg"},
        {"name": "Maybach S-Class", "price": 250000, "type": "Luxury", "market_price_range": "$260,000 - $280,000", "image": "maybach.jpg"},
    ],
    "supercar": [
        {"name": "Ferrari F8", "price": 300000, "type": "Supercar", "market_price_range": "$310,000 - $350,000", "image": "ferrari_f8.jpg"},
        {"name": "Lamborghini Huracan", "price": 310000, "type": "Supercar", "market_price_range": "$320,000 - $360,000", "image": "huracan.jpg"},
        {"name": "McLaren 720S", "price": 320000, "type": "Supercar", "market_price_range": "$330,000 - $370,000", "image": "mclaren_720s.jpg"},
    ]
}

# --- Start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Welcome to the Car Advisor Bot! 🚗💨\n\n"
        "Available categories: budget, mid_range, luxury, supercar\n"
        "Type your category to get recommendations."
    )
    await update.message.reply_text(welcome_text)

# --- Handle messages ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip().lower()

    # If user types "start" as text
    if user_input == "start":
        await start(update, context)
        return

    # Check if user input is a valid category
    if user_input in car_database:
        cars = car_database[user_input]
        top_3 = random.sample(cars, min(3, len(cars)))

        for idx, car in enumerate(top_3, start=1):
            market_range = car['market_price_range'].replace('$','').replace(',','').split(' - ')
            market_avg = sum([int(price) for price in market_range]) // 2
            price_diff = car['price'] - market_avg

            if price_diff < 0:
                diff_msg = f"✅ ${abs(price_diff)} below market average!"
            elif price_diff > 0:
                diff_msg = f"⚠️ ${price_diff} above market average!"
            else:
                diff_msg = "💵 Price matches market average!"

            msg = (
                f"⭐️ {idx}. {car['name']} - Type: {car['type']}\n"
                f"💵 Bot Price: ${car['price']}\n"
                f"🏷 Market Price Range: {car['market_price_range']}\n"
                f"{diff_msg}"
            )

            # Send the image with caption
            if os.path.exists(car['image']):
                with open(car['image'], "rb") as photo:
                    await update.message.reply_photo(photo=photo, caption=msg)
            else:
                await update.message.reply_text(msg)
    else:
        await update.message.reply_text("❌ Sorry, we don't have recommendations for that category yet.")

# --- Main ---
if __name__ == "__main__":
    TOKEN = "8113149317:AAG3_mZkNdlN0QtD6wCcZGuJM5ItyrxbCZQ"  # <-- Replace with your bot token

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()
