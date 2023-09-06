import telebot
from telebot import types
import os
import replicate
import requests

API_TOKEN = '6156740897:AAEHYXnJtS5O8yMduvTe8LG3M6ePh7ptnsA'
os.environ["REPLICATE_API_TOKEN"] = "r8_8XpHTOEsZzRpRWXS6GUBcCwuBpnaqHz4Ln80K"

bot = telebot.TeleBot(API_TOKEN)

scalestan = {}
lang = {}
mainText = None
# Главное меню
@bot.message_handler(commands=["start"])
def main_menu(message):
    chat_id = message.chat.id
    langNow = lang.get(chat_id)
    if langNow == None:
        mainText = """\
Welcome to the Upscale bot powered by real-esrgan! 🚀

I'll enhance your photos using advanced upscaling technology. Just send me a photo, and I'll make it look even better! ✨📸

Share your photo (JPG or PNG) with me, and let's unlock its full potential together! Enjoy the upscale experience! ✨💯

For upscale menu, settings, or about, use the buttons below. Have a great time! 🎉👇\
"""
        keyboard = types.InlineKeyboardMarkup()
        key_start = types.InlineKeyboardButton(text='📸✨ Upscale photos', callback_data='start')
        key_set = types.InlineKeyboardButton(text='⚙ Settings', callback_data='set')
        key_about = types.InlineKeyboardButton(text='ℹ About', callback_data='about')
    elif langNow == "ru":
        mainText = """\
Добро пожаловать в бот Upscale, работающий на основе технологии real-esrgan! 🚀

Я улучшу ваши фотографии с помощью передовой технологии масштабирования. Просто отправьте мне фото, и я сделаю его еще лучше! ✨📸

Поделитесь своей фотографией (в формате JPG или PNG), и давайте вместе раскроем ее полный потенциал! Наслаждайтесь улучшением качества! ✨💯

Для доступа к меню масштабирования, настроек или информации о боте используйте кнопки ниже. Приятного времяпрепровождения! 🎉👇\
"""
        keyboard = types.InlineKeyboardMarkup()
        key_start = types.InlineKeyboardButton(text='📸✨ Масштабировать фотографии', callback_data='start')
        key_set = types.InlineKeyboardButton(text='⚙ Настройки', callback_data='set')
        key_about = types.InlineKeyboardButton(text='ℹ О Боте', callback_data='about')
    keyboard.add(key_start)
    keyboard.add(key_set, key_about)
    bot.send_message(message.chat.id, text=mainText, reply_markup=keyboard)

@bot.message_handler(commands=["lang"])
def language(message):
    chat_id = message.chat.id
    langNow = lang.get(chat_id)
    if langNow == None:
        keyboard = types.InlineKeyboardMarkup()
        key_en = types.InlineKeyboardButton(text='English', callback_data='en')
        key_ru = types.InlineKeyboardButton(text='Russian', callback_data='ru')
        keyboard.add(key_en, key_ru)
        text="""\
Hey, it's a menu where you can change the bot's language!
        
Choose a language ⬇
        """
    elif langNow == "ru":
        keyboard = types.InlineKeyboardMarkup()
        key_ru = types.InlineKeyboardButton(text='Русский', callback_data='ru')
        key_en = types.InlineKeyboardButton(text='Английский', callback_data='en')
        keyboard.add(key_ru, key_en)
        text="""\
Хей, это меню, где можно поменять язык бота!
        
Выбери язык ⬇
        """
    bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

# Обработчик нажатия кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    chat_id = call.message.chat.id
    if call.data == "start":
        langNow = lang.get(chat_id)
        keyboard = types.InlineKeyboardMarkup()
        if langNow == None:
            back_button = types.InlineKeyboardButton(text='🔙 Back to Main Menu', callback_data='back')
            keyboard.row(back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""\
📸✨ Upscale photos

Send me a photo or file (in JPG or PNG format), and I will enhance it using real-esrgan. After processing, you will receive the improved version. Click the "🔙 Back to Main Menu" button to return.

Get ready for amazing results! ✨📷
""", reply_markup=keyboard)
        elif langNow == "ru":
            back_button = types.InlineKeyboardButton(text='🔙 Вернуться в Главное Меню', callback_data='back')
            keyboard.row(back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""\
📸✨ Масштабировать фотографии

Отправьте мне фотографию или файл (в форматах JPG или PNG), и я улучшу его с помощью real-esrgan. После обработки вы получите улучшенную версию. Нажмите кнопку "🔙 Вернуться в Главное Меню", чтобы вернуться обратно.

Ожидайте удивительные результаты! ✨📷
\
""", reply_markup=keyboard)
        variable_value = scalestan.get(chat_id)
        if variable_value is None:
            keyboard = types.InlineKeyboardMarkup()
            if langNow == None:
                upscale_message = "Please enter an upscale scale factor between 1 and 10 by sending a numerical value."
                back_button = types.InlineKeyboardButton(text='🔙 Back to Main Menu', callback_data='back')
                keyboard.row(back_button)
            elif langNow == "ru":
                upscale_message = "Пожалуйста введите силу масштабирования числом в радиусе от 1 до 10."
                back_button = types.InlineKeyboardButton(text='🔙 Вернуться в Главное Меню', callback_data='back')
                keyboard.row(back_button)
            bot.send_message(call.message.chat.id, upscale_message, reply_markup=keyboard)
    elif call.data == "set":
        langNow = lang.get(chat_id)
        variable_value = scalestan.get(chat_id)
        keyboard = types.InlineKeyboardMarkup()
        if langNow == None:
            back_button = types.InlineKeyboardButton(text='🔙 Back to Main Menu', callback_data='back')
            keyboard.row(back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""\
⚙️ Settings Menu

Customize the default upscaling strength for your images. Enter a value between 1 and 10 to set the default upscale strength.

Note: Higher values create a more pronounced upscaling effect, but very high values may lead to unrealistic images. Find the right balance.

To set the default upscale strength, enter a number in the chat. For example, for a 5x strength, type "5" and press enter.

Remember, you can adjust the strength for individual images. This default setting applies when no specific strength is specified.

To return to the main menu, click the "🔙 Back to Main Menu" button. Enjoy customizing your upscale experience! 🚀📸

Current default upscale strength: {variable_value} times

To change the bot's language, use the /lang command.
\
""", reply_markup=keyboard)
        elif langNow == "ru":
            back_button = types.InlineKeyboardButton(text='🔙 Вернуться в Главное Меню', callback_data='back')
            keyboard.row(back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""\
⚙️ Меню настроек

Настройте стандартную силу увеличения для ваших изображений. Введите значение от 1 до 10, чтобы установить стандартную силу увеличения.

Обратите внимание: Чем выше значение, тем сильнее будет эффект увеличения. Однако очень высокие значения могут привести к нереалистичным изображениям. Найдите правильный баланс.

Чтобы установить стандартную силу увеличения, введите число в чат. Например, для силы увеличения в 5 раз введите "5" и нажмите Ввод(Enter).

Помните, что вы можете настроить силу увеличения для отдельных изображений. Эта стандартная настройка будет использоваться, когда не указана конкретная сила увеличения.

Чтобы вернуться в главное меню, нажмите кнопку "🔙 Назад в главное меню". Наслаждайтесь настройкой вашего опыта увеличения! 🚀📸

Текущая стандартная сила увеличения: {variable_value} раз

Чтобы изменить язык бота, используйте команду /lang.
\
""", reply_markup=keyboard)
    elif call.data == "about":
        langNow = lang.get(chat_id)
        keyboard = types.InlineKeyboardMarkup()
        if langNow == None:
            back_button = types.InlineKeyboardButton(text='🔙 Back to Main Menu', callback_data='back')
            keyboard.row(back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""\
ℹ️ About Menu

This Upscale bot was created by a team of talented individuals:

👨‍💻 Developer - IarChep. He made a significant contribution to the development and enhancement of this bot.

🤖 ChatGPT - A powerful neural network that assisted in the development of the bot.

🌟 WunderWungiel - A cool person😎.

If you ever want to go back to the main menu, simply click the "🔙 Back to Main Menu" button. Stay tuned for updates and improvements in the future! 🚀🖼️
\
""", reply_markup=keyboard)
        elif langNow == "ru":
            back_button = types.InlineKeyboardButton(text='🔙 Вернуться в Главное Меню', callback_data='back')
            keyboard.row(back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""\
ℹ️ О нашем боте

Этот бот Upscale был создан несколькими талантливыми людьми:

👨‍💻 Разработчик - IarChep. Он разработал этого бота.

🤖 ChatGPT - Мощная нейросеть, которая помогла в разработке бота.

🌟 WunderWungiel - Замечательный человек.

Если вы хотите вернуться в главное меню, просто нажмите кнопку "🔙 Назад в главное меню". Следите за обновлениями и улучшениями в будущем! 🚀🖼️
\
""", reply_markup=keyboard)
    elif call.data == "back":
        langNow = lang.get(chat_id)
        if langNow == None:
            mainText = """\
Welcome to the Upscale bot powered by real-esrgan! 🚀

I'll enhance your photos using advanced upscaling technology. Just send me a photo, and I'll make it look even better! ✨📸

Share your photo (JPG or PNG) with me, and let's unlock its full potential together! Enjoy the upscale experience! ✨💯

For upscale menu, settings, or about, use the buttons below. Have a great time! 🎉👇\
"""
            keyboard = types.InlineKeyboardMarkup()
            key_start = types.InlineKeyboardButton(text='📸✨ Upscale photos', callback_data='start')
            key_set = types.InlineKeyboardButton(text='⚙ Settings', callback_data='set')
            key_about = types.InlineKeyboardButton(text='ℹ About', callback_data='about')
        elif langNow == "ru":
            mainText = """\
Добро пожаловать в бот Upscale, работающий на основе технологии real-esrgan! 🚀

Я улучшу ваши фотографии с помощью передовой технологии масштабирования. Просто отправьте мне фото, и я сделаю его еще лучше! ✨📸

Поделитесь своей фотографией (в формате JPG или PNG), и давайте вместе раскроем ее полный потенциал! Наслаждайтесь улучшением качества! ✨💯

Для доступа к меню масштабирования, настроек или информации о боте используйте кнопки ниже. Приятного времяпрепровождения! 🎉👇\
"""
            keyboard = types.InlineKeyboardMarkup()
            key_start = types.InlineKeyboardButton(text='📸✨ Масштабировать фотографии', callback_data='start')
            key_set = types.InlineKeyboardButton(text='⚙ Настройки', callback_data='set')
            key_about = types.InlineKeyboardButton(text='ℹ О Боте', callback_data='about')
        keyboard.add(key_start)
        keyboard.add(key_set, key_about)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mainText, reply_markup=keyboard)
    elif call.data == "back2":
        langNow = lang.get(chat_id)
        if langNow == None:
            mainText = """\
Welcome to the Upscale bot powered by real-esrgan! 🚀

I'll enhance your photos using advanced upscaling technology. Just send me a photo, and I'll make it look even better! ✨📸

Share your photo (JPG or PNG) with me, and let's unlock its full potential together! Enjoy the upscale experience! ✨💯

For upscale menu, settings, or about, use the buttons below. Have a great time! 🎉👇\
"""
            keyboard = types.InlineKeyboardMarkup()
            key_start = types.InlineKeyboardButton(text='📸✨ Upscale photos', callback_data='start')
            key_set = types.InlineKeyboardButton(text='⚙ Settings', callback_data='set')
            key_about = types.InlineKeyboardButton(text='ℹ About', callback_data='about')
        elif langNow == "ru":
            mainText = """\
Добро пожаловать в бот Upscale, работающий на основе технологии real-esrgan! 🚀

Я улучшу ваши фотографии с помощью передовой технологии масштабирования. Просто отправьте мне фото, и я сделаю его еще лучше! ✨📸

Поделитесь своей фотографией (в формате JPG или PNG), и давайте вместе раскроем ее полный потенциал! Наслаждайтесь улучшением качества! ✨💯

Для доступа к меню масштабирования, настроек или информации о боте используйте кнопки ниже. Приятного времяпрепровождения! 🎉👇\
"""
            keyboard = types.InlineKeyboardMarkup()
            key_start = types.InlineKeyboardButton(text='📸✨ Масштабировать фотографии', callback_data='start')
            key_set = types.InlineKeyboardButton(text='⚙ Настройки', callback_data='set')
            key_about = types.InlineKeyboardButton(text='ℹ О Боте', callback_data='about')
        keyboard.add(key_start)
        keyboard.add(key_set, key_about)
        bot.send_message(chat_id=call.message.chat.id, text=mainText, reply_markup=keyboard)
    elif call.data == "en":
        lang[chat_id] = None
        keyboard = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(text='🔙 Back to Main Menu', callback_data='back')
        keyboard.row(back_button)
        bot.send_message(chat_id=call.message.chat.id, text="Language was sucsessfully updated!", reply_markup=keyboard)
    elif call.data == "ru":
        lang[chat_id]= "ru"
        keyboard = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(text='🔙 Вернуться в Главное Меню', callback_data='back')
        keyboard.row(back_button)
        bot.send_message(chat_id=call.message.chat.id, text="Язык был успешно обновлен!", reply_markup=keyboard)


# Обработчик входящих сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    if message.text.isdigit() and 1 <= int(message.text) <= 10:
        langNow = lang.get(chat_id)
        variable_value = int(message.text)
        scalestan[chat_id] = variable_value
        if langNow == None:
            keyboard = types.InlineKeyboardMarkup()
            back_button = types.InlineKeyboardButton(text='🔙 Back to Main Menu', callback_data='back')
            keyboard.row(back_button)
            bot.send_message(message.chat.id, "Default upscale scale factor has been set and saved. Now, go to Start and send your image. If you're alredy in Start, just send the image!", reply_markup=keyboard)
        elif langNow == "ru":
            keyboard = types.InlineKeyboardMarkup()
            back_button = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='back')
            keyboard.row(back_button)
            bot.send_message(message.chat.id, 'Сила масштабирования изображения была установлена и сохранена по умолчанию. Теперь, иди в меню "📸✨ Масштабировать фотографии" и отправляй свое фото. Если уже находишся в "📸✨ Масштабировать фотографии, то просто отправь нужное фото!', reply_markup=keyboard)
    else:
        langNow = lang.get(chat_id)
        if langNow == None:
            bot.send_message(message.chat.id, "Please enter a numerical value between 1 and 10.")
        elif langNow == "ru":
            bot.send_message(message.chat.id, "Пожалуйста, введи цифрами значение между 1 и 10.")

@bot.message_handler(content_types=['photo', 'document'])
def upscale_image(message):
    chat_id = message.chat.id
    langNow = lang.get(chat_id)
    variable_value = scalestan.get(chat_id)
    if variable_value == None:
        langNow = lang.get(chat_id)
        if langNow == None:
            upscale_message = "Please choose an upscale scale factor between 1 and 10 by sending a numerical value."
            keyboard = types.InlineKeyboardMarkup()
            back_button = types.InlineKeyboardButton(text='🔙 Back to Main Menu', callback_data='back')
        elif langNow == "ru":
            upscale_message = "Пожалуйста, укажи силу масштабирования изображения, выслав цифровое значение от 1 до 10."
            keyboard = types.InlineKeyboardMarkup()
            back_button = types.InlineKeyboardButton(text='🔙 Вернуться в Главное Меню', callback_data='back')
        keyboard.row(back_button)
        bot.send_message(message.chat.id, upscale_message, reply_markup=keyboard)
    else:
        langNow = lang.get(chat_id)
        keyboard = types.InlineKeyboardMarkup()
        if langNow == None:
            back_button = types.InlineKeyboardButton(text='🔙 Back to Main Menu', callback_data='back2')
            keyboard.row(back_button)
            wait_message = bot.send_message(message.chat.id, f"Please wait until real-esrgan upscales your photo by {variable_value} times...")
        elif langNow == "ru":
            back_button = types.InlineKeyboardButton(text='🔙 Вернуться в Главное Меню', callback_data='back2')
            keyboard.row(back_button)
            wait_message = bot.send_message(message.chat.id, f"Пожалуйста, подожди, пока real-esrgan будет масштабировать твое фото в {variable_value} раз...")
        bot.send_chat_action(message.chat.id, 'upload_photo')
        file_id = None
        if message.photo:
            # Если отправлено фото
            file_id = message.photo[-1].file_id
        elif message.document:
            # Если отправлен файл
            if message.document.mime_type == 'image/jpeg' or message.document.mime_type == 'image/png':
                file_id = message.document.file_id
            else:
                if langNow == None:
                    bot.reply_to(message, "⚠️ Please send a photo in JPG or PNG format.")
                elif langNow == "ru":
                    bot.reply_to(message, "⚠️ Пожалуйста, отправь фото в JPG или PNG форматах.")
                return
            

        # Формируем ссылку на фото
        file_link = f"https://api.telegram.org/file/bot{bot.token}/{bot.get_file(file_id).file_path}"

        response = requests.get(file_link)

            # получение расширения файла из ссылки
        extension = file_link.split(".")[-1]

    # сохранение файла в текущей директории
        with open(f"temp.{extension}", "wb") as f:
            f.write(response.content)
        
        name = f"\\temp.{extension}"
        dir=str(os.getcwd()) +name
        
        upscale(dir, message)
        
        # Отправляем ссылку на фото обратно пользователю
        if langNow == None:
            bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id, text=f"Here is your upscaled by {variable_value} times photo: {output}", reply_markup=keyboard)
        elif langNow == "ru":
            bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message.message_id, text=f"Твое улучшенное в {variable_value} раз фото: {output}", reply_markup=keyboard)
        os.unlink(dir)
def upscale(link, message):
        chat_id = message.chat.id
    
    # Получаем значение переменной из словаря
        variable_value = scalestan.get(chat_id)
        global output
    #обработка изображения real-esrgan'ом
        model_name = "xinntao/realesrgan:1b976a4d456ed9e4d1a846597b7614e79eadad3032e9124fa63859db0fd59b56"
        input_data = {
            "img": open(link, "rb"),
            "scale": variable_value
        }

        output = replicate.run(model_name, input=input_data)
        return output


        
bot.polling(none_stop=True)