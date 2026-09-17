import os
from netmiko import ConnectHandler


# ============================================================
# CONNECT TO A SYSTEM
# ============================================================

def connect_to_system(system):
    username = os.getenv(system["username_env"])
    password = os.getenv(system["password_env"])

    connection_info = {
        "device_type": system["type"],
        "host": system["host"],
        "username": username,
        "password": password,
    }

    return ConnectHandler(**connection_info)


# ============================================================
# LINUX - CREATE INTERFACE
# ============================================================

def create_linux_interface(connection, interface):
    output = connection.send_command(
        f"sudo ip link add {interface} type dummy"
    )

    connection.send_command(
        f"sudo ip link set {interface} up"
    )

    return output


# ============================================================
# LINUX - READ INTERFACE
# ============================================================

def read_linux_interface(connection, interface):
    output = connection.send_command(
        f"ip addr show {interface}"
    )

    return output


# ============================================================
# LINUX - REMOVE INTERFACE
# ============================================================

def remove_linux_interface(connection, interface):
    output = connection.send_command(
        f"sudo ip link delete {interface}"
    )

    return output


# ============================================================
# CISCO - CREATE LOOPBACK
# ============================================================

def create_cisco_loopback(connection, interface):
    commands = [
        f"interface {interface}",
        "description FONI temporary loopback",
        "no shutdown",
    ]

    output = connection.send_config_set(commands)

    return output


# ============================================================
# CISCO - READ LOOPBACK
# ============================================================

def read_cisco_loopback(connection, interface):
    output = connection.send_command(
        f"show ip interface brief | include {interface}"
    )

    if not output.strip():
        return f'Interface "{interface}" does not exist.'

    return output


# ============================================================
# CISCO - REMOVE LOOPBACK
# ============================================================

def remove_cisco_loopback(connection, interface):
    commands = [
        f"no interface {interface}"
    ]

    output = connection.send_config_set(commands)

    return output