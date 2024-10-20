import telebot
from telebot import types,formatting
from telebot.types import InputFile, InlineKeyboardButton,InputMediaPhoto
from Photo import telegram_Photo
from ascii import Ascii
import keyboards

class Bot():
    def __init__(self, token):
        print("initializing bot...")
        self.bot = telebot.TeleBot(token)
        self.init_welcome()
        self.init_image()
        self.init_start_render()

        self.default_font_size = 14
        self.default_distance = 14
        self.default_expand_layout = False
        print("bot initialized successfully")


    def init_welcome(self):
        @self.bot.message_handler(commands = ['help','start'])
        def send_welcome(message):
            self.bot.reply_to(message,"отправь картинку")

    def init_image(self):
        @self.bot.message_handler(content_types = ['photo'])
        def handle_image(message):
            # chat_id = message.chat.id
            self.reply_ascii_art_settings(message)
            # self.bot.reply_to(message,"картинка получена")
            # self.bot.send_message(chat_id, "скачиваю изображение")
            # self.bot.send_message(chat_id, "скачал фотографию")
            # self.bot.send_message(chat_id, "обрабатываю фотографию")


    def init_start_render(self):
        @self.bot.callback_query_handler()
        def handle_callback(callback):
            message = callback.message
            data = callback.data
            if data == "render":
                self.render_and_send(message)
                return 
            if data == "save":
                self.render_and_save(message)
                return
            
            elif data.startswith("+") or data.startswith("-"):
                caption = Caption.from_text(message.caption)
                literal = data[0]
                parameter = data[1::]
                if literal == "+":
                    change = 1
                else:
                    change = -1
                if parameter == 'distance':
                    caption.distance+=change
                elif parameter == 'font_size':
                    caption.font_size+=change
                self.bot.edit_message_caption(chat_id = message.chat.id,message_id =message.id,caption = caption.generate())
                self.bot.edit_message_reply_markup(message.chat.id,message.id,reply_markup = keyboards.keyboards[parameter].keyboard())
            elif data.startswith("!"):
                caption = Caption.from_text(message.caption)
                literal = data[0]
                parameter = data[1::]
                print(parameter)
                print(caption.expand_layout)
                if parameter == 'expand_layout':
                    caption.expand_layout = not caption.expand_layout
                print(caption.expand_layout)

                self.bot.edit_message_caption(chat_id = message.chat.id,message_id = message.id,caption = caption.generate())
                self.bot.edit_message_reply_markup(message.chat.id,message.id,reply_markup = keyboards.keyboards["choice_keyboard"].keyboard())
                
                
            elif not data.startswith("="):
                self.bot.edit_message_reply_markup(message.chat.id,message.id,reply_markup = keyboards.keyboards[callback.data].keyboard())
                return
            

    def render(self,message,caption):
        photo = telegram_Photo.from_message(message,self.bot)
        photo.save_photo(self.bot)
        
        ascii_art = Ascii.render_art(photo.path,caption)
        result_image = ascii_art.result_image

        return result_image


    def render_and_save(self,message):
        chat_id = message.chat.id
        caption = Caption.from_text(message.caption)
        result_image = self.render(message.reply_to_message,caption)
        result_image.save()
        self.bot.send_document(chat_id = chat_id,reply_to_message_id =message.id, document =  open(result_image.path, "rb"))
        self.bot.edit_message_caption(chat_id = message.chat.id,message_id =message.id,caption = caption.generate())
        self.bot.edit_message_reply_markup(message.chat.id,message.id,reply_markup = keyboards.keyboards["choice_keyboard"].keyboard())

    def render_and_send(self,message):
        chat_id = message.chat.id
        caption = Caption.from_text(message.caption)
        result_image = self.render(message.reply_to_message,caption)
        result_image.save()
        self.bot.edit_message_media(chat_id = chat_id,message_id =message.id,media = InputMediaPhoto(media = open(result_image.path, "rb")))
        self.bot.edit_message_caption(chat_id = message.chat.id,message_id =message.id,caption = caption.generate())
        self.bot.edit_message_reply_markup(message.chat.id,message.id,reply_markup = keyboards.keyboards["choice_keyboard"].keyboard())
        

    def reply_ascii_art_settings(self,message):
        caption=Caption(self.default_distance,self.default_font_size,self.default_expand_layout)
        result_image = self.render(message,caption)
        result_image.save()
        

        self.bot.send_photo(message.chat.id,InputFile(result_image.path),caption=caption.generate(),reply_to_message_id=message.id,reply_markup = keyboards.choice_keyboard.keyboard())
        self.bot.edit_message_reply_markup(message.chat.id,message.id,reply_markup = keyboards.keyboards["choice_keyboard"].keyboard())
        # self.bot.reply_to(message,text = "123",reply_markup = keyboards.choice_keyboard.keyboard(),photo=)

    def run(self):
        print("running bot...")
        self.bot.infinity_polling()


class Caption():
    def __init__(self,distance,font_size,expand_layout):
        self.distance = distance
        self.font_size = font_size
        self.expand_layout = expand_layout

    def from_text(text):
        for i in text.splitlines():
            if i.startswith("Дистанция:"):
                distance = int(i.split(":")[1].strip())
            elif i.startswith("размер шрифта:"):
                font_size = int(i.split(":")[1].strip())
            elif i.startswith("развернуть раскладку:"):
                value = (i.split(":")[1].strip())
                print(value)
                if value =="❌":
                    expand_layout = False
                else:
                    expand_layout = True

        return Caption(distance,font_size,expand_layout)
    def generate(self):
        return f"\
Дистанция: {self.distance}\n\
размер шрифта: {self.font_size}\n\
развернуть раскладку: {'✅' if self.expand_layout else '❌'}"

    