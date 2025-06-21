# Juniper Config Melter - Development Plan

## Project Overview

A Python application that parses Juniper Junos configuration files and translates them into network topology diagrams using the diagrams Python library. This tool helps network engineers visualize their network configurations and understand the relationships between different network components.

## Core Features

1. **Juniper Config Parser**: Parse Junos configuration files (text format)
2. **Network Component Extraction**: Identify interfaces, routing protocols, VLANs, security zones, etc.
3. **Relationship Mapping**: Map connections between network devices and interfaces
4. **Diagrams Library Generation**: Create network topology diagrams using the diagrams Python library
5. **Web Interface**: Simple web UI to upload configs and view generated diagrams
6. **User Experience**: Copy-to-clipboard, delete functionality, and responsive design
7. **Real-time Diagram Display**: Live diagram rendering in the web interface

## Technical Architecture

### 1. Backend (Python)

- **Framework**: FastAPI for REST API
- **Config Parser**: Custom parser using regex and state machines
- **Data Models**: Pydantic models for structured data
- **Diagram Generation**: diagrams Python library with Graphviz backend
- **Dependencies**:
  - `fastapi` - Web framework
  - `uvicorn` - ASGI server
  - `pydantic` - Data validation
  - `diagrams` - Diagram generation library
  - `graphviz` - Diagram rendering backend
  - `jinja2` - Template engine (for HTML generation)

### 2. Frontend (HTML/JavaScript)

- **Framework**: Vanilla JavaScript with custom CSS (no external dependencies)
- **Diagram Display**: SVG rendering of diagrams library output
- **File Upload**: Drag-and-drop interface for config files
- **Real-time Preview**: Live diagram updates
- **User Experience**: Copy-to-clipboard, delete configurations, responsive design
- **Interactive Diagrams**: Zoom, pan, and click interactions

### 3. Data Flow

`Juniper Config File → Parser → Network Model → Diagrams Generator → SVG Output → Web Display`

## Implementation Plan

### Phase 1: Core Parser ✅ COMPLETED

1. **Create project structure** ✅
   - Set up Python virtual environment
   - Initialize FastAPI application
   - Create basic directory structure

2. **Build Juniper config parser** ✅
   - Parse interface configurations (`ge-0/0/0`, `xe-0/0/0`, etc.)
   - Extract IP addresses and subnet information
   - Parse routing protocols (OSPF, BGP, static routes)
   - Extract VLAN configurations
   - Parse security zones and policies

3. **Create data models** ✅
   - `Interface` model (name, IP, description, status)
   - `Device` model (hostname, interfaces, routing)
   - `Network` model (devices, connections, topology)

### Phase 2: Diagrams Library Generator 🔄 IN PROGRESS

1. **Design diagram templates** 🔄
   - Network topology diagram layout using diagrams library
   - Device representation (routers, switches, firewalls) using OnPremises nodes
   - Interface connections and labels with proper styling
   - Color coding for different device types and connection types

2. **Implement diagrams library generation** 🔄
   - Convert network model to diagrams library syntax
   - Generate node definitions for devices using appropriate icons
   - Create edge definitions for connections with labels
   - Add styling and formatting for professional appearance

3. **Create diagram types** 🔄
   - Physical topology (interface connections)
   - Logical topology (routing protocols)
   - Security zones and policies
   - VLAN diagrams
   - Interface diagrams
   - Network overview

### Phase 3: Web Interface with Real-time Diagram Display 🔄 PLANNED

1. **Build FastAPI endpoints** 🔄
   - `POST /upload` - Upload config file
   - `GET /parse/{config_id}` - Get parsed network data
   - `GET /diagrams/{config_id}` - Get all diagrams as SVG
   - `GET /diagram/{config_id}/{diagram_type}` - Get specific diagram as SVG
   - `GET /configs` - List uploaded configurations
   - `DELETE /config/{config_id}` - Delete configuration
   - `GET /health` - Health check

2. **Create web frontend with diagram display** 🔄
   - File upload interface
   - SVG diagram display area with interactive controls
   - Diagram type switching with real-time updates
   - Configuration options (diagram style, layout)
   - Configuration management (list, delete)
   - Self-contained design (no external dependencies)

3. **Add interactive diagram features** 🔄
   - Zoom and pan controls for diagrams
   - Click interactions to show device details
   - Diagram export as PNG/SVG
   - Copy-to-clipboard for diagram code
   - Delete configuration functionality
   - Responsive design for mobile/desktop
   - Loading states and error handling

### Phase 4: Advanced Features 🔄 PLANNED

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
   - Export diagrams as high-resolution images
   - Share diagrams via URL
   - Save configurations to database
   - Version control for configs

4. **Advanced diagram features**
   - Interactive diagram elements with tooltips
   - Device information overlays
   - Network traffic flow visualization
   - Configuration validation indicators

## File Structure

```conf
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
│   │   └── diagrams_generator.py # Diagrams library generator
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css       # Custom CSS (Bootstrap-like)
│   │   ├── js/
│   │   │   └── app.js          # Frontend JavaScript
│   │   └── diagrams/           # Generated diagram files
│   └── templates/
│       └── index.html          # Web interface template
├── tests/
│   ├── __init__.py
│   └── test_parser.py          # Parser tests
├── test-configs/
│   └── ex3300-1.conf           # Sample Juniper config
├── generated_diagrams/          # Generated diagram files (SVG/PNG)
├── requirements.txt
├── README.md
├── plans.md
└── .cursorrules                # Development guidelines
```

## Key Components

### 1. Juniper Parser (`parsers/juniper_parser.py`) ✅

```python
class JuniperParser:
    def parse_config(self, config_text: str) -> NetworkModel
    def parse_interfaces(self, config_text: str) -> List[Interface]
    def parse_routing(self, config_text: str) -> List[Route]
    def parse_vlans(self, config_text: str) -> List[VLAN]
```

### 2. Diagrams Generator (`parsers/diagrams_generator.py`) 🔄

```python
class DiagramsGenerator:
    def generate_topology(self, network: NetworkModel) -> str
    def generate_routing_diagram(self, network: NetworkModel) -> str
    def generate_vlan_diagram(self, network: NetworkModel) -> str
    def generate_interface_diagram(self, network: NetworkModel) -> str
    def generate_network_overview(self, network: NetworkModel) -> str
    def generate_svg(self, diagram_type: str, network: NetworkModel) -> str
```

### 3. Web Interface (`templates/index.html`) 🔄

- File upload with drag-and-drop
- SVG diagram display with zoom/pan controls
- Interactive controls for diagram type selection
- Configuration management (list, delete)
- Responsive design for all devices
- Real-time diagram updates

### 4. User Experience Features 🔄

- Interactive SVG diagrams with click interactions
- Zoom and pan controls for detailed examination
- Copy-to-clipboard functionality for diagram code
- Delete configuration with confirmation dialogs
- Diagram export as PNG/SVG
- Loading states and error handling
- Success/error notifications

## Diagrams Library Integration

### Advantages over Mermaid.js

1. **Better Visual Quality**: Professional-looking diagrams with proper styling
2. **More Control**: Fine-grained control over node placement and styling
3. **Network-Specific Icons**: Built-in icons for routers, switches, firewalls
4. **Scalability**: Better handling of large network diagrams
5. **Export Options**: High-quality image export (PNG, SVG, PDF)
6. **Python Native**: Direct integration with Python backend

### Diagram Types with Diagrams Library

```python
from diagrams import Diagram, Cluster
from diagrams.onprem.network import Router, Switch, Firewall
from diagrams.onprem.compute import Server

# Example topology diagram
with Diagram("Network Topology", show=False):
    with Cluster("Core Network"):
        router = Router("Core Router")
        switch = Switch("Core Switch")
        firewall = Firewall("Firewall")
        
    router >> switch >> firewall
```

### Web Interface Integration

- **SVG Rendering**: Display diagrams as interactive SVG in web browser
- **Real-time Updates**: Generate new diagrams on-the-fly
- **Interactive Elements**: Click on devices to show details
- **Export Functionality**: Download diagrams as high-resolution images

## Sample Juniper Config Parsing

The parser successfully handles configurations like:

```conf
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

## Success Metrics 🔄 TARGETED

1. **Accuracy**: Successfully parse 95%+ of common Juniper config elements 🔄
2. **Performance**: Parse 1MB config file in <5 seconds 🔄
3. **Usability**: Generate clear, professional network diagrams 🔄
4. **Compatibility**: Support Junos versions 15.1 and later 🔄
5. **User Experience**: Intuitive web interface with interactive diagrams 🔄
6. **Visual Quality**: Professional-grade diagram output 🔄

## Current Status

- ✅ **Phase 1**: Core Parser - COMPLETED
- 🔄 **Phase 2**: Diagrams Library Generator - IN PROGRESS
- 🔄 **Phase 3**: Web Interface with Real-time Diagram Display - PLANNED
- 🔄 **Phase 4**: Advanced Features - PLANNED

## Next Steps (Phase 2 - Diagrams Library)

1. **Install diagrams library** - Add to requirements.txt and install dependencies
2. **Create diagrams generator** - Replace MermaidGenerator with DiagramsGenerator
3. **Implement diagram types** - Convert existing Mermaid diagrams to diagrams library format
4. **Test diagram generation** - Verify output quality and performance
5. **Update web interface** - Modify to display SVG diagrams instead of Mermaid code

## Future Enhancements

1. **Multi-vendor support**: netgear, ubiquiti, cisco
2. **Configuration validation**: Check for common misconfigurations
3. **Network simulation**: Basic traffic flow analysis
4. **Integration**: REST API for external tools
5. **Collaboration**: Multi-user editing and sharing
6. **Advanced visualizations**: 3D network diagrams, traffic flow animations
