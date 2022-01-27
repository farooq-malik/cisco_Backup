#   File: "cisco_Backup_ASA.py"
#   Please refer to str 'help'

import getpass
import os
import os.path
from os import system
import sys, getopt
import time
import paramiko 
from paramiko_expect import SSHClientInteraction

help = '''
Connect via SSH to save and get running_config of both single and multiconext Cisco ASA appliances.
Output --> (Time)(IP).txt file in same working directory.
Arguments List:
    -h --help --> Help
    -i --host --> IPAddress
    -u --username --> UserName
    -p --password --> Password
    -s --secret --> EnableSecret
'''

def cisco_Backup_ASA(device_ip, device_username, device_password, device_enable):
    '''
    Writes running_config of both single and multiconext Cisco ASA appliances.
    Arguments --> IP, User, Password, Enable_Secret.
    Output --> File_Name.txt    || Please refer to str 'filename'
    ASA Maximum config file size : 2MB (Tested)
    '''
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()     # Loading SSH host keys
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())       # Add SSH host key automatically
    prompt_P1 = '.*>\s+'        # Define Prompt for privilege 1
    prompt_P15 = '.*#\s+'       # Define Prompt for privilege 15
    print('-'*96)
    try:
        print('Connection attempt for IP: ' + device_ip)
        ssh.connect(device_ip, 22, device_username, device_password)
        with SSHClientInteraction(ssh, timeout=2,display=False) as interact:
            #invoke sub session for multiple command executions
            # Login and Enable Privilege
            try:
                interact.expect(prompt_P1,timeout=2)
                interact.send('enable')
                interact.expect('.*:\s+',timeout=2)
                interact.send(device_enable)
                interact.expect(prompt_P15,timeout=2)
            except Exception():
                print('Login prompt may not be as expected. \n')
            # Identify ASA Mode
            interact.send('show mode')
            interact.expect(prompt_P15,timeout=2)
            string_output = interact.current_output_clean.split()
            if ((string_output[-1].split()[-1]) == 'single'):   # Single Mode ASA
                print('Security context mode: single\n')
                cli_commands = [
                    'terminal pager 0',
                    'write memory',
                    'show run | e #',
                ]
                string_output = [' ']
                for command in cli_commands:
                    interact.send(command)
                    if 'write' in command: print('Writing running configuration before backup.\n')
                    interact.expect(prompt_P15,timeout=15)
                    if 'write' in command: print('Running configuration saved.\n')
                    for line in interact.current_output_clean.splitlines(): string_output += [line]
            elif ((string_output[-1].split()[-1]) == 'multiple'):   # Multi Mode ASA
                cli_commands = [
                    'terminal pager 0',
                    'changeto system',
                    'write memory all /noconfirm',
                    'show run | e #',
                ]
                string_output = [' ']
                for command in cli_commands:
                    interact.send(command)
                    if 'write' in command: print('Writing Device Configurations before backup.')
                    interact.expect(prompt_P15,timeout=30)
                    if 'write' in command: print('Running configuration saved.')
                    for line in interact.current_output_clean.splitlines(): string_output += [line]
                context_output = []
                context_names = []
                interact.send('show context')
                interact.expect(prompt_P15,timeout=5)
                for line in interact.current_output_clean.splitlines(): context_output += [line]
                for counter in range(len(context_output)):      # Identify context Names and remove '*' within Admin context
                    if 'disk' in context_output[counter]:
                        context_output[counter] = context_output[counter].replace('*', ' ')
                        context_names.append(context_output[counter].split()[0])
                print('Security context mode: multiple')
                print('{:18}{:20}'.format('Total Contexts:',str(len(context_names))))
                for context in range(len(context_names)):       # Execute 'show run' command in each context
                    print('{:18}{:30}'.format('Reading Context:',context_names[context]))
                    context_command = [
                        'changeto context ' + context_names[context],
                        'show run | e #'
                    ]
                    for command in context_command:
                        interact.send(command)
                        interact.expect(prompt_P15,timeout=15)
                        for line in interact.current_output_clean.splitlines(): string_output += [line]
            else: 
                print('ASA Mode identification issue. Exiting')
                return()
            
            # File Save in pwd+subFolder '\BACKUP_CFGs'
            if string_output != None:    
                try:
                    os.mkdir('BACKUP_CFGs/')
                    open(os.path.join(os.getcwd(),'ASA_IP_List.txt'))
                    print('Created new Directory',os.getcwd(),'\'BACKUP_CFGs\'')
                except FileExistsError:
                    print('Using existing directory', os.getcwd(),'\'BACKUP_CFGs\'')
                try:
                    time_stamp = time.strftime('%Y.%m.%d--%H.%M.%S')
                    filename = 'BACKUP_CFGs\\' + time_stamp + '--' + device_ip + '.txt'
                    with open(filename, 'w') as file_handler:
                        for line in string_output:  file_handler.write(line+'\n')
                        file_handler.flush()
                except Exception as error_message:
                    print('File save failed')
                    print(error_message)
                finally:
                    file_handler.close()
            else:
                print('No output taken from IP' + device_ip)
    except Exception as error_message:
        print('Connection failed for device IP: ' + device_ip)
        print(error_message)
        return()
    else:
        ssh.close()   
    print('Backup process completed for Device: '+device_ip)
    print('-'*96)
    return()

def main(arguments):
    device_ip = ''
    device_username = ''
    device_password = ''
    device_enable = ''
    options = 'hi:u:p:s:'
    long_options = ['help','host =','username =','password =','secret =',]
    system('cls')
    print('-'*96)
    try:
        arguments, values = getopt.getopt(arguments, options, long_options)
        for option, value in arguments:
            if option in ('-h', '--help'):
                print(help, '\n','-'*96)
                sys.exit(2)
            elif option in ('-i', '--ip'):  device_ip = value
            elif option in ('-u', '--username'):  device_username = value
            elif option in ('-p', '--password'):  device_password= value
            elif option in ('-s', '--secret'):  device_enable = value
    except getopt.GetoptError as error:
        print('Failed to grab input arguments. Program will Exit now... ')
        print(str(error))
        sys.exit(2)
    cisco_Backup_ASA(device_ip, device_username, device_password, device_enable)
    print('Exiting main \n','-'*96)

if __name__ == '__main__':
    main(sys.argv[1:])