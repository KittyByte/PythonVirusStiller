import json

# -------------------------------------- FIREFOX ----------------------------------------

# [{
#     "Host raw": "http://.brotorrent.org/",
#     "Name raw": "_ym_uid",
#     "Path raw": "/",
#     "Content raw": "1679343128278647830",
#     "Expires": "19-03-2024 23:12:07",
#     "Expires raw": "1710879127",
#     "Send for": "Any type of connection",
#     "Send for raw": "false",
#     "HTTP only raw": "false",
#     "SameSite raw": "no_restriction",
#     "This domain only": "Valid for subdomains",
#     "This domain only raw": "false",
#     "Store raw": "firefox-default",
#     "First Party Domain": ""
# }]

# .brotorrent.org(Host raw)   false(This domain only raw) /(Path raw) false(Send for raw) 1710879127(Expires raw) _ym_uid(Name raw)   1679343128278647830(Content raw)

# -------------------------------------- FIREFOX ----------------------------------------

path = r'C:\Users\Isa\Desktop\Cookies_Chrome.txt'  # путь к кукисам
out_path = r''  # путь вывода результата


def parser():
    with open(path, 'r') as f:
        jsf = json.load(f)
        res = '['
        for i in jsf:
            if i['domain'] == ".instagram.com":  # за место .instagram.com то что нужно вам
                res += str(i)+','
        res += ']'

    with open(out_path, 'w', encoding='utf8') as f:
        res = res.replace("'", '"')
        res = res.replace('True', 'true')
        res = res.replace('False', 'false')
        res = res[:-2]
        res += ']'
        f.write(res)




if __name__ == "__main__":
    # parser()
    ...
