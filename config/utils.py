import string
import secrets


def password_gen():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(9))
    return password


def print_for_users(table_name, acc_name, passwd, pcname=None, addr_list=None):
    if table_name == '***':
        l2tp_key = '*****'
    elif table_name == '****':
        l2tp_key = '*****'
    print()
    print('--------------------------------------------------------------')
    print()
    print('Добрый день!')
    print('Инструкции во вложении, данные для подключения ниже: ')
    print()
    print('Адрес сервера для подключения: ' + table_name + '*****')
    print('Имя пользователя VPN: ' + acc_name)
    print('Пароль пользователя VPN: ' + passwd)
    print('L2TP+ipsec Общий ключ: ' + l2tp_key)
    print()
    if addr_list.find('default') != -1 and pcname:
        print('Имя компьютера для подключения по RDP: ' + pcname)
        print('Имя пользователя при подключении по RDP: ****\\' + acc_name)
        print()
        print('---------------------------------------------------------------')

def ip_gen(gateway, ppp_secret):
    if gateway == '*****':
        #### creating pool of free IP addresses ####
        pool = set()
        for i in range(2, 255):
            pool.add('172.22.10.' + str(i)) #special addresses for gateway
            pool.add('172.22.11.' + str(i)) #special addresses for gateway
        used = set()
        for i in tuple(ppp_secret):
            used.add(i['remote-address'])
        free = list(pool - used)
        return free[0]
    elif gateway == '*****':
        pool = set()
        for i in range(2, 255):
            pool.add('172.22.2.' + str(i)) #special addresses for gateway
            pool.add('172.22.3.' + str(i)) #special addresses for gateway
        used = set()
        for i in tuple(ppp_secret):
            used.add(i['remote-address'])
        free = list(pool - used)
        return free[0]


def printAddrLists(gateway):
    if gateway.find('****') != -1:
        print('''Choose a address list to add:
                            *some1
                            *some2
                            *some3
                            or pass''')

    elif gateway.find('****') != -1:
        print('''Choose a address list to add:
                            *some1
                            *some2
                            *some3
                            or pass''')


def getLocalIp(gateway):
    if gateway.find('****') != -1:
        return '172.22.10.1'
    elif gateway.find('****') != -1:
        return '127.22.3.1'

def getProfile(gateway):
    if gateway.find('****') != -1:
        return '*****'
    elif gateway.find('****') != -1:
        return '*****'