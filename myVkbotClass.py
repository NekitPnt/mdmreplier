import json
import vk


class VkMethods:
    def __init__(self, token, api_version, service_token=''):
        self.session = vk.Session()
        self.api = vk.API(self.session, v=api_version)
        self.token = token
        self.service_token = service_token

    def send_message(self, user_id, message="", keyboard=None, attachment=()):
        if keyboard is None:
            keyboard = {'one_time': True, 'buttons': []}
        # отображение русских клавиш
        keyboard = json.dumps(keyboard, ensure_ascii=False)

        self.api.messages.send(access_token=self.token, user_id=user_id, message=message,
                               keyboard=keyboard, attachment=attachment)

    def send_message_to_chat(self, peer_id, message="", attachment=()):
        self.api.messages.send(access_token=self.token, peer_id=peer_id, message=message, attachment=attachment)

    def set_activity(self, user_id, group_id, activity_type='typing'):
        self.api.messages.setActivity(access_token=self.token, user_id=user_id, type=activity_type, group_id=group_id)

    def execute(self, code):
        self.api.execute(access_token=self.token, code=code)

    def check_user_sub(self, group_id, user_id):
        return self.api.groups.isMember(access_token=self.token, group_id=group_id, user_id=user_id)

    def photo_by_id(self, photo_id):
        return self.api.photos.getById(access_token=self.service_token, photos=photo_id)[0]

    def count_wall_posts(self, group_id):
        return self.api.wall.get(access_token=self.service_token, owner_id=group_id, count=1)["count"]

    def get_group_wall(self, group_id, size=None, shift=0):
        if size is None:
            size = self.api.wall.get(access_token=self.service_token, owner_id=group_id, count=1)["count"]
        c = size//100 + 1
        result = []
        for i in range(c):
            d = self.api.wall.get(access_token=self.service_token, owner_id=group_id, offset=i*100+shift, count=100)
            for j in d['items']:
                if len(result) < size:
                    result.append(j)

        return result

    def user_get(self, user_ids, fields):
        return self.api.users.get(access_token=self.token, user_ids=user_ids, fields=fields)

    def user_name(self, user_id):
        # [{'id': id, 'first_name': 'Name', 'last_name': 'Lname'}]
        user = self.api.users.get(access_token=self.token, user_ids=user_id)[0]
        return user['first_name'], user['last_name']

    def linked_user_name(self, user_id):
        full_name = self.user_name(user_id)
        first_name = '@id' + str(user_id) + '(' + full_name[0] + ')'
        last_name = '@id' + str(user_id) + '(' + full_name[1] + ')'
        return first_name, last_name

    @staticmethod
    def create_keyboard(one_time_flag=True, buttons=()):
        btn_colors = {
            'white': 'default',
            'blue': 'primary',
            'red': 'negative',
            'green': 'positive'
        }
        for i in buttons:
            for j in range(len(i)):
                payload = json.dumps({"command": ""})
                color = btn_colors['white']
                if len(i[j]) == 3:
                    payload = json.dumps({"command": i[j][2]})
                    color = btn_colors[i[j][1]]
                elif len(i[j]) == 2:
                    color = btn_colors[i[j][1]]
                label = str(i[j][0])[:40]
                i[j] = {'action': {'type': 'text', 'payload': payload, 'label': label}, 'color': color}
        keyboard = {'one_time': one_time_flag, 'buttons': buttons}
        return keyboard

        # example
        # print(create_keyboard(False, [[['text1'], ['text2','blue']],
        #                               [['text3','red','123']]]))
