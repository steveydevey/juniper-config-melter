# Juniper Config Melter

A Python application that parses Juniper Junos configuration files and translates them into professional network topology diagrams using the diagrams Python library. This tool helps network engineers visualize their network configurations and understand the relationships between different network components.

## Features

### ✅ Phase 1: Core Parser (Completed)
- **Juniper Config Parser**: Parse Junos configuration files (text format)
- **Network Component Extraction**: Identify interfaces, routing protocols, VLANs
- **Data Models**: Pydantic models for structured data representation

### ✅ Phase 2: Diagrams Library Generator (Completed)
- **Professional Diagram Generation**: Using the diagrams Python library with Graphviz backend
- **Multiple Diagram Types**: Generate different types of network diagrams
  - Physical topology diagrams
  - Logical routing diagrams  
  - VLAN diagrams with complete interface visibility
  - Interface diagrams with detailed grouping
  - Network overview diagrams
- **Styled Diagrams**: Color-coded nodes for different device types and VLANs
- **Comprehensive Parsing**: Extract hostnames, interfaces, IP addresses, VLANs, and routes
- **Dual Format Output**: Generate both PNG and SVG formats

### ✅ Phase 3: Web Interface (Completed)
- **FastAPI REST API**: Complete backend with file upload and diagram generation
- **Modern Web Frontend**: Self-contained interface with no external dependencies
- **Real-time Diagram Preview**: Interactive diagram display with image files
- **Multiple Diagram Views**: Switch between different diagram types
- **Configuration Management**: Upload, view, and manage multiple configurations

### ✅ Phase 3 Enhancements: User Experience (Completed)
- **Copy-to-Clipboard**: One-click copying of diagram code with visual feedback
- **Delete Functionality**: Remove configurations with confirmation dialogs
- **Left-Justified Text**: Better readability for diagram code display
- **Self-Contained Design**: No external CDN dependencies for offline functionality
- **Enhanced UI**: Improved configuration list and responsive design

### ✅ Phase 4: Diagrams Library Migration (Completed)
- **Migration from Mermaid.js**: Replaced with diagrams Python library for better quality
- **Professional Output**: High-quality PNG and SVG diagram files
- **File-Based Serving**: Direct file serving instead of code generation
- **Enhanced Layout**: Optimized spacing and clustering for better readability
- **Color Coding**: Consistent color schemes for VLANs and device types

### ✅ Phase 5: VLAN Diagram Enhancements (Completed)
- **Complete Interface Visibility**: VLAN diagram now shows ALL interfaces (65 total)
- **VLAN Assignment Status**: Clear categorization of VLAN-assigned vs untagged interfaces
- **Color Coding**: Red for newlab VLANs, orange for oob VLANs, blue for untagged
- **Layout Optimization**: Improved spacing and clustering for dense diagrams
- **Auto-Load Sample**: One-click loading of sample configuration for testing

### 📋 Phase 6: Advanced Features (Planned)
- Multi-device support
- Enhanced parsing capabilities
- Export and sharing features
- Database integration for persistent storage
- Interactive diagram elements with tooltips

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

3. Upload a Juniper configuration file (.conf or .txt) or use the "Auto-Load Sample Config" button to test with the included sample!

### Command Line Testing

Run the test suite to verify functionality:

```bash
python3 -m unittest tests/test_parser.py -v
```

## Web Interface Features

### 📤 File Upload
- Drag-and-drop or click to upload Juniper configuration files
- **Auto-Load Sample**: One-click loading of the included sample configuration
- Supports .conf and .txt file formats
- Real-time processing with progress indicators
- Automatic parsing and diagram generation

### 📊 Interactive Diagrams
- **Overview**: High-level network summary with key interfaces and VLANs
- **Topology**: Physical interface connections with IP addresses
- **VLANs**: Complete VLAN assignments showing ALL interfaces with VLAN status
- **Interfaces**: Detailed interface grouping by type (GE, XE, etc.)
- **Routing**: Network routing information and paths

### 🔧 Configuration Management
- View uploaded configurations in a list with details
- Switch between different configurations
- See configuration details and statistics
- **Delete configurations** with confirmation dialogs
- Automatic list refresh after operations

### 🎨 Enhanced User Experience
- **Copy-to-Clipboard**: Click the 📋 button to copy diagram code instantly
- **Left-justified text**: Better readability for diagram code
- **Visual feedback**: Success/error notifications for all operations
- **Responsive design**: Works on mobile and desktop
- **Self-contained**: No external dependencies, works offline
- **Loading states**: Clear feedback during file processing
- **Auto-Load Sample**: Quick testing with included configuration

### 📋 Diagram Code Management
- **Easy Copying**: One-click copy button for each diagram
- **Visual Feedback**: Button changes to "✅ Copied!" when successful
- **Fallback Support**: Works in older browsers with clipboard API fallback
- **Error Handling**: Clear messages if copying fails

## API Endpoints

The web interface provides a complete REST API:

- `GET /` - Main web interface
- `GET /health` - Health check
- `GET /sample-config` - Get sample configuration file for auto-loading
- `POST /upload` - Upload and parse configuration file
- `GET /parse/{config_id}` - Get parsed network data
- `GET /diagram/{config_id}` - Get specific diagram (PNG/SVG)
- `GET /configs` - List all uploaded configurations
- `DELETE /config/{config_id}` - Delete a configuration

## Generated Diagrams

The application generates several types of professional diagrams using the diagrams Python library:

1. **Overview Diagram**: Styled summary with color-coded elements
2. **Topology Diagram**: Shows physical interface connections
3. **VLAN Diagram**: Complete VLAN visualization with ALL interfaces and color coding
4. **Interface Diagram**: Detailed interface grouping and information
5. **Routing Diagram**: Displays routing information and paths

### Example Output

The parser successfully extracts:
- **65 interfaces** from the sample configuration
- **2 VLANs** (newlab200, oob) with interface assignments
- **1 static route** (default route)
- **Hostname**: ex3300

### VLAN Diagram Enhancements

The VLAN diagram now provides complete visibility:
- **8 VLAN-assigned interfaces**: Grouped under their respective VLANs
- **57 untagged interfaces**: All interfaces not assigned to named VLANs
- **Color coding**: Red for newlab, orange for oob, blue for untagged
- **Complete inventory**: No missing interfaces in the VLAN view

## Project Structure

```
juniper-config-melter/
├── app/
│   ├── models/
│   │   ├── network.py          # Core network models
│   │   └── juniper.py          # Juniper-specific models
│   ├── parsers/
│   │   ├── juniper_parser.py   # Main parser logic
│   │   └── diagrams_generator.py # Diagrams library generator
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css       # Custom styling (Bootstrap-like)
│   │   └── js/
│   │       └── app.js          # Frontend JavaScript
│   ├── templates/
│   │   └── index.html          # Main web interface
│   └── main.py                 # FastAPI application
├── tests/
│   └── test_parser.py          # Comprehensive test suite
├── test-configs/
│   └── ex3300-1.conf           # Sample Juniper configuration
├── generated_diagrams/          # Generated diagram files (PNG/SVG)
├── requirements.txt
├── README.md
├── plans.md
└── .cursorrules                # Development guidelines
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
- **Phase 2**: ✅ Complete - Diagrams library diagram generation
- **Phase 3**: ✅ Complete - Web interface with FastAPI
- **Phase 3 Enhancements**: ✅ Complete - User experience improvements
- **Phase 4**: ✅ Complete - Diagrams library migration
- **Phase 5**: ✅ Complete - VLAN diagram enhancements and layout optimization
- **Phase 6**: 📋 Planned - Advanced features

## Key User Experience Features

### 🎯 Copy-to-Clipboard Functionality
- **Modern API**: Uses navigator.clipboard API with fallback
- **Visual Feedback**: Button changes appearance when copying
- **Cross-browser**: Works in all modern browsers
- **Error Handling**: Graceful fallback for older browsers

### 🗑️ Delete Configuration Management
- **Confirmation Dialogs**: Prevents accidental deletions
- **Visual Feedback**: Success/error notifications
- **State Cleanup**: Automatically clears display when current config is deleted
- **List Refresh**: Updates configuration list automatically

### 📱 Self-Contained Design
- **No External Dependencies**: Works offline without internet
- **No CORS Issues**: No external CDN resources
- **Fast Loading**: No external resource downloads
- **Consistent Behavior**: No version conflicts or outages

### 🚀 Auto-Load Sample Configuration
- **One-Click Loading**: Instant access to sample configuration
- **Quick Testing**: No need to locate and upload files manually
- **Consistent Demo**: Always uses the same sample for testing
- **User-Friendly**: Perfect for first-time users

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

# Test API endpoints
curl -X POST -F "file=@test-configs/ex3300-1.conf" http://localhost:8000/upload
curl http://localhost:8000/configs
curl http://localhost:8000/sample-config
```

## Technical Highlights

### Frontend Architecture
- **Vanilla JavaScript**: No external framework dependencies
- **Custom CSS**: Bootstrap-like styling without external CDN
- **Modern APIs**: Clipboard API, Fetch API, async/await
- **Responsive Design**: Mobile-first approach

### Backend Architecture
- **FastAPI**: Modern, fast Python web framework
- **Pydantic Models**: Type-safe data validation
- **Diagrams Library**: Professional diagram generation with Graphviz
- **Async Processing**: Non-blocking file upload and parsing
- **RESTful API**: Clean, consistent endpoint design

### Diagram Generation
- **Diagrams Python Library**: Professional-quality network diagrams
- **Graphviz Backend**: Industry-standard graph rendering
- **Dual Format Output**: PNG and SVG formats for different use cases
- **Optimized Layouts**: Efficient use of space with clustering and staggering
- **Color Coding**: Consistent visual language for different network elements

### User Experience Design
- **Progressive Enhancement**: Works in all browsers
- **Accessibility**: Keyboard navigation and screen reader support
- **Performance**: Optimized for fast loading and response
- **Error Handling**: Comprehensive error messages and recovery
- **Complete Visibility**: All interfaces shown in VLAN diagrams

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

[Add your license information here] 