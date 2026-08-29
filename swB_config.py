from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

switch = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.244.128",
    "port": 5006,

    "username": "",
    "password": "",
    "secret": "",

    "fast_cli": False,
    "global_delay_factor": 4,
    "read_timeout_override": 120,
}

commands = [
    "hostname swB",

    "vlan 37",
    "name Orders",
    "exit",

    "vlan 47",
    "name Warehouse",
    "exit",

    "interface range gigabitEthernet0/1 - 3",
    "switchport mode access",
    "switchport access vlan 37",
    "spanning-tree portfast",
    "no shutdown",
    "exit",

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
    "ip address 172.25.37.2 255.255.255.0",
    "no shutdown",
    "exit",

    "ip default-gateway 172.25.37.1",

    "line console 0",
    "no login",
    "exec-timeout 0 0",
    "exit",

    "line vty 0 4",
    "no login",
    "transport input telnet",
    "exec-timeout 0 0",
    "exit",
]

connection = None

try:
    print("Connecting to SWB...")
    connection = ConnectHandler(**switch)
    print("Connected to SWB successfully.")

    print("Current prompt:")
    print(connection.find_prompt())

    if not connection.check_enable_mode():
        connection.enable()

    print("Privileged EXEC mode ready.")
    print("Prompt:", connection.find_prompt())

    print("\nSending SWB configuration...")

    output = connection.send_config_set(
        commands,
        cmd_verify=False,
        read_timeout=120,
        exit_config_mode=False,
    )

    end_output = connection.send_command_timing(
        "end",
        read_timeout=60,
    )
    output += end_output

    print("\n================ CONFIGURATION OUTPUT ================\n")
    print(output)
    print("\n=======================================================\n")

    print("Saving configuration...")
    save_output = connection.send_command_timing(
        "write memory",
        read_timeout=60,
    )
    print(save_output)

    print("SWB CONFIGURATION COMPLETED SUCCESSFULLY")
    
except NetmikoTimeoutException:
    print("\nERROR: Connection timed out.")
    print(
        "Check:\n"
        "1. GNS3 is running\n"
        "2. SWB is started\n"
        "3. GNS3 server IP is 192.168.244.128\n"
        "4. SWB console port is 5006"
    )

except NetmikoAuthenticationException:
    print("\nERROR: Authentication failed.")
    print(
        "SWB is requesting a username/password on the Telnet "
        "console. Configure the console without login first."
    )

except Exception as error:
    print("\nUNEXPECTED ERROR:")
    print(error)

finally:
    if connection is not None:
        connection.disconnect()
        print("\nTELNET connection closed.")