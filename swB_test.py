from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

switch = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.244.128",
    "username": "",
    "password": "",
    "secret": "",
    "port": 5006,
    "fast_cli": False,
    "global_delay_factor": 2,
    "read_timeout_override": 60,
}

testing_commands = [
    "show mac address-table",
    "ping 172.25.37.1",
    "ping 172.25.47.1",
]

connection = None

try:
    connection = ConnectHandler(**switch)

    print("Connected to SWB successfully.")

    if not connection.check_enable_mode():
        connection.enable()

    for command in testing_commands:
        print(f"\n--- Testing: {command} ---")

        output = connection.send_command(
            command,
            read_timeout=30,
            cmd_verify=False
        )

        print(output)

    print("\nSWB network testing completed.")

except NetmikoTimeoutException:
    print(
        "Connection timed out. Check the GNS3 VM IP address, "
        "SWB TELNET console port, GNS3 VM, and switch state."
    )

except NetmikoAuthenticationException:
    print(
        "Authentication failed. Check the username, password, "
        "and enable password."
    )

except Exception as error:
    print(f"Unexpected error: {error}")

finally:
    if connection is not None:
        connection.disconnect()