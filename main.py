import requests
import random
import pickle
import t


def maomaotu(now_chat_id):
    try:
        with open('photo_ids.pickle', 'rb') as f:
            photo_ids = pickle.load(f)
        len_photo = len(photo_ids)
        i = random.randrange(len_photo)
        url_photo = 'https://api.telegram.org/' + t.token + '/sendPhoto'
        args_photo = {'chat_id': now_chat_id, 'photo': photo_ids[i]}
        r_photo = requests.post(url_photo, json=args_photo)
    except (IndexError, ValueError):
        pass

def send_cute_return(now_chat_id):
    try:
        url_send_cute_return = 'https://api.telegram.org/' + t.token + '/sendMessage'
        args_send_cute_return = {'chat_id': now_chat_id, 'text': '现在请发送仅一张猫猫图！'}
        r_send_cute_return = requests.post(url_send_cute_return, json=args_send_cute_return)
    except (IndexError, ValueError):
        pass

def photo_return(now_chat_id):
    try:
        url_photo_return = 'https://api.telegram.org/' + t.token + '/sendMessage'
        args_photo_return = {'chat_id': now_chat_id, 'text': '已经收到一张猫猫图！'}
        r_photo_return = requests.post(url_photo_return, json=args_photo_return)
    except (IndexError, ValueError):
     pass


if __name__ == '__main__':

    while True:
        with open('update_id.pickle', 'rb') as f_update_id:
            args_getUpdates = pickle.load(f_update_id)
        url_getUpdates = 'https://api.telegram.org/' + t.token + '/getUpdates'
        r_getUpdates = requests.post(url_getUpdates, json = args_getUpdates)
        data_getUpdates = r_getUpdates.json()
        print(data_getUpdates)

        try:
            now_update_id = data_getUpdates['result'][0]['update_id']+1
            args_getUpdates['offset'] = now_update_id
            with open('update_id.pickle', 'wb') as f_update_id2:
                pickle.dump(args_getUpdates, f_update_id2)
        except (IndexError, KeyError):
            pass

        try:
            now_chat_id = data_getUpdates['result'][0]['message']['from']['id']
            with open('chat_ids.pickle', 'rb') as f_chat_ids:
                chat_ids = pickle.load(f_chat_ids)
            if now_chat_id not in chat_ids:
                chat_ids.append(now_chat_id)
                with open('chat_ids.pickle', 'wb') as f_chat_ids2:
                    pickle.dump(chat_ids, f_chat_ids2)
        except (IndexError, KeyError):
            pass

        try:
            now_photo_id = data_getUpdates['result'][0]['message']['photo'][0]['file_id']
            now_chat_id = data_getUpdates['result'][0]['message']['from']['id']

            with open('send_bool.pickle', 'rb') as f_send_bool:
                send_bool = pickle.load(f_send_bool)
            if send_bool:
                with open('photo_ids.pickle', 'rb') as f_photo_ids:
                    photo_ids = pickle.load(f_photo_ids)
                photo_ids.append(now_photo_id)
                with open('photo_ids.pickle', 'wb') as f_photo_ids2:
                    pickle.dump(photo_ids, f_photo_ids2)
                with open('send_bool.pickle', 'wb') as f_send_bool4:
                    send_bool = False
                    pickle.dump(send_bool, f_send_bool4)
                photo_return(now_chat_id)
        except (IndexError, KeyError):
            pass

        try:
            now_text = data_getUpdates['result'][0]['message']['text']
            now_chat_id = data_getUpdates['result'][0]['message']['from']['id']
            if (now_text[-5:] == '/cute') or ('/cute ' in now_text):
                maomaotu(now_chat_id)

            if (now_text[-10:] == '/send_cute') or ('/send_cute ' in now_text):
                with open('send_bool.pickle', 'wb') as f_send_bool2:
                    send_bool = True
                    pickle.dump(send_bool, f_send_bool2)
                send_cute_return(now_chat_id)


            else:
                with open('send_bool.pickle', 'wb') as f_send_bool3:
                    send_bool = False
                    pickle.dump(send_bool, f_send_bool3)
        except (IndexError, KeyError):
            pass




