# Juniper Config Melter

A Python application that parses Juniper Junos configuration files and translates them into Mermaid.js network topology diagrams. This tool helps network engineers visualize their network configurations and understand the relationships between different network components.

## Features

### ✅ Phase 1: Core Parser (Completed)
- **Juniper Config Parser**: Parse Junos configuration files (text format)
- **Network Component Extraction**: Identify interfaces, routing protocols, VLANs
- **Data Models**: Pydantic models for structured data representation

### ✅ Phase 2: Mermaid.js Generator (Completed)
- **Multiple Diagram Types**: Generate different types of network diagrams
  - Physical topology diagrams
  - Logical routing diagrams  
  - VLAN diagrams
  - Interface diagrams
  - Network overview diagrams
- **Styled Diagrams**: Color-coded nodes for different device types
- **Comprehensive Parsing**: Extract hostnames, interfaces, IP addresses, VLANs, and routes

### 🚧 Phase 3: Web Interface (In Progress)
- FastAPI REST endpoints
- Web frontend with file upload
- Real-time diagram preview

### 📋 Phase 4: Advanced Features (Planned)
- Multi-device support
- Enhanced parsing capabilities
- Export and sharing features

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd juniper-config-melter
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

## Usage

### Command Line Demo

Run the Phase 2 demo to see the parser and diagram generator in action:

```bash
python3 demo_phase2.py
```

This will:
- Parse the sample Juniper configuration
- Extract network information (interfaces, VLANs, routes)
- Generate multiple types of Mermaid.js diagrams
- Save diagrams to the `generated_diagrams/` directory

### Testing

Run the test suite to verify functionality:

```bash
python3 -m unittest tests/test_parser.py -v
```

## Generated Diagrams

The application generates several types of Mermaid.js diagrams:

1. **Topology Diagram**: Shows physical interface connections
2. **Routing Diagram**: Displays routing information and paths
3. **VLAN Diagram**: Visualizes VLAN configurations
4. **Interface Diagram**: Detailed interface grouping and information
5. **Overview Diagram**: Styled summary with color-coded elements

### Example Output

The parser successfully extracts:
- **57 interfaces** from the sample configuration
- **2 VLANs** (newlab200, oob)
- **1 static route** (default route)
- **Hostname**: ex3300

## Project Structure

```
juniper-config-melter/
├── app/
│   ├── models/
│   │   ├── network.py          # Core network models
│   │   └── juniper.py          # Juniper-specific models
│   ├── parsers/
│   │   ├── juniper_parser.py   # Main parser logic
│   │   └── mermaid_generator.py # Mermaid.js generator
│   └── main.py                 # FastAPI application
├── tests/
│   └── test_parser.py          # Comprehensive test suite
├── test-configs/
│   └── ex3300-1.conf           # Sample Juniper configuration
├── generated_diagrams/          # Output directory for diagrams
├── demo_phase2.py              # Phase 2 demonstration script
└── requirements.txt
```

## Supported Juniper Config Elements

The parser currently supports:
- ✅ Interface configurations (ge-, xe-, vlan interfaces)
- ✅ IP address extraction
- ✅ Interface descriptions
- ✅ VLAN definitions and IDs
- ✅ Static routing
- ✅ Hostname extraction

## Development Status

- **Phase 1**: ✅ Complete - Core parser and data models
- **Phase 2**: ✅ Complete - Mermaid.js diagram generation
- **Phase 3**: 🚧 In Progress - Web interface development
- **Phase 4**: 📋 Planned - Advanced features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

[Add your license information here] 