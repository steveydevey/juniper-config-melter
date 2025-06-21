from diagrams import Diagram, Cluster
from diagrams.generic.network import Router, Switch, Firewall
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Client
from diagrams.onprem.network import Internet
from typing import Optional, Dict, List
import os

from app.models.network import Network, Device, Interface

class DiagramsGenerator:
    def __init__(self, output_dir: Optional[str] = None, use_mindmap_style: bool = True):
        self.output_dir = output_dir or "generated_diagrams"
        self.use_mindmap_style = use_mindmap_style
        os.makedirs(self.output_dir, exist_ok=True)

    def _get_mindmap_graph_attr(self, diagram_type: str = "general") -> Dict[str, str]:
        """
        Get graph attributes optimized for mind-map style layouts.
        Uses radial layout with curved edges for a more organic, mind-map appearance.
        """
        base_attrs = {
            "fontsize": "10",
            "nodesep": "0.8",      # More spacing for radial layout
            "ranksep": "1.2",      # More rank separation for mind-map
            "splines": "curved",   # Curved edges for organic look
            "concentrate": "false", # Don't merge edges for mind-map clarity
            "overlap": "false",    # Prevent node overlap
            "sep": "0.5",          # Edge separation
            "K": "1.5",            # Spring constant for layout
            "maxiter": "1000",     # More iterations for better layout
            "start": "random"      # Random start for better distribution
        }
        
        if diagram_type == "interfaces":
            return {
                **base_attrs,
                "nodesep": "1.0",  # More spacing for interface diagrams
                "ranksep": "1.5"
            }
        elif diagram_type == "vlans":
            return {
                **base_attrs,
                "nodesep": "0.6",  # Tighter spacing for VLAN grouping
                "ranksep": "1.0"
            }
        else:
            return base_attrs

    def _get_optimized_graph_attr(self, diagram_type: str = "general") -> Dict[str, str]:
        """
        Get optimized graph attributes for different diagram types.
        Now supports both traditional hierarchical and mind-map styles.
        """
        if self.use_mindmap_style:
            return self._get_mindmap_graph_attr(diagram_type)
        
        # Original hierarchical layout attributes
        base_attrs = {
            "fontsize": "10",      # Smaller font for more content
            "nodesep": "0.3",      # Tighter node spacing
            "ranksep": "0.5",      # Tighter rank spacing
            "splines": "ortho",    # Clean, straight edges
            "concentrate": "true"  # Merge parallel edges
        }
        
        if diagram_type == "interfaces":
            # Optimized for interface diagrams with many nodes
            return {
                **base_attrs,
                "rankdir": "LR",   # Left to Right for wide layouts
                "nodesep": "0.2",  # Even tighter spacing for interfaces
                "ranksep": "0.4"   # Tighter rank separation
            }
        elif diagram_type == "vlans":
            # Optimized for VLAN diagrams with hierarchical structure
            return {
                **base_attrs,
                "rankdir": "LR",   # Left to Right for VLAN arrangement
                "nodesep": "0.4",  # Slightly more spacing for VLAN clarity
                "ranksep": "0.8"   # More separation between VLAN levels
            }
        else:
            # General purpose attributes
            return base_attrs

    def _get_diagram_direction(self, diagram_type: str = "general") -> str:
        """
        Get the appropriate direction for the diagram based on style preference.
        For mind-map style, we use 'TB' (top-to-bottom) as the base direction
        and let the radial layout handle the positioning.
        """
        if self.use_mindmap_style:
            return "TB"  # Base direction for mind-map, actual layout is radial
        
        # Original directional logic
        if diagram_type == "interfaces":
            return "LR"  # Left to Right for interface diagrams
        elif diagram_type == "vlans":
            return "LR"  # Left to Right for VLAN diagrams
        else:
            return "TB"  # Top to Bottom for general diagrams

    def generate_topology(self, network: Network, config_id: str) -> Dict[str, str]:
        """
        Generate a network topology diagram from the Network model.
        Returns paths to both PNG and SVG files.
        """
        filename = f"{config_id}_topology"
        png_path = os.path.join(self.output_dir, f"{filename}.png")
        svg_path = os.path.join(self.output_dir, f"{filename}.svg")
        
        graph_attr = self._get_optimized_graph_attr("general")
        
        with Diagram("Network Topology", show=False, filename=os.path.join(self.output_dir, filename), 
                     outformat="png", direction=self._get_diagram_direction("general"), graph_attr=graph_attr):
            # Create device nodes
            device_nodes = {}
            for device in network.devices:
                # Use Router icon for all devices for now (can be improved)
                node = Router(device.hostname)
                device_nodes[device.hostname] = node
                
                # Add interfaces as Switches
                for interface in device.interfaces:
                    iface_label = interface.name
                    if interface.ip:
                        iface_label += f"\n{interface.ip}"
                    if interface.description:
                        iface_label += f"\n{interface.description}"
                    iface_node = Switch(iface_label)
                    node >> iface_node
        
        # Generate SVG version
        with Diagram("Network Topology", show=False, filename=os.path.join(self.output_dir, filename), 
                     outformat="svg", direction=self._get_diagram_direction("general"), graph_attr=graph_attr):
            # Create device nodes
            device_nodes = {}
            for device in network.devices:
                node = Router(device.hostname)
                device_nodes[device.hostname] = node
                
                for interface in device.interfaces:
                    iface_label = interface.name
                    if interface.ip:
                        iface_label += f"\n{interface.ip}"
                    if interface.description:
                        iface_label += f"\n{interface.description}"
                    iface_node = Switch(iface_label)
                    node >> iface_node
        
        return {
            "png": png_path,
            "svg": svg_path
        }

    def generate_interface_diagram(self, network: Network, config_id: str) -> Dict[str, str]:
        """
        Generate an interface-focused diagram showing interface details.
        Uses horizontal layout for better space utilization.
        """
        filename = f"{config_id}_interfaces"
        png_path = os.path.join(self.output_dir, f"{filename}.png")
        svg_path = os.path.join(self.output_dir, f"{filename}.svg")
        
        graph_attr = self._get_optimized_graph_attr("interfaces")
        
        with Diagram("Interface Diagram", show=False, filename=os.path.join(self.output_dir, filename), 
                     outformat="png", direction=self._get_diagram_direction("interfaces"), graph_attr=graph_attr):
            for device in network.devices:
                with Cluster(f"Device: {device.hostname}"):
                    # Group interfaces by type first
                    interface_groups = {}
                    for interface in device.interfaces:
                        interface_type = interface.name.split('-')[0] if '-' in interface.name else "other"
                        if interface_type not in interface_groups:
                            interface_groups[interface_type] = []
                        interface_groups[interface_type].append(interface)
                    
                    # Create interface layout without arbitrary grouping
                    for interface_type, interfaces in interface_groups.items():
                        with Cluster(f"{interface_type.upper()} Interfaces"):
                            # Sort interfaces by port number for consistent ordering
                            sorted_interfaces = sorted(interfaces, key=lambda x: self._extract_port_number(x.name))
                            
                            for interface in sorted_interfaces:
                                iface_label = interface.name
                                if interface.ip:
                                    iface_label += f"\n{interface.ip}"
                                if interface.description:
                                    iface_label += f"\n{interface.description}"
                                Switch(iface_label)
        
        # Generate SVG version
        with Diagram("Interface Diagram", show=False, filename=os.path.join(self.output_dir, filename), 
                     outformat="svg", direction=self._get_diagram_direction("interfaces"), graph_attr=graph_attr):
            for device in network.devices:
                with Cluster(f"Device: {device.hostname}"):
                    interface_groups = {}
                    for interface in device.interfaces:
                        interface_type = interface.name.split('-')[0] if '-' in interface.name else "other"
                        if interface_type not in interface_groups:
                            interface_groups[interface_type] = []
                        interface_groups[interface_type].append(interface)
                    
                    for interface_type, interfaces in interface_groups.items():
                        with Cluster(f"{interface_type.upper()} Interfaces"):
                            sorted_interfaces = sorted(interfaces, key=lambda x: self._extract_port_number(x.name))
                            
                            for interface in sorted_interfaces:
                                iface_label = interface.name
                                if interface.ip:
                                    iface_label += f"\n{interface.ip}"
                                if interface.description:
                                    iface_label += f"\n{interface.description}"
                                Switch(iface_label)
        
        return {
            "png": png_path,
            "svg": svg_path
        }

    def _extract_port_number(self, interface_name: str) -> int:
        """
        Extract port number from interface name for sorting.
        Examples: ge-0/0/0 -> 0, ge-0/0/47 -> 47, xe-0/1/3 -> 3
        """
        try:
            # Extract the last number from interface name
            parts = interface_name.split('/')
            if len(parts) >= 3:
                return int(parts[-1])
            return 0
        except (ValueError, IndexError):
            return 0

    def generate_vlan_diagram(self, network: Network, config_id: str) -> Dict[str, str]:
        """
        Generate a VLAN-focused diagram showing VLAN relationships.
        Now uses a radial (mind-map) layout for better visualization.
        Only shows interfaces assigned to VLANs (no untagged ports).
        """
        filename = f"{config_id}_vlans"
        png_path = os.path.join(self.output_dir, f"{filename}.png")
        svg_path = os.path.join(self.output_dir, f"{filename}.svg")

        # Force mind-map style for VLAN diagram
        graph_attr = self._get_mindmap_graph_attr("vlans")
        direction = "TB"  # Radial layout uses TB as base

        for outformat in ["png", "svg"]:
            with Diagram(
                "VLAN Diagram", show=False,
                filename=os.path.join(self.output_dir, filename),
                outformat=outformat, direction=direction, graph_attr=graph_attr
            ):
                for device in network.devices:
                    with Cluster(f"Device: {device.hostname}"):
                        vlan_assignments = {}
                        all_vlan_interfaces = set()
                        if device.routing and "vlans" in device.routing:
                            for vlan in device.routing["vlans"]:
                                vlan_assignments[vlan.name] = []
                        for interface in device.interfaces:
                            if interface.vlan_members and len(interface.vlan_members) > 0:
                                for vlan_name in interface.vlan_members:
                                    if vlan_name in vlan_assignments:
                                        vlan_assignments[vlan_name].append(interface)
                                        all_vlan_interfaces.add(interface.name)
                        for vlan_name, interfaces in vlan_assignments.items():
                            vlan_details = None
                            if device.routing and "vlans" in device.routing:
                                for vlan in device.routing["vlans"]:
                                    if vlan.name == vlan_name:
                                        vlan_details = vlan
                                        break
                            if vlan_details:
                                vlan_label = f"VLAN {vlan_details.vlan_id}\n{vlan_details.name}"
                                if vlan_details.description:
                                    vlan_label += f"\n{vlan_details.description}"
                            else:
                                vlan_label = f"VLAN {vlan_name}"
                            if "newlab" in vlan_name.lower():
                                vlan_node = Switch(vlan_label, style="filled", fillcolor="lightcoral", fontcolor="black")
                            elif "oob" in vlan_name.lower():
                                vlan_node = Switch(vlan_label, style="filled", fillcolor="moccasin", fontcolor="black")
                            else:
                                vlan_node = Switch(vlan_label)
                            if interfaces:
                                with Cluster(f"{vlan_name} Interfaces"):
                                    for interface in interfaces:
                                        iface_label = interface.name
                                        if interface.ip:
                                            iface_label += f"\n{interface.ip}"
                                        if interface.description:
                                            iface_label += f"\n{interface.description}"
                                        interface_node = Switch(iface_label)
                                        vlan_node >> interface_node
        return {"png": png_path, "svg": svg_path}

    def generate_untagged_ports_diagram(self, network: Network, config_id: str) -> Dict[str, str]:
        """
        Generate a diagram showing only untagged interfaces (not assigned to any VLAN) for each device.
        """
        filename = f"{config_id}_untagged_ports"
        png_path = os.path.join(self.output_dir, f"{filename}.png")
        svg_path = os.path.join(self.output_dir, f"{filename}.svg")
        graph_attr = self._get_optimized_graph_attr("interfaces")
        direction = self._get_diagram_direction("interfaces")
        for outformat in ["png", "svg"]:
            with Diagram(
                "Untagged Ports", show=False,
                filename=os.path.join(self.output_dir, filename),
                outformat=outformat, direction=direction, graph_attr=graph_attr
            ):
                for device in network.devices:
                    with Cluster(f"Device: {device.hostname}"):
                        all_vlan_interfaces = set()
                        if device.routing and "vlans" in device.routing:
                            for vlan in device.routing["vlans"]:
                                if hasattr(vlan, 'interfaces') and vlan.interfaces:
                                    all_vlan_interfaces.update(vlan.interfaces)
                        untagged_interfaces = []
                        for interface in device.interfaces:
                            if interface.name not in all_vlan_interfaces:
                                untagged_interfaces.append(interface)
                        if untagged_interfaces:
                            with Cluster("Untagged Ports"):
                                for interface in untagged_interfaces:
                                    iface_label = interface.name
                                    if interface.ip:
                                        iface_label += f"\n{interface.ip}"
                                    if interface.description:
                                        iface_label += f"\n{interface.description}"
                                    Switch(iface_label)
        return {"png": png_path, "svg": svg_path}

    def generate_routing_diagram(self, network: Network, config_id: str) -> Dict[str, str]:
        """
        Generate a routing-focused diagram showing routing information.
        """
        filename = f"{config_id}_routing"
        png_path = os.path.join(self.output_dir, f"{filename}.png")
        svg_path = os.path.join(self.output_dir, f"{filename}.svg")
        
        graph_attr = self._get_optimized_graph_attr("general")
        
        with Diagram("Routing Diagram", show=False, filename=os.path.join(self.output_dir, filename), 
                     outformat="png", direction=self._get_diagram_direction("general"), graph_attr=graph_attr):
            for device in network.devices:
                with Cluster(f"Device: {device.hostname}"):
                    device_node = Router(device.hostname)
                    
                    # Add routes if they exist
                    if device.routing and "routes" in device.routing:
                        for route in device.routing["routes"]:
                            route_label = f"{route.destination}\nvia {route.next_hop}"
                            route_node = Switch(route_label)
                            device_node >> route_node
        
        # Generate SVG version
        with Diagram("Routing Diagram", show=False, filename=os.path.join(self.output_dir, filename), 
                     outformat="svg", direction=self._get_diagram_direction("general"), graph_attr=graph_attr):
            for device in network.devices:
                with Cluster(f"Device: {device.hostname}"):
                    device_node = Router(device.hostname)
                    
                    if device.routing and "routes" in device.routing:
                        for route in device.routing["routes"]:
                            route_label = f"{route.destination}\nvia {route.next_hop}"
                            route_node = Switch(route_label)
                            device_node >> route_node
        
        return {
            "png": png_path,
            "svg": svg_path
        }

    def generate_overview_diagram(self, network: Network, config_id: str) -> Dict[str, str]:
        """
        Generate an overview diagram showing key network elements.
        """
        filename = f"{config_id}_overview"
        png_path = os.path.join(self.output_dir, f"{filename}.png")
        svg_path = os.path.join(self.output_dir, f"{filename}.svg")
        
        graph_attr = self._get_optimized_graph_attr("general")
        
        with Diagram("Network Overview", show=False, filename=os.path.join(self.output_dir, filename), 
                     outformat="png", direction=self._get_diagram_direction("general"), graph_attr=graph_attr):
            for device in network.devices:
                with Cluster(f"Device: {device.hostname}"):
                    device_node = Router(device.hostname)
                    
                    # Show key interfaces (first 5 with IP addresses)
                    ip_interfaces = [i for i in device.interfaces if i.ip][:5]
                    for interface in ip_interfaces:
                        iface_label = f"{interface.name}\n{interface.ip}"
                        iface_node = Switch(iface_label)
                        device_node >> iface_node
                    
                    # Show VLANs if they exist
                    if device.routing and "vlans" in device.routing:
                        for vlan in device.routing["vlans"]:
                            vlan_label = f"VLAN {vlan.vlan_id}\n{vlan.name}"
                            vlan_node = Switch(vlan_label)
                            device_node >> vlan_node
        
        # Generate SVG version
        with Diagram("Network Overview", show=False, filename=os.path.join(self.output_dir, filename), 
                     outformat="svg", direction=self._get_diagram_direction("general"), graph_attr=graph_attr):
            for device in network.devices:
                with Cluster(f"Device: {device.hostname}"):
                    device_node = Router(device.hostname)
                    
                    ip_interfaces = [i for i in device.interfaces if i.ip][:5]
                    for interface in ip_interfaces:
                        iface_label = f"{interface.name}\n{interface.ip}"
                        iface_node = Switch(iface_label)
                        device_node >> iface_node
                    
                    if device.routing and "vlans" in device.routing:
                        for vlan in device.routing["vlans"]:
                            vlan_label = f"VLAN {vlan.vlan_id}\n{vlan.name}"
                            vlan_node = Switch(vlan_label)
                            device_node >> vlan_node
        
        return {
            "png": png_path,
            "svg": svg_path
        }

    def generate_all_diagrams(self, network: Network, config_id: str) -> Dict[str, Dict[str, str]]:
        """
        Generate all types of diagrams for a network.
        Returns a dictionary mapping diagram types to their file paths.
        """
        return {
            "topology": self.generate_topology(network, config_id),
            "interfaces": self.generate_interface_diagram(network, config_id),
            "vlans": self.generate_vlan_diagram(network, config_id),
            "untagged_ports": self.generate_untagged_ports_diagram(network, config_id),
            "routing": self.generate_routing_diagram(network, config_id),
            "overview": self.generate_overview_diagram(network, config_id)
        } 