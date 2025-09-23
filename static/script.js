// Production Order Tracking System - JavaScript Functions

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// Form validation
function validateForm(formId) {
    var form = document.getElementById(formId);
    if (form.checkValidity() === false) {
        form.classList.add('was-validated');
        return false;
    }
    return true;
}

// Confirmation dialog for delete actions
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// Search functionality with debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Table sorting functionality
function sortTable(tableId, column, dataType) {
    var table = document.getElementById(tableId);
    if (!table) return;
    
    var tbody = table.querySelector('tbody');
    var rows = Array.from(tbody.querySelectorAll('tr'));
    
    var isAscending = table.getAttribute('data-sort-direction') !== 'asc';
    table.setAttribute('data-sort-direction', isAscending ? 'asc' : 'desc');
    
    rows.sort(function(a, b) {
        var aValue = a.cells[column].textContent.trim();
        var bValue = b.cells[column].textContent.trim();
        
        if (dataType === 'number') {
            aValue = parseFloat(aValue) || 0;
            bValue = parseFloat(bValue) || 0;
            return isAscending ? aValue - bValue : bValue - aValue;
        } else if (dataType === 'date') {
            aValue = new Date(aValue);
            bValue = new Date(bValue);
            return isAscending ? aValue - bValue : bValue - aValue;
        } else {
            return isAscending ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
        }
    });
    
    // Re-append sorted rows
    rows.forEach(function(row) {
        tbody.appendChild(row);
    });
    
    // Update sort indicators
    var headers = table.querySelectorAll('th[data-sort]');
    headers.forEach(function(header) {
        header.classList.remove('sort-asc', 'sort-desc');
    });
    
    var currentHeader = table.querySelector('th[data-column="' + column + '"]');
    if (currentHeader) {
        currentHeader.classList.add(isAscending ? 'sort-asc' : 'sort-desc');
    }
}

// Export table to CSV
function exportTableToCSV(tableId, filename) {
    var table = document.getElementById(tableId);
    if (!table) return;
    
    var csv = [];
    var rows = table.querySelectorAll('tr');
    
    for (var i = 0; i < rows.length; i++) {
        var row = [];
        var cols = rows[i].querySelectorAll('td, th');
        
        for (var j = 0; j < cols.length; j++) {
            var cell = cols[j].textContent.trim();
            // Escape quotes and wrap in quotes if contains comma
            if (cell.includes('"')) {
                cell = cell.replace(/"/g, '""');
            }
            if (cell.includes(',') || cell.includes('"') || cell.includes('\n')) {
                cell = '"' + cell + '"';
            }
            row.push(cell);
        }
        csv.push(row.join(','));
    }
    
    var csvContent = csv.join('\n');
    var blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    
    var link = document.createElement('a');
    if (link.download !== undefined) {
        var url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename || 'export.csv');
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Print functionality
function printPage() {
    window.print();
}

// Local storage helpers for user preferences
function saveUserPreference(key, value) {
    try {
        localStorage.setItem('pots_' + key, JSON.stringify(value));
    } catch (e) {
        console.log('Could not save user preference:', e);
    }
}

function getUserPreference(key, defaultValue) {
    try {
        var stored = localStorage.getItem('pots_' + key);
        return stored ? JSON.parse(stored) : defaultValue;
    } catch (e) {
        console.log('Could not load user preference:', e);
        return defaultValue;
    }
}

// Theme toggle (if needed in future)
function toggleTheme() {
    var html = document.documentElement;
    var currentTheme = html.getAttribute('data-bs-theme');
    var newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-bs-theme', newTheme);
    saveUserPreference('theme', newTheme);
}

// Load saved theme preference
document.addEventListener('DOMContentLoaded', function() {
    var savedTheme = getUserPreference('theme', 'dark');
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
});

// Utility functions
function formatDateTime(date) {
    if (!(date instanceof Date)) {
        date = new Date(date);
    }
    return date.toLocaleString('en-GB', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

function formatNumber(num, decimals = 0) {
    return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    }).format(num);
}

// Session timeout warning (optional)
var sessionWarningTimeout;
var sessionTimeout = 30 * 60 * 1000; // 30 minutes

function resetSessionTimer() {
    clearTimeout(sessionWarningTimeout);
    sessionWarningTimeout = setTimeout(function() {
        if (confirm('Your session will expire soon. Do you want to continue?')) {
            resetSessionTimer();
        } else {
            window.location.href = '/logout';
        }
    }, sessionTimeout - 5 * 60 * 1000); // Warning 5 minutes before expiry
}

// Reset timer on user activity
document.addEventListener('click', resetSessionTimer);
document.addEventListener('keypress', resetSessionTimer);
document.addEventListener('scroll', resetSessionTimer);

// Initialize session timer
resetSessionTimer();
