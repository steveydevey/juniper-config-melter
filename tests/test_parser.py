import unittest
import os
from app.parsers.juniper_parser import JuniperParser
from app.parsers.mermaid_generator import MermaidGenerator
from app.models.network import Network

class TestJuniperParser(unittest.TestCase):
    def setUp(self):
        self.parser = JuniperParser()
        self.generator = MermaidGenerator()
        
        # Load test configuration
        config_path = os.path.join(os.path.dirname(__file__), '..', 'test-configs', 'ex3300-1.conf')
        with open(config_path, 'r') as f:
            self.config_text = f.read()
    
    def test_hostname_extraction(self):
        """Test hostname extraction from configuration"""
        hostname = self.parser._extract_hostname(self.config_text)
        self.assertEqual(hostname, "ex3300")
    
    def test_interface_parsing(self):
        """Test interface parsing"""
        interfaces = self.parser.parse_interfaces(self.config_text)
        
        # Should find multiple interfaces
        self.assertGreater(len(interfaces), 0)
        
        # Check specific interface details
        ge_interface = next((i for i in interfaces if i.name == "ge-0/0/0"), None)
        self.assertIsNotNone(ge_interface)
        self.assertEqual(ge_interface.description, "uplink to edge router")
        
        # Check interface with IP address
        vlan_interface = next((i for i in interfaces if i.name == "vlan"), None)
        self.assertIsNotNone(vlan_interface)
    
    def test_vlan_parsing(self):
        """Test VLAN parsing"""
        vlans = self.parser.parse_vlans(self.config_text)
        
        # Should find VLANs
        self.assertGreater(len(vlans), 0)
        
        # Check specific VLAN
        newlab_vlan = next((v for v in vlans if v.name == "newlab200"), None)
        self.assertIsNotNone(newlab_vlan)
        self.assertEqual(newlab_vlan.vlan_id, 200)
        self.assertEqual(newlab_vlan.description, "vlan 200 for the lab")
    
    def test_routing_parsing(self):
        """Test routing parsing"""
        routes = self.parser.parse_routing(self.config_text)
        
        # Should find static routes
        self.assertGreater(len(routes), 0)
        
        # Check default route
        default_route = next((r for r in routes if r.destination == "0.0.0.0/0"), None)
        self.assertIsNotNone(default_route)
        self.assertEqual(default_route.next_hop, "192.168.254.254")
        self.assertEqual(default_route.protocol, "static")
    
    def test_full_config_parsing(self):
        """Test complete configuration parsing"""
        network = self.parser.parse_config(self.config_text)
        
        # Should have one device
        self.assertEqual(len(network.devices), 1)
        
        device = network.devices[0]
        self.assertEqual(device.hostname, "ex3300")
        
        # Should have interfaces
        self.assertGreater(len(device.interfaces), 0)
        
        # Should have routing information
        self.assertIsNotNone(device.routing)
        self.assertIn("routes", device.routing)
        self.assertIn("vlans", device.routing)

class TestMermaidGenerator(unittest.TestCase):
    def setUp(self):
        self.parser = JuniperParser()
        self.generator = MermaidGenerator()
        
        # Load test configuration and parse it
        config_path = os.path.join(os.path.dirname(__file__), '..', 'test-configs', 'ex3300-1.conf')
        with open(config_path, 'r') as f:
            config_text = f.read()
        
        self.network = self.parser.parse_config(config_text)
    
    def test_topology_generation(self):
        """Test topology diagram generation"""
        diagram = self.generator.generate_topology(self.network)
        
        # Should start with graph TD
        self.assertTrue(diagram.startswith("graph TD"))
        
        # Should contain device node
        self.assertIn("ex3300", diagram)
        
        # Should contain interface nodes
        self.assertIn("ge-0/0/0", diagram)
    
    def test_vlan_diagram_generation(self):
        """Test VLAN diagram generation"""
        diagram = self.generator.generate_vlan_diagram(self.network)
        
        # Should start with graph TD
        self.assertTrue(diagram.startswith("graph TD"))
        
        # Should contain VLAN information
        self.assertIn("VLAN 200", diagram)
        self.assertIn("newlab200", diagram)
    
    def test_routing_diagram_generation(self):
        """Test routing diagram generation"""
        diagram = self.generator.generate_routing_diagram(self.network)
        
        # Should start with graph LR
        self.assertTrue(diagram.startswith("graph LR"))
        
        # Should contain route information
        self.assertIn("0.0.0.0/0", diagram)
        self.assertIn("192.168.254.254", diagram)
    
    def test_interface_diagram_generation(self):
        """Test interface diagram generation"""
        diagram = self.generator.generate_interface_diagram(self.network)
        
        # Should start with graph TD
        self.assertTrue(diagram.startswith("graph TD"))
        
        # Should contain interface groups
        self.assertIn("GE Interfaces", diagram)
    
    def test_network_overview_generation(self):
        """Test network overview diagram generation"""
        diagram = self.generator.generate_network_overview(self.network)
        
        # Should start with graph TD
        self.assertTrue(diagram.startswith("graph TD"))
        
        # Should contain styling classes
        self.assertIn("classDef", diagram)
        self.assertIn("class", diagram)
    
    def test_all_diagrams_generation(self):
        """Test generation of all diagram types"""
        diagrams = self.generator.generate_all_diagrams(self.network)
        
        # Should have all diagram types
        expected_types = ["topology", "routing", "vlans", "interfaces", "overview"]
        for diagram_type in expected_types:
            self.assertIn(diagram_type, diagrams)
            self.assertIsInstance(diagrams[diagram_type], str)
            self.assertGreater(len(diagrams[diagram_type]), 0)
    
    def test_id_sanitization(self):
        """Test ID sanitization for Mermaid nodes"""
        # Test normal hostname
        sanitized = self.generator._sanitize_id("ex3300")
        self.assertEqual(sanitized, "ex3300")
        
        # Test hostname with special characters
        sanitized = self.generator._sanitize_id("router-1")
        self.assertEqual(sanitized, "router_1")
        
        # Test hostname starting with number
        sanitized = self.generator._sanitize_id("1router")
        self.assertEqual(sanitized, "node_1router")

if __name__ == '__main__':
    unittest.main() 