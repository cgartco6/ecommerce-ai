// static/js/main.js
// Main JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    initializePlatform();
    setupEventListeners();
});

function initializePlatform() {
    // Initialize any platform-specific JavaScript
    console.log('AI Learning Platform initialized');
}

function setupEventListeners() {
    // Setup modal close buttons
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        const closeBtn = modal.querySelector('.close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                modal.style.display = 'none';
            });
        }
        
        // Close modal when clicking outside
        window.addEventListener('click', (event) => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    });
    
    // Setup chat widget
    const chatWidget = document.getElementById('chatWidget');
    if (chatWidget) {
        chatWidget.addEventListener('click', () => {
            window.location.href = '/chat';
        });
    }
}

// Enrollment modal functions
function showCourseModal(courseId) {
    fetch(`/api/courses/${courseId}`)
        .then(response => response.json())
        .then(course => {
            const modal = document.getElementById('enrollmentModal');
            const modalBody = modal.querySelector('.modal-body');
            
            modalBody.innerHTML = `
                <div class="enrollment-modal">
                    <div class="urgency-alert">
                        ⚡ Only 27 spots left at this price!
                    </div>
                    
                    <div class="course-summary">
                        <h3>${course.title}</h3>
                        <p>${course.description}</p>
                        
                        <div class="pricing-breakdown">
                            <div class="price-original">WAS: R${course.original_price}</div>
                            <div class="price-current">NOW: R${course.price}/month</div>
                            <div class="savings">You save R${course.original_price - course.price}</div>
                        </div>
                    </div>
                    
                    <div class="enrollment-form">
                        <h4>Secure Your Spot</h4>
                        <form id="enrollmentForm">
                            <div class="form-group">
                                <label>Full Name</label>
                                <input type="text" required>
                            </div>
                            <div class="form-group">
                                <label>Email</label>
                                <input type="email" required>
                            </div>
                            <div class="form-group">
                                <label>Payment Method</label>
                                <select required>
                                    <option value="fnb">FNB Transfer</option>
                                    <option value="credit_card">Credit Card</option>
                                    <option value="debit_card">Debit Card</option>
                                </select>
                            </div>
                            <button type="submit" class="enroll-btn">
                                🔥 Enroll Now - Transform My Life!
                            </button>
                        </form>
                    </div>
                    
                    <div class="bonuses">
                        <h5>🎁 LIMITED TIME BONUSES:</h5>
                        <ul>
                            <li>1-on-1 AI Mentor Session (Value: R2,997)</li>
                            <li>Private Success Community Access</li>
                            <li>Lifetime Course Updates</li>
                            <li>AI Tools Package</li>
                        </ul>
                    </div>
                </div>
            `;
            
            // Setup form submission
            const form = document.getElementById('enrollmentForm');
            form.addEventListener('submit', handleEnrollment);
            
            modal.style.display = 'block';
        })
        .catch(error => {
            console.error('Error loading course:', error);
        });
}

function handleEnrollment(event) {
    event.preventDefault();
    
    // In production, implement actual enrollment logic
    const formData = new FormData(event.target);
    
    // Show success message
    alert('🎉 Congratulations! Your enrollment is being processed. Check your email for confirmation.');
    
    // Close modal
    document.getElementById('enrollmentModal').style.display = 'none';
}

// Utility functions
function formatCurrency(amount) {
    return 'R' + amount.toLocaleString('en-ZA');
}

function createUrgencyTimer(endTime) {
    // Create urgency timer functionality
    return {
        start: function() {
            // Timer implementation
        }
    };
}

// Export for use in other modules
window.Platform = {
    showCourseModal,
    formatCurrency
};
