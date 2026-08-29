from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# Start RB in GNS3 before running this script.
# Enter the connection details for R1.
# Use the current GNS3 VM/server IP address and R1 TELNET console port.
router = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.244.128",
    "username": "",
    "password": "",
    "secret": "",
    "port": 5002,
}


# Enter the Cisco IOS commands required to configure R1
# according to the current network topology.
# rB_config.py
commands = [

    "hostname rB",

    # WAN link to rA
    "interface gigabitEthernet0/0",
    "ip address 10.21.21.2 255.255.255.252",
    "no shutdown",
    "exit",

    # Site B VLAN 37 — Orders
    "interface gigabitEthernet0/1.37",
    "encapsulation dot1Q 37",
    "ip address 172.25.37.1 255.255.255.0",
    "no shutdown",
    "exit",

    # Site B VLAN 47 — Warehouse
    "interface gigabitEthernet0/1.47",
    "encapsulation dot1Q 47",
    "ip address 172.25.47.1 255.255.255.0",
    "no shutdown",
    "exit",

    # Enable the physical trunk interface
    "interface gigabitEthernet0/1",
    "no shutdown",
    "exit",

    # Routes to Site A
    "ip route 172.24.37.0 255.255.255.0 10.21.21.1",
    "ip route 172.24.47.0 255.255.255.0 10.21.21.1",

    # Add this block here
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
    # Connect to RA through the GNS3 TELNET console.
    connection = ConnectHandler(**router)

    # Enter privileged EXEC mode if an enable password is configured.
    if router["secret"]:
        connection.enable()

    # Send the configuration commands to R1.
    output = connection.send_config_set(commands,
    cmd_verify=False,
    read_timeout=60,)
    print(output)

    # Save the configuration.
    connection.save_config()

    print("\nRB configuration completed successfully.")


except NetmikoTimeoutException:
    print(
        "Connection timed out. Check the GNS3 VM IP address, "
        "RB TELNET console port, GNS3 VM, and router state."
    )


except NetmikoAuthenticationException:
    print(
        "Authentication failed. Check the username, password, "
        "and enable password."
    )


except Exception as error:
    print(f"Unexpected error: {error}")


finally:
    # Close the TELNET session if a connection was opened.
    if connection is not None:
        connection.disconnect()