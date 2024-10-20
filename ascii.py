from Photo import Photo
import numpy as np
from PIL import Image,ImageDraw,ImageFont


class Ascii_art(Photo):
    def __init__():
        pass

class color_scheme:
    def __init__(self):
        self.char_color = [255,255,255]
        self.background_color = [0,0,0]
    def set_char_color(self, color):
        self.char_color = color
    def set_background_color(self, color):
        self.background_color = color

class Ascii(color_scheme):
    def __init__(self,path,parameters):
        self.path = path
        self.chars = ' .",:;!~+-xmo*#W&8@'
        if parameters.expand_layout:
            self.chars = self.chars[::-1]
        self.char_coefficent = len(self.chars)/255
        color_scheme.__init__(self)
        self.source_image = Pillow_image.from_path(self.path)
        self.source_npArray = self.source_image.get_npArray()
        self.distance = parameters.distance
        self.font_size = parameters.font_size

        self.height = len(self.source_npArray)
        self.width = len(self.source_npArray[0])
        self.sizes = (self.width,self.height)
        self.result_image = Pillow_image.new(self.source_image.sizes[0]*3,self.source_image.sizes[1]*3)
        self.draw = ImageDraw.Draw(self.result_image.image)
        self.fnt = ImageFont.truetype("./fonts/consolas.ttf",self.font_size)
        
#todo: parameters is caption redooo pls
    def render_art(path,parameters):
        self = Ascii(path,parameters)

        self.draw_chars()

        return self
    
    def draw_chars(self):
        for row in range(0,self.height,self.distance//3):
            for col in range(0,self.width,self.distance//3):
                self.draw_char(col,row)

    def draw_char(self,x,y):
        try:
            coordinates = (x*3,y*3)
            pixel = tuple(self.source_npArray[y][x])

            while len(pixel)<3:
                pixel = tuple(pixel + (0,))

            char_index = int(self.char_coefficent*pixel[0])-1
            char = self.chars[char_index]


            if True: #TODO: add bool value and else here
                fill_color = pixel
                fill_color = (255,255,255)
            self.draw.text(coordinates,
                            char,
                            fill=fill_color,
                            font = self.fnt)
        except Exception:
            pass   

class Pillow_image(Photo):
    def __init__(self, path):
        self.path = f'{path}'
    
    def from_path(path):
        img = Pillow_image(path)
        img.image = Image.open(path).convert('RGB')
        img.update_sizes()
        return img

    def new(width, height):
        img = Pillow_image("dsadsa.jpg")
        img.image = Image.new('RGB', (width, height))
        img.update_sizes()
        return img

    def update_sizes(self):
        self.sizes = (self.image.width, self.image.height)

    def get_npArray(self):
        arr = np.array(self.image)
        return arr

    def save(self):
        self.image.save(self.path)