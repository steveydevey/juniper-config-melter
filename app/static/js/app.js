// Juniper Config Melter - Frontend JavaScript (Diagrams Library Integration)

// Global variables
let currentConfigId = null;
let currentDiagramTypes = [];
let currentDiagramFormat = 'png'; // 'png' or 'svg'
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
        this.element.style.opacity = '1';
        this.isVisible = true;
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }
    
    hide() {
        this.element.style.display = 'none';
        this.element.style.opacity = '0';
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
    
    // Auto-load sample config
    const autoLoadBtn = document.getElementById('autoLoadBtn');
    if (autoLoadBtn) {
        autoLoadBtn.addEventListener('click', handleAutoLoad);
        console.log('Auto-load button listener added');
    } else {
        console.error('Auto-load button not found');
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
    
    // Format selection toggle
    const formatInputs = document.querySelectorAll('input[name="diagramFormat"]');
    formatInputs.forEach(input => {
        input.addEventListener('change', function() {
            currentDiagramFormat = this.value;
            if (currentConfigId && currentDiagramTypes.length > 0) {
                // Re-display current diagram with new format
                const activeDiagramBtn = document.querySelector('#diagramControls .btn.active');
                if (activeDiagramBtn) {
                    showDiagram(activeDiagramBtn.dataset.diagram);
                }
            }
        });
    });
    console.log('Format selection listeners added');
    
    // Style selection toggle
    const styleInputs = document.querySelectorAll('input[name="diagramStyle"]');
    styleInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Show the style change button when style is changed
            const styleChangeSection = document.getElementById('styleChangeSection');
            if (styleChangeSection) {
                styleChangeSection.style.display = 'block';
            }
        });
    });
    console.log('Style selection listeners added');
    
    // Style change button
    const changeStyleBtn = document.getElementById('changeStyleBtn');
    if (changeStyleBtn) {
        changeStyleBtn.addEventListener('click', handleStyleChange);
        console.log('Style change button listener added');
    } else {
        console.error('Style change button not found');
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
        // Create FormData for file upload
        const formData = new FormData();
        formData.append('file', file);
        
        console.log('Uploading file to server...');
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Upload failed');
        }
        
        const result = await response.json();
        console.log('Upload successful:', result);
        
        // Store the config ID and diagram types
        currentConfigId = result.config_id;
        currentDiagramTypes = result.diagram_types || [];
        
        // Show success message
        showAlert(`Configuration uploaded successfully! Generated ${result.diagram_types?.length || 0} diagram types.`, 'success');
        
        // Load configuration details
        await loadConfigurationDetails(currentConfigId);
        
        // Show the first available diagram
        if (currentDiagramTypes.length > 0) {
            showDiagram(currentDiagramTypes[0]);
            // Update the active button
            const firstBtn = document.querySelector(`[data-diagram="${currentDiagramTypes[0]}"]`);
            if (firstBtn) {
                updateActiveButton(firstBtn);
            }
        }
        
        // Refresh configuration list
        await loadConfigurations();
        
        // Clear the file input
        configFile.value = '';
        
    } catch (error) {
        console.error('Upload error:', error);
        showAlert(`Upload failed: ${error.message}`, 'danger');
    } finally {
        // Hide loading state
        if (loadingModal) {
            loadingModal.hide();
        } else {
            // Reset button state
            uploadBtn.innerHTML = 'Upload & Parse';
        }
        uploadBtn.disabled = false;
        if (spinner) {
            spinner.classList.add('d-none');
        }
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
    console.log('Showing diagram:', diagramType, 'Format:', currentDiagramFormat);
    
    const diagramContainer = document.getElementById('diagramContainer');
    if (!diagramContainer) {
        console.error('Diagram container not found');
        return;
    }
    
    if (!currentConfigId) {
        diagramContainer.innerHTML = `
            <div class="text-muted">
                <span style="font-size: 2em;">⚠️</span>
                <p>No configuration selected</p>
            </div>
        `;
        return;
    }
    
    if (!currentDiagramTypes.includes(diagramType)) {
        diagramContainer.innerHTML = `
            <div class="text-muted">
                <span style="font-size: 2em;">⚠️</span>
                <p>Diagram type '${diagramType}' not available</p>
            </div>
        `;
        return;
    }
    
    // Show loading state
    diagramContainer.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading diagram...</span>
            </div>
            <p class="mt-2">Loading ${diagramType} diagram...</p>
        </div>
    `;
    
    // Load the diagram image
    loadDiagramImage(diagramContainer, diagramType);
}

async function loadDiagramImage(container, diagramType) {
    try {
        const imageUrl = `/diagram/${currentConfigId}?diagram_type=${diagramType}&format=${currentDiagramFormat}`;
        console.log('Loading diagram from:', imageUrl);
        
        // Create image element
        const img = new Image();
        img.className = 'img-fluid';
        img.style.maxWidth = '100%';
        img.style.height = 'auto';
        img.style.border = '1px solid #dee2e6';
        img.style.borderRadius = '0.375rem';
        
        // Handle image load success
        img.onload = function() {
            container.innerHTML = `
                <div class="text-center">
                    <h5>${diagramType.charAt(0).toUpperCase() + diagramType.slice(1)} Diagram</h5>
                    <div class="alert alert-info">
                        <p><strong>Network Diagram (${currentDiagramFormat.toUpperCase()})</strong></p>
                        <p>This diagram shows the network topology in visual format.</p>
                        <div class="diagram-container">
                            <img src="${imageUrl}" alt="${diagramType} diagram" class="img-fluid" style="max-width: 100%; height: auto; border: 1px solid #dee2e6; border-radius: 0.375rem;">
                        </div>
                        <div class="mt-3">
                            <a href="${imageUrl}" download="${currentConfigId}_${diagramType}.${currentDiagramFormat}" class="btn btn-primary">
                                💾 Download ${currentDiagramFormat.toUpperCase()}
                            </a>
                            <button class="btn btn-secondary" onclick="copyImageUrl('${imageUrl}')">
                                📋 Copy URL
                            </button>
                        </div>
                        <p><small>💡 Tip: You can switch between PNG and SVG formats using the format controls above.</small></p>
                    </div>
                </div>
            `;
        };
        
        // Handle image load error
        img.onerror = function() {
            container.innerHTML = `
                <div class="text-center">
                    <div class="text-muted">
                        <span style="font-size: 2em;">⚠️</span>
                        <p>Failed to load diagram</p>
                        <p><small>The diagram file may not exist or there was an error loading it.</small></p>
                    </div>
                </div>
            `;
        };
        
        // Set the source to trigger loading
        img.src = imageUrl;
        
    } catch (error) {
        console.error('Error loading diagram:', error);
        container.innerHTML = `
            <div class="text-center">
                <div class="text-muted">
                    <span style="font-size: 2em;">⚠️</span>
                    <p>Error loading diagram</p>
                    <p><small>${error.message}</small></p>
                </div>
            </div>
        `;
    }
}

// Global function for copying image URL
window.copyImageUrl = async function(imageUrl) {
    const success = await copyToClipboard(imageUrl);
    
    if (success) {
        showAlert('Image URL copied to clipboard!', 'success');
    } else {
        showAlert('Failed to copy URL to clipboard', 'danger');
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
            // Don't trigger if clicking delete button
            if (e.target.classList.contains('delete-config-btn')) {
                return;
            }
            
            const configId = this.dataset.configId;
            loadConfiguration(configId);
        });
    });
}

// Global function for deleting configurations
window.deleteConfiguration = async function(configId, event) {
    event.stopPropagation(); // Prevent triggering config selection
    
    if (!confirm('Are you sure you want to delete this configuration?')) {
        return;
    }
    
    try {
        const response = await fetch(`/config/${configId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showAlert('Configuration deleted successfully', 'success');
            
            // If this was the current config, clear it
            if (currentConfigId === configId) {
                currentConfigId = null;
                currentDiagramTypes = [];
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
            
            // Refresh the configuration list
            await loadConfigurations();
        } else {
            throw new Error('Failed to delete configuration');
        }
    } catch (error) {
        console.error('Error deleting configuration:', error);
        showAlert('Failed to delete configuration', 'danger');
    }
};

async function loadConfiguration(configId) {
    console.log('Loading configuration:', configId);
    
    // Update current config
    currentConfigId = configId;
    
    // Load configuration details
    await loadConfigurationDetails(configId);
    
    // Get available diagram types from the upload response
    // For now, we'll assume all diagram types are available
    currentDiagramTypes = ['overview', 'topology', 'interfaces', 'vlans', 'untagged_ports', 'routing'];
    
    // Show the first diagram
    showDiagram('overview');
    
    // Update the active button
    const overviewBtn = document.querySelector('[data-diagram="overview"]');
    if (overviewBtn) {
        updateActiveButton(overviewBtn);
    }
}

async function handleAutoLoad(event) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    console.log('Auto-loading sample configuration...');
    
    const autoLoadBtn = document.getElementById('autoLoadBtn');
    if (!autoLoadBtn) {
        console.error('Auto-load button not found');
        showAlert('Error: Auto-load button not found', 'danger');
        return;
    }
    
    // Show loading state
    if (loadingModal) {
        loadingModal.show();
    } else {
        // Fallback loading indicator
        autoLoadBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Loading Sample...';
    }
    autoLoadBtn.disabled = true;
    const spinner = autoLoadBtn.querySelector('.spinner-border');
    if (spinner) {
        spinner.classList.remove('d-none');
    }
    
    try {
        // First, fetch the sample configuration file
        console.log('Fetching sample configuration file...');
        const configResponse = await fetch('/sample-config');
        
        if (!configResponse.ok) {
            throw new Error('Failed to fetch sample configuration file');
        }
        
        const configBlob = await configResponse.blob();
        const configFile = new File([configBlob], 'ex3300-1.conf', { type: 'text/plain' });
        
        console.log('Sample config loaded, uploading to server...');
        
        // Create FormData and upload the sample config
        const formData = new FormData();
        formData.append('file', configFile);
        
        const uploadResponse = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        if (!uploadResponse.ok) {
            const errorData = await uploadResponse.json();
            throw new Error(errorData.detail || 'Upload failed');
        }
        
        const result = await uploadResponse.json();
        console.log('Auto-load successful:', result);
        
        // Store the config ID and diagram types
        currentConfigId = result.config_id;
        currentDiagramTypes = result.diagram_types || [];
        
        // Show success message
        showAlert(`Sample configuration loaded successfully! Generated ${result.diagram_types?.length || 0} diagram types.`, 'success');
        
        // Load configuration details and refresh the list
        await loadConfigurationDetails(currentConfigId);
        await loadConfigurations();
        
        // Show the overview diagram by default
        if (currentDiagramTypes.includes('overview')) {
            showDiagram('overview');
            const overviewBtn = document.querySelector('#diagramControls [data-diagram="overview"]');
            if (overviewBtn) {
                updateActiveButton(overviewBtn);
            }
        }
        
    } catch (error) {
        console.error('Auto-load failed:', error);
        showAlert(`Auto-load failed: ${error.message}`, 'danger');
    } finally {
        // Reset button state
        if (loadingModal) {
            loadingModal.hide();
        }
        autoLoadBtn.disabled = false;
        autoLoadBtn.innerHTML = '<span class="spinner-border spinner-border-sm d-none" role="status"></span>🚀 Auto-Load Sample Config';
        const spinner = autoLoadBtn.querySelector('.spinner-border');
        if (spinner) {
            spinner.classList.add('d-none');
        }
    }
}

async function handleStyleChange() {
    console.log('Style change requested');
    
    if (!currentConfigId) {
        showAlert('No configuration loaded. Please upload a configuration first.', 'warning');
        return;
    }
    
    const changeStyleBtn = document.getElementById('changeStyleBtn');
    if (!changeStyleBtn) {
        console.error('Style change button not found');
        return;
    }
    
    // Get the selected style
    const selectedStyle = document.querySelector('input[name="diagramStyle"]:checked');
    if (!selectedStyle) {
        showAlert('Please select a diagram style.', 'warning');
        return;
    }
    
    const useMindmapStyle = selectedStyle.value === 'mindmap';
    console.log('Selected style:', selectedStyle.value, 'Use mind-map:', useMindmapStyle);
    
    // Show loading state
    if (loadingModal) {
        loadingModal.show();
    } else {
        // Fallback loading indicator
        changeStyleBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Regenerating...';
    }
    changeStyleBtn.disabled = true;
    const spinner = changeStyleBtn.querySelector('.spinner-border');
    if (spinner) {
        spinner.classList.remove('d-none');
    }
    
    try {
        // Call the regenerate endpoint
        const response = await fetch(`/regenerate-diagrams/${currentConfigId}?use_mindmap_style=${useMindmapStyle}`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Style regeneration failed');
        }
        
        const result = await response.json();
        console.log('Style regeneration successful:', result);
        
        // Update current diagram types
        currentDiagramTypes = result.diagram_types || [];
        
        // Show success message
        const styleName = useMindmapStyle ? 'mind-map' : 'hierarchical';
        showAlert(`Diagrams regenerated successfully with ${styleName} style!`, 'success');
        
        // Re-display current diagram with new style
        const activeDiagramBtn = document.querySelector('#diagramControls .btn.active');
        if (activeDiagramBtn) {
            showDiagram(activeDiagramBtn.dataset.diagram);
        }
        
        // Hide the style change section
        const styleChangeSection = document.getElementById('styleChangeSection');
        if (styleChangeSection) {
            styleChangeSection.style.display = 'none';
        }
        
    } catch (error) {
        console.error('Style change error:', error);
        showAlert(`Style change failed: ${error.message}`, 'danger');
    } finally {
        // Reset button state
        if (loadingModal) {
            loadingModal.hide();
        }
        changeStyleBtn.disabled = false;
        changeStyleBtn.innerHTML = '<span class="spinner-border spinner-border-sm d-none" role="status"></span>🔄 Regenerate with New Style';
        const spinner = changeStyleBtn.querySelector('.spinner-border');
        if (spinner) {
            spinner.classList.add('d-none');
        }
    }
}

function showAlert(message, type) {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to page
    document.body.appendChild(alertDiv);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
    
    // Manual dismiss
    const closeBtn = alertDiv.querySelector('.btn-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            if (alertDiv.parentNode) {
                alertDiv.parentNode.removeChild(alertDiv);
            }
        });
    }
} 