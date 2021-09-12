from config.utils import print_for_users, printAddrLists, getLocalIp, getProfile
from config.objects import Gateway, Database, GW_ADDRESS


print('What vpn-gateway you want to change?'+'\n'+'\n'+'1.{}'.format(GW_ADDRESS)+'\n'+'2.****'+'\n')
choice = input('Choose your destiny?...')

def looping_check(gateway, host_ip):
    loop = True
    db_instance = Database(gateway)
    gw_instance = Gateway(host_ip)
    while loop:
        start_msg = ('''
        PROGRAM IS RUNNING, be care..
        Choose:
        1. Delete account from gateway and db
        2. Add account to gateway and db
        3. Print account details
        4. Disable/Enable account
        ''')
        print(start_msg)
        choice1 = input('Choose your destiny... ')
        if choice1 == '1':
            ################# Delete account section #####################
            print()
            acc_name = input('Enter STRICT account name, you want to delete: ')
            db_instance.deleteAcc(acc_name)
            gw_instance.deleteAcc(acc_name)
            print('----------------------------------------------------')
            print()
            print(acc_name + ' was deleted')
            print()
        elif choice1 == '2':
            ################# Creating account section ###################
            print()
            acc_name = input('Enter RIGHT account name you want to add: ')
            status = 'Active'
            creation_time = input('Enter account creation date: ')
            approve = input('Enter base of approve: ')
            location = input('Enter location of worker: ')
            dept = input('Enter department of user: ')
            printAddrLists(gateway)
            pcname = ''
            addr_list = input('Enter strict address list name: ')
            if addr_list.find('default') != -1:
                pcname = input("Enter user's computer hostname: ")
                pcname += '.puls.local'
            profile = getProfile(gateway)
            ip_local = getLocalIp(gateway)
            db_instance.createAcc(acc_name, creation_time, approve, location, addr_list)
            gw_instance.createAcc(acc_name, ip_local, approve, dept, addr_list, pcname, profile)
            print_for_users(gateway, acc_name, gw_instance.passwd, pcname, addr_list)
        elif choice1 == '3':
            ################# Print account details section #################
            print()
            acc_name = input('Enter account name (or part) you want to see: ')
            result = db_instance.printDetail(acc_name)
            print('-----------------------------------------------')
            print()
            for item in result:
                print(item)
                print()
        elif choice1 == '4':
            ############### Enabling/disabling section #############
            print()
            print('''Choose action:
                    1. Enable account
                    2. Disable account
                    ''')
            print()
            enable_choice = input('Choose your destiny?...')
            if enable_choice == '1':
                acc_name = input('Print a strict name of account u want to enable: ')
                db_instance.enableAcc(acc_name)
                gw_instance.enableAcc(acc_name)
                print()
                print(acc_name, 'is enabled')
            elif enable_choice == '2':
                acc_name = input('Print a strict name of account u want to disable: ')
                db_instance.disableAcc(acc_name)
                gw_instance.disableAcc(acc_name)
                print()
                print(acc_name, 'is disabled')
            #############################################################
        print()
        print('-----------------------------------------------')
        print()
        again = input('Anything else? (yes/no):  ')
        if again.lower().find('yes') != -1 or again.lower().find('y') != -1:
            continue
        else:
            loop = False
            print()
            print()
            print('Closed')
            print()
            print()

if choice == '1':
    table_name = '***'
    looping_check(table_name, GW_ADDRESS)

elif choice == '2':
    table_name = '***'
    looping_check(table_name, ****)