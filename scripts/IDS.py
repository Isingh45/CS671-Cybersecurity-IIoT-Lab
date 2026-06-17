import sys
from scapy.all import PcapReader, Raw

def analyze_pcap_combined(file_path):
    """
    Analyzes a PCAP file using a multi-layered IDS approach:
    1. Signature-based (Payload inspection)
    2. Metadata-based (Packet size anomalies)
    3. Pattern-based (Repetitive packet sequences)
    """
    print(f"[*] Analyzing {file_path}...")
    
    # --- IDS Rules & Thresholds ---
    SIGNATURE = b"ATTACK"
    SUSPICIOUS_LENGTH_THRESHOLD = 60
    CONSECUTIVE_THRESHOLD = 15
    
    # --- State & Counters ---
    packet_count = 0
    signature_alerts = 0
    size_alerts = 0
    pattern_alerts = 0
    
    previous_size = -1
    consecutive_identical_sizes = 0
    
    try:
        with PcapReader(file_path) as pcap_reader:
            for packet in pcap_reader:
                packet_count += 1
                current_size = len(packet)
                
                # ===================================================
                # LAYER 1: Deep Packet Inspection (Content/Signature)
                # ===================================================
                if packet.haslayer(Raw):
                    if SIGNATURE in packet[Raw].load:
                        signature_alerts += 1
                        
                # ===================================================
                # LAYER 2: Metadata Heuristics (Packet Size)
                # ===================================================
                if current_size <= SUSPICIOUS_LENGTH_THRESHOLD:
                    size_alerts += 1
                    
                # ===================================================
                # LAYER 3: Traffic Behavior (Pattern Recognition)
                # ===================================================
                if current_size == previous_size:
                    consecutive_identical_sizes += 1
                else:
                    consecutive_identical_sizes = 0
                    
                # We trigger an alert every time a sequence hits the threshold
                if consecutive_identical_sizes == CONSECUTIVE_THRESHOLD:
                    pattern_alerts += 1
                    
                previous_size = current_size
                
    except FileNotFoundError:
        print(f"[-] Error: The file {file_path} was not found.")
        return
    except Exception as e:
        print(f"[-] An error occurred while parsing the file: {e}")
        return

    # --- Generate Threat Report ---
    print(f"    Total packets processed: {packet_count}")
    
    if signature_alerts == 0 and size_alerts == 0 and pattern_alerts == 0:
        print("    [+] STATUS: SECURE. No anomalies detected.")
    else:
        print("    [!] STATUS: THREATS DETECTED")
        print("        Alerts Triggered:")
        if signature_alerts > 0:
            print(f"        - [Layer 1] Payload Signatures: {signature_alerts} packets contained malicious content.")
        if size_alerts > 0:
            print(f"        - [Layer 2] Size Anomalies:     {size_alerts} packets fell below normal size thresholds.")
        if pattern_alerts > 0:
            print(f"        - [Layer 3] Traffic Patterns:   {pattern_alerts} automated flood sequences detected.")
            
    print("-" * 70)

if __name__ == "__main__":
    # Add filename to test to this list
    pcap_files = [
        "iiot_baseline.pcap",
        "attack.pcap"
    ]
    
    for pcap in pcap_files:
        analyze_pcap_combined(pcap)