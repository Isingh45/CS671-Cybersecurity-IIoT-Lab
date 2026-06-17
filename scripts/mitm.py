from scapy.all import *

iface = "s1-eth1"

sensor_ip = "10.0.0.1"
gateway_ip = "10.0.0.2"

pkt = Ether()/IP(src=sensor_ip, dst=gateway_ip)/TCP(dport=502)/Raw(load="ATTACK")

sendp(pkt, iface=iface, count=1000, verbose=True)
