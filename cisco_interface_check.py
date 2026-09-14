from netmiko import ConnectHandler
import os

device = {
    "device_type": "cisco_ios",
    "host": os.getenv("CISCO_HOST"),
    "username": os.getenv("CISCO_USERNAME"),
    "password": os.getenv("CISCO_PASSWORD")
}

connection = ConnectHandler(**device)

interface_output = connection.send_command("show ip interface brief")
version_output = connection.send_command("show version")
interface_lines = interface_output.splitlines()
for line in interface_lines:
    if "Loopback" in line:
        fields = line.split()

        interface_name = fields[0]
        ip_address = fields[1]
        interface_status = fields[-2]
        protocol_status = fields[-1]

        if interface_status == "up" and protocol_status == "up":
            print(interface_name, "- OPERATIONAL")
        else:
            print(interface_name, "- CHECK REQUIRED")

        print("Interface:", interface_name)
        print("IP Address:", ip_address)
        print("Status:", interface_status)
        print("Protocol:", protocol_status)
        
print("=== SHOW IP INTERFACE BRIEF ===")
print(interface_output)

print("=== SHOW VERSION ===")
print(version_output)

connection.disconnect()