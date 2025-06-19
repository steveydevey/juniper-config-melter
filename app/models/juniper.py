from pydantic import BaseModel
from typing import List, Optional, Dict

class VLAN(BaseModel):
    name: str
    vlan_id: int
    description: Optional[str] = None
    interfaces: Optional[List[str]] = None

class Route(BaseModel):
    destination: str
    next_hop: str
    protocol: str = "static"
    metric: Optional[int] = None
    preference: Optional[int] = None

class SecurityZone(BaseModel):
    name: str
    interfaces: List[str]
    policies: Optional[List[str]] = None

class SecurityPolicy(BaseModel):
    name: str
    from_zone: str
    to_zone: str
    match: Optional[Dict] = None
    then: Optional[Dict] = None

class JuniperConfig(BaseModel):
    hostname: str
    interfaces: List[Dict]
    vlans: List[VLAN]
    routes: List[Route]
    security_zones: Optional[List[SecurityZone]] = None
    security_policies: Optional[List[SecurityPolicy]] = None
    version: Optional[str] = None 