from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# Start SW1 in GNS3 before running this script.
# Enter the GNS3 VM/server IP address and the TELNET
# console port assigned to SW1.
switch = {
    "device_type": "generic_termserver_telnet",
    "host": "192.168.244.128",
    "username": "",
    "password": "",
    "secret": "",
    "port": 5004,
    "fast_cli": False,
    "global_delay_factor": 3,
    "read_timeout_override": 120,
    "session_log": "swb_session.log",
}


# Enter the show commands required to verify SW1.
# swB_verify.py
verification_commands = [
    "show vlan brief",
    "show interfaces trunk",
    "show interfaces status",
    "show ip interface brief",
    "show mac address-table dynamic",
]


connection = None

try:
    # Connect to SW1 through its GNS3 TELNET console.
    connection = ConnectHandler(**switch)

    # Enter privileged EXEC mode if required.
    connection.enable()
    connection.send_command_timing("terminal length 0")

    # Run each verification command.
    for command in verification_commands:
        print(f"\n--- {command} ---")

        output = connection.send_command_timing(
            command,
            read_timeout=30,
            last_read=3,
        )

        print(output)

    print("\nSWA verification completed.")


except NetmikoTimeoutException:
    print(
        "Connection timed out. Check the GNS3 VM IP address, "
        "SWA TELNET console port, GNS3 VM, and switch state."
    )


except NetmikoAuthenticationException:
    print(
        "Authentication failed. Check the username, password, "
        "and enable password."
    )


except Exception as error:
    print(f"Unexpected error: {error}")


finally:
    # Close the TELNET session.
    if connection is not None:
        connection.disconnect()
