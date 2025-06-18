# Juniper Config Melter - Development Plan

## Project Overview
A Python application that parses Juniper Junos configuration files and translates them into Mermaid.js network topology diagrams. This tool will help network engineers visualize their network configurations and understand the relationships between different network components.

## Core Features
1. **Juniper Config Parser**: Parse Junos configuration files (text format)
2. **Network Component Extraction**: Identify interfaces, routing protocols, VLANs, security zones, etc.
3. **Relationship Mapping**: Map connections between network devices and interfaces
4. **Mermaid.js Generation**: Create network topology diagrams in Mermaid.js format
5. **Web Interface**: Simple web UI to upload configs and view generated diagrams

## Technical Architecture

### 1. Backend (Python)
- **Framework**: FastAPI for REST API
- **Config Parser**: Custom parser using regex and state machines
- **Data Models**: Pydantic models for structured data
- **Dependencies**: 
  - `fastapi` - Web framework
  - `uvicorn` - ASGI server
  - `pydantic` - Data validation
  - `jinja2` - Template engine (for HTML generation)

### 2. Frontend (HTML/JavaScript)
- **Framework**: Vanilla JavaScript with Bootstrap for styling
- **Mermaid.js**: For diagram rendering
- **File Upload**: Drag-and-drop interface for config files
- **Real-time Preview**: Live diagram updates

### 3. Data Flow
```
Juniper Config File → Parser → Network Model → Mermaid Generator → Web Display
```

## Implementation Plan

### Phase 1: Core Parser (Week 1)
1. **Create project structure**
   - Set up Python virtual environment
   - Initialize FastAPI application
   - Create basic directory structure

2. **Build Juniper config parser**
   - Parse interface configurations (`ge-0/0/0`, `xe-0/0/0`, etc.)
   - Extract IP addresses and subnet information
   - Parse routing protocols (OSPF, BGP, static routes)
   - Extract VLAN configurations
   - Parse security zones and policies

3. **Create data models**
   - `Interface` model (name, IP, description, status)
   - `Device` model (hostname, interfaces, routing)
   - `Network` model (devices, connections, topology)

### Phase 2: Mermaid.js Generator (Week 2)
1. **Design diagram templates**
   - Network topology diagram layout
   - Device representation (routers, switches, firewalls)
   - Interface connections and labels
   - Color coding for different device types

2. **Implement Mermaid.js generation**
   - Convert network model to Mermaid.js syntax
   - Generate node definitions for devices
   - Create edge definitions for connections
   - Add styling and formatting

3. **Create diagram types**
   - Physical topology (interface connections)
   - Logical topology (routing protocols)
   - Security zones and policies
   - VLAN diagrams

### Phase 3: Web Interface (Week 3)
1. **Build FastAPI endpoints**
   - `POST /upload` - Upload config file
   - `GET /parse/{file_id}` - Get parsed network data
   - `GET /diagram/{file_id}` - Get Mermaid.js diagram
   - `GET /health` - Health check

2. **Create web frontend**
   - File upload interface
   - Diagram display area
   - Configuration options (diagram type, styling)
   - Export functionality (PNG, SVG)

3. **Add interactive features**
   - Zoom and pan controls
   - Device information tooltips
   - Diagram type switching
   - Real-time updates

### Phase 4: Advanced Features (Week 4)
1. **Multi-device support**
   - Parse multiple config files
   - Build complete network topology
   - Inter-device relationship mapping

2. **Enhanced parsing**
   - Support for different Junos versions
   - Parse complex routing policies
   - Extract QoS configurations
   - Parse firewall rules

3. **Export and sharing**
   - Export diagrams as images
   - Share diagrams via URL
   - Save configurations to database
   - Version control for configs

## File Structure
```
juniper-config-melter/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── models/
│   │   ├── __init__.py
│   │   ├── network.py          # Pydantic models
│   │   └── juniper.py          # Juniper-specific models
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── juniper_parser.py   # Main parser logic
│   │   └── mermaid_generator.py # Mermaid.js generator
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── index.html          # Web interface
│   └── templates/
│       └── diagram.html        # Diagram template
├── tests/
│   ├── __init__.py
│   ├── test_parser.py
│   └── test_mermaid.py
├── examples/
│   └── sample_configs/         # Sample Juniper configs
├── requirements.txt
├── README.md
└── plans.md
```

## Key Components

### 1. Juniper Parser (`parsers/juniper_parser.py`)
```python
class JuniperParser:
    def parse_config(self, config_text: str) -> NetworkModel
    def parse_interfaces(self, config_text: str) -> List[Interface]
    def parse_routing(self, config_text: str) -> List[Route]
    def parse_vlans(self, config_text: str) -> List[VLAN]
```

### 2. Mermaid Generator (`parsers/mermaid_generator.py`)
```python
class MermaidGenerator:
    def generate_topology(self, network: NetworkModel) -> str
    def generate_routing_diagram(self, network: NetworkModel) -> str
    def generate_vlan_diagram(self, network: NetworkModel) -> str
```

### 3. Web Interface (`static/index.html`)
- File upload with drag-and-drop
- Mermaid.js diagram rendering
- Interactive controls
- Export functionality

## Sample Juniper Config Parsing
The parser will handle configurations like:
```
interfaces {
    ge-0/0/0 {
        unit 0 {
            family inet {
                address 192.168.1.1/24;
            }
        }
    }
    ge-0/0/1 {
        unit 0 {
            family inet {
                address 10.0.0.1/30;
            }
        }
    }
}
```

## Success Metrics
1. **Accuracy**: Successfully parse 95%+ of common Juniper config elements
2. **Performance**: Parse 1MB config file in <5 seconds
3. **Usability**: Generate clear, readable network diagrams
4. **Compatibility**: Support Junos versions 15.1 and later

## Future Enhancements
1. **Multi-vendor support**: Cisco, Arista, Nokia
2. **Configuration validation**: Check for common misconfigurations
3. **Network simulation**: Basic traffic flow analysis
4. **Integration**: REST API for external tools
5. **Collaboration**: Multi-user editing and sharing

## Development Environment Setup
1. Python 3.8+
2. Virtual environment
3. FastAPI development server
4. Modern web browser with Mermaid.js support
5. Sample Juniper configuration files for testing

This plan provides a solid foundation for building a comprehensive Juniper configuration visualization tool that will be valuable for network engineers and architects. 