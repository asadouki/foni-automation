from netmiko import ConnectHandler
import os

devices = [
    {
        "device_type": "cisco_ios",
        "host": os.getenv("CISCO_HOST"),
        "username": os.getenv("CISCO_USERNAME"),
        "password": os.getenv("CISCO_PASSWORD")
    },
    {
        "device_type": "linux",
        "host": os.getenv("LINUX_HOST"),
        "username": os.getenv("LINUX_USERNAME"),
        "password": os.getenv("LINUX_PASSWORD")

    
    }
]


for device in devices:
    connection = ConnectHandler(**device)
    output = connection.send