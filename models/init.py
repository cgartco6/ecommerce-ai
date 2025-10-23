# models/__init__.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import uuid

db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    country = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)
    support_tickets = db.relationship('SupportTicket', backref='user', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_zar = db.Column(db.Numeric(10, 2), nullable=False)
    original_price_zar = db.Column(db.Numeric(10, 2))
    duration_hours = db.Column(db.Integer, default=0)
    difficulty = db.Column(db.String(20), default='beginner')
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(500))
    video_url = db.Column(db.String(500))
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    modules = db.relationship('CourseModule', backref='course', lazy=True)
    subscriptions = db.relationship('Subscription', backref='course', lazy=True)

class CourseModule(db.Model):
    __tablename__ = 'course_modules'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    video_url = db.Column(db.String(500))
    duration_minutes = db.Column(db.Integer, default=0)
    order_index = db.Column(db.Integer, nullable=False)
    is_free_preview = db.Column(db.Boolean, default=False)

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False)
    amount_zar = db.Column(db.Numeric(10, 2), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, cancelled, expired
    payment_method = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    subscription_id = db.Column(db.String(36), db.ForeignKey('subscriptions.id'))
    amount_zar = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='ZAR')
    payment_method = db.Column(db.String(50), nullable=False)
    fnb_reference = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded
    distribution = db.Column(db.JSON)  # Store payout distribution
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    subscription = db.relationship('Subscription', backref='payments')

class SupportTicket(db.Model):
    __tablename__ = 'support_tickets'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open')  # open, in_progress, resolved, closed
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    category = db.Column(db.String(50))  # technical, billing, content, other
    assigned_to = db.Column(db.String(36))  # AI agent or human support
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = db.relationship('SupportMessage', backref='ticket', lazy=True)

class SupportMessage(db.Model):
    __tablename__ = 'support_messages'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    ticket_id = db.Column(db.String(36), db.ForeignKey('support_tickets.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_from_user = db.Column(db.Boolean, default=True)
    sender_type = db.Column(db.String(20), default='user')  # user, ai_agent, human_agent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatConversation(db.Model):
    __tablename__ = 'chat_conversations'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, closed
    
    # Relationships
    messages = db.relationship('ChatMessage', backref='conversation', lazy=True)

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    conversation_id = db.Column(db.String(36), db.ForeignKey('chat_conversations.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_user = db.Column(db.Boolean, default=True)
    message_type = db.Column(db.String(20), default='text')  # text, image, suggestion
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class RevenueTracking(db.Model):
    __tablename__ = 'revenue_tracking'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    date = db.Column(db.Date, nullable=False)
    total_revenue_zar = db.Column(db.Numeric(12, 2), default=0)
    new_subscriptions = db.Column(db.Integer, default=0)
    active_subscriptions = db.Column(db.Integer, default=0)
    churn_rate = db.Column(db.Numeric(5, 4), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemHealth(db.Model):
    __tablename__ = 'system_health'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    component = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # healthy, warning, critical
    metrics = db.Column(db.JSON)
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
