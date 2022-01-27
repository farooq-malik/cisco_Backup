# cisco_Backup

Script to automate Cisco appliances backup process

## cisco_Backup_ASA.py

Connect via SSH to save and get running_config of both single and multiconext Cisco ASA appliances.
</br>
Output --> (Time)(IP).txt file in same working directory.
</br>
#### CLI Arguments List:</br>
*    -h --help --> Help
*    -i --host --> IPAddress
*    -u --username --> UserName
*    -p --password --> Password
*    -s --secret --> EnableSecret</br>
#### Function Call Arguments --> IP, User, Password, Enable_Secret
*    Output --> File_Name.txt    || Please refer to str 'filename'
*    ASA Maximum config file size : 2MB (Tested)

Note: Only developed and tested in windows platform.
