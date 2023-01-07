import json

path = r'' # путь к кукисам
out_path = r'' # путь вывода результата


def parser(path):
    with open(path, 'r') as f:
        jsf = json.load(f)
        res = '['
        for i in jsf:
            if i['domain'] == ".instagram.com":
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
    parser(path)
