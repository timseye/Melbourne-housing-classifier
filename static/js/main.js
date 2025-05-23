// Melbourne Housing Classifier - Main JavaScript

// Show loading indicator when form is submitted
function initLoading() {
    const predictionForm = document.getElementById('prediction-form');
    const loaderContainer = document.getElementById('loader-container');
    
    if (predictionForm && loaderContainer) {
        predictionForm.addEventListener('submit', function() {
            loaderContainer.style.display = 'flex';
        });
    }
}

// Basic form validation
function initFormValidation() {
    const predictionForm = document.getElementById('prediction-form');
    
    if (predictionForm) {
        predictionForm.addEventListener('submit', function(e) {
            let isValid = true;
            const requiredFields = predictionForm.querySelectorAll('[required]');
            
            // Check if required fields are filled
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                    
                    // Add error message if not exists
                    let errorMessage = field.parentNode.querySelector('.error-message');
                    if (!errorMessage) {
                        errorMessage = document.createElement('div');
                        errorMessage.className = 'error-message';
                        errorMessage.textContent = 'This field is required';
                        field.parentNode.appendChild(errorMessage);
                    }
                } else {
                    field.classList.remove('error');
                    const errorMessage = field.parentNode.querySelector('.error-message');
                    if (errorMessage) {
                        errorMessage.remove();
                    }
                }
            });
            
            // Check optional numeric fields for valid format if they're not empty
            const optionalNumericFields = ['building_area', 'year_built'];
            optionalNumericFields.forEach(fieldId => {
                const field = document.getElementById(fieldId);
                if (field && field.value.trim() !== '') {
                    // Check if it's a valid number
                    if (isNaN(parseFloat(field.value))) {
                        isValid = false;
                        field.classList.add('error');
                        
                        // Add error message if not exists
                        let errorMessage = field.parentNode.querySelector('.error-message');
                        if (!errorMessage) {
                            errorMessage = document.createElement('div');
                            errorMessage.className = 'error-message';
                            errorMessage.textContent = 'Please enter a valid number or leave empty';
                            field.parentNode.appendChild(errorMessage);
                        }
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
        
        // Add event listeners to remove error state when user types
        const inputFields = predictionForm.querySelectorAll('input, select');
        inputFields.forEach(field => {
            field.addEventListener('input', function() {
                field.classList.remove('error');
                const errorMessage = field.parentNode.querySelector('.error-message');
                if (errorMessage) {
                    errorMessage.remove();
                }
            });
        });
    }
}

// Initialize tooltips for form fields
function initTooltips() {
    const tooltipElements = document.querySelectorAll('.tooltip-icon');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = this.querySelector('.tooltip-text');
            if (tooltip) {
                tooltip.style.visibility = 'visible';
                tooltip.style.opacity = '1';
            }
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltip = this.querySelector('.tooltip-text');
            if (tooltip) {
                tooltip.style.visibility = 'hidden';
                tooltip.style.opacity = '0';
            }
        });
    });
}

// Animate the confidence meter in the results page
function animateConfidenceMeter() {
    const confidenceMeter = document.querySelector('.confidence-meter-fill');
    
    if (confidenceMeter) {
        const confidenceValue = parseFloat(confidenceMeter.getAttribute('data-confidence'));
        confidenceMeter.style.width = confidenceValue + '%';
        
        // Also update the predicted range in the median price context
        const predictedRange = document.querySelector('.predicted-range');
        if (predictedRange) {
            // Calculate a reasonable range width based on confidence (limiting to reasonable min/max)
            const rangeWidth = Math.max(30, Math.min(90, confidenceValue));
            predictedRange.style.width = rangeWidth + '%';
        }
    }
}

// Add animation to skyline on page load
function animateSkyline() {
    const skylineImage = document.querySelector('.skyline-image');
    if (skylineImage) {
        skylineImage.classList.add('skyline-loaded');
    }
}

// Show current date in the footer
function showCurrentDate() {
    const dateElement = document.getElementById('current-date');
    if (dateElement) {
        const now = new Date();
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        dateElement.textContent = now.toLocaleDateString('en-AU', options);
    }
}

// Initialize all features when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize form validation
    initFormValidation();
    
    // Initialize loading indicators
    initLoading();

    // Initialize tooltips
    initTooltips();
    
    // Initialize custom dropdowns
    initCustomDropdowns();
    
    // Animate skyline
    animateSkyline();
    
    // Show current date
    showCurrentDate();
    
    // If on results page, animate the confidence meter
    if (document.querySelector('.confidence-meter')) {
        animateConfidenceMeter();
    }
});

// Function to initialize custom dropdowns
function initCustomDropdowns() {
    // Get all custom dropdown containers
    const dropdowns = document.querySelectorAll('.custom-dropdown');
    
    dropdowns.forEach(dropdown => {
        const input = dropdown.querySelector('.custom-dropdown-input');
        const options = dropdown.querySelector('.dropdown-options');
        
        if (!input || !options) return;
        
        // Toggle dropdown on input click
        input.addEventListener('click', function(e) {
            e.preventDefault();
            options.classList.toggle('show');
        });
        
        // Filter options on input
        input.addEventListener('input', function() {
            const value = this.value.toLowerCase();
            const optionElements = options.querySelectorAll('.dropdown-option');
            
            optionElements.forEach(option => {
                const text = option.textContent.toLowerCase();
                if (text.includes(value)) {
                    option.style.display = 'block';
                } else {
                    option.style.display = 'none';
                }
            });
            
            // Show options list if it was hidden
            if (!options.classList.contains('show')) {
                options.classList.add('show');
            }
        });
        
        // Handle option selection
        options.addEventListener('click', function(e) {
            if (e.target.classList.contains('dropdown-option')) {
                input.value = e.target.textContent.trim();
                options.classList.remove('show');
                
                // Highlight selected option
                const allOptions = options.querySelectorAll('.dropdown-option');
                allOptions.forEach(opt => opt.classList.remove('selected'));
                e.target.classList.add('selected');
                
                // Trigger change event
                const event = new Event('change', { bubbles: true });
                input.dispatchEvent(event);
            }
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!dropdown.contains(e.target)) {
                options.classList.remove('show');
            }
        });
    });
}
