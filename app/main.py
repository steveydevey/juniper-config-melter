from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
import tempfile
import uuid
import logging
from typing import Dict, Optional

from app.parsers.juniper_parser import JuniperParser
from app.parsers.diagrams_generator import DiagramsGenerator
from app.models.network import Network

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Juniper Config Melter", version="1.0.0")

# Initialize parsers
parser = JuniperParser()
generator = DiagramsGenerator()

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# In-memory storage for demo purposes (in production, use a database)
config_storage: Dict[str, dict] = {}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Main web interface"""
    logger.info("Serving main page")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {"status": "healthy", "service": "juniper-config-melter"}

@app.post("/upload")
async def upload_config(file: UploadFile = File(...)):
    """Upload and parse a Juniper configuration file"""
    logger.info(f"Upload request received for file: {file.filename}")
    
    if not file.filename or not file.filename.endswith(('.conf', '.txt')):
        logger.warning(f"Invalid file type: {file.filename}")
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .conf or .txt file")
    
    try:
        # Read file content
        logger.info("Reading file content...")
        content = await file.read()
        config_text = content.decode('utf-8')
        logger.info(f"File read successfully, size: {len(config_text)} characters")
        
        # Generate unique ID for this configuration
        config_id = str(uuid.uuid4())
        logger.info(f"Generated config ID: {config_id}")
        
        # Parse configuration
        logger.info("Parsing configuration...")
        network = parser.parse_config(config_text)
        logger.info(f"Configuration parsed successfully: {len(network.devices)} devices")
        
        # Generate diagrams
        logger.info("Generating diagrams...")
        diagrams = generator.generate_all_diagrams(network, config_id)
        logger.info(f"Diagrams generated: {list(diagrams.keys())}")
        
        # Store results
        config_storage[config_id] = {
            "filename": file.filename,
            "network": network.dict(),
            "diagrams": diagrams,
            "timestamp": "2024-01-01T00:00:00Z"  # In production, use actual timestamp
        }
        
        result = {
            "config_id": config_id,
            "filename": file.filename,
            "device_count": len(network.devices),
            "interface_count": sum(len(device.interfaces) for device in network.devices),
            "vlan_count": sum(len(device.routing.get("vlans", [])) for device in network.devices),
            "diagram_types": list(diagrams.keys())
        }
        
        logger.info(f"Upload completed successfully: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error processing configuration: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing configuration: {str(e)}")

@app.get("/parse/{config_id}")
async def get_parsed_config(config_id: str):
    """Get parsed network data for a configuration"""
    logger.info(f"Parse request for config: {config_id}")
    if config_id not in config_storage:
        logger.warning(f"Configuration not found: {config_id}")
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    config_data = config_storage[config_id]
    return {
        "config_id": config_id,
        "filename": config_data["filename"],
        "network": config_data["network"]
    }

@app.get("/diagram/{config_id}")
async def get_diagram(
    config_id: str, 
    diagram_type: str = "topology",
    format: str = Query("png", description="Diagram format: png or svg")
):
    """Get a specific diagram for a configuration"""
    logger.info(f"Diagram request for config: {config_id}, type: {diagram_type}, format: {format}")
    
    if config_id not in config_storage:
        logger.warning(f"Configuration not found: {config_id}")
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    if format not in ["png", "svg"]:
        raise HTTPException(status_code=400, detail="Format must be 'png' or 'svg'")
    
    config_data = config_storage[config_id]
    diagrams = config_data["diagrams"]
    
    if diagram_type not in diagrams:
        logger.warning(f"Diagram type not available: {diagram_type}")
        raise HTTPException(status_code=400, detail=f"Diagram type '{diagram_type}' not available")
    
    # Get the diagram file path
    diagram_path = diagrams[diagram_type].get(format)
    if not diagram_path or not os.path.exists(diagram_path):
        logger.warning(f"Diagram file not found: {diagram_path}")
        raise HTTPException(status_code=404, detail="Diagram file not found")
    
    # Return the file
    return FileResponse(
        path=diagram_path,
        media_type=f"image/{format}",
        filename=f"{config_id}_{diagram_type}.{format}"
    )

@app.get("/diagrams/{config_id}")
async def get_all_diagrams(config_id: str):
    """Get all diagrams for a configuration"""
    logger.info(f"All diagrams request for config: {config_id}")
    if config_id not in config_storage:
        logger.warning(f"Configuration not found: {config_id}")
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    config_data = config_storage[config_id]
    return {
        "config_id": config_id,
        "filename": config_data["filename"],
        "diagrams": config_data["diagrams"]
    }

@app.get("/configs")
async def list_configs():
    """List all uploaded configurations"""
    logger.info("Config list request")
    configs = []
    for config_id, data in config_storage.items():
        configs.append({
            "config_id": config_id,
            "filename": data["filename"],
            "timestamp": data["timestamp"],
            "device_count": len(data["network"]["devices"])
        })
    logger.info(f"Returning {len(configs)} configurations")
    return {"configs": configs}

@app.delete("/config/{config_id}")
async def delete_config(config_id: str):
    """Delete a configuration"""
    logger.info(f"Delete request for config: {config_id}")
    if config_id not in config_storage:
        logger.warning(f"Configuration not found: {config_id}")
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    del config_storage[config_id]
    logger.info(f"Configuration deleted: {config_id}")
    return {"message": "Configuration deleted successfully"}

@app.get("/sample-config")
async def get_sample_config():
    """Serve the sample configuration file for auto-loading"""
    sample_config_path = "test-configs/ex3300-1.conf"
    if not os.path.exists(sample_config_path):
        raise HTTPException(status_code=404, detail="Sample configuration file not found")
    
    return FileResponse(
        path=sample_config_path,
        media_type="text/plain",
        filename="ex3300-1.conf"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 