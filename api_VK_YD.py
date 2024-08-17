import requests, json, os
from pprint import pprint

#Ввод ключа api Яндекс.Диск и id страницы пользователя ВК
OAuth = input('Всавьте ключ API Яндекс.Диск: ')
user_id = input('Всавьте id-пользователя VK: ')

#Данные для запроса в ВК
url = 'https://api.vk.com/method'
access_token = 'vk1.a.MmuLP_RPCRr-K4c_6Cw9xb2pJE7nsajpXLNhA1qqitQ84Q-JGfvgNVsrcZPlWHY7I6iui8Hk1856BeSj9PLaRsYNZE45FE6_Nc8TeQ6oY_uJ0tkqGJdsVXyBNNJZOaxZHgDsOj9rS8OYF3V_1uonGUaph75I06OcA53Iprvvm7UW0jEpg6EeUiypkadYNGUp'

class VK:
    def __init__(self, access_token, user_id):
        self.token = access_token
        self.id = user_id

    def get_common_params(self):  # Создаем отдельный метод по передачи токена и версии API
        return {
            'access_token': self.token,
            'v': 5.199
        }
    def get_profile_photo(self):
        params = self.get_common_params()
        params.update({'owner_id': user_id, 'album_id': 'profile', 'extended': 1, 'rev': 0, 'photo_sizes': 1})
        response = requests.get(f'{url}/photos.get', params=params)
        return response.json()

# Метод загрузки json на диск
class json_file_download:
    def __init__(self, filename):
        self.filename = 'vk_photos.json'
        # Отправка файла в папку на Яндекс Диск
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                params={'path': f'Profile_{user_id}/{filename}'},
                                headers=headers)
        # Ответом на запрос будет ссылка, по которой можно загружать файл
        print(f'Получена ссылка для загрузки файла')
        # print(response.json()['href'])
        url_upload = response.json()['href']
        # Загрузка файла по полученной ссылке
        print(f'Начинаем загрузку файла')
        with open(filename, 'rb') as f:
            requests.put(url_upload, files={'file': f})
        print(f'Файл JSON загружен на Яндекс.Диск')

# Метод загрузки файла на диск
class photo:
    def __init__(self, a, c, x, filename):
        self.a = a
        self.c = c
        self.x = x
        self.filename = filename
        print(f'Получена ссылка для скачивания фото №{x}')
        # Скачивание фото
        response = requests.get(a)
        print(f'Фото №{x} скачано')

        # Сохранение картинки
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'Фото №{x} сохранено')
        # Отправка файла в папку на Яндекс Диск
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                params={'path': f'Profile_{user_id}/{filename}'},
                                headers=headers)
        # Ответом на запрос будет ссылка, по которой можно загружать файл
        print(f'Получена ссылка для загрузки фото №{x}')
        url_upload = response.json()['href']
        # Загрузка файла по полученной ссылке
        print(f'Начинаем загрузку фото №{x}')
        with open(filename, 'rb') as f:
            requests.put(url_upload, files={'file': f})
        print(f'Удален временный файл фото №{x}')
        os.remove(f'{filename}')
        print(f'Фото №{x} загружено')


# Создание папки на Яндекс Диск
url_create_folder = 'https://cloud-api.yandex.net/v1/disk/resources'
params = {
    'path': f'Profile_{user_id}'
}
headers = {
    'Authorization': OAuth
}

# Отправляем запрос на создание папки на Яндекс Диск
response = requests.put(url_create_folder,
                        params=params,
                        headers=headers)
print('Папка на Яндекс.Диск создана')

vk = VK(access_token, user_id)
photos_info = vk.get_profile_photo()

#Сохранение файла json
with open('vk_photos.json', 'w') as f:
    json_data = json.dump(photos_info, f)


#Заходим в первый уровень ответа на запрос
list1 = photos_info.get('response')
print(f'в профиле {list1.get('count')} фотографий')
#Заходим в список items
List2 = list1.get('items')

photos_list = []
x = 0
#Ищем в items разделы, в которых есть size = x
for i in List2:
    if 'sizes' in i:
        photos_dict = {}
        b = i.get('likes').get('count')
        list_dict = i.get('sizes') #Создаем список размеров фото, в котором будем искать максимальный
        # z - оригинал
        # y - 2-й по размеру
        # x - 3-й по размеру


        dict_photos_3 = {} #Создаем словарь где пары будут размер - ссылка
        for i in list_dict:
            size = i.get('type')
            url_size = i.get('url')
            dict_photos_3.setdefault(size, url_size)


        #Поиск максимального размера фото в словаре
        if dict_photos_3.get('z') != None:
            print('найден размер фото "z"')
            c = 'z'
            url = dict_photos_3.get('z')

        elif dict_photos_3.get('y') != None:
            print('найден размер фото "y"')
            c = 'y'
            url = dict_photos_3.get('y')

        elif dict_photos_3.get('x') != None:
            print('найден размер фото "x"')
            c = 'x'
            url = dict_photos_3.get('x')

        x += 1
        filename = f'File_{x}-likes_{b}-size_{c}.jpg'
        a = i.get('url')
        photo(a, c, x, filename)


        photos_dict.setdefault('filename', filename)
        photos_dict.setdefault('likes', b)
        photos_dict.setdefault('size', c)

        photos_list.append(photos_dict)


sorted_list = sorted(photos_list, key=lambda x: x['likes'], reverse=True)

print(f' Загружено {x} из {list1.get('count')} фотографий')

print(f' Json-файл:')
pprint(sorted_list)

json_file_download('vk_photos.json')

