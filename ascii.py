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
        self.image_scale = 3
        self.distance = parameters.distance
        self.font_size = parameters.font_size

        
        self.path = path
        self.chars = ' .",:;!~+-xmo*#W&8@'
        #self.chars = r'@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
        if parameters.expand_layout:
            self.chars = self.chars[::-1]
        self.is_original_colors = parameters.original_colors
        self.char_coefficent = len(self.chars)/255
        color_scheme.__init__(self)
        self.source_image = Pillow_image.from_path(self.path)
        self.source_npArray = self.source_image.get_npArray()



        self.height = len(self.source_npArray)
        self.width = len(self.source_npArray[0])
        self.sizes = (self.width,self.height)
        self.result_image = Pillow_image.new(self.source_image.sizes[0]*self.image_scale,self.source_image.sizes[1]*self.image_scale)
        self.draw = ImageDraw.Draw(self.result_image.image)
        self.fnt = ImageFont.truetype("./fonts/consolas.ttf",self.font_size)
        
#todo: parameters is caption redooo pls
    def render_art(path,parameters):
        self = Ascii(path,parameters)

        self.draw_chars()

        return self
    
    def draw_chars(self):
        for row in range(0,self.height,self.distance//self.image_scale):
            for col in range(0,self.width,self.distance//self.image_scale):
                self.draw_char(col,row)

    def draw_char(self,x,y):
        try:
            coordinates = (x*self.image_scale,y*self.image_scale)
            pixel = tuple(map(int, self.source_npArray[y][x]))
            avg_color = sum(pixel)/3
            char_index = int(self.char_coefficent*avg_color) 
            if char_index<0:
                char_index = 0
            elif char_index>len(self.chars)-1:
                char_index = len(self.chars)-1
            
            char = self.chars[char_index]
            print(avg_color)

            if self.is_original_colors: 
                fill_color = pixel
            else:
                fill_color = (255,255,255) #todo: add color_scheme
            

            self.draw.text(coordinates,
                            char,
                            fill=fill_color,
                            font = self.fnt)
        except Exception as e:
            print(len(self.chars)-1 - char_index)
            print(f"error: {e}")   

class Pillow_image(Photo):
    def __init__(self, path):
        self.path = f'{path}'
    
    def from_path(path):
        img = Pillow_image(path)
        img.image = Image.open(path).convert('RGB')
        img.update_sizes()
        return img

    def new(width, height):
        img = Pillow_image("dsadsa.jpg") #todo: add image name there
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