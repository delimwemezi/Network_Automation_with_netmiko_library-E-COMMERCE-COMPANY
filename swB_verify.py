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
    "global_delay_factor": 3,
    "read_timeout_override": 120,
    "session_log": "swb_session.log",
}

verification_commands = [
    "show vlan brief",
    "show interfaces status",
    "show ip interface brief",
    "show interfaces trunk",
]

connection = None

try:
    connection = ConnectHandler(**switch)

    print("Connected to SWB successfully.")
    print("Prompt:", connection.find_prompt())

    if not connection.check_enable_mode():
        connection.enable()

    for command in verification_commands:
        print(f"\n--- {command} ---")

        output = connection.send_command(
            command,
            cmd_verify=False,
            read_timeout=60
        )

        print(output)

    print("\nSWB verification completed.")

except NetmikoTimeoutException:
    print("Connection timed out. Check GNS3 and Telnet port 5006.")

except NetmikoAuthenticationException:
    print("Authentication failed. Check the SWB console configuration.")

except Exception as error:
    print(f"Unexpected error: {error}")

finally:
    if connection is not None:
        connection.disconnect()
        print("TELNET connection closed.")