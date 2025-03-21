# import asyncio
# import nest_asyncio
# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# import pandas as pd
# import openpyxl
#
# nest_asyncio.apply()
#
#
# # حداکثر ظرفیت
# max_male = 200
# max_female = 200
#
# # لیست ثبت‌نام شدگان
# registered_males = []
# registered_females = []
# current_user_state = {}
#
# # تابع شروع ربات
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await update.message.reply_text('سلام! برای ثبت نام جشن لطفا از دستور /register استفاده کنید.')
#
#
# # تابع ثبت نام
# async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     user_id = update.message.from_user.id
#     if len(registered_males) < max_male or len(registered_females) < max_female:
#         current_user_state[user_id] = {"stage": "gender", "id": user_id} # اضافه شدن id به user_data
#         await update.message.reply_text('لطفا جنسیت خود را مشخص کنید (مرد یا زن).')
#     else:
#         await update.message.reply_text('متاسفانه ظرفیت ثبت نام پر شده است.')
#
#
# # تابع دریافت جنسیت و اطلاعات دیگر
# async def handle_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     user_id = update.message.from_user.id
#     user_data = current_user_state.get(user_id)
#     if not user_data:
#         return
#
#     text = update.message.text.lower()

    # if user_data["stage"] == "gender":
    #     if text == 'مرد':
    #         if len(registered_males) < max_male:
    #             user_data["gender"] = "مرد"  # ذخیره جنسیت در user_data
    #             current_user_state[user_id]["stage"] = "student_id"
    #             await update.message.reply_text('لطفا کد دانشجویی خود را وارد کنید.')
    #         else:
    #             await update.message.reply_text('متاسفانه ظرفیت آقایان پر شده است.')
    #             del current_user_state[user_id]
    #     elif text == 'زن':
    #         if len(registered_females) < max_female:
    #             user_data["gender"] = "زن"  # ذخیره جنسیت در user_data
    #             current_user_state[user_id]["stage"] = "student_id"
    #             await update.message.reply_text('لطفا کد دانشجویی خود را وارد کنید.')
    #         else:
    #             await update.message.reply_text('متاسفانه ظرفیت خانم‌ها پر شده است.')
    #             del current_user_state[user_id]
    #     else:
    #         await update.message.reply_text('لطفا فقط "مرد" یا "زن" را وارد کنید.')
    # elif user_data["stage"] == "student_id":
    #     user_data["student_id"] = text
    #     current_user_state[user_id]["stage"] = "full_name"
    #     await update.message.reply_text('لطفا نام و نام خانوادگی خود را وارد کنید.')
    # elif user_data["stage"] == "full_name":
    #     user_data["full_name"] = text
    #     current_user_state[user_id]["stage"] = "major"
    #     await update.message.reply_text('لطفا رشته تحصیلی خود را وارد کنید.')
    # elif user_data["stage"] == "major":
    #     user_data["major"] = text
    #
    #     #  اضافه کردن اطلاعات کامل به لیست مربوطه
    #     if user_data["gender"] == "مرد":
    #         registered_males.append(user_data)
    #     else:
    #         registered_females.append(user_data)
    #
    #     del current_user_state[user_id]
    #     save_to_excel()
    #     await update.message.reply_text('ثبت نام شما با موفقیت انجام شد و اطلاعات شما ذخیره شد.')
#
#
# تابع ذخیره اطلاعات در فایل اکسل
# def save_to_excel():
#     try:
#         males_df = pd.DataFrame(registered_males)
#         females_df = pd.DataFrame(registered_females)
#
#
#         # اضافه کردن ستون جنسیت
#         # males_df['جنسیت'] = 'مرد'
#         # females_df['جنسیت'] = 'زن'
#
#         all_participants = pd.concat([males_df, females_df ], ignore_index=True)
#         all_participants.to_excel("registered_participants.xlsx", index=False)
#         print(f"Excel file saved to: registered_participants.xlsx")
#     except Exception as e:
#         print(f"Error saving to Excel: {e}")
#
#
# # تابع اصلی برای راه‌اندازی ربات
# async def main() -> None:
#     application = ApplicationBuilder().token("8094992532:AAEVoVu8cgZ6Flsj3VB2pJbXaf_e6wovkGQ").build() # توکن خود را اینجا وارد کنید
#
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CommandHandler("register", register))
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_input))
#
#     await application.run_polling()
#
#
# if __name__ == '__main__':
#     asyncio.run(main())


# =================================================


import logging
import asyncio
import nest_asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import pandas as pd

# پیکربندی لاگینگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# حداکثر ظرفیت
max_male = 200
max_female = 200

# لیست ثبت‌نام شدگان
registered_males = []
registered_females = []
current_user_state = {}


# تابع ذخیره اطلاعات در فایل اکسل
def save_to_excel():
    try:
        males_df = pd.DataFrame(registered_males)
        females_df = pd.DataFrame(registered_females)
        all_participants = pd.concat([males_df, females_df], ignore_index=True)
        all_participants.to_excel("registered_participants.xlsx", index=False)
        logger.info("Excel file saved to: registered_participants.xlsx")
    except Exception as e:
        logger.error(f"Error saving to Excel: {e}")


# تابع ایجاد اپلیکیشن
def create_application() -> ApplicationBuilder:
    return ApplicationBuilder().token("8094992532:AAEVoVu8cgZ6Flsj3VB2pJbXaf_e6wovkGQ").build()  # توکن خود را در اینجا قرار دهید


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("جشن بگیریم! 🎉", callback_data='celebrate')]]
    await update.message.reply_text('سلام! برای شرکت در جشن ، لطفا دکمه زیر را بزنید.',
                                    reply_markup=InlineKeyboardMarkup(keyboard))


async def register(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(registered_males) < max_male or len(registered_females) < max_female:
        current_user_state[user_id] = {"stage": "gender", "id": user_id}
        await context.bot.send_message(user_id, 'لطفا جنسیت خود را مشخص کنید (مرد یا زن).')
    else:
        await context.bot.send_message(user_id, 'متاسفانه ظرفیت ثبت نام پر شده است.')


async def handle_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    user_data = current_user_state.get(user_id)
    if not user_data:
        return

    text = update.message.text.lower()

    if user_data["stage"] == "gender":
        if text == 'مرد':
            if len(registered_males) < max_male:
                user_data["gender"] = "مرد"  # ذخیره جنسیت در user_data
                current_user_state[user_id]["stage"] = "student_id"
                await update.message.reply_text('لطفا کد دانشجویی خود را وارد کنید.')
            else:
                await update.message.reply_text('متاسفانه ظرفیت آقایان پر شده است.')
                del current_user_state[user_id]
        elif text == 'زن':
            if len(registered_females) < max_female:
                user_data["gender"] = "زن"  # ذخیره جنسیت در user_data
                current_user_state[user_id]["stage"] = "student_id"
                await update.message.reply_text('لطفا کد دانشجویی خود را وارد کنید.')
            else:
                await update.message.reply_text('متاسفانه ظرفیت خانم‌ها پر شده است.')
                del current_user_state[user_id]
        else:
            await update.message.reply_text('لطفا فقط "مرد" یا "زن" را وارد کنید.')
    elif user_data["stage"] == "student_id":
        user_data["student_id"] = text
        current_user_state[user_id]["stage"] = "full_name"
        await update.message.reply_text('لطفا نام و نام خانوادگی خود را وارد کنید.')
    elif user_data["stage"] == "full_name":
        user_data["full_name"] = text
        current_user_state[user_id]["stage"] = "major"
        await update.message.reply_text('لطفا رشته تحصیلی خود را وارد کنید.')
    elif user_data["stage"] == "major":
        user_data["major"] = text

        #  اضافه کردن اطلاعات کامل به لیست مربوطه
        if user_data["gender"] == "مرد":
            registered_males.append(user_data)
        else:
            registered_females.append(user_data)

        del current_user_state[user_id]
        save_to_excel()
        await update.message.reply_text('ثبت نام شما با موفقیت انجام شد و اطلاعات شما ذخیره شد.')


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'celebrate':
        await query.edit_message_text(text="اکنون برای ثبت نام در ((جشن)) مراحل را ادامه دهید.")

        user_id = query.from_user.id
        await register(user_id, context)  # شروع ثبت نام بعد از فشردن دکمه


async def main() -> None:
    global registered_males, registered_females, current_user_state
    registered_males = []
    registered_females = []
    current_user_state = {}

    application = create_application()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_input))
    application.add_handler(CallbackQueryHandler(button))

    await application.run_polling()


if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.run(main())

# 8094992532:AAEVoVu8cgZ6Flsj3VB2pJbXaf_e6wovkGQ