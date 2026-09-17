import os

from flask import Flask, render_template
from netmiko.exceptions import (
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
)

from Automate_One_Full_Lifecycle import (
    connect_to_system,
    create_linux_interface,
    read_linux_interface,
    remove_linux_interface,
    create_cisco_loopback,
    read_cisco_loopback,
    remove_cisco_loopback,
)


app = Flask(__name__)


@app.route("/interfaces")
def interfaces():

    systems = [
        {
            "name": "FONI-Linux",
            "username_env": "LINUX_USERNAME",
            "password_env": "LINUX_PASSWORD",
            "type": "linux",
            "host": "3.145.195.223",
            "interface": "foni48",
        },
        {
            "name": "FONI-Router-01",
            "username_env": "CISCO_USERNAME",
            "password_env": "CISCO_PASSWORD",
            "type": "cisco_ios",
            "host": "54.90.112.247",
            "interface": "Loopback100",
        },
    ]

    for device in systems:

        connection = None

        try:
            connection = connect_to_system(device)

            # CREATE
            if device["type"] == "linux":
                create_output = create_linux_interface(
                    connection,
                    device["interface"],
                )
            else:
                create_output = create_cisco_loopback(
                    connection,
                    device["interface"],
                )

            device["create_output"] = create_output

            # READ AFTER CREATE
            if device["type"] == "linux":
                after_create = read_linux_interface(
                    connection,
                    device["interface"],
                )
            else:
                after_create = read_cisco_loopback(
                    connection,
                    device["interface"],
                )

            device["after_create"] = after_create

            # REMOVE
            if device["type"] == "linux":
                remove_output = remove_linux_interface(
                    connection,
                    device["interface"],
                )
            else:
                remove_output = remove_cisco_loopback(
                    connection,
                    device["interface"],
                )

            device["remove_output"] = remove_output

            # READ AFTER REMOVE
            if device["type"] == "linux":
                after_remove = read_linux_interface(
                    connection,
                    device["interface"],
                )
            else:
                after_remove = read_cisco_loopback(
                    connection,
                    device["interface"],
                )

            device["after_remove"] = after_remove

        except NetmikoAuthenticationException:
            device["error"] = "Authentication failed."

        except NetmikoTimeoutException:
            device["error"] = "Connection timed out."

        except Exception as e:
            device["error"] = f"Another error occurred: {e}"

        finally:
            if connection:
                connection.disconnect()

    return render_template(
        "interfaces.html",
        systems=systems,
    )


if __name__ == "__main__":
    app.run(debug=True)