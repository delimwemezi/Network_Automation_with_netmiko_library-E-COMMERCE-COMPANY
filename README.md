# Network Automation Usage Examples

This folder contains reusable Python templates and completed usage examples for configuring, verifying, and testing network devices using Netmiko.

## 0. Project Topology — E-Commerce Fulfilment Centre

This set of templates and usage examples is applied to a GNS3 lab simulating
an e-commerce company that operates **two fulfilment centres**. At each
centre, order-processing computers and warehouse terminals are kept on
**separate VLANs**.

| Site | Switch | Router | PCs |
|------|--------|--------|-----|
| Fulfilment Centre A | swA | rA | PC1–PC6 |
| Fulfilment Centre B | swB | rB | PC7–PC12 |

**WAN link:** `rA Gi0/1` ↔ `rB Gi0/0` — the only connection between the two
fulfilment centres.

### VLAN Design

| VLAN ID | Name              | Centre A ports (swA) | Centre A hosts | Centre B ports (swB) | Centre B hosts |
|---------|-------------------|-----------------------|-----------------|-----------------------|-----------------|
| 10      | ORDER_PROCESSING  | Gi0/1, Gi0/2, Gi0/3   | PC1, PC2, PC3   | Gi0/1, Gi0/2, Gi0/3   | PC7, PC8, PC9   |
| 20      | WAREHOUSE         | Gi1/0, Gi1/1, Gi1/2   | PC4, PC5, PC6   | Gi1/0, Gi1/1, Gi1/2   | PC10, PC11, PC12|

Trunk ports:
- `swA Gi0/0` → `rA Gi0/0` (trunk, carries VLAN 10 + 20)
- `swB Gi0/0` → `rB Gi0/1` (trunk, carries VLAN 10 + 20)

> Adjust VLAN IDs/names/port mappings above if your actual `swA`/`swB`
> configs differ.

### IP Addressing Scheme

Router-on-a-stick sub-interfaces provide inter-VLAN routing at each centre;
the two centres are joined by a routed WAN link.

| Segment | Network | Gateway |
|---|---|---|
| Centre A – VLAN 10 (Order Processing) | 192.168.10.0/24 | rA Gi0/0.10 → 192.168.10.1 |
| Centre A – VLAN 20 (Warehouse) | 192.168.20.0/24 | rA Gi0/0.20 → 192.168.20.1 |
| Centre B – VLAN 10 (Order Processing) | 192.168.30.0/24 | rB Gi0/1.10 → 192.168.30.1 |
| Centre B – VLAN 20 (Warehouse) | 192.168.40.0/24 | rB Gi0/1.20 → 192.168.40.1 |
| WAN link (rA – rB) | 10.0.0.0/30 | rA: 10.0.0.1, rB: 10.0.0.2 |

Routing between centres is handled via **static routes** on rA and rB
pointing across the WAN link (or replace with a dynamic protocol if used).

> Replace these subnets with your actual addressing if it differs — this
> scheme is inferred from the topology diagram, not from a live config dump.

### GNS3 Lab Access (Telnet Console)

All nodes run on GNS3 VM at `192.168.244.128`.

| Node | Role | Telnet |
|------|------|--------|
| rA | Router — Centre A | `telnet 192.168.244.128 5000` |
| rB | Router — Centre B | `telnet 192.168.244.128 5002` |
| swA | Switch — Centre A | `telnet 192.168.244.128 5004` |
| swB | Switch — Centre B | `telnet 192.168.244.128 5006` |
| PC1–PC6 | Centre A hosts | ports 5008–5018 |
| PC7–PC12 | Centre B hosts | ports 5020–5030 |

### Mapping Topology Devices to the Generic Naming Convention

The templates and usage-example naming pattern described below (`r1`, `r2`,
`sw1`, `sw2`, ...) is generic. For this specific fulfilment-centre topology,
the generic names map to the actual GNS3 node names as follows:

| Generic template name | Actual device in this topology |
|---|---|
| `r1` | `rA` (Fulfilment Centre A router) |
| `r2` | `rB` (Fulfilment Centre B router) |
| `sw1` | `swA` (Fulfilment Centre A switch) |
| `sw2` | `swB` (Fulfilment Centre B switch) |

So for this project, the device-level scripts are named:

```text
rA_config.py
rA_verify.py
rA_test.py

rB_config.py
rB_verify.py
rB_test.py

swA_config.py
swA_verify.py
swA_test.py

swB_config.py
swB_verify.py
swB_test.py
```

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

For this fulfilment-centre topology, `network_verify.py` and `network_test.py`
should confirm:

- VLAN 10 (Order Processing) hosts at Centre A can reach VLAN 10 hosts at
  Centre B (PC1–3 ↔ PC7–9).
- VLAN 20 (Warehouse) hosts at Centre A can reach VLAN 20 hosts at Centre B
  (PC4–6 ↔ PC10–12).
- VLAN 10 and VLAN 20 remain isolated from each other unless inter-VLAN
  access is explicitly configured.
- The WAN link between rA and rB is up and routes are correctly exchanged.

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

## 7. Folder Structure for This Project (Fulfilment Centre Topology)

Applying the generic structure above to the actual fulfilment-centre
topology (rA, rB, swA, swB), the project's `Usage_Examples` folder looks
like this:

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
    ├── rA_config.py
    ├── rA_verify.py
    ├── rA_test.py
    ├── rB_config.py
    ├── rB_verify.py
    ├── rB_test.py
    ├── swA_config.py
    ├── swA_verify.py
    ├── swA_test.py
    ├── swB_config.py
    ├── swB_verify.py
    ├── swB_test.py
    ├── network_verify.py
    └── network_test.py
```

- `rA_config.py` / `rB_config.py` — configure sub-interfaces, VLAN
  routing, and static routes across the WAN link on each router.
- `swA_config.py` / `swB_config.py` — create VLAN 10 (Order Processing)
  and VLAN 20 (Warehouse), and assign access/trunk ports as described in
  Section 0.
- `network_verify.py` / `network_test.py` — confirm VLAN isolation and
  end-to-end reachability between the two fulfilment centres as described
  in Section 3.
