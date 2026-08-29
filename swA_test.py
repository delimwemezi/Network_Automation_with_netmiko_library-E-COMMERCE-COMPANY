from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# SWA GNS3 TELNET CONNECTION
switch = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.244.128",
    "username": "",
    "password": "",
    "secret": "",
    "port": 5004,

    "fast_cli": False,
    "global_delay_factor": 2,
    "read_timeout_override": 60,

    "session_log": "swa_session.log",
}

# SWA TESTING COMMANDS
testing_commands = [
    "ping 172.24.37.1",
    "ping 172.24.47.1",
    "ping 172.25.37.1",
    "show mac address-table dynamic",
]


connection = None

try:
    # CONNECT TO SWA
    print("Connecting to SWA...")

    connection = ConnectHandler(**switch)

    print("Connected to SWA successfully.")

    # ENTER PRIVILEGED EXEC MODE
   
    if not connection.check_enable_mode():
        connection.enable()

    print("Privileged EXEC mode ready.")
    print("Prompt:", connection.find_prompt())

    # RUN TESTS

    for command in testing_commands:

        print(f"\n--- Testing: {command} ---")

        output = connection.send_command(
            command,
            read_timeout=30,
            cmd_verify=False
        )

        print(output)

    print("\n======================================")
    print("SWA NETWORK TESTING COMPLETED")
    print("======================================")


except NetmikoTimeoutException:
    print(
        "\nERROR: Connection timed out.\n"
        "Check the GNS3 VM IP address, SWA TELNET console port "
        "5004, GNS3 server, and SWA state."
    )


except NetmikoAuthenticationException:
    print(
        "\nERROR: Authentication failed.\n"
        "Check whether SWA requires a username or password."
    )


except Exception as error:
    print(f"\nUnexpected error: {error}")


finally:

    if connection is not None:
        connection.disconnect()
        print("\nTELNET connection closed.")