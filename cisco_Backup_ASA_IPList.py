#   File: "cisco_Backup_ASA_IPList.py"
#   This module is add-on to previous task named "cisco_Backup_ASA.py"
#   The additional functionality is to read list of ASA IPs from txt file
#   The seed credentials paramter for funcation call are statically added instead of argvs.
#   If requried for OS scehduling purpose, feel free to modify main() for your use.

import os
from os import system
import os.path
import sys
import cisco_Backup_ASA

def main():
    system('cls')
    try:
        with open(os.path.join(os.getcwd(),'ASA_IP_List.txt')) as ip_List_File:
            ip_List = ip_List_File.readlines()
            ip_List_File.close()
            for line in ip_List:
                print('Initiating backup attempt for Device IP: '+ line.strip('\n'))
                cisco_Backup_ASA.cisco_Backup_ASA(line.strip('\n'), 'username', 'password', 'secret')
    except Exception as error_message:
                    print('IP List File open failed')
                    print(error_message)
    return()

if __name__ == '__main__':
    main()