import pymysql
import pymysql.cursors
from librouteros import connect
from librouteros.query import Key
from config.utils import ip_gen, password_gen

GW_ADDRESS = '10.0.0.1'


GATEWAY_USERNAME = '*****'
GATEWAY_PASSWORD = '*****'

DB_HOST = 'localhost'
DB_NAME = '****'
DB_USERNAME = '*****'
DB_PASSWORD = '*****'


class Gateway:
    def __init__(self, host):
        self.host = host
        self.api = connect(username=GATEWAY_USERNAME,
                      password=GATEWAY_PASSWORD,
                      host=self.host,
                      )
        self.ip_fw_addrlist = self.api.path('ip/firewall/address-list')
        self.ip_fw_filter = self.api.path('ip/firewall/filter')
        self.ppp_secret = self.api.path('ppp/secret')

    def createAcc(self, acc_name, ip_local, approve, dept, addr_list, pcname, profile):
        self.passwd = password_gen()
        ip_remote = ip_gen(self.host, self.ppp_secret)
        if addr_list.find('default') != -1 and pcname != -1:
            pcname += '.puls.local'
            ppp_params = {'name': acc_name, 'profile': profile,'local-address':ip_local, 'password':self.passwd, 'remote-address':ip_remote, 'comment': acc_name + ' ' + dept + ' ' + approve}
            fw_addrlist_params = {'address': pcname, 'list':acc_name}
            fw_rule_params = {'chain':'forward','action':'drop','src-address':ip_remote,'dst-address-list':'!'+acc_name}
            self.ppp_secret.add(**ppp_params)
            self.ip_fw_addrlist.add(**fw_addrlist_params)
            self.ip_fw_filter.add(**fw_rule_params)
        elif addr_list:
            ppp_params = {'name': acc_name, 'profile': profile, 'local-address': ip_local, 'password': self.passwd,
                         'remote-address': ip_remote, 'comment': acc_name + ' ' + dept + ' ' + approve}
            fwalparams = {'address': ip_remote, 'list': addr_list}
            self.ppp_secret.add(**ppp_params)
            self.ip_fw_addrlist.add(**fwalparams)
        else:
            ppp_params = {'name': acc_name, 'profile': profile, 'local-address': ip_local, 'password': self.passwd,
                         'remote-address': ip_remote, 'comment': acc_name + ' ' + dept + ' ' + approve}
            self.ppp_secret.add(**ppp_params)
        print(ip_remote) #for diagnostic reason

    def deleteAcc(self, acc_name):
        for secret in self.ppp_secret.select(Key('.id'), Key('name'), Key('remote-address')).where(Key('name') == acc_name):
            ppp_id = secret.get('.id')
            ip_addr = secret.get('remote-address')
            self.ppp_secret.remove(ppp_id)
            for filter in self.ip_fw_filter.select(Key('.id'), Key('src-address')).where(
                    Key('src-address') == ip_addr):
                filter_id = filter.get('.id')
                self.ip_fw_filter.remove(filter_id)
            for addr_list in self.ip_fw_addrlist.select(Key('.id'), Key('list'), Key('address')):
                addr_list_id = addr_list.get('.id')
                addr_list_name = addr_list.get('list')
                addr_list_addr = addr_list.get('address')
                if addr_list_name == acc_name or addr_list_addr == ip_addr:
                    self.ip_fw_addrlist.remove(addr_list_id)

    def disableAcc(self, acc_name):
        for row in self.ppp_secret.select(Key('.id'), Key('name')).where(Key('name') == acc_name):
            id_number = row.get('.id')
            ppp_params = {'disabled': True, '.id': id_number}
            self.ppp_secret.update(**ppp_params)

    def enableAcc(self, acc_name):
        for row in self.ppp_secret.select(Key('.id'), Key('name')).where(Key('name') == acc_name):
            id_number = row.get('.id')
            ppp_params = {'disabled': False, '.id': id_number}
            self.ppp_secret.update(**ppp_params)






class Database:
    def __init__(self, table_name):
        self.connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USERNAME,
                                     password=DB_PASSWORD,
                                     db=DB_NAME,
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
        self.table_name = table_name

    def createAcc(self, acc_name, creation_time, approve, location, addr_list):
        status = 'Active'
        self.curs = self.connection.cursor()
        self.sql = "INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s)".format(self.table_name)
        self.curs.execute(self.sql, (acc_name, status, creation_time, approve, location, addr_list))
        self.connection.commit()

    def deleteAcc(self, acc_name):
        self.curs = self.connection.cursor()
        self.sql = "DELETE FROM {} WHERE name=%s".format(self.table_name)
        self.curs.execute(self.sql, (acc_name))
        self.connection.commit()

    def printDetail(self, acc_name):
        self.curs = self.connection.cursor()
        self.sql = "SELECT * FROM {} WHERE name LIKE %s".format(self.table_name)
        self.curs.execute(self.sql, ('%' + acc_name + '%'))
        return self.curs.fetchall()

    def disableAcc(self, acc_name):
        self.curs = self.connection.cursor()
        self.sql = "UPDATE {} SET status = 'Disabled' WHERE name = %s".format(self.table_name)
        self.curs.execute(self.sql, (acc_name))

    def enableAcc(self, acc_name):
        self.curs = self.connection.cursor()
        self.sql = "UPDATE {} SET status = 'Active' WHERE name = %s".format(self.table_name)
        self.curs.execute(self.sql, (acc_name))
