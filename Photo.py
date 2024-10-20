import os

class Photo:
    def __init__(self,path):
        self.path = path

    
    def __del__(self):
        print(f"deleting {self.path}")
        try:
            os.remove(self.path)
        except Exception as e:
            print(f"Error deleting file: {e}")

class telegram_Photo(Photo):
    def __init__(self,file_id,file_info):
        self.file_id = file_id
        self.file_info = file_info
        self.path = f'./save_folder/{self.file_id}.jpg'

    def from_message(message,bot):
        photo = message.photo[-1]
        file_id = photo.file_id 
        file_info = bot.get_file(file_id)
        return telegram_Photo(file_id,file_info)

    def from_file_id(file_id):
        file_info = bot.get_file(file_id)
        return telegram_Photo(file_id,file_info)


    def save_photo(self,bot):
        #TODO: add is not exsits
        downloaded_file = bot.download_file(self.file_info.file_path)
        with open(self.path, 'wb') as new_file:
            new_file.write(downloaded_file)