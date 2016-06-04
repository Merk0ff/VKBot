import vk_api
import time
import random
import os
import sys


# bot generate system
def BotName(Name):
    if (Name):
        return '30_bot'
    else:
        return '30 bot'


# ban system
def AntiSpam(resp):
    if (resp['items'][0].get('chat_id') == 51 or resp['items'][0].get('chat_id') == 67):
        return 1
    return 0
    # return 1


def GetMsgData(respdata, data):
    if respdata['items'][0].get('body').lower().find('30_bot') == -1 and respdata['items'][0].get(
            'body').lower().find('30 bot') == -1:
        if (respdata['items'][0].get('body')).lower().find(data) != -1:
            return True
        else:
            return False
    else:
        return False


def GetMsg(adm, resp):
    if resp['items'][0].get('date') > adm['items'][0].get('date'):
        return [resp, 0]
    else:
        return [adm, 1]


def GetUser(resp, vk):
    if resp[1] == 0:
        Name = vk.users.get(user_ids=(resp[0]['items'][0].get('user_id')))
        return Name[0]['first_name'] + ' ' + Name[0]['last_name']
    else:
        Name = vk.account.getProfileInfo()
        return Name['first_name'] + ' ' + Name['last_name']


def GetPickFromAniWall(vk, domain):
    d = domain[random.randint(0, len(domain) - 1)]
    wall = vk.wall.get(domain=d, offset=random.randint(0, 300), count=1)
    if not ('photo' in wall['items'][0]['attachments'][0]):
        return ['photo67073585_417366128', 'PD6']
    owid = str(wall['items'][0]['attachments'][0]['photo'].get('owner_id'))
    id = str(wall['items'][0]['attachments'][0]['photo'].get('id'))
    acces = str(wall['items'][0]['attachments'][0]['photo'].get('access_key'))
    return ['photo' + owid + '_' + id + '_' + acces, d]


def GetChatId(resp):
    if not ('chat_id' in resp['items'][0]):
        return [resp['items'][0].get('user_id'), 0]
    else:
        return [resp['items'][0].get('chat_id'), 1]


def SendMessage(vk, resp, message, attachment):
    Id = GetChatId(resp[0])

    if attachment != -1:
        if Id[1] == 1:
            vk.messages.send(chat_id=Id[0],
                             message=message,
                             attachment=attachment)
        else:
            vk.messages.send(user_id=Id[0],
                             message=message,
                             attachment=attachment)
    else:
        if Id[1] == 1:
            vk.messages.send(chat_id=Id[0],
                             message=message)
        else:
            vk.messages.send(user_id=Id[0],
                             message=message)


def MessageHandle(vk):
    last = lastadm = 0
    i = 0
    Name = 1
    run_flag = True
    Leybos = ['mudakoff', 'iface', 'iface', 'best', 'why4ch']
    Mem = ['oldlentach', 'pikabu', 'tnull', 'sysodmins', 'leprum']

    while (True):
        user = vk.messages.get(count=1)
        admin = vk.messages.get(count=1, out=1)
        response = GetMsg(admin, user)
        if (response[0]['items'][0].get('id') != last and run_flag):
            print(GetUser(response, vk) + ": " + str(response[0]['items'][0].get('body')))
            if AntiSpam(response[0]):
                # here we can do massage handle
                if GetMsgData(response[0], '$голос'):
                    SendMessage(vk, response, BotName(Name) + ' ГАВ', 'video67073585_456239040')
                if GetMsgData(response[0], '$лейбович'):
                    ret = GetPickFromAniWall(vk, Leybos)
                    SendMessage(vk, response, (BotName(Name) + ' ' + 'from' + ' ' + ret[1] + ':'), ret[0])
                if GetMsgData(response[0], '$mem'):
                    ret = GetPickFromAniWall(vk, Mem)
                    SendMessage(vk, response, (BotName(Name) + ' ' + 'from' + ' ' + ret[1] + ':'), ret[0])

                if GetMsgData(response[0], "ыыы"):
                    while i < 3:
                        SendMessage(vk, response, (BotName(
                            Name) + ' ыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыы'),
                                    -1)
                        i += 1
                    i = 0
        if (admin['items'][0].get('body') == '$stop'):
            run_flag = False
            SendMessage(vk, response, '30_bot: остановлено', -1)
        if (admin['items'][0].get('body') == '$start'):
            run_flag = True
            SendMessage(vk, response, '30_bot: запущено', -1)
        if Name:
            Name = 0
        else:
            Name = 1
        last = response[0]['items'][0].get('id')
        time.sleep(0.5)


def main():
    login = input('Login:')
    password = input('Password:')

    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    MessageHandle(vk)


if __name__ == '__main__':
    main()
