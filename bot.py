import telebot
from telebot import types,formatting
from telebot.types import InputFile, InlineKeyboardButton,InputMediaPhoto
from Photo import telegram_Photo
from ascii import Ascii
import keyboards
from config import bot_config

class Bot():
    def __init__(self, token):
        print("initializing bot...")
        self.bot = telebot.TeleBot(token)
        self.init_welcome()
        self.init_image()
        self.init_start_render()

        self.default_font_size = bot_config.default_font_size
        self.default_distance = bot_config.default_distance
        self.default_expand_layout = bot_config.default_expand_layout
        self.default_original_colors = bot_config.default_original_colors
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
            chat_id = message.chat.id
            message_id = message.id
            if data == "render" or data =="save":
                if data == "save":
                    self.render_and_save(message)
                else:
                    self.render_and_send(message)
                keyboards.menu_keyboards["choice_menu"].set_reply_keyboard(self.bot,chat_id,message_id)
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
                self.bot.edit_message_caption(chat_id = chat_id, message_id =message_id, caption = caption.generate())
                keyboards.menu_keyboards[parameter].set_reply_keyboard(self.bot,chat_id,message_id)

            elif data.startswith("!"):
                caption = Caption.from_text(message.caption)
                literal = data[0]
                parameter = data[1::]
                if parameter == 'expand_layout':
                    caption.expand_layout = not caption.expand_layout
                if parameter == 'original_colors':
                    caption.original_colors = not caption.original_colors
                self.bot.edit_message_caption(chat_id = message.chat.id,message_id = message.id,caption = caption.generate())
                keyboards.menu_keyboards["choice_menu"].set_reply_keyboard(self.bot,chat_id,message_id)
                
                
            elif not data.startswith("="):
                #self.bot.edit_message_reply_markup(message.chat.id,message.id,reply_markup = keyboards.keyboards[callback.data].keyboard())
                keyboards.menu_keyboards[data].set_reply_keyboard(self.bot,chat_id,message_id)
                return
            

    def render(self,message,caption):
        photo = telegram_Photo.from_message(message,self.bot)
        photo.save_photo(self.bot)
        ascii_art = Ascii.render_art(photo.path,caption)
        result_image = ascii_art.result_image
        return result_image

    def render_decorator(func):
        def wrapper(self,message):
            chat_id = message.chat.id
            message_id = message.id
            caption = Caption.from_text(message.caption)
            result_image = self.render(message.reply_to_message,caption)
            result_image.save()
            print(chat_id)
            func(self.bot,chat_id,message_id,result_image)
            self.bot.edit_message_caption(chat_id = chat_id,message_id =message_id,caption = caption.generate())
        return wrapper

    @render_decorator
    def render_and_save(bot,chat_id,message_id,result_image):
        bot.send_document(chat_id = chat_id,reply_to_message_id =message_id, document =  open(result_image.path, "rb"))
        
    @render_decorator
    def render_and_send(bot,chat_id,message_id,result_image):
        bot.edit_message_media(chat_id = chat_id,message_id =message_id,media = InputMediaPhoto(media = open(result_image.path, "rb")))
        
    def reply_ascii_art_settings(self,message):
        caption=Caption(self.default_distance,self.default_font_size,self.default_expand_layout,self.default_original_colors)
        result_image = self.render(message,caption)
        result_image.save()
        

        self.bot.send_photo(message.chat.id,
                            InputFile(result_image.path),
                            caption=caption.generate(),
                            reply_to_message_id=message.id,
                            reply_markup = keyboards.choice_telegram_keyboard.get_keyboard()) #,
        # keyboards.choice_telegram_keyboard.set_reply_keyboard(self.bot,message.chat.id,message.id)
        
        #self.bot.edit_message_reply_markup(message.chat.id,message.id,reply_markup = keyboards.keyboards["choice_keyboard"].keyboard())
        # self.bot.reply_to(message,text = "123",reply_markup = keyboards.choice_keyboard.keyboard(),photo=)

    def run(self):
        print("running bot...")
        self.bot.infinity_polling()


class Caption():
    def __init__(self,distance,font_size,expand_layout,original_colors=True):
        self.distance = distance
        self.font_size = font_size
        self.expand_layout = expand_layout #todo make this two bool variables to tuple
        self.original_colors = original_colors

    def check_emoji(value):
        if value =="❌":
            return False
        return True
    def from_text(text):
        for i in text.splitlines():
            if i.startswith("Дистанция:"):
                distance = int(i.split(":")[1].strip())
            elif i.startswith("размер шрифта:"):
                font_size = int(i.split(":")[1].strip())
            elif i.startswith("развернуть раскладку:"):
                value = (i.split(":")[1].strip())
                expand_layout = Caption.check_emoji(value)
            elif i.startswith("изначальные цвета:"):
                value = (i.split(":")[1].strip())
                original_colors = Caption.check_emoji(value)


        return Caption(distance,font_size,expand_layout,original_colors)
    def generate(self):
        return f"\
Дистанция: {self.distance}\n\
размер шрифта: {self.font_size}\n\
развернуть раскладку: {'✅' if self.expand_layout else '❌'}\n\
изначальные цвета: {'✅' if self.original_colors else '❌'}"

    