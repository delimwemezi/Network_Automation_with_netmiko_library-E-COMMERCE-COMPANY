# Network Automation Usage Examples

This folder contains reusable Python templates and completed usage examples for configuring, verifying, and testing network devices using Netmiko.

## 1. Templates

The `Templates` folder contains reusable scripts that students can copy and adapt to different devices and network topologies.

```text
Templates/
├── router_config_template.py
├── router_verify_template.py
├── router_test_template.py
├── switch_config_template.py
├── switch_verify_template.py
├── switch_test_template.py
├── network_verify_template.py
└── network_test_template.py
```

A template provides the common Python structure, including:

- Netmiko connection setup;
- GNS3 VM/server IP address and TELNET console port placeholders;
- configuration, verification, or testing command placeholders;
- exception handling; and
- safe disconnection from the device.

Students should copy the appropriate template, rename it for the target device, and replace the placeholders with values from the current GNS3 topology.

For example:

```text
router_config_template.py  →  r1_config.py
router_config_template.py  →  r2_config.py

switch_config_template.py  →  sw1_config.py
switch_config_template.py  →  sw2_config.py
```

## 2. Device-Level Usage Examples

For Router R1:

```text
r1_config.py
r1_verify.py
r1_test.py
```

For Switch SW1:

```text
sw1_config.py
sw1_verify.py
sw1_test.py
```

The same naming pattern can be extended to additional devices.

For example:

```text
r2_config.py
r2_verify.py
r2_test.py

sw2_config.py
sw2_verify.py
sw2_test.py
```

Each device is therefore configured, verified, and tested independently before the complete network is examined.

## 3. Network-Level Scripts

At the network level, there is normally no separate configuration script because configuration is performed on the individual devices.

```text
network_verify.py
network_test.py
```

`network_verify.py` collects and checks information from multiple devices to confirm that the integrated network is operating as intended.

`network_test.py` performs end-to-end network tests such as connectivity and path testing between devices or networks.

## 4. Recommended Workflow

Use the scripts in the following order:

```text
Configure individual devices
        ↓
Verify individual devices
        ↓
Test individual devices
        ↓
Verify the integrated network
        ↓
Test end-to-end network operation
```

This sequence ensures that problems can first be isolated at the device level before troubleshooting the integrated network.

## 5. Adding Other Device Types

The same structure can be extended beyond the sample Cisco routers and switches.

### Additional Routers and Switches

Copy the appropriate template and rename the script using the device name.

```text
r3_config.py
r3_verify.py
r3_test.py

sw3_config.py
sw3_verify.py
sw3_test.py
```

Update the GNS3 VM/server IP address, TELNET console port, credentials, and device-specific commands to match the current topology.

### Docker Containers

Docker containers can also be included in the network automation workflow. Their scripts may be named according to the container role.

```text
server1_verify.py
server1_test.py

web1_verify.py
web1_test.py
```

A container may not require a Netmiko router or switch template. The Python method used should match the service provided by the container, such as SSH, a shell command, or an application-specific interface.

### Firewalls

Firewall scripts can follow the same device-level naming pattern.

```text
fw1_config.py
fw1_verify.py
fw1_test.py
```

The connection parameters and commands must be adapted to the firewall platform.

### Devices from Different Vendors

Netmiko supports many network operating systems. When adding a different vendor, copy the closest template and change the `device_type`, connection details, and commands to match that device.

For example, the structure can be extended as follows:

```text
cisco_r1_config.py
juniper_r1_config.py
arista_sw1_config.py
fortinet_fw1_config.py
```

The exact `device_type` value must correspond to a device type supported by the installed Netmiko version.

Do not assume that Cisco IOS commands will work on another vendor. Configuration, verification, and testing commands must be written for the operating system of the target device.

## 6. Suggested Folder Structure

```text
Network_Automation/
│
├── Templates/
│   ├── router_config_template.py
│   ├── router_verify_template.py
│   ├── router_test_template.py
│   ├── switch_config_template.py
│   ├── switch_verify_template.py
│   ├── switch_test_template.py
│   ├── network_verify_template.py
│   └── network_test_template.py
│
└── Usage_Examples/
    ├── r1_config.py
    ├── r1_verify.py
    ├── r1_test.py
    ├── sw1_config.py
    ├── sw1_verify.py
    ├── sw1_test.py
    ├── network_verify.py
    └── network_test.py
```

Additional routers, switches, firewalls, containers, and devices from other vendors can be added to `Usage_Examples` using the same naming and workflow principles.
