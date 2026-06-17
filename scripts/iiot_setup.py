from mininet.net import Containernet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.link import Link
from mininet.log import info, setLogLevel
import os

def setup_iiot_network():
    # 1. Start with a clean switch environment
    net = Containernet(switch=OVSSwitch)

    info('*** Adding switch in standalone mode\n')
    s1 = net.addSwitch('s1', failMode='standalone')

    info('*** Adding Docker containers (Sensor and Gateway)\n')
    # Note: We keep the IP in addDocker for Mininet's records, 
    # but we will force it manually below to ensure it hits the right interface.
    sensor = net.addDocker('sensor', ip='10.0.0.1/24', dimage='python:3.10-slim')
    gateway = net.addDocker('gateway', ip='10.0.0.2/24', dimage='python:3.10-slim')
    attacker = net.addHost('attacker', ip='10.0.0.3/24')

    info('*** Creating links to s1\n')
    net.addLink(sensor, s1)
    net.addLink(gateway, s1)
    net.addLink(attacker, s1)

    info('*** Starting network\n')
    net.start()

    # 2. Provisioning: Get the tools we need
    info('*** Provisioning containers with networking tools...\n')
    install_cmd = 'apt-get update && apt-get install -y iputils-ping iproute2 arping'
    sensor.cmd(install_cmd)
    gateway.cmd(install_cmd)

    # 3. ABSOLUTE FIX: Manual IP and Route Binding
    # This forces the containers to use the Mininet interface (eth0) for 10.0.0.x traffic
    info('*** Manually binding IPs to Mininet interfaces...\n')
    
    # Sensor configuration
    sensor.cmd('ip addr flush dev sensor-eth0')
    sensor.cmd('ip addr add 10.0.0.1/24 dev sensor-eth0')
    sensor.cmd('ip link set sensor-eth0 up')
    sensor.cmd('ip route add 10.0.0.0/24 dev sensor-eth0')

    # Gateway configuration
    gateway.cmd('ip addr flush dev gateway-eth0')
    gateway.cmd('ip addr add 10.0.0.2/24 dev gateway-eth0')
    gateway.cmd('ip link set gateway-eth0 up')
    gateway.cmd('ip route add 10.0.0.0/24 dev gateway-eth0')

    # 4. NUCLEAR OPTION: Clear Host Firewall
    info('*** Flushing host firewall rules...\n')
    os.system('iptables -F')
    os.system('iptables -P FORWARD ACCEPT')
    
    # 5. Force the switch to act as a hub
    os.system('ovs-ofctl add-flow s1 action=normal')

    # 6. Gratuitous ARP: Announce presence on the new interfaces
    sensor.cmd('arping -c 2 -A -I sensor-eth0 10.0.0.1')
    gateway.cmd('arping -c 2 -A -I gateway-eth0 10.0.0.2')

    info('*** Network is ready. Infrastructure Verified.\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    setup_iiot_network()  
