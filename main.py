from telegram import (
    Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
import nest_asyncio
import asyncio

nest_asyncio.apply()

import os

TOKEN = os.getenv("TOKEN")
ADMIN_IDS = [373588422, 113250960]  # لیست ادمین‌ها

SITE_URL = "https://mvmchery.com/"  # آدرس سایت رسمی

brands = {
    "XTRIM": {
        "models": {
            "VX": {
                "price": "3,850,000,000 تومان",
                "plan": "نقدی و اقساطی",
                "image": "https://via.placeholder.com/500x300.png?text=LV"
            },
            "TXL": {
                "price": "4,000,000,000 تومان",
                "plan": "نقدی",
                "image": "https://via.placeholder.com/500x300.png?text=MV"
            },
            "LX": {
                "price": "4,250,000,000 تومان",
                "plan": "اقساطی",
                "image": "https://via.placeholder.com/500x300.png?text=UV"
            }
        }
    },
    "FOWNIX": {
        "models": {
            "تیگو 8": {
                "price": "3,850,000,000 تومان",
                "plan": "نقدی و اقساطی",
                "image": "https://via.placeholder.com/500x300.png?text=LV"
            },
            "تیگو 7": {
                "price": "4,000,000,000 تومان",
                "plan": "نقدی",
                "image": "https://via.placeholder.com/500x300.png?text=MV"
            },
            "آریزو 8": {
                "price": "4,000,000,000 تومان",
                "plan": "نقدی",
                "image": "https://via.placeholder.com/500x300.png?text=MV"
            },
            "آریزو 6": {
                "price": "4,000,000,000 تومان",
                "plan": "نقدی",
                "image": "https://via.placeholder.com/500x300.png?text=MV"
            },
            " آریزو  6 پرو": {
                "price": "4,000,000,000 تومان",
                "plan": "نقدی",
                "image": "https://via.placeholder.com/500x300.png?text=MV"
            },
            "آریزو  5": {
                "price": "4,250,000,000 تومان",
                "plan": "اقساطی",
                "image": "https://via.placeholder.com/500x300.png?text=UV"
            }
        }
    },
    "MVM": {
        "models": {
            "X22": {
                "price": "2,950,000,000 تومان",
                "plan": "نقدی و اقساطی",
                "image": "https://via.placeholder.com/500x300.png?text=X22"
            },
            "X33": {
                "price": "3,150,000,000 تومان",
                "plan": "نقدی",
                "image": "https://via.placeholder.com/500x300.png?text=X33"
            },
            "X55": {
                "price": "3,450,000,000 تومان",
                "plan": "اقساطی",
                "image": "https://via.placeholder.com/500x300.png?text=X55"
            }
        }
    }
}

user_states = {}

def get_main_keyboard():
    keyboard = [[brand] for brand in brands.keys()]
    keyboard.append(["📞 تماس با مشاور"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_models_keyboard(brand_name):
    models = brands[brand_name]["models"]
    keyboard = [[model] for model in models.keys()]
    keyboard.append(["بازگشت به برندها"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_welcome_message():
    return (
        "🚗 به صفحه فروش مدیران خودرو خوش آمدید!\n"
        "👩‍💼 کارشناس فروش: مریم جوزی\n"
        "📞 شماره تماس: 02634057700 داخلی 2003\n"
        f"🌐 برای مشاهده جزئیات بیشتر محصولات به سایت ما مراجعه کنید:\n{SITE_URL}\n\n"
        "لطفاً با زدن ستارت برند خودرو را انتخاب کنید."
    )

async def send_car_info(update: Update, brand_name, model_name):
    car = brands[brand_name]["models"][model_name]
    caption = (
        f"📌 مشخصات خودرو {model_name} از برند {brand_name}:\n"
        f"💰 قیمت: {car['price']}\n"
        f"📝 شرایط ثبت‌نام: {car['plan']}\n\n"
        "📞 تماس با مشاور: 02634057700 داخلی 2003\n"
        f"🌐 برای توضیحات بیشتر و اطلاعات کامل‌تر به سایت مراجعه کنید:\n{SITE_URL}"
    )
    try:
        await update.message.reply_photo(photo=car["image"], caption=caption)
    except Exception as e:
        await update.message.reply_text("❗️خطا در ارسال تصویر. متن خودرو:\n" + caption)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_states[user_id] = "main_menu"
    await update.message.reply_text(get_welcome_message(), reply_markup=get_main_keyboard())

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔️ شما دسترسی به پنل مدیریت ندارید.")
        return
    user_states[user_id] = "admin_select_brand"
    await update.message.reply_text("🛠 لطفاً یک برند برای ویرایش انتخاب کنید:", reply_markup=get_main_keyboard())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()
    state = user_states.get(user_id, "main_menu")

    if text == "📞 تماس با مشاور":
        await update.message.reply_text(
            "📞 برای تماس با مشاور فروش با شماره 02634057700 داخلی 2003 تماس بگیرید.\n"
            "🏢 اداره تحویل: تهران، بلوار ایران خودرو خیابان زامیاد پلاک 17"
        )
        await update.message.reply_text(
            "👇 انتخاب کنید:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 تماس مستقیم", url="tel:02634057700")],
                [InlineKeyboardButton("💬 واتساپ", url="https://wa.me/989123456789")]
            ])
        )
        return

    if user_id in ADMIN_IDS:
        if state == "admin_select_brand":
            if text in brands:
                context.user_data["admin_brand"] = text
                user_states[user_id] = "admin_select_model"
                await update.message.reply_text("✅ برند انتخاب شد. حالا مدل رو انتخاب کنید:", reply_markup=get_models_keyboard(text))
            else:
                await update.message.reply_text("❗️ برند نادرست.")
            return

        elif state == "admin_select_model":
            brand = context.user_data.get("admin_brand")
            if brand and text in brands[brand]["models"]:
                context.user_data["admin_model"] = text
                user_states[user_id] = "admin_edit_price"
                await update.message.reply_text(f"✏️ قیمت جدید برای {text} را وارد کنید:")
            else:
                await update.message.reply_text("❗️ مدل نادرست.")
            return

        elif state == "admin_edit_price":
            context.user_data["new_price"] = text
            user_states[user_id] = "admin_edit_plan"
            await update.message.reply_text("📝 شرایط جدید فروش را وارد کنید:")
            return

        elif state == "admin_edit_plan":
            brand = context.user_data["admin_brand"]
            model = context.user_data["admin_model"]
            brands[brand]["models"][model]["price"] = context.user_data["new_price"]
            brands[brand]["models"][model]["plan"] = text
            user_states[user_id] = "main_menu"
            await update.message.reply_text(f"✅ اطلاعات «{model}» به‌روزرسانی شد.")
            return

    if state == "main_menu":
        if text in brands:
            user_states[user_id] = f"brand_selected:{text}"
            await update.message.reply_text(f"✅ برند {text} انتخاب شد. مدل رو انتخاب کنید:", reply_markup=get_models_keyboard(text))
        else:
            await update.message.reply_text("❗️ لطفاً یکی از برندهای لیست رو انتخاب کنید.", reply_markup=get_main_keyboard())
        return

    elif state.startswith("brand_selected:"):
        brand = state.split(":")[1]
        if text == "بازگشت به برندها":
            user_states[user_id] = "main_menu"
            await update.message.reply_text("🔙 بازگشت به منوی برندها.", reply_markup=get_main_keyboard())
            return
        if text in brands[brand]["models"]:
            await send_car_info(update, brand, text)
            await update.message.reply_text("🔁 مدل دیگه‌ای رو انتخاب کن یا بازگرد.", reply_markup=get_models_keyboard(brand))
        else:
            await update.message.reply_text("❗️ مدل نامعتبره.", reply_markup=get_models_keyboard(brand))
        return

    await update.message.reply_text("❗️ لطفاً از دکمه‌های موجود استفاده کنید.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin_panel))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

asyncio.get_event_loop().run_until_complete(app.run_polling())
