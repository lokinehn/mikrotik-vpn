Simple script to automate work with VPN accounts based on Mikrotik routers.

Script is using for creating, deleteng, disabling/enabling VPN accounts on gateways. 
Also script is saving (deleting, changing, printing) information about VPN account in MySQL database.

All "*****" strings in config and main python files means special information (username, password, gateways addresses, table names in SQL base, etc.)

Requirements: pymysql and librouteros libraries must be installed.

Use: python main.py
