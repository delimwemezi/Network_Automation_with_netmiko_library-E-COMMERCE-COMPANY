from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# SWA - GNS3 TELNET CONNECTION

switch = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.244.128",
    "port": 5004,

    # No username/password
    "username": "",
    "password": "",
    "secret": "",

    "fast_cli": False,
    "global_delay_factor": 2,
    "read_timeout_override": 60,
}

# SWA CONFIGURATION COMMANDS
commands = [
    "hostname swA",

    # VLAN 37 - ORDERS
    "vlan 37",
    "name Orders",
    "exit",

    # VLAN 47 - WAREHOUSE
    "vlan 47",
    "name Warehouse",
    "exit",

    # PC1, PC2, PC3 - ORDERS VLAN
    "interface range gigabitEthernet0/1 - 3",
    "switchport mode access",
    "switchport access vlan 37",
    "spanning-tree portfast",
    "no shutdown",
    "exit",

    # PC4, PC5, PC6 - WAREHOUSE VLAN
    "interface range gigabitEthernet1/0 - 2",
    "switchport mode access",
    "switchport access vlan 47",
    "spanning-tree portfast",
    "no shutdown",
    "exit",

    "interface gigabitEthernet0/0",
    "switchport mode trunk",
    "switchport trunk allowed vlan 37,47",
    "no shutdown",
    "exit",
 
    "interface vlan 37",
    "ip address 172.24.37.2 255.255.255.0",
    "no shutdown",
    "exit",

    "ip default-gateway 172.24.37.1",

    # CONSOLE - NO LOGIN
    
    "line console 0",
    "no login",
    "exec-timeout 0 0",
    "exit",

    # TELNET - NO LOGIN
    
    "line vty 0 4",
    "no login",
    "transport input telnet",
    "exec-timeout 0 0",
    "exit",
]


connection = None

try:

    # CONNECT
    
    print("Connecting to SWA...")

    connection = ConnectHandler(**switch)

    print("Connected to SWA successfully.")

    # CHECK CURRENT PROMPT
    
    print("Current prompt:")
    print(connection.find_prompt())

    # ENTER PRIVILEGED EXEC MODE
    
    if not connection.check_enable_mode():

        print("Entering privileged EXEC mode...")

        connection.enable()

    print("Privileged EXEC mode ready.")
    print("Prompt:", connection.find_prompt())

    # ENTER CONFIGURATION MODE
   
    print("Testing configuration mode...")

    connection.config_mode()

    print("Configuration mode entered successfully.")

    # Leave configuration mode again.
    # send_config_set() will enter it automatically.
    connection.exit_config_mode()

    # SEND CONFIGURATION
   
    print("\nSending SWA configuration...")

    output = connection.send_config_set(
        commands,
        cmd_verify=False,
        read_timeout=60,
        exit_config_mode=True,
    )

    print("\n================ CONFIGURATION OUTPUT ================\n")
    print(output)
    print("\n=======================================================\n")

    # SAVE CONFIGURATION
   
    print("Saving configuration...")

    save_output = connection.send_command_timing(
        "write memory",
        read_timeout=60,
    )

    print(save_output)

    print("SWA CONFIGURATION COMPLETED SUCCESSFULLY")
    
except NetmikoTimeoutException:
    print("\nERROR: Connection timed out.")
    print(
        "Check:\n"
        "1. GNS3 is running\n"
        "2. SWA is started\n"
        "3. GNS3 server IP is 192.168.244.128\n"
        "4. SWA console port is 5004"
    )


except NetmikoAuthenticationException:
    print("\nERROR: Authentication failed.")
    print(
        "SWA is requesting a username/password on the Telnet "
        "console. Configure the console without login first."
    )


except Exception as error:
    print("\nUNEXPECTED ERROR:")
    print(error)


finally:

    if connection is not None:
        connection.disconnect()
        print("\nTELNET connection closed.")