from pydantic import BaseModel
from typing import List, Optional

class Interface(BaseModel):
    name: str
    ip: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class Device(BaseModel):
    hostname: str
    interfaces: List[Interface]
    routing: Optional[dict] = None

class Network(BaseModel):
    devices: List[Device]
    connections: Optional[List[dict]] = None
    topology: Optional[str] = None 