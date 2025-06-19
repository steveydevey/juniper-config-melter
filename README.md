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

### ✅ Phase 3: Web Interface (Completed)
- **FastAPI REST API**: Complete backend with file upload and diagram generation
- **Modern Web Frontend**: Bootstrap-based interface with drag-and-drop file upload
- **Real-time Diagram Preview**: Interactive Mermaid.js diagram rendering
- **Multiple Diagram Views**: Switch between different diagram types
- **Configuration Management**: Upload, view, and manage multiple configurations

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

### Web Interface (Recommended)

1. Start the web server:
```bash
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

3. Upload a Juniper configuration file (.conf or .txt) and view the generated diagrams!

### Command Line Testing

Run the test suite to verify functionality:

```bash
python3 -m unittest tests/test_parser.py -v
```

## Web Interface Features

### 📤 File Upload
- Drag-and-drop or click to upload Juniper configuration files
- Supports .conf and .txt file formats
- Real-time processing with progress indicators

### 📊 Interactive Diagrams
- **Overview**: High-level network summary with key interfaces and VLANs
- **Topology**: Physical interface connections with IP addresses
- **VLANs**: VLAN assignments showing which interfaces belong to each VLAN
- **Interfaces**: Detailed interface grouping by type (GE, XE, etc.)
- **Routing**: Network routing information and paths

### 🔧 Configuration Management
- View uploaded configurations in a list
- Switch between different configurations
- See configuration details and statistics
- Delete configurations when no longer needed

### 🎨 Enhanced Visuals
- Left-to-right diagram layout for better readability
- Color-coded nodes (devices, VLANs, interfaces)
- Professional styling with Bootstrap
- Responsive design for mobile and desktop

## API Endpoints

The web interface provides a complete REST API:

- `GET /` - Main web interface
- `GET /health` - Health check
- `POST /upload` - Upload and parse configuration file
- `GET /parse/{config_id}` - Get parsed network data
- `GET /diagram/{config_id}` - Get specific diagram type
- `GET /diagrams/{config_id}` - Get all diagrams for a configuration
- `GET /configs` - List all uploaded configurations
- `DELETE /config/{config_id}` - Delete a configuration

## Generated Diagrams

The application generates several types of Mermaid.js diagrams:

1. **Overview Diagram**: Styled summary with color-coded elements
2. **Topology Diagram**: Shows physical interface connections
3. **VLAN Diagram**: Visualizes VLAN configurations with interface assignments
4. **Interface Diagram**: Detailed interface grouping and information
5. **Routing Diagram**: Displays routing information and paths

### Example Output

The parser successfully extracts:
- **65 interfaces** from the sample configuration
- **2 VLANs** (newlab200, oob) with interface assignments
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
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css       # Custom styling
│   │   └── js/
│   │       └── app.js          # Frontend JavaScript
│   ├── templates/
│   │   └── index.html          # Main web interface
│   └── main.py                 # FastAPI application
├── tests/
│   └── test_parser.py          # Comprehensive test suite
├── test-configs/
│   └── ex3300-1.conf           # Sample Juniper configuration
├── improved_diagrams/          # Output directory for diagrams
└── requirements.txt
```

## Supported Juniper Config Elements

The parser currently supports:
- ✅ Interface configurations (ge-, xe-, vlan interfaces)
- ✅ IP address extraction
- ✅ Interface descriptions
- ✅ VLAN definitions and interface assignments
- ✅ Static routing
- ✅ Hostname extraction
- ✅ Port mode and VLAN membership

## Development Status

- **Phase 1**: ✅ Complete - Core parser and data models
- **Phase 2**: ✅ Complete - Mermaid.js diagram generation
- **Phase 3**: ✅ Complete - Web interface with FastAPI
- **Phase 4**: 📋 Planned - Advanced features

## Testing

The application includes comprehensive testing:

```bash
# Run parser tests
python3 -m unittest tests/test_parser.py -v

# Test web interface (requires server running)
python3 -c "
import requests
response = requests.get('http://localhost:8000/health')
print('Web interface status:', response.json())
"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

[Add your license information here] 