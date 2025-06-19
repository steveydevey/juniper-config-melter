// Juniper Config Melter - Frontend JavaScript (No external dependencies)

// Global variables
let currentConfigId = null;
let currentDiagrams = {};
let loadingModal = null;

// Simple modal implementation
class SimpleModal {
    constructor(element) {
        this.element = element;
        this.isVisible = false;
        this.setupModal();
    }
    
    setupModal() {
        // Add click handler to close modal when clicking outside
        this.element.addEventListener('click', (e) => {
            if (e.target === this.element) {
                this.hide();
            }
        });
        
        // Add escape key handler
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isVisible) {
                this.hide();
            }
        });
    }
    
    show() {
        this.element.style.display = 'block';
        this.element.classList.add('show');
        this.isVisible = true;
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }
    
    hide() {
        this.element.style.display = 'none';
        this.element.classList.remove('show');
        this.isVisible = false;
        document.body.style.overflow = ''; // Restore scrolling
    }
}

// Copy to clipboard functionality
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch (err) {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            document.body.removeChild(textArea);
            return true;
        } catch (err) {
            document.body.removeChild(textArea);
            return false;
        }
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing application...');
    initializeApp();
});

function initializeApp() {
    // Initialize simple modal
    const modalElement = document.getElementById('loadingModal');
    if (modalElement) {
        loadingModal = new SimpleModal(modalElement);
        console.log('Loading modal initialized');
    } else {
        console.warn('Modal element not available');
        loadingModal = null;
    }
    
    // Initialize other components
    loadConfigurations();
    setupEventListeners();
    console.log('Application initialized');
}

function setupEventListeners() {
    console.log('Setting up event listeners...');
    
    // File upload
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', handleFileUpload);
        console.log('Upload form listener added');
    } else {
        console.error('Upload form not found');
    }
    
    // Diagram type selection
    const diagramControls = document.getElementById('diagramControls');
    if (diagramControls) {
        diagramControls.addEventListener('click', function(e) {
            if (e.target.classList.contains('btn') && e.target.dataset.diagram) {
                showDiagram(e.target.dataset.diagram);
                updateActiveButton(e.target);
            }
        });
        console.log('Diagram controls listener added');
    } else {
        console.error('Diagram controls not found');
    }
}

async function handleFileUpload(e) {
    e.preventDefault();
    console.log('File upload started');
    
    const configFile = document.getElementById('configFile');
    const uploadBtn = document.getElementById('uploadBtn');
    
    if (!configFile || !uploadBtn) {
        console.error('Required elements not found');
        showAlert('Error: Required elements not found', 'danger');
        return;
    }
    
    const file = configFile.files[0];
    if (!file) {
        showAlert('Please select a file to upload.', 'warning');
        return;
    }
    
    console.log('File selected:', file.name, 'Size:', file.size);
    
    // Show loading state
    if (loadingModal) {
        loadingModal.show();
    } else {
        // Fallback loading indicator
        uploadBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Processing...';
    }
    uploadBtn.disabled = true;
    const spinner = uploadBtn.querySelector('.spinner-border');
    if (spinner) {
        spinner.classList.remove('d-none');
    }
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        console.log('Sending upload request...');
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        console.log('Upload response status:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Upload failed:', errorText);
            let errorMessage = 'Upload failed';
            try {
                const error = JSON.parse(errorText);
                errorMessage = error.detail || errorMessage;
            } catch (e) {
                errorMessage = errorText || errorMessage;
            }
            throw new Error(errorMessage);
        }
        
        const result = await response.json();
        console.log('Upload successful:', result);
        
        currentConfigId = result.config_id;
        
        // Load diagrams
        await loadDiagrams(result.config_id);
        
        // Show success message
        showAlert(`Configuration uploaded successfully! Found ${result.device_count} device(s), ${result.interface_count} interface(s), and ${result.vlan_count} VLAN(s).`, 'success');
        
        // Load configuration list
        loadConfigurations();
        
        // Show overview diagram by default
        showDiagram('overview');
        
    } catch (error) {
        console.error('Upload error:', error);
        showAlert(`Upload failed: ${error.message}`, 'danger');
    } finally {
        // Hide loading state
        if (loadingModal) {
            loadingModal.hide();
        }
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<span class="spinner-border spinner-border-sm d-none" role="status"></span>Upload & Parse';
        if (spinner) {
            spinner.classList.add('d-none');
        }
        if (configFile) {
            configFile.value = '';
        }
    }
}

async function loadDiagrams(configId) {
    console.log('Loading diagrams for config:', configId);
    try {
        const response = await fetch(`/diagrams/${configId}`);
        if (!response.ok) {
            throw new Error('Failed to load diagrams');
        }
        
        const result = await response.json();
        currentDiagrams = result.diagrams;
        console.log('Diagrams loaded:', Object.keys(currentDiagrams));
        
        // Load configuration details
        await loadConfigurationDetails(configId);
        
    } catch (error) {
        console.error('Error loading diagrams:', error);
        showAlert('Failed to load diagrams', 'danger');
    }
}

async function loadConfigurationDetails(configId) {
    try {
        const response = await fetch(`/parse/${configId}`);
        if (!response.ok) {
            throw new Error('Failed to load configuration details');
        }
        
        const result = await response.json();
        displayConfigurationDetails(result);
        
    } catch (error) {
        console.error('Error loading configuration details:', error);
    }
}

function displayConfigurationDetails(config) {
    const network = config.network;
    const device = network.devices[0]; // Assuming single device for now
    
    const deviceInfo = document.getElementById('deviceInfo');
    const networkSummary = document.getElementById('networkSummary');
    const configDetails = document.getElementById('configDetails');
    
    if (!deviceInfo || !networkSummary || !configDetails) {
        console.error('Configuration detail elements not found');
        return;
    }
    
    // Device information
    deviceInfo.innerHTML = `
        <div class="info-item">
            <span class="info-label">Hostname:</span>
            <span class="info-value">${device.hostname}</span>
        </div>
        <div class="info-item">
            <span class="info-label">Interfaces:</span>
            <span class="info-value">${device.interfaces.length}</span>
        </div>
        <div class="info-item">
            <span class="info-label">VLANs:</span>
            <span class="info-value">${device.routing?.vlans?.length || 0}</span>
        </div>
        <div class="info-item">
            <span class="info-label">Routes:</span>
            <span class="info-value">${device.routing?.routes?.length || 0}</span>
        </div>
    `;
    
    // Network summary
    const vlans = device.routing?.vlans || [];
    const vlanInfo = vlans.map(vlan => 
        `${vlan.name} (ID: ${vlan.vlan_id})`
    ).join(', ') || 'None';
    
    networkSummary.innerHTML = `
        <div class="info-item">
            <span class="info-label">VLANs:</span>
            <span class="info-value">${vlanInfo}</span>
        </div>
        <div class="info-item">
            <span class="info-label">Interfaces with IP:</span>
            <span class="info-value">${device.interfaces.filter(i => i.ip).length}</span>
        </div>
        <div class="info-item">
            <span class="info-label">Interfaces with VLANs:</span>
            <span class="info-value">${device.interfaces.filter(i => i.vlan_members && i.vlan_members.length > 0).length}</span>
        </div>
    `;
    
    configDetails.style.display = 'block';
}

function showDiagram(diagramType) {
    console.log('Showing diagram:', diagramType);
    
    const diagramContainer = document.getElementById('diagramContainer');
    if (!diagramContainer) {
        console.error('Diagram container not found');
        return;
    }
    
    if (!currentDiagrams[diagramType]) {
        diagramContainer.innerHTML = `
            <div class="text-muted">
                <span style="font-size: 2em;">⚠️</span>
                <p>Diagram type '${diagramType}' not available</p>
            </div>
        `;
        return;
    }
    
    const mermaidCode = currentDiagrams[diagramType];
    
    // Show as text with copy button
    showTextDiagram(diagramContainer, mermaidCode, diagramType);
}

function showTextDiagram(container, mermaidCode, diagramType) {
    const diagramId = `diagram-${Date.now()}`;
    container.innerHTML = `
        <div class="text-center">
            <h5>${diagramType.charAt(0).toUpperCase() + diagramType.slice(1)} Diagram</h5>
            <div class="alert alert-info">
                <p><strong>Diagram Code (Mermaid.js format)</strong></p>
                <p>This diagram can be rendered using Mermaid.js. Here's the code:</p>
                <div class="diagram-code-container">
                    <div class="diagram-code-header">
                        <span>Mermaid.js Code</span>
                        <button class="copy-button" onclick="copyDiagramCode('${diagramId}')">📋 Copy Code</button>
                    </div>
                    <pre id="${diagramId}">${mermaidCode}</pre>
                </div>
                <p><small>💡 Tip: You can copy this code and paste it into a Mermaid.js editor to visualize the diagram.</small></p>
            </div>
        </div>
    `;
}

// Global function for copy button
window.copyDiagramCode = async function(diagramId) {
    const preElement = document.getElementById(diagramId);
    const copyButton = preElement.previousElementSibling.querySelector('.copy-button');
    
    if (!preElement) {
        console.error('Diagram element not found');
        return;
    }
    
    const success = await copyToClipboard(preElement.textContent);
    
    if (success) {
        // Visual feedback
        copyButton.textContent = '✅ Copied!';
        copyButton.classList.add('copied');
        
        // Reset after 2 seconds
        setTimeout(() => {
            copyButton.textContent = '📋 Copy Code';
            copyButton.classList.remove('copied');
        }, 2000);
        
        showAlert('Diagram code copied to clipboard!', 'success');
    } else {
        showAlert('Failed to copy to clipboard', 'danger');
    }
};

function updateActiveButton(activeButton) {
    const diagramControls = document.getElementById('diagramControls');
    if (!diagramControls) return;
    
    // Remove active class from all buttons
    diagramControls.querySelectorAll('.btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Add active class to clicked button
    activeButton.classList.add('active');
}

async function loadConfigurations() {
    try {
        const response = await fetch('/configs');
        if (!response.ok) {
            throw new Error('Failed to load configurations');
        }
        
        const result = await response.json();
        displayConfigurations(result.configs);
        
    } catch (error) {
        console.error('Error loading configurations:', error);
    }
}

function displayConfigurations(configs) {
    const configList = document.getElementById('configList');
    if (!configList) {
        console.error('Config list element not found');
        return;
    }
    
    if (configs.length === 0) {
        configList.innerHTML = '<div class="text-muted">No configurations uploaded yet</div>';
        return;
    }
    
    configList.innerHTML = configs.map(config => `
        <div class="config-list-item" data-config-id="${config.config_id}">
            <div class="config-info">
                <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">${config.filename}</h6>
                    <small class="text-muted">${config.device_count} device(s)</small>
                </div>
                <small class="text-muted">${new Date(config.timestamp).toLocaleString()}</small>
            </div>
            <div class="config-actions">
                <button class="delete-config-btn" onclick="deleteConfiguration('${config.config_id}', event)">🗑️</button>
            </div>
        </div>
    `).join('');
    
    // Add click handlers for configuration selection
    configList.querySelectorAll('.config-list-item').forEach(item => {
        item.addEventListener('click', function(e) {
            // Don't trigger if clicking on delete button
            if (e.target.classList.contains('delete-config-btn')) {
                return;
            }
            
            const configId = this.dataset.configId;
            loadConfiguration(configId);
            
            // Update active state
            configList.querySelectorAll('.config-list-item').forEach(i => i.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

// Global function for delete button
window.deleteConfiguration = async function(configId, event) {
    event.stopPropagation(); // Prevent triggering the config selection
    
    if (!confirm('Are you sure you want to delete this configuration? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`/config/${configId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showAlert('Configuration deleted successfully', 'success');
            
            // If this was the currently selected config, clear the display
            if (currentConfigId === configId) {
                currentConfigId = null;
                currentDiagrams = {};
                const diagramContainer = document.getElementById('diagramContainer');
                if (diagramContainer) {
                    diagramContainer.innerHTML = `
                        <div class="text-center">
                            <div class="text-muted">
                                <span style="font-size: 3em;">📁</span>
                                <p>Upload a Juniper configuration file to generate network diagrams</p>
                            </div>
                        </div>
                    `;
                }
                const configDetails = document.getElementById('configDetails');
                if (configDetails) {
                    configDetails.style.display = 'none';
                }
            }
            
            // Reload the configuration list
            loadConfigurations();
        } else {
            throw new Error('Failed to delete configuration');
        }
    } catch (error) {
        console.error('Error deleting configuration:', error);
        showAlert('Failed to delete configuration', 'danger');
    }
};

async function loadConfiguration(configId) {
    currentConfigId = configId;
    await loadDiagrams(configId);
    showDiagram('overview');
    
    const overviewBtn = document.querySelector('[data-diagram="overview"]');
    if (overviewBtn) {
        updateActiveButton(overviewBtn);
    }
}

function showAlert(message, type) {
    console.log('Showing alert:', type, message);
    
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    // Add to page
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
} 