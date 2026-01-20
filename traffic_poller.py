```python
from pysnmp.hlapi import *
import time

# ============================================================
# SNMP Bandwidth Poller (Backend for Graphing)
# Author: Sheikh Alamin Santo
# Description: Calculates Mbps from OID Counters
# ============================================================

# --- Configuration ---
TARGET_IP = "192.168.88.1"   # Router IP
COMMUNITY = "public"         # SNMP Community String
INTERFACE_OID_IN = "1.3.6.1.2.1.2.2.1.10.1"  # OID for Ether1 In-Octets
INTERFACE_OID_OUT = "1.3.6.1.2.1.2.2.1.16.1" # OID for Ether1 Out-Octets

def get_snmp_data(oid):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(COMMUNITY),
        UdpTransportTarget((TARGET_IP, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(f"[-] SNMP Error: {errorIndication}")
        return 0
    elif errorStatus:
        print(f"[-] SNMP Error: {errorStatus.prettyPrint()}")
        return 0
    else:
        for varBind in varBinds:
            return int(varBind[1])

def monitor_traffic():
    print(f"[+] Monitoring Bandwidth on {TARGET_IP} (Press Ctrl+C to stop)...")
    print("-" * 50)
    
    # Initial Fetch
    prev_in = get_snmp_data(INTERFACE_OID_IN)
    prev_out = get_snmp_data(INTERFACE_OID_OUT)
    prev_time = time.time()

    while True:
        try:
            time.sleep(1) # Poll every 1 second
            
            # Current Fetch
            curr_in = get_snmp_data(INTERFACE_OID_IN)
            curr_out = get_snmp_data(INTERFACE_OID_OUT)
            curr_time = time.time()
            
            # Calculate Delta
            time_diff = curr_time - prev_time
            delta_in = (curr_in - prev_in) * 8   # Convert Bytes to Bits
            delta_out = (curr_out - prev_out) * 8
            
            # Calculate Speed (Mbps)
            speed_in_mbps = (delta_in / time_diff) / 1000000
            speed_out_mbps = (delta_out / time_diff) / 1000000
            
            print(f"⬇ Download: {speed_in_mbps:.2f} Mbps | ⬆ Upload: {speed_out_mbps:.2f} Mbps")
            
            # Update Previous Values
            prev_in = curr_in
            prev_out = curr_out
            prev_time = curr_time
            
        except KeyboardInterrupt:
            print("\n[!] Monitoring Stopped.")
            break

if __name__ == "__main__":
    monitor_traffic()
