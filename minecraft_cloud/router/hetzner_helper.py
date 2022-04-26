import os
import paramiko
from hcloud import Client
from sqlalchemy.orm import Session

from minecraft_cloud import models

install_script_url = ""
hetzner_token = os.getenv('HETZNER_TOKEN')

client = Client(token=hetzner_token)


def start_minecraft_server(server: models.MinecraftServer, db: Session):
    """
    Start a minecraft server.
    """

    response = client.servers.create(
        name="minecraft_cloud" + server.name,
        image=client.images.get_by_name("debian-11"),
        type=client.server_types.get_by_name(server.server_type),
    )

    hetzner_server = response.server

    server.ip = hetzner_server.public_net.ipv4.ip
    server.root_pw = response.root_password
    db.commit()
    ssh = paramiko.SSHClient()
    ssh.connect(hetzner_server.public_net.ipv4.ip, username="root", password=response.root_password)
    ssh.exec_command("apt-get update")
    ssh.exec_command("apt-get upgrade -y")
    ssh.exec_command(f"curl -fsSL {install_script_url} -o install.sh && $ sh install.sh")
    return "start_minecraft_server"
