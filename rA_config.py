from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# Start R1 in GNS3 before running this script.
# Enter the connection details for R1.
# Use the current GNS3 VM/server IP address and R1 TELNET console port.
router = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.244.128",
    "username": "",
    "password": "",
    "secret": "",
    "port": 5000,
}


# Enter the Cisco IOS commands required to configure R1
# according to the current network topology.
# rA_config.py
commands = [
    "hostname rA",

    # WAN link to rB
    "interface gigabitEthernet0/1",
    "ip address 10.21.21.1 255.255.255.252",
    "no shutdown",
    "exit",

    # Site A VLAN 37 — Orders
    "interface gigabitEthernet0/0.37",
    "encapsulation dot1Q 37",
    "ip address 172.24.37.1 255.255.255.0",
    "no shutdown",
    "exit",

    # Site A VLAN 47 — Warehouse
    "interface gigabitEthernet0/0.47",
    "encapsulation dot1Q 47",
    "ip address 172.24.47.1 255.255.255.0",
    "no shutdown",
    "exit",

    # Enable the physical trunk interface
    "interface gigabitEthernet0/0",
    "no shutdown",
    "exit",

    # Routes to Site B
    "ip route 172.25.37.0 255.255.255.0 10.21.21.2",
    "ip route 172.25.47.0 255.255.255.0 10.21.21.2",

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
    # Connect to R1 through the GNS3 TELNET console.
    connection = ConnectHandler(**router)

    # Enter privileged EXEC mode if an enable password is configured.
    if router["secret"]:
        connection.enable()

    # Send the configuration commands to R1.
    output = connection.send_config_set(commands)
    print(output)

    # Save the configuration.
    connection.save_config()

    print("\nRA configuration completed successfully.")


except NetmikoTimeoutException:
    print(
        "Connection timed out. Check the GNS3 VM IP address, "
        "RA TELNET console port, GNS3 VM, and router state."
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