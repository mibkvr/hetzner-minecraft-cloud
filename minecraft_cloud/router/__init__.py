import os

from fastapi import APIRouter, Depends
from hcloud import Client
from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session

from minecraft_cloud import models
from minecraft_cloud.database import get_db
from minecraft_cloud.router.hetzner_helper import start_minecraft_server

home_router = APIRouter(
    tags=['home']
)




@home_router.post('/create-server')
async def create_server(name: str, github_token, github_username, db=Depends(get_db)):
    """
    Create a server in local DB
    """
    server = models.MinecraftServer(
        name=name,
        github_token=github_token,
        github_username=github_username,
    )
    db.add(server)
    db.commit()

    return server


@home_router.post('/start-server')
async def start_server(server_id: int, db: Session = Depends(get_db)):
    """
    Start a server on Hetzner Cloud.
    """

    server: models.MinecraftServer = db.query(models.MinecraftServer).filter(
        models.MinecraftServer.id == server_id).first()
    if server is None:
        return {'error': 'Server not found'}

    if server.running:
        return {'error': 'Server already running'}
    else:
        return start_minecraft_server(server, db)


@home_router.get('/list-servers')
async def list_servers():
    """
    List all servers on Hetzner Cloud.
    """
    servers = client.servers.all()
    return servers
