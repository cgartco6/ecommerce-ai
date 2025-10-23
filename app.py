# app.py
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import asyncio
import json
from decimal import Decimal
from datetime import datetime, timedelta

from config import config
from models import db, User, Course, Subscription, Payment, SupportTicket, ChatConversation
from ai_core import (
    UltimateEcommerceAIPlatform, 
    MeganChatbot, 
    CustomerSupportSystem,
    MassAcquisitionOrchestrator
)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config['development'])

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize AI platform
platform = UltimateEcommerceAIPlatform()
chatbot = MeganChatbot()
support_system = CustomerSupportSystem()
mass_acquisition = MassAcquisitionOrchestrator()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.before_first_request
def initialize_platform():
    """Initialize AI platform on first request"""
    asyncio.run(platform.initialize_platform())

# Routes
@app.route('/')
def index():
    """Main landing page with psychological triggers"""
    courses = Course.query.filter_by(is_published=True).all()
    subscriber_count = Subscription.query.filter_by(status='active').count()
    
    return render_template('index.html',
                         courses=courses,
                         subscriber_count=subscriber_count,
                         limited_time_offer=True,
                         flash_sale=True)

@app.route('/courses')
def courses():
    """Course catalog page"""
    courses = Course.query.filter_by(is_published=True).all()
    return render_template('courses.html', courses=courses)

@app.route('/course/<course_id>')
def course_detail(course_id):
    """Individual course page"""
    course = Course.query.get_or_404(course_id)
    return render_template('course_detail.html', course=course)

@app.route('/api/chat', methods=['POST'])
@login_required
async def chat_with_megan():
    """Chat endpoint for Megan AI chatbot"""
    data = request.json
    user_message = data.get('message', '')
    conversation_id = data.get('conversation_id')
    
    response = await chatbot.process_message(
        user_message, 
        current_user.id, 
        conversation_id
    )
    
    return jsonify(response)

@app.route('/api/support/ticket', methods=['POST'])
@login_required
async def create_support_ticket():
    """Create support ticket"""
    data = request.json
    subject = data.get('subject', '')
    description = data.get('description', '')
    
    result = await support_system.handle_support_ticket(
        current_user.id, subject, description
    )
    
    return jsonify(result)

@app.route('/api/subscribe', methods=['POST'])
@login_required
async def subscribe_to_course():
    """Subscribe to a course with FNB payment"""
    data = request.json
    course_id = data.get('course_id')
    payment_method = data.get('payment_method', 'fnb_transfer')
    
    course = Course.query.get_or_404(course_id)
    
    # Process payment
    payment_result = await platform.payment_distributor.payment_processor.process_payment(
        Decimal(str(course.price_zar)),
        {
            'user_id': current_user.id,
            'email': current_user.email,
            'name': f"{current_user.first_name} {current_user.last_name}"
        }
    )
    
    if payment_result['payment_status'] == 'completed':
        # Create subscription
        subscription = Subscription(
            user_id=current_user.id,
            course_id=course_id,
            amount_zar=course.price_zar,
            payment_method=payment_method,
            status='active'
        )
        db.session.add(subscription)
        db.session.commit()
        
        # Track revenue
        await platform.revenue_tracker.track_revenue({
            'user_id': current_user.id,
            'amount': float(course.price_zar),
            'type': 'subscription',
            'course_id': course_id
        })
        
        return jsonify({
            'status': 'success',
            'message': 'Successfully enrolled in course!',
            'subscription_id': subscription.id,
            'payment_reference': payment_result['transaction_id']
        })
    
    return jsonify({
        'status': 'error',
        'message': 'Payment failed. Please try again.'
    })

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard with analytics"""
    if not current_user.is_admin:
        return redirect(url_for('index'))
    
    total_revenue = db.session.query(db.func.sum(Payment.amount_zar)).filter(
        Payment.status == 'completed'
    ).scalar() or 0
    
    total_subscribers = Subscription.query.filter_by(status='active').count()
    recent_subscriptions = Subscription.query.order_by(
        Subscription.created_at.desc()
    ).limit(10).all()
    
    return render_template('admin.html',
                         total_revenue=total_revenue,
                         total_subscribers=total_subscribers,
                         recent_subscriptions=recent_subscriptions,
                         revenue_targets=platform.revenue_targets)

@app.route('/admin/revenue-analytics')
@login_required
async def revenue_analytics():
    """Revenue analytics API"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    analytics = await platform.revenue_tracker.get_revenue_analytics('weekly')
    return jsonify(analytics)

@app.route('/admin/launch-mass-acquisition', methods=['POST'])
@login_required
async def launch_mass_acquisition():
    """Launch massive subscriber acquisition campaign"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    budget = float(request.json.get('budget', 500000))
    results = await mass_acquisition.execute_mass_acquisition(budget)
    
    return jsonify(results)

@app.route('/support')
@login_required
def support_page():
    """Customer support page"""
    user_tickets = SupportTicket.query.filter_by(
        user_id=current_user.id
    ).order_by(SupportTicket.created_at.desc()).all()
    
    return render_template('support.html', tickets=user_tickets)

@app.route('/chat')
@login_required
def chat_page():
    """Chat interface with Megan"""
    conversations = ChatConversation.query.filter_by(
        user_id=current_user.id
    ).order_by(ChatConversation.last_activity.desc()).all()
    
    return render_template('chat.html', conversations=conversations)

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        country = request.form.get('country', 'ZA')
        
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            country=country
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    return redirect(url_for('index'))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=True)
