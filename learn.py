import pickle


args_getUpdates = {'offset': 217220878}
chat_ids = [850108007]
photo_ids = []
send_bool = False

with open('update_id.pickle', 'wb') as f1:
    pickle.dump(args_getUpdates, f1)

with open('chat_ids.pickle', 'wb') as f2:
    pickle.dump(chat_ids, f2)

with open('photo_ids.pickle', 'wb') as f3:
    pickle.dump(photo_ids, f3)

with open('send_bool.pickle', 'wb') as f4:
    pickle.dump(send_bool, f4)




