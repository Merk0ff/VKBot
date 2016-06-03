import vk_api
import time
import random
import os

def BotName(Name):
    if (Name):
        return '1488_bot'
    else:
        return '1488 bot'


def AntiSpam(resp):
    if (resp['items'][0].get('chat_id') == 51 or resp['items'][0].get('chat_id') == 67):
        return 1
    return 0


def GetMsgData(respdata, data):
    if respdata['items'][0].get('body').lower().find('1488_bot') == -1 and respdata['items'][0].get(
            'body').lower().find('1488 bot') == -1:
        if (respdata['items'][0].get('body')).lower().find(data) != -1:
            return True
        else:
            return False
    else:
        return False


def GetMeg(adm, resp):
    if resp['items'][0].get('date') > adm['items'][0].get('date'):
        return resp
    else:
        return adm


def GetUser(resp, vk):
    Name = list(vk.users.get(user_ids=(resp['items'][0].get('user_id'))))

    return Name[0]['first_name'] + ' ' + Name[0]['last_name']


def GetPickFromAniWall(vk):
    domain = ['mudakoff', 'iface', 'iface', 'best']
    d = domain[random.randint(0, 3)]
    wall = vk.wall.get(domain=d, offset=random.randint(0, 300), count=1)
    if not ('photo' in wall['items'][0]['attachments'][0]):
        return ['photo67073585_417366128', 'PD6']
    owid = str(wall['items'][0]['attachments'][0]['photo'].get('owner_id'))
    id = str(wall['items'][0]['attachments'][0]['photo'].get('id'))
    acces = str(wall['items'][0]['attachments'][0]['photo'].get('access_key'))
    return ['photo' + owid + '_' + id + '_' + acces, d]


def MessageHandle(vk):
    last = lastadm = 0
    i = 0
    Name = 1
    run_flag = True

    while (True):
        user = vk.messages.get(count=1)
        admin = vk.messages.get(count=1, out=1)
        response = GetMeg(admin, user)
        if (user['items'][0].get('id') != last and admin['items'][0].get('id') != lastadm and run_flag):
            print(GetUser(response, vk) + ": " + str(response['items'][0].get('body')))
            if AntiSpam(response):
                # here we can do massage handle
                if GetMsgData(response, '$голос'):
                    vk.messages.send(chat_id=response['items'][0].get('chat_id'), message=(BotName(Name) + ' ГАВ'),
                                     attachment='video67073585_456239040')
                if GetMsgData(response, '$лейбович'):
                    ret = GetPickFromAniWall(vk)
                    vk.messages.send(chat_id=response['items'][0].get('chat_id'),
                                     message=(BotName(Name) + ' ' + 'from' + ' ' + ret[1] + ':'),
                                     attachment=ret[0])
                if GetMsgData(response, "ыыы"):
                    while i < 3:
                        vk.messages.send(chat_id=response['items'][0].get('chat_id'), message=(BotName(
                            Name) + ' ыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыы'))
                        i += 1
                    i = 0
        if (admin['items'][0].get('body') == '$stop'):
            run_flag == False
            vk.messages.send(chat_id=response['items'][0].get('chat_id'), message='1488_bot: остановлено')
        if (admin['items'][0].get('body') == '$start'):
            run_flag == True
            vk.messages.send(chat_id=response['items'][0].get('chat_id'), message='1488_bot: запущено')
        if Name:
            Name = 0
        else:
            Name = 1
        last = response['items'][0].get('id')
        lastadm = admin['items'][0].get('id')
        time.sleep(0.5)


def main():
    login = input('Login:')
    password = input('Password:')
    os.system('cls')

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
