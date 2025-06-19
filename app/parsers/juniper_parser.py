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
        # Use a more sophisticated approach to handle nested blocks
        interface_blocks = re.finditer(
            r'(vlan|\w+-\d+/\d+/\d+)\s*\{',
            config_text,
            re.DOTALL
        )
        
        for match in interface_blocks:
            interface_name = match.group(1)
            start_pos = match.end()
            
            # Find the matching closing brace by counting braces
            brace_count = 1
            end_pos = start_pos
            while brace_count > 0 and end_pos < len(config_text):
                if config_text[end_pos] == '{':
                    brace_count += 1
                elif config_text[end_pos] == '}':
                    brace_count -= 1
                end_pos += 1
            
            if brace_count == 0:
                interface_config = config_text[start_pos:end_pos-1]  # -1 to exclude the closing brace
                
                # Extract description
                desc_match = re.search(r'description\s+"([^"]+)";', interface_config)
                description = desc_match.group(1) if desc_match else None
                
                # Extract IP address - look for family inet blocks
                ip_match = re.search(r'family\s+inet\s*\{[^}]*address\s+(\d+\.\d+\.\d+\.\d+/\d+);[^}]*\}', interface_config, re.DOTALL)
                ip_address = ip_match.group(1) if ip_match else None
                
                # Extract VLAN membership
                vlan_members = []
                vlan_matches = re.finditer(r'vlan\s*\{[^}]*members\s+(\w+);[^}]*\}', interface_config, re.DOTALL)
                for vlan_match in vlan_matches:
                    vlan_members.append(vlan_match.group(1))
                
                # Extract port mode
                port_mode = None
                port_mode_match = re.search(r'port-mode\s+(\w+);', interface_config)
                if port_mode_match:
                    port_mode = port_mode_match.group(1)
                
                # Extract status (enabled/disabled)
                status = "enabled"
                if re.search(r'disable;', interface_config):
                    status = "disabled"
                
                interface = Interface(
                    name=interface_name,
                    ip=ip_address,
                    description=description,
                    status=status,
                    vlan_members=vlan_members,
                    port_mode=port_mode
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
        """Parse VLAN configurations and their member interfaces"""
        vlans = []
        
        # First, find VLAN definitions
        vlan_blocks = re.finditer(
            r'(\w+)\s*\{[^}]*description\s+"([^"]+)";[^}]*vlan-id\s+(\d+);[^}]*\}',
            config_text,
            re.DOTALL
        )
        
        # Create VLAN objects and build ID to name mapping
        vlan_map = {}
        vlan_id_to_name = {}
        for match in vlan_blocks:
            vlan_name = match.group(1)
            description = match.group(2)
            vlan_id = int(match.group(3))
            
            vlan = VLAN(
                name=vlan_name,
                vlan_id=vlan_id,
                description=description,
                interfaces=[]
            )
            vlans.append(vlan)
            vlan_map[vlan_name] = vlan
            vlan_id_to_name[str(vlan_id)] = vlan_name
        
        # Now scan all interfaces to find VLAN memberships
        interface_blocks = re.finditer(
            r'(vlan|\w+-\d+/\d+/\d+)\s*\{',
            config_text,
            re.DOTALL
        )
        
        for match in interface_blocks:
            interface_name = match.group(1)
            start_pos = match.end()
            
            # Find the matching closing brace by counting braces
            brace_count = 1
            end_pos = start_pos
            while brace_count > 0 and end_pos < len(config_text):
                if config_text[end_pos] == '{':
                    brace_count += 1
                elif config_text[end_pos] == '}':
                    brace_count -= 1
                end_pos += 1
            
            if brace_count == 0:
                interface_config = config_text[start_pos:end_pos-1]  # -1 to exclude the closing brace
                
                # Look for VLAN memberships in this interface
                vlan_matches = re.finditer(r'vlan\s*\{[^}]*members\s+(\w+);[^}]*\}', interface_config, re.DOTALL)
                for vlan_match in vlan_matches:
                    vlan_identifier = vlan_match.group(1)
                    
                    # Try to find the VLAN by name or ID
                    target_vlan = None
                    if vlan_identifier in vlan_map:
                        # Direct name match
                        target_vlan = vlan_map[vlan_identifier]
                    elif vlan_identifier in vlan_id_to_name:
                        # ID match - get the actual VLAN name
                        vlan_name = vlan_id_to_name[vlan_identifier]
                        target_vlan = vlan_map[vlan_name]
                    
                    if target_vlan:
                        target_vlan.interfaces.append(interface_name)
        
        return vlans
    
    def parse_security_zones(self, config_text: str) -> List[Dict]:
        """Parse security zones (placeholder for future implementation)"""
        # TODO: Implement security zone parsing
        return []
    
    def parse_policies(self, config_text: str) -> List[Dict]:
        """Parse security policies (placeholder for future implementation)"""
        # TODO: Implement policy parsing
        return [] 