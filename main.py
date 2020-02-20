import myVkbotClass as myVkbot
import jsonReadWrite as jRW
import settings
import manager


# создание объекта класса VkMethods для работы со всеми нужными методами для вк
vk_bot6_for_chat = myVkbot.VkMethods(settings.vk_token_06, settings.vk_api_version_for_chat)
vk_bot3_for_chat = myVkbot.VkMethods(settings.vk_token_03, settings.vk_api_version_for_chat)
# создание объекта класса VkMethods для работы со всеми нужными методами для вк
vk_bot6_for_ls = myVkbot.VkMethods(settings.vk_token_06, settings.vk_api_version_for_ls)
vk_bot3_for_ls = myVkbot.VkMethods(settings.vk_token_03, settings.vk_api_version_for_ls)


# функция уведомляющая админа об ошибке
def error_notificator(error):
    vk_bot6_for_chat.send_message(settings.error_receiver_id, error)


def response_handler_for_vk(data):
    # блок обработки запросов пришедших с 6 группы
    if data['group_id'] == settings.group_6_id:
        if data['type'] == 'confirmation':
            return settings.group_6_confirmation_token
        elif data['type'] == 'wall_post_new':
            send_message_to_chat(settings.conf_6_id, attachment='wall%s_%s' % (data['object']['owner_id'], data['object']['id']), group_num=settings.group_num_6)
        elif (data['type'] == 'message_new' or data['type'] == 'message_edit') and \
                data['object']['from_id'] != -settings.group_6_id:
            create_answer(data['object'], settings.group_num_6, 'vk')

    # блок обработки запросов пришедших с 3 группы
    elif data['group_id'] == settings.group_3_id:
        if data['type'] == 'confirmation':
            return settings.group_3_confirmation_token
        elif data['type'] == 'wall_post_new':
            if 'text' in data['object'] and sum([i.lower() in settings.shared_hashtags for i in data['object']['text'].split(' ')]):
                message = data['object']['text']
                attach = ()
                if 'attachments' in data['object']:
                    attach = ['%s%s_%s' % (att['type'], att[att['type']]['owner_id'], att[att['type']]['id']) for att in data['object']['attachments']]
                send_message_to_chat(settings.conf_6_id, message=message, attachment=attach, group_num=settings.group_num_6)
            send_message_to_chat(settings.conf_3_id, attachment='wall%s_%s' % (data['object']['owner_id'], data['object']['id']), group_num=settings.group_num_3)
        elif (data['type'] == 'message_new' or data['type'] == 'message_edit') and \
                data['object']['from_id'] != -settings.group_3_id:
            create_answer(data['object'], settings.group_num_3, 'vk')

    # возвращаем ок для серверов вк
    return 'ok'


def create_answer(data, group_num, source='vk'):
    if data['text'].lower() in manager.menu['activators']:
        message = manager.menu['text'] + '\n – ' + '\n – '.join([i['text'] for i in manager.menu['features']])
        keyboard = [[[i['button']]] for i in manager.menu['features']]
        send_message_to_ls(data['from_id'], message, keyboard=keyboard, group_num=group_num)
    elif data['text'].lower() in manager.rasp['today']:
        pass
    elif data['text'].lower() in manager.rasp['tomorrow']:
        pass
    elif data['text'].lower() in manager.rasp['semester']:
        sem_rasp = manager.sem_rasp_6 if group_num == settings.group_num_6 else manager.sem_rasp_3
        keyboard = [[["Главное меню"]]]
        send_message_to_ls(data['from_id'], keyboard=keyboard, attachment=sem_rasp, group_num=group_num)
    elif data['text'].lower() in manager.rooms_info_activators:
        message = manager.rooms_info
        keyboard = [[["Главное меню"]]]
        send_message_to_ls(data['from_id'], message, keyboard=keyboard, attachment=manager.rooms_info_attach, group_num=group_num)


def send_message_to_ls(user_id, message='', keyboard=None, attachment=(), group_num=settings.group_num_6):
    if keyboard:
        keyboard = vk_bot6_for_ls.create_keyboard(buttons=keyboard)

    if group_num == settings.group_num_6:
        vk_bot6_for_ls.send_message(user_id, message, keyboard, attachment)
    elif group_num == settings.group_num_3:
        vk_bot3_for_ls.send_message(user_id, message, keyboard, attachment)


def send_message_to_chat(peer_id, message='', attachment=(), group_num=settings.group_num_6):
    if group_num == settings.group_num_6:
        vk_bot6_for_chat.send_message_to_chat(peer_id, message, attachment)
    elif group_num == settings.group_num_3:
        vk_bot3_for_chat.send_message_to_chat(peer_id, message, attachment)
