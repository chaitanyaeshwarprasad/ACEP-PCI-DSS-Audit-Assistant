/**
 * ACEP PCI DSS AUDIT ASSISTANT - Optimized JavaScript
 * Created by Chaitanya Eshwar Prasad
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap components with error handling
    try {
        // Initialize tooltips
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));
        
        // Initialize popovers
        const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
        popoverTriggerList.forEach(el => new bootstrap.Popover(el));
    } catch (error) {
        console.warn('Bootstrap components not available:', error);
    }
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(() => {
        document.querySelectorAll('.alert:not(.alert-permanent)').forEach(alert => {
            try {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } catch (error) {
                alert.remove();
            }
        });
    }, 5000);
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Enhanced form validation
    document.querySelectorAll('.needs-validation').forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // File upload enhancement
    document.querySelectorAll('input[type="file"]').forEach(input => {
        input.addEventListener('change', function() {
            const fileName = this.files[0]?.name;
            const feedback = this.parentElement.querySelector('.file-feedback');
            if (feedback && fileName) {
                feedback.textContent = `Selected: ${fileName}`;
                feedback.className = 'file-feedback text-success small';
            }
        });
    });
    
    // Risk score calculation
    const riskForm = document.querySelector('#risk-form');
    if (riskForm) {
        const likelihoodInput = riskForm.querySelector('#likelihood');
        const impactInput = riskForm.querySelector('#impact');
        const scoreDisplay = riskForm.querySelector('#risk-score');
        
        const updateRiskScore = () => {
            const likelihood = parseInt(likelihoodInput.value) || 0;
            const impact = parseInt(impactInput.value) || 0;
            const score = likelihood * impact;
            
            if (scoreDisplay) {
                scoreDisplay.textContent = score;
                scoreDisplay.className = `badge ${getRiskClass(score)}`;
            }
        };
        
        if (likelihoodInput && impactInput) {
            likelihoodInput.addEventListener('change', updateRiskScore);
            impactInput.addEventListener('change', updateRiskScore);
            updateRiskScore(); // Initial calculation
        }
    }
    
    // Control status change handling
    document.querySelectorAll('.control-status').forEach(select => {
        select.addEventListener('change', function() {
            const controlRow = this.closest('tr');
            if (controlRow) {
                updateControlRowStyle(controlRow, this.value);
            }
        });
    });
    
    // Enhanced table interactions
    document.querySelectorAll('.table tbody tr').forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.01)';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // Performance optimization: Lazy load images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
});

// Utility functions
function getRiskClass(score) {
    if (score <= 4) return 'risk-low';
    if (score <= 9) return 'risk-medium';
    return 'risk-high';
}

function updateControlRowStyle(row, status) {
    // Remove existing status classes
    row.classList.remove('table-success', 'table-danger', 'table-warning', 'table-info');
    
    // Add appropriate status class
    switch(status) {
        case 'compliant':
            row.classList.add('table-success');
            break;
        case 'non-compliant':
            row.classList.add('table-danger');
            break;
        case 'not-applicable':
            row.classList.add('table-info');
            break;
        case 'not-assessed':
            row.classList.add('table-warning');
            break;
    }
}

// Enhanced form auto-save functionality
function autoSaveForm(form) {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // Save to localStorage
    localStorage.setItem(`form_${form.id}`, JSON.stringify(data));
    
    // Show save indicator
    const saveIndicator = form.querySelector('.save-indicator') || createSaveIndicator(form);
    saveIndicator.textContent = 'Saved';
    saveIndicator.className = 'save-indicator text-success small';
    
    setTimeout(() => {
        saveIndicator.textContent = '';
        saveIndicator.className = 'save-indicator small';
    }, 2000);
}

function createSaveIndicator(form) {
    const indicator = document.createElement('div');
    indicator.className = 'save-indicator small';
    form.appendChild(indicator);
    return indicator;
}

// Loading state management
function showLoading(element) {
    element.disabled = true;
    element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    
    return function hideLoading() {
        element.disabled = false;
        element.innerHTML = element.dataset.originalText || 'Submit';
    };
}

// File size formatting
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Smooth counter animation
function animateCounter(element, start, end, duration = 1000) {
    const startTime = performance.now();
    
    const step = (timestamp) => {
        const elapsed = timestamp - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(start + (end - start) * progress);
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(step);
        }
    };
    
    requestAnimationFrame(step);
}
