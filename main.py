# импорты
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from conf import comunity_token, acces_token
from core import VkTools

from baza import new_user_id, search_id



class BotInterface():

    def __init__(self, comunity_token, acces_token):
        self.interface = vk_api.VkApi(token=comunity_token)
        self.api = VkTools(acces_token)
        self.params = None

    def message_send(self, user_id, message, attachment=None):
        self.interface.method('messages.send',
                              {'user_id': user_id,
                               'message': message,
                               'attachment': attachment,
                               'random_id': get_random_id()
                               }
                              )

    def event_handler(self):
        longpoll = VkLongPoll(self.interface)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()

                if command == 'привет':
                    self.params = self.api.get_profile_info(event.user_id)
                    self.message_send(event.user_id, f'Здравствуй, {self.params["name"]}')

                    if not self.params['city']:
                        self.message_send(event.user_id, 'Введи свой город')

                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                self.params['city'] = event.text.lower()
                                self.message_send(event.user_id, 'Спасибо , информацию принял')
                                break

                    if self.params['sex'] == 0:
                        self.message_send(event.user_id, 'Уточни свой пол , ответь цифрой: 1 если жен., 2 если муж.')

                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                self.params['sex'] = event.text.lower()
                                self.params['sex'] = int(self.params['sex'])
                                self.message_send(event.user_id, 'Спасибо , информацию принял')
                                break

                    if self.params['relation'] == 0:
                        self.message_send(event.user_id, "Уточни семеное положение , ответь цифрой:\n"\
                                "1 — не женат/не замужем;\n"\
                                "2 — есть друг/есть подруга;\n"\
                                "3 — помолвлен/помолвлена;\n"\
                                "4 — женат/замужем;\n"\
                                "5 — всё сложно;\n"\
                                "6 — в активном поиске;\n"\
                                "7 — влюблён/влюблена;\n"\
                                "8 — в гражданском браке;\n")

                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                self.params['relation'] = event.text.lower()
                                self.params['relation'] = int(self.params['relation'])
                                self.message_send(event.user_id, 'Спасибо , информацию принял')
                                break

                    if not self.params['bdate']:
                        self.message_send(event.user_id, 'Уточни свою дату рождения в формате D.M.YYYY')

                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                self.params['bdate'] = event.text.lower()
                                self.message_send(event.user_id, 'Спасибо , информацию принял')
                                break

                elif command == 'поиск':

                    users = self.api.serch_users(self.params)
                    # print(users, "1")
                    if len(users) == 0:
                        while len(users) == 0:
                            users = self.api.serch_users(self.params)
                            # print(users, "2")
                            if len(users) == 0:
                                continue
                            else:
                                break

                    user = users[0]

                    # print(user)
                    if str(user['id']) in search_id():
                        while str(user['id']) in search_id():
                            users = self.api.serch_users(self.params)
                            # print(users, "3")
                            if len(users) == 0:
                                print(len(users), "len 0 (3)")
                                continue
                            if str(user['id']) in search_id():
                                # print(len(users), "v bd")
                                continue
                            else:
                                user = users[0]
                                break


                    # user = {"id": 0}
                    # new_user_id(user['id'])
                    #
                    # print(user["id"])
                    # i = 0
                    #
                    # while str(user['id']) in search_id():
                    #     print("Цикл")
                    #
                    #     if i != 0:
                    #         user = users.pop()
                    #         print(len(users))
                    #     else:
                    #         users = self.api.serch_users(self.params)
                    #         print(users)
                    #         user = users.pop()
                    #         print(len(users))
                    #         if len(users) > 2:
                    #             i = 1
                    #         else:
                    #             i = 0




                    photos_user = self.api.get_photos(user['id'])

                    attachment = ''
                    for num, photo in enumerate(photos_user):
                        attachment += f'photo{photo["owner_id"]}_{photo["id"]}'
                        if num == 2:
                            break
                    self.message_send(event.user_id,
                                      f'Встречайте, {user["name"]}',
                                      attachment=attachment
                                      )
                    #логика для внесения в бд
                    new_user_id(user['id'])
                elif command == 'пока':
                    self.message_send(event.user_id, 'Пока')
                else:
                    self.message_send(event.user_id, 'Команда не опознана')



if __name__ == '__main__':
    bot = BotInterface(comunity_token, acces_token)
    bot.event_handler()
