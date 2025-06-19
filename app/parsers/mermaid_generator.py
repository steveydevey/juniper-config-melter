import re
from app.models.network import Network, Device, Interface
from app.models.juniper import VLAN, Route
from typing import List, Dict, Optional

class MermaidGenerator:
    def __init__(self):
        self.node_id_counter = 0
        self.edge_id_counter = 0
    
    def generate_topology(self, network: Network) -> str:
        """Generate a physical topology diagram showing device connections"""
        mermaid_lines = ["graph LR"]
        
        # Add styling for better visual appeal
        mermaid_lines.extend([
            "    classDef device fill:#e1f5fe,stroke:#01579b,stroke-width:3px,color:#000",
            "    classDef interface fill:#ffffff,stroke:#666,stroke-width:1px,color:#000",
            "    classDef vlanInterface fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px,color:#000",
            "    classDef ipInterface fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000"
        ])
        
        for device in network.devices:
            # Add device node
            device_id = self._sanitize_id(device.hostname)
            mermaid_lines.append(f'    {device_id}["{device.hostname}"]')
            mermaid_lines.append(f'    class {device_id} device')
            
            # Add interface nodes and connections
            for interface in device.interfaces:
                interface_id = f"{device_id}_{interface.name.replace('-', '_')}"
                
                # Create interface label
                interface_label = interface.name
                if interface.ip:
                    interface_label += f"<br/>{interface.ip}"
                if interface.description:
                    interface_label += f"<br/>{interface.description}"
                if interface.vlan_members:
                    vlan_info = ", ".join(interface.vlan_members)
                    interface_label += f"<br/>VLAN: {vlan_info}"
                
                mermaid_lines.append(f'    {interface_id}["{interface_label}"]')
                mermaid_lines.append(f'    {device_id} --> {interface_id}')
                
                # Apply styling based on interface characteristics
                if interface.vlan_members:
                    mermaid_lines.append(f'    class {interface_id} vlanInterface')
                elif interface.ip:
                    mermaid_lines.append(f'    class {interface_id} ipInterface')
                else:
                    mermaid_lines.append(f'    class {interface_id} interface')
        
        return "\n".join(mermaid_lines)
    
    def generate_routing_diagram(self, network: Network) -> str:
        """Generate a logical routing diagram showing network paths"""
        mermaid_lines = ["graph LR"]
        
        for device in network.devices:
            device_id = self._sanitize_id(device.hostname)
            mermaid_lines.append(f'    {device_id}["{device.hostname}"]')
            
            # Add routes
            if device.routing and "routes" in device.routing:
                for route in device.routing["routes"]:
                    route_id = f"{device_id}_route_{self.edge_id_counter}"
                    self.edge_id_counter += 1
                    mermaid_lines.append(f'    {route_id}["{route.destination}<br/>via {route.next_hop}"]')
                    mermaid_lines.append(f'    {device_id} -.-> {route_id}')
        
        return "\n".join(mermaid_lines)
    
    def generate_vlan_diagram(self, network: Network) -> str:
        """Generate a VLAN diagram showing VLAN relationships and interface assignments"""
        mermaid_lines = ["graph LR"]
        
        # Add styling for better visual appeal
        mermaid_lines.extend([
            "    classDef device fill:#e1f5fe,stroke:#01579b,stroke-width:3px,color:#000",
            "    classDef vlan fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px,color:#000",
            "    classDef interface fill:#f3e5f5,stroke:#4a148c,stroke-width:1px,color:#000"
        ])
        
        for device in network.devices:
            device_id = self._sanitize_id(device.hostname)
            mermaid_lines.append(f'    {device_id}["{device.hostname}"]')
            mermaid_lines.append(f'    class {device_id} device')
            
            # Add VLANs with their interface assignments
            if device.routing and "vlans" in device.routing:
                for vlan in device.routing["vlans"]:
                    vlan_id = f"{device_id}_vlan_{vlan.vlan_id}"
                    vlan_label = f"VLAN {vlan.vlan_id}<br/>{vlan.name}"
                    if vlan.description:
                        vlan_label += f"<br/>{vlan.description}"
                    
                    mermaid_lines.append(f'    {vlan_id}["{vlan_label}"]')
                    mermaid_lines.append(f'    {device_id} --> {vlan_id}')
                    mermaid_lines.append(f'    class {vlan_id} vlan')
                    
                    # Add interfaces assigned to this VLAN
                    if vlan.interfaces:
                        for interface_name in vlan.interfaces:
                            interface_id = f"{vlan_id}_{interface_name.replace('-', '_')}"
                            interface_label = interface_name
                            
                            # Find the interface object to get additional info
                            interface_obj = next((i for i in device.interfaces if i.name == interface_name), None)
                            if interface_obj and interface_obj.description:
                                interface_label += f"<br/>{interface_obj.description}"
                            
                            mermaid_lines.append(f'    {interface_id}["{interface_label}"]')
                            mermaid_lines.append(f'    {vlan_id} --> {interface_id}')
                            mermaid_lines.append(f'    class {interface_id} interface')
        
        return "\n".join(mermaid_lines)
    
    def generate_interface_diagram(self, network: Network) -> str:
        """Generate a detailed interface diagram with VLAN information"""
        mermaid_lines = ["graph LR"]
        
        # Add styling for better visual appeal
        mermaid_lines.extend([
            "    classDef device fill:#e1f5fe,stroke:#01579b,stroke-width:3px,color:#000",
            "    classDef interfaceGroup fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000",
            "    classDef interface fill:#ffffff,stroke:#666,stroke-width:1px,color:#000",
            "    classDef vlanInterface fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px,color:#000",
            "    classDef trunkInterface fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000"
        ])
        
        for device in network.devices:
            device_id = self._sanitize_id(device.hostname)
            mermaid_lines.append(f'    {device_id}["{device.hostname}"]')
            mermaid_lines.append(f'    class {device_id} device')
            
            # Group interfaces by type
            interface_groups = {}
            for interface in device.interfaces:
                interface_type = interface.name.split('-')[0]  # ge, xe, etc.
                if interface_type not in interface_groups:
                    interface_groups[interface_type] = []
                interface_groups[interface_type].append(interface)
            
            # Add interface groups
            for interface_type, interfaces in interface_groups.items():
                group_id = f"{device_id}_{interface_type}"
                group_label = f"{interface_type.upper()} Interfaces"
                mermaid_lines.append(f'    {group_id}["{group_label}"]')
                mermaid_lines.append(f'    {device_id} --> {group_id}')
                mermaid_lines.append(f'    class {group_id} interfaceGroup')
                
                # Add individual interfaces
                for interface in interfaces:
                    interface_id = f"{group_id}_{interface.name.replace('-', '_')}"
                    
                    # Create interface label with VLAN information
                    interface_label = f"{interface.name}"
                    if interface.ip:
                        interface_label += f"<br/>IP: {interface.ip}"
                    if interface.description:
                        interface_label += f"<br/>{interface.description}"
                    if interface.vlan_members:
                        vlan_info = ", ".join(interface.vlan_members)
                        interface_label += f"<br/>VLAN: {vlan_info}"
                    if interface.port_mode:
                        interface_label += f"<br/>Mode: {interface.port_mode}"
                    
                    mermaid_lines.append(f'    {interface_id}["{interface_label}"]')
                    mermaid_lines.append(f'    {group_id} --> {interface_id}')
                    
                    # Apply appropriate styling based on interface type
                    if interface.vlan_members:
                        mermaid_lines.append(f'    class {interface_id} vlanInterface')
                    elif interface.port_mode == "trunk":
                        mermaid_lines.append(f'    class {interface_id} trunkInterface')
                    else:
                        mermaid_lines.append(f'    class {interface_id} interface')
        
        return "\n".join(mermaid_lines)
    
    def generate_network_overview(self, network: Network) -> str:
        """Generate a comprehensive network overview diagram"""
        mermaid_lines = ["graph TD"]
        
        # Add styling
        mermaid_lines.extend([
            "    classDef device fill:#e1f5fe,stroke:#01579b,stroke-width:2px",
            "    classDef interface fill:#f3e5f5,stroke:#4a148c,stroke-width:1px",
            "    classDef vlan fill:#e8f5e8,stroke:#1b5e20,stroke-width:1px",
            "    classDef route fill:#fff3e0,stroke:#e65100,stroke-width:1px"
        ])
        
        for device in network.devices:
            device_id = self._sanitize_id(device.hostname)
            mermaid_lines.append(f'    {device_id}["{device.hostname}"]')
            mermaid_lines.append(f'    class {device_id} device')
            
            # Add key interfaces
            for interface in device.interfaces[:5]:  # Limit to first 5 interfaces
                if interface.ip:
                    interface_id = f"{device_id}_{interface.name.replace('-', '_')}"
                    interface_label = f"{interface.name}<br/>{interface.ip}"
                    mermaid_lines.append(f'    {interface_id}["{interface_label}"]')
                    mermaid_lines.append(f'    {device_id} --> {interface_id}')
                    mermaid_lines.append(f'    class {interface_id} interface')
            
            # Add VLANs
            if device.routing and "vlans" in device.routing:
                for vlan in device.routing["vlans"]:
                    vlan_id = f"{device_id}_vlan_{vlan.vlan_id}"
                    vlan_label = f"VLAN {vlan.vlan_id}<br/>{vlan.name}"
                    mermaid_lines.append(f'    {vlan_id}["{vlan_label}"]')
                    mermaid_lines.append(f'    {device_id} -.-> {vlan_id}')
                    mermaid_lines.append(f'    class {vlan_id} vlan')
        
        return "\n".join(mermaid_lines)
    
    def _sanitize_id(self, text: str) -> str:
        """Convert text to a valid Mermaid node ID"""
        # Remove special characters and replace with underscores
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', text)
        # Ensure it starts with a letter
        if sanitized and not sanitized[0].isalpha():
            sanitized = f"node_{sanitized}"
        return sanitized if sanitized else "node"
    
    def generate_all_diagrams(self, network: Network) -> Dict[str, str]:
        """Generate all types of diagrams for a network"""
        return {
            "topology": self.generate_topology(network),
            "routing": self.generate_routing_diagram(network),
            "vlans": self.generate_vlan_diagram(network),
            "interfaces": self.generate_interface_diagram(network),
            "overview": self.generate_network_overview(network)
        } 