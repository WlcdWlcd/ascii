from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup

class KeyboardMarkup():
    def __init__(self):
        pass

    def switch_keyboard(self):
        pass #todo: implement that if it will work

class Settings_markup(KeyboardMarkup):
    def __init__(self,callback_data,text):
        super().__init__()
        self.callback_data = callback_data
        self.text  = text
        self.minus_button = InlineKeyboardButton("-" , callback_data = f"-{self.callback_data}")
        self.description_button = InlineKeyboardButton(f'{self.text}' , callback_data = f"={self.callback_data}")
        self.plus_button = InlineKeyboardButton("+" , callback_data = f"+{self.callback_data}")
        self.back_button = choice_markup.get_redirect_button()
        

    def keyboard(self):
        keyboard = InlineKeyboardMarkup()

        keyboard.row(self.minus_button,self.description_button,self.plus_button).row(self.back_button)
        
        return keyboard

    def get_redirect_button(self):
        return InlineKeyboardButton(self.text, callback_data = self.callback_data)

class choice_markup(KeyboardMarkup):
    def __init__(self):
        # self.font_size_button =
        # self.distance_settings_button = 

        self.buttons = [ font_size_settings.get_redirect_button(),
                        distance_settings.get_redirect_button()]
        self.expand_layout_button = InlineKeyboardButton("развернуть раскладку", callback_data = "!expand_layout" )

        self.render_button = InlineKeyboardButton("начать обработку", callback_data = "render" )
        self.save_button = InlineKeyboardButton("получить без сжатия",callback_data = "save")

    def keyboard(self):
        keyboard = InlineKeyboardMarkup()
        for button in self.buttons:
            keyboard.add(button)
        keyboard.add(self.expand_layout_button)
        keyboard.add(self.render_button)
        keyboard.add(self.save_button)
        return keyboard

    def get_redirect_button():
        return InlineKeyboardButton("выбрать настройку", callback_data = "choice_keyboard" )

font_size_settings = Settings_markup("font_size","размер шрифта")
distance_settings = Settings_markup("distance","дистанция")
choice_keyboard = choice_markup()

keyboards = {
    "distance": distance_settings,
    "font_size": font_size_settings,
    "choice_keyboard": choice_keyboard
}
