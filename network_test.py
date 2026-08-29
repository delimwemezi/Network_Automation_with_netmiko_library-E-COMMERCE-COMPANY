from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

devices = [
    {
        "name": "rA",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.244.128",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5000,
        "fast_cli": False,
        "global_delay_factor": 3,
        "read_timeout_override": 120,
    },
    {
        "name": "rB",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.244.128",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5002,
        "fast_cli": False,
        "global_delay_factor": 3,
        "read_timeout_override": 120,
    },
    {
        "name": "SWA",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.244.128",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5004,
        "fast_cli": False,
        "global_delay_factor": 3,
        "read_timeout_override": 120,
    },
    {
        "name": "SWB",
        "device_type": "cisco_ios_telnet",
        "host": "192.168.244.128",
        "username": "",
        "password": "",
        "secret": "",
        "port": 5006,
        "fast_cli": False,
        "global_delay_factor": 3,
        "read_timeout_override": 120,
    },
]

testing_commands = {
    "rA": [
        "ping 172.24.37.1",
        "ping 172.24.47.1",
        "ping 172.24.37.2",
        "ping 172.25.37.2",
    ],

    "rB": [
        "ping 172.25.37.1",
        "ping 172.25.47.1",
        "ping 172.25.37.2",
        "ping 172.24.37.2",
    ],

    "SWA": [
        "ping 172.24.37.1",
        "ping 172.24.47.1",
        "ping 172.24.37.2",
        "ping 172.25.37.2",
    ],

    "SWB": [
        "ping 172.25.37.1",
        "ping 172.25.47.1",
        "ping 172.25.37.2",
        "ping 172.24.37.2",
    ],
}

for device in devices:

    connection = None
    device_name = device["name"]

    connection_details = {
        key: value
        for key, value in device.items()
        if key != "name"
    }

    try:
        print(f"\nConnecting to {device_name}...")

        connection = ConnectHandler(**connection_details)

        print(f"Connected to {device_name} successfully.")

        if not connection.check_enable_mode():
            connection.enable()

        for command in testing_commands[device_name]:

            print(f"\n--- {device_name}: {command} ---")

            output = connection.send_command(
                command,
                cmd_verify=False,
                read_timeout=60
            )

            print(output)

        print(f"\n{device_name} testing completed.")

    except NetmikoTimeoutException:
        print(
            f"{device_name}: Connection timed out. "
            "Check GNS3, Telnet port, and device state."
        )

    except NetmikoAuthenticationException:
        print(
            f"{device_name}: Authentication failed. "
            "Check username, password, and enable password."
        )

    except Exception as error:
        print(f"{device_name}: Unexpected error: {error}")

    finally:
        if connection is not None:
            connection.disconnect()

print("\nNetwork testing completed.")