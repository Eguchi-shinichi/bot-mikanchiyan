import requests
from influxdb import InfluxDBClient

import re
import sqlite3
import datetime
from time import sleep

import t


def send_cute_return(id_):
    try:
        url_send_cute_return = 'https://api.telegram.org/bot' + t.token + '/sendMessage'
        args_send_cute_return = {'chat_id': id_, 'text': '现在请发送仅一张猫猫图！'}
        r_send_cute_return = requests.post(url_send_cute_return, json=args_send_cute_return, timeout=10)
    except (IndexError, ValueError, TimeoutError):
        pass


def photo_return(id_):
    try:
        url_photo_return = 'https://api.telegram.org/bot' + t.token + '/sendMessage'
        args_photo_return = {'chat_id': id_, 'text': '已经收到一张猫猫图！'}
        r_photo_return = requests.post(url_photo_return, json=args_photo_return, timeout=10)
    except (IndexError, ValueError, TimeoutError):
        pass


class Parser:
    def __init__(self):
        client = InfluxDBClient(t.utl, 23333, t.username, t.key, '温度传感器')
        temperature = list(client.query('select last(temperature) from "温度传感器";')["温度传感器"])[0]['last']
        pressure = list(client.query('select last(pressure) from "温度传感器";')["温度传感器"])[0]['last']
        humidity = list(client.query('select last(humidity) from "温度传感器";')["温度传感器"])[0]['last']
        time = list(client.query('select last(temperature) from "温度传感器";')["温度传感器"])[0]['time']
        r_time = r'([0-9]{4}?-[0-9]{2}?-[0-9]{2}?T[0-9]{2}?:[0-9]{2}?:[0-9]{2})?.'
        re_time = re.match(r_time, time)
        time_g = re_time.group(1)
        utc_format = "%Y-%m-%dT%H:%M:%S"
        utcTime = datetime.datetime.strptime(time_g, utc_format)
        localtime = utcTime + datetime.timedelta(hours=8)
        localtime = str(localtime)
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.time = localtime


def send_get(id_):
    print(1)
    try:
        print(2)
        url_send_get = 'https://api.telegram.org/bot' + t.token + '/sendMessage'
        parser = Parser()
        text = '温度: ' + parser.temperature + '\n' + '湿度: ' + parser.humidity + '\n' + '气压: ' + parser.pressure + '\n' + '时间: ' + parser.time
        args_send_get = {'chat_id': id_, 'text': text}
        r_send_get = requests.post(url_send_get, json=args_send_get, timeout=10)
    except (ImportError, ValueError, TimeoutError):
        print(3)
        pass


class CheckTemperatureAndHumidity:
    def __init__(self):
        self.bool_temperature_up = True
        self.bool_temperature_down = True
        self.bool_humidity_up = True
        self.bool_humidity_down = True
        self.check_temperature_up = 28
        self.check_temperature_down = 24
        self.check_humidity_up = 65
        self.check_humidity_down = 35

    def check(self):
        chat_id_eguchi = '850108007'
        url_send_check = 'https://api.telegram.org/bot' + t.token + '/sendMessage'
        parser = Parser()
        text = '温度: ' + parser.temperature + '\n' + '湿度: ' + parser.humidity + '\n' + '气压: ' + parser.pressure + '\n' + '时间: ' + parser.time
        if float(parser.temperature) > self.check_temperature_up:
            if self.bool_temperature_up:
                self.check_temperature_up = 27
                self.bool_temperature_up = False
                args_check = {'chat_id': chat_id_eguchi, 'text': '温度过高！：\n' + text}
                r_check = requests.post(url_send_check, json=args_check, timeout=10)
        else:
            if not self.bool_temperature_up:
                self.check_temperature_up = 28
                self.bool_temperature_up = True
                args_check = {'chat_id': chat_id_eguchi, 'text': '温度恢复正常！：\n' + text}
                r_check = requests.post(url_send_check, json=args_check, timeout=10)

        if float(parser.temperature) < self.check_temperature_down:
            if self.bool_temperature_down:
                self.check_temperature_down = 25
                self.bool_temperature_down = False
                args_check = {'chat_id': chat_id_eguchi, 'text': '温度过低！：\n' + text}
                r_check = requests.post(url_send_check, json=args_check, timeout=10)
        else:
            if not self.bool_temperature_down:
                self.check_temperature_down = 24
                self.bool_temperature_down = True
                args_check = {'chat_id': chat_id_eguchi, 'text': '温度恢复正常！：\n' + text}
                r_check = requests.post(url_send_check, json=args_check, timeout=10)

        if float(parser.humidity) > self.check_humidity_up:
            if self.bool_humidity_up:
                self.check_humidity_up = 55
                self.bool_humidity_up = False
                args_check = {'chat_id': chat_id_eguchi, 'text': '湿度过高！：\n' + text}
                r_check = requests.post(url_send_check, json=args_check, timeout=10)
        else:
            if not self.bool_humidity_up:
                self.check_humidity_up = 65
                self.bool_humidity_up = True
                args_check = {'chat_id': chat_id_eguchi, 'text': '湿度恢复正常！：\n' + text}
                r_check = requests.post(url_send_check, json=args_check, timeout=10)

        if float(parser.humidity) < self.check_humidity_down:
            if self.bool_humidity_down:
                self.check_humidity_down = 45
                self.bool_humidity_down = False
                args_check = {'chat_id': chat_id_eguchi, 'text': '湿度过低！：\n' + text}
                r_check = requests.post(url_send_check, json=args_check, timeout=10)
        else:
            if not self.bool_humidity_down:
                self.check_humidity_down = 35
                self.bool_humidity_down = True
                args_check = {'chat_id': chat_id_eguchi, 'text': '湿度恢复正常！：\n' + text}
                r_check = requests.post(url_send_check, json=args_check, timeout=10)


def maomaotu(id_):
    try:
        the_id = list(photo_ids0.execute('select photoid from photo_ids order by random() limit 1'))[0][0]
        print(the_id)
        url_photo = 'https://api.telegram.org/bot' + t.token + '/sendPhoto'
        args_photo = {'chat_id': id_, 'photo': the_id}
        r_photo = requests.post(url_photo, json=args_photo, timeout=10)
    except (IndexError, ValueError, TimeoutError):
        pass


if __name__ == '__main__':
    # 尝试创建猫猫图数据库
    photo_ids0 = sqlite3.connect('maomao.db', isolation_level=None)
    try:
        photo_ids0.execute('create table photo_ids(photoid)')
    except sqlite3.OperationalError:
        pass

    now_update_id = 217220878
    # send_bool 判断收到的图片是不是猫猫图
    check = CheckTemperatureAndHumidity()

    while True:
        # 检查温湿度
        check.check()
        # 更新并尝试获取用户需求
        args_getUpdates = {'offset': now_update_id, 'timeout': 60}
        url_getUpdates = 'https://api.telegram.org/bot' + t.token + '/getUpdates'
        try:
            r_getUpdates = requests.post(url_getUpdates, json=args_getUpdates, timeout=70)
            data_getUpdates = r_getUpdates.json()
        except (IndexError, ValueError, TimeoutError, requests.exceptions.ConnectionError):
            continue
        print(data_getUpdates)
        # update id 更新
        try:
            now_update_id = data_getUpdates['result'][0]['update_id'] + 1
        except (IndexError, KeyError):
            pass
        # 尝试获取chat id 和 photo id
        try:
            now_photo_id = data_getUpdates['result'][0]['message']['photo'][0]['file_id']
            now_chat_id = data_getUpdates['result'][0]['message']['from']['id']
            # 发送猫猫图
            if send_bool:
                photo_ids0.execute('insert into photo_ids(photoid) values (?)', (now_photo_id,))
                send_bool = False
                photo_return(now_chat_id)
        except (IndexError, KeyError):
            pass
        # 匹配用户需求
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
