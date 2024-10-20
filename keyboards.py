from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup

# class KeyboardMarkup():
#     def __init__(self):
#         pass

#     def switch_keyboard(self):
#         pass #todo: implement that if it will work

# class Settings_markup(KeyboardMarkup):
#     def __init__(self,callback_data,text):
#         super().__init__()
#         self.callback_data = callback_data
#         self.text  = text
#         self.minus_button = InlineKeyboardButton("-" , callback_data = f"-{self.callback_data}")
#         self.description_button = InlineKeyboardButton(f'{self.text}' , callback_data = f"={self.callback_data}")
#         self.plus_button = InlineKeyboardButton("+" , callback_data = f"+{self.callback_data}")
#         self.back_button = choice_markup.get_redirect_button()
        

#     def keyboard(self):
#         keyboard = InlineKeyboardMarkup()

#         keyboard.row(self.minus_button,self.description_button,self.plus_button).row(self.back_button)
        
#         return keyboard

#     def get_redirect_button(self):
#         return InlineKeyboardButton(self.text, callback_data = self.callback_data)

# class choice_markup(KeyboardMarkup):
#     def __init__(self):
#         # self.font_size_button =
#         # self.distance_settings_button = 

#         self.buttons = [ font_size_settings.get_redirect_button(),
#                         distance_settings.get_redirect_button()]
#         self.expand_layout_button = InlineKeyboardButton("развернуть раскладку", callback_data = "!expand_layout" )

#         self.render_button = InlineKeyboardButton("начать обработку", callback_data = "render" )
#         self.save_button = InlineKeyboardButton("получить без сжатия",callback_data = "save")

#     def keyboard(self):
#         keyboard = InlineKeyboardMarkup()
#         for button in self.buttons:
#             keyboard.add(button)
#         keyboard.add(self.expand_layout_button)
#         keyboard.add(self.render_button)
#         keyboard.add(self.save_button)
#         return keyboard

#     def get_redirect_button():
#         return InlineKeyboardButton("выбрать настройку", callback_data = "choice_keyboard" )

# font_size_settings = Settings_markup("font_size","размер шрифта")
# distance_settings = Settings_markup("distance","дистанция")
# choice_keyboard = choice_markup()

# keyboards = {
#     "distance": distance_settings,
#     "font_size": font_size_settings,
#     "choice_keyboard": choice_keyboard
# }
#----------------------------------------------------------------

class Telegram_button():
    def __init__(self, text, callback_data):
        self.text = text
        self.callback_data = callback_data
    
    def generate_button(self):
        return InlineKeyboardButton(self.text, callback_data = self.callback_data)
    


class Telegram_keyboard():
    def __init__(self):
        self.keyboard = InlineKeyboardMarkup()

    def set_reply_keyboard(self,bot,chat_id,message_id):
        bot.edit_message_reply_markup(chat_id,message_id,reply_markup = self.keyboard)

    # def generate_keyboard(self):
    #     pass
    
    def get_keyboard(self):
        return self.keyboard


    def from_buttons(buttons):
        keyboard = Telegram_keyboard()
        for button in buttons:
            keyboard.keyboard.add(button.generate_button())
        return keyboard

class Adder_telegram_keyboard(Telegram_keyboard):
    def __init__(self):
        super().__init__()
        

    def from_callback_data(callback_data):
        buttons = [
            Telegram_button("-",f"-{callback_data}").generate_button(),
            Telegram_button(callback_data_texts[callback_data],f"={callback_data}").generate_button(),
            Telegram_button("+",f"+{callback_data}").generate_button(),
            Telegram_button("к выбору","choice_menu").generate_button()
        ]
        keyboard = Adder_telegram_keyboard.from_buttons(buttons)
        return keyboard

    def from_buttons(buttons):
        keyboard = Adder_telegram_keyboard()
        keyboard.keyboard.row(buttons[0],buttons[1],buttons[2])
        keyboard.keyboard.row(buttons[3])
        return keyboard

callback_data_texts = {
    "font_size"      : "размер шрифта",
    "distance"       : "дистанция",
    "render"         : "начать обработку",
    "save"           : "получить без сжатия",
    "!expand_layout" : "развернуть раскладку",
    "!original_colors" : "оригинальные цвета",
}

choice_telegram_keyboard_buttons = [
    Telegram_button(callback_data_texts ["font_size"     ] , "font_size")      ,
    Telegram_button(callback_data_texts ["distance"     ]  , "distance")       ,
    Telegram_button(callback_data_texts ["!expand_layout"] , "!expand_layout") ,
    Telegram_button(callback_data_texts ["!original_colors"] , "!original_colors") ,
    Telegram_button(callback_data_texts ["render"        ] , "render")         ,
    Telegram_button(callback_data_texts ["save"          ] , "save")           ,
]
choice_telegram_keyboard = Telegram_keyboard.from_buttons(choice_telegram_keyboard_buttons)
menu_keyboards = {
    "font_size":Adder_telegram_keyboard.from_callback_data("font_size"),
    "distance":Adder_telegram_keyboard.from_callback_data("distance"),
    "choice_menu":choice_telegram_keyboard,
}
    




font_size_keyboard = Adder_telegram_keyboard.from_callback_data("font_size")

# class Choice_telegram_keyboard(telegram_keyboard):
#     def __init__(self):
#         super().__init__()
#         self.render_button = InlineKeyboardButton("начать обработку", callback_data = "render" )
#         self.save_button = InlineKeyboardButton("получить без сжатия",callback_data = "save")
#         self.expand_layout_button = InlineKeyboardButton("развернуть раскладку", callback_data = "!expand_layout" )