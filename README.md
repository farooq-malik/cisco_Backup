# cisco_Backup
Script to automate Cisco appliances backup process and related generic operations.
## File: cisco_Backup_ASA.py
Connect via SSH to save and get running_config of both single and multiconext Cisco ASA appliances. </br>
Output --> (Time)(IP).txt file in same working directory. </br>
#### CLI Arguments List:</br>
*    -h --help --> Help
*    -i --host --> IPAddress
*    -u --username --> UserName
*    -p --password --> Password
*    -s --secret --> EnableSecret</br>
#### Function Call Arguments --> IP, User, Password, Enable_Secret
*    Output --> File_Name.txt    || Please refer to str 'filename'
*    ASA Maximum config file size : 2MB-Tested, please check for possible truncations applied by IDE/environment. </br>
*    Developed and tested in windows platform only.

## File: cdp_Crawl.py
Connect via SSH to grab CDP neighbor information from Cisco IOS appliances.</br>
Output --> JSON</br>
#### CLI Arguments List:</br>
*    -h --help --> Help
*    -i --host --> IPAddress
*    -u --username --> UserName
*    -p --password --> Password
#### Function Call Arguments --> IP, User, Password
*    Output --> JSON
*    Developed and tested in windows platform only.

## File: primeGetInventory.py
Calls Cisco Prime API to get device list</br>
Output --> JSON file 'prime_devices.txt' file in source directory</br>
#### CLI Arguments List:</br>
*    -h --help --> Help
*    -i --host --> IPAddress
*    -u --username --> UserName
*    -p --password --> Password
#### Function Call Arguments --> IP, User, Password
*    Output --> JSON Filef'prime_devices.txt' file in source directory
*    Developed and tested in windows platform only.
