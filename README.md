# CS671 Cybersecurity IIoT Lab

## Overview

A virtual Industrial Internet of Things (IIoT) cybersecurity laboratory developed for **CS671 Cybersecurity** at **California State University, East Bay**.

The project demonstrates a virtual Industrial Control System (ICS) environment using Containernet, Docker, Modbus/TCP, Python, Scapy, and Wireshark. The laboratory simulates industrial communications, cybersecurity attacks, packet capture, and intrusion detection techniques commonly used in Operational Technology (OT) environments.

The platform provides a reproducible software-defined testbed for studying industrial network security without requiring physical PLC hardware.

---

## Technologies

* Python
* Containernet
* Docker
* Open vSwitch (OVS)
* Modbus/TCP
* Scapy
* Wireshark

---

## Architecture

```text
Sensor (Modbus Client: 10.0.0.1)
            │
            ▼
      Open vSwitch (s1)
       /            \
      ▼              ▼
Gateway/PLC      Attacker
(Modbus Server)   (10.0.0.3)
10.0.0.2
```

---

## Features

* **Automated IIoT Network Deployment:** Deploys a virtual industrial network using Containernet, Docker containers, and Open vSwitch to create an isolated software-defined environment.

* **Industrial Protocol Simulation:** Simulates Modbus/TCP communication between a sensor (client) and gateway (server) to emulate industrial control system traffic.

* **Attack Traffic Simulation:** Uses Scapy to generate abnormal Modbus/TCP network traffic for cybersecurity testing and intrusion detection experiments.

* **Multi-Layer Intrusion Detection System (IDS):** Detects suspicious traffic using payload signature inspection, packet-size heuristics, and repeated traffic-pattern analysis.

* **Packet Capture and Analysis:** Captures normal and attack traffic using tcpdump and analyzes network behavior with Wireshark.

---

## Repository Structure

* **scripts/**

  * `iiot_setup.py` — Deploys the virtual IIoT topology and configures the network.
  * `IDS.py` — Multi-layer intrusion detection system.
  * `mitm.py` — Scapy-based attack traffic generation script.

* **pcaps/**

  * `iiot_baseline.pcapng` — Baseline industrial network traffic capture.
  * `attack_big.pcap` — Packet capture generated during attack simulation.

* **reports/**

  * `CS671_Project_Proposal.pdf` — Project proposal.
  * `CS671_IIoT_Virtual_Lab_Report.pdf` — Final project report.

* **presentation/**

  * `Secure_IIoT_Virtual_Lab_Development.pptx` — Final presentation.

---

## How to Run

### Prerequisites

Install the following on Ubuntu Linux (WSL2):

* Containernet
* Docker
* Open vSwitch
* Python 3

---

### Execution Steps

#### 1. Deploy the IIoT Network

```bash
sudo python3 scripts/iiot_setup.py
```

#### 2. Generate Attack Traffic

```bash
sudo python3 scripts/mitm.py
```

#### 3. Run the Intrusion Detection System

```bash
sudo python3 scripts/IDS.py
```

---

## What I Learned

* Building virtual Industrial Control System (ICS) environments using Containernet and Docker.
* Simulating Modbus/TCP communications within software-defined industrial networks.
* Generating and analyzing cybersecurity attack traffic using Scapy and Wireshark.
* Designing intrusion detection techniques using payload inspection, packet metadata, and traffic-pattern analysis.
* Developing reproducible cybersecurity laboratories for industrial network security research.

---

## Future Improvements

* Support additional industrial communication protocols such as DNP3 and OPC UA.
* Expand the IDS using machine learning–based anomaly detection.
* Simulate larger multi-substation industrial network topologies.
* Add real-time dashboards for network monitoring and visualization.

---

## Institution

**California State University, East Bay**

**Course:** CS671 – Cybersecurity

---

## Collaborators

* Inderpal Singh
* Sukhpinder Singh
* Jesse
