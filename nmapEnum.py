import os
import subprocess
import re
import threading
import time

def run_nmap_ping_scan(network, callback):
    def scan():
        # Running Nmap ping scan
        result = subprocess.run(['nmap', '-sn', network], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = result.stdout.decode()
        callback(output)
    threading.Thread(target=scan).start()

def extract_ips(nmap_output):
    # Extract IP addresses from Nmap output
    ips = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', nmap_output)
    return set(ips)  # Removing duplicates

def save_ips_to_file(ips, network):
    file_name = f"hostsUp_{network.replace('/', '_')}.txt"
    with open(file_name, 'w') as file:
        for ip in ips:
            file.write(f"{ip}\n")
    return file_name

def run_nmap_port_scan(file_name, callback):
    def scan():
        # Running Nmap port scan using the IP addresses file
        subprocess.run(['nmap', '-sV', '-Pn', '-n', '-iL', file_name, '-o', 'hostPortScan.txt'])
        callback()
    threading.Thread(target=scan).start()

# Callbacks for scan completions
def on_ping_scan_complete(output):
    global ips
    ips = extract_ips(output)
    print("\nPing Scan Complete!")

def on_nmap_scan_complete():
    print("\nNmap Scan Complete!")

# Replace this with the desired Class C network
class_c_network = "192.168.1.0/24"

# Step 1: Run Nmap Ping Scan with Countdown
run_nmap_ping_scan(class_c_network, on_ping_scan_complete)
print("Performing Ping Scan")

# Wait for ping scan to complete
while 'ips' not in globals():
    time.sleep(1)

# Step 2: Save IPs to a File
hosts_file = save_ips_to_file(ips, class_c_network)

# Step 3: Run Nmap Port Scan with Countdown
run_nmap_port_scan(hosts_file, on_nmap_scan_complete)
print("Performing Nmap Scan")
