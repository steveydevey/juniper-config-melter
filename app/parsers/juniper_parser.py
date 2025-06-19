import re
from app.models.network import Network, Interface, Device
from app.models.juniper import VLAN, Route, JuniperConfig
from typing import List, Dict, Optional

class JuniperParser:
    def __init__(self):
        self.config = None
        
    def parse_config(self, config_text: str) -> Network:
        """Parse a complete Juniper configuration and return a Network model"""
        self.config = config_text
        
        # Extract hostname
        hostname = self._extract_hostname(config_text)
        
        # Parse interfaces
        interfaces = self.parse_interfaces(config_text)
        
        # Parse routing
        routes = self.parse_routing(config_text)
        
        # Parse VLANs
        vlans = self.parse_vlans(config_text)
        
        # Create device
        device = Device(
            hostname=hostname,
            interfaces=interfaces,
            routing={"routes": routes, "vlans": vlans}
        )
        
        return Network(devices=[device], connections=[])
    
    def _extract_hostname(self, config_text: str) -> str:
        """Extract hostname from configuration"""
        hostname_match = re.search(r'host-name\s+(\S+);', config_text)
        return hostname_match.group(1) if hostname_match else "unknown"
    
    def parse_interfaces(self, config_text: str) -> List[Interface]:
        """Parse interface configurations from Juniper config"""
        interfaces = []
        
        # Find all interface blocks - including VLAN interfaces
        interface_blocks = re.finditer(
            r'(vlan|\w+-\d+/\d+/\d+)\s*\{([^}]+)\}',
            config_text,
            re.DOTALL
        )
        
        for match in interface_blocks:
            interface_name = match.group(1)
            interface_config = match.group(2)
            
            # Extract description
            desc_match = re.search(r'description\s+"([^"]+)";', interface_config)
            description = desc_match.group(1) if desc_match else None
            
            # Extract IP address - look for family inet blocks
            ip_match = re.search(r'family\s+inet\s*\{[^}]*address\s+(\d+\.\d+\.\d+\.\d+/\d+);[^}]*\}', interface_config, re.DOTALL)
            ip_address = ip_match.group(1) if ip_match else None
            
            # Extract status (enabled/disabled)
            status = "enabled"
            if re.search(r'disable;', interface_config):
                status = "disabled"
            
            interface = Interface(
                name=interface_name,
                ip=ip_address,
                description=description,
                status=status
            )
            interfaces.append(interface)
        
        return interfaces
    
    def parse_routing(self, config_text: str) -> List[Route]:
        """Parse routing configurations"""
        routes = []
        
        # Parse static routes
        static_routes = re.finditer(
            r'route\s+(\d+\.\d+\.\d+\.\d+/\d+)\s+next-hop\s+(\d+\.\d+\.\d+\.\d+);',
            config_text
        )
        
        for match in static_routes:
            route = Route(
                destination=match.group(1),
                next_hop=match.group(2),
                protocol="static"
            )
            routes.append(route)
        
        return routes
    
    def parse_vlans(self, config_text: str) -> List[VLAN]:
        """Parse VLAN configurations"""
        vlans = []
        
        # Find VLAN blocks
        vlan_blocks = re.finditer(
            r'(\w+)\s*\{[^}]*description\s+"([^"]+)";[^}]*vlan-id\s+(\d+);[^}]*\}',
            config_text,
            re.DOTALL
        )
        
        for match in vlan_blocks:
            vlan_name = match.group(1)
            description = match.group(2)
            vlan_id = int(match.group(3))
            
            vlan = VLAN(
                name=vlan_name,
                vlan_id=vlan_id,
                description=description
            )
            vlans.append(vlan)
        
        return vlans
    
    def parse_security_zones(self, config_text: str) -> List[Dict]:
        """Parse security zones (placeholder for future implementation)"""
        # TODO: Implement security zone parsing
        return []
    
    def parse_policies(self, config_text: str) -> List[Dict]:
        """Parse security policies (placeholder for future implementation)"""
        # TODO: Implement policy parsing
        return [] 