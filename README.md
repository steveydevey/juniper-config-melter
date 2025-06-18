# Juniper Config Melter

## Overview
A Python application to parse Juniper Junos configuration files and translate them into Mermaid.js network topology diagrams.

## Setup
1. Create and activate a virtual environment:
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the API
Start the FastAPI server:
```sh
.venv/bin/uvicorn app.main:app --reload
```

Check the health endpoint:
```
curl http://127.0.0.1:8000/health
```

## Testing
Run the parser tests:
```sh
python -m unittest tests/test_parser.py
``` 