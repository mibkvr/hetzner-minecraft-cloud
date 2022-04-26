from sqlalchemy import Column, String, Integer, Boolean

from .database import Base


class MinecraftServer(Base):
    __tablename__ = 'minecraft_servers'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)

    #
    #   System Properties
    #
    running = Column(Boolean)
    ip = Column(String(255))
    root_pw = Column(String(255))

    server_type = Column(String(255))

    github_url = Column(String(255))
    github_username = Column(String(255))
    github_repository = Column(String(255))
    github_token = Column(String(255))
