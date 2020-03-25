import requests
import t
import re
from influxdb import InfluxDBClient
import sqlite3


def send_cute_return(now_chat_id):
    try:
        url_send_cute_return = 'https://api.telegram.org/bot' + t.token + '/sendMessage'
        args_send_cute_return = {'chat_id': now_chat_id, 'text': '现在请发送仅一张猫猫图！'}
        r_send_cute_return = requests.post(url_send_cute_return, json=args_send_cute_return)
    except (IndexError, ValueError):
        pass


def photo_return(now_chat_id):
    try:
        url_photo_return = 'https://api.telegram.org/bot' + t.token + '/sendMessage'
        args_photo_return = {'chat_id': now_chat_id, 'text': '已经收到一张猫猫图！'}
        r_photo_return = requests.post(url_photo_return, json=args_photo_return)
    except (IndexError, ValueError):
     pass


def send_get(now_chat_id):
    try:
        url_send_get = 'https://api.telegram.org/bot' + t.token + '/sendMessage'
        client = InfluxDBClient('rpi', 8086, 'root', 'root', '温度传感器')
        temperature = list(client.query('select last(temperature) from "温度传感器";')["温度传感器"])[0]['last']
        pressure = list(client.query('select last(pressure) from "温度传感器";')["温度传感器"])[0]['last']
        humidity = list(client.query('select last(humidity) from "温度传感器";')["温度传感器"])[0]['last']
        print(temperature)
        text = '温度：' + temperature + '\n' + '湿度：' + humidity +'\n' + '气压：' + pressure + '\n'
        args_send_get = {'chat_id': now_chat_id, 'text': text}
        r_send_get = requests.post(url_send_get, json=args_send_get)
    except (ImportError, ValueError):
        pass


def maomaotu(now_chat_id):
    try:
        the_id = list(photo_ids0.execute('select photoid from photo_ids order by random() limit 1'))[0][0]
        print(the_id)
        url_photo = 'https://api.telegram.org/bot' + t.token + '/sendPhoto'
        args_photo = {'chat_id': now_chat_id, 'photo': the_id}
        r_photo = requests.post(url_photo, json=args_photo)
    except (IndexError, ValueError):
        pass


if __name__ == '__main__':

    photo_ids0 = sqlite3.connect('maomao.db', isolation_level=None)
    try:
        photo_ids0.execute('create table photo_ids(photoid)')
    except sqlite3.OperationalError:
        pass
    now_update_id = 217220878
    send_bool = False

    while True:
        args_getUpdates = {'offset': now_update_id}
        url_getUpdates = 'https://api.telegram.org/bot' + t.token + '/getUpdates'
        r_getUpdates = requests.post(url_getUpdates, json=args_getUpdates)
        data_getUpdates = r_getUpdates.json()
        print(data_getUpdates)

        try:
            now_update_id = data_getUpdates['result'][0]['update_id']+1
        except (IndexError, KeyError):
            pass

        try:
            now_photo_id = data_getUpdates['result'][0]['message']['photo'][0]['file_id']
            now_chat_id = data_getUpdates['result'][0]['message']['from']['id']

            if send_bool:
                photo_ids0.execute('insert into photo_ids(photoid) values (?)', (now_photo_id,))
                send_bool = False
                photo_return(now_chat_id)
        except (IndexError, KeyError):
            pass

        try:
            r_cute = r'.*?/cute'
            r_send_cute = r'.*?/send_cute'
            r_get = r'.*?/get'
            now_text = data_getUpdates['result'][0]['message']['text']
            now_chat_id = data_getUpdates['result'][0]['message']['from']['id']
            re_cute = re.match(r_cute, now_text)
            re_send_cute = re.match(r_send_cute, now_text)
            re_get = re.match(r_get, now_text)

            if re_get:
                send_get(now_chat_id)

            if re_cute:
                maomaotu(now_chat_id)

            if re_send_cute:
                send_bool = True
                send_cute_return(now_chat_id)

            else:
                send_bool = False
        except (IndexError, KeyError):
            pass




