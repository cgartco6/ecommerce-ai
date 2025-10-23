# models/__init__.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import uuid
import bcrypt

db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    country = db.Column(db.String(50), nullable=False, default='ZA')
    timezone = db.Column(db.String(50), default='Africa/Johannesburg')
    language = db.Column(db.String(10), default='en')
    
    # Profile fields
    profile_picture = db.Column(db.String(500))
    bio = db.Column(db.Text)
    occupation = db.Column(db.String(100))
    company = db.Column(db.String(100))
    
    # Status fields
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    email_verified = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    last_activity = db.Column(db.DateTime)
    
    # Relationships
    subscriptions = db.relationship('Subscription', backref='user', lazy=True, cascade='all, delete-orphan')
    support_tickets = db.relationship('SupportTicket', backref='user', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='user', lazy=True, cascade='all, delete-orphan')
    chat_conversations = db.relationship('ChatConversation', backref='user', lazy=True, cascade='all, delete-orphan')
    course_progress = db.relationship('CourseProgress', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Check password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def get_full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<User {self.email}>'

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(200), nullable=False, index=True)
    subtitle = db.Column(db.String(300))
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(500))
    
    # Pricing
    price_zar = db.Column(db.Numeric(10, 2), nullable=False)
    original_price_zar = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(3), default='ZAR')
    
    # Course details
    duration_hours = db.Column(db.Integer, default=0)
    difficulty = db.Column(db.String(20), default='beginner')
    category = db.Column(db.String(50), nullable=False, index=True)
    subcategory = db.Column(db.String(50))
    level = db.Column(db.String(20), default='all_levels')
    
    # Media
    image_url = db.Column(db.String(500))
    video_url = db.Column(db.String(500))
    promo_video_url = db.Column(db.String(500))
    thumbnail_url = db.Column(db.String(500))
    
    # Content
    learning_objectives = db.Column(db.Text)
    prerequisites = db.Column(db.Text)
    target_audience = db.Column(db.Text)
    what_you_get = db.Column(db.Text)
    
    # Stats
    total_students = db.Column(db.Integer, default=0)
    total_rating = db.Column(db.Numeric(3, 2), default=0.0)
    review_count = db.Column(db.Integer, default=0)
    total_lessons = db.Column(db.Integer, default=0)
    
    # Status
    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    is_ai_generated = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    # Relationships
    modules = db.relationship('CourseModule', backref='course', lazy=True, cascade='all, delete-orphan')
    subscriptions = db.relationship('Subscription', backref='course', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('CourseReview', backref='course', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Course {self.title}>'

class CourseModule(db.Model):
    __tablename__ = 'course_modules'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    
    # Media
    video_url = db.Column(db.String(500))
    video_duration = db.Column(db.Integer)  # in seconds
    thumbnail_url = db.Column(db.String(500))
    
    # Module details
    duration_minutes = db.Column(db.Integer, default=0)
    order_index = db.Column(db.Integer, nullable=False)
    is_free_preview = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    
    # Resources
    resources = db.Column(db.JSON)  # JSON list of resources
    assignments = db.Column(db.JSON)  # JSON list of assignments
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lessons = db.relationship('CourseLesson', backref='module', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<CourseModule {self.title}>'

class CourseLesson(db.Model):
    __tablename__ = 'course_lessons'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    module_id = db.Column(db.String(36), db.ForeignKey('course_modules.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    
    # Media
    video_url = db.Column(db.String(500))
    video_duration = db.Column(db.Integer)
    audio_url = db.Column(db.String(500))
    document_url = db.Column(db.String(500))
    
    # Lesson details
    lesson_type = db.Column(db.String(20), default='video')  # video, text, quiz, assignment
    order_index = db.Column(db.Integer, nullable=False)
    is_published = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CourseLesson {self.title}>'

class CourseProgress(db.Model):
    __tablename__ = 'course_progress'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False, index=True)
    module_id = db.Column(db.String(36), db.ForeignKey('course_modules.id'))
    lesson_id = db.Column(db.String(36), db.ForeignKey('course_lessons.id'))
    
    # Progress tracking
    progress_percentage = db.Column(db.Numeric(5, 2), default=0.0)
    completed_lessons = db.Column(db.Integer, default=0)
    total_lessons = db.Column(db.Integer, default=0)
    time_spent_minutes = db.Column(db.Integer, default=0)
    
    # Completion status
    is_course_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    
    # Current activity
    last_accessed_at = db.Column(db.DateTime, default=datetime.utcnow)
    current_lesson_id = db.Column(db.String(36))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Index for efficient queries
    __table_args__ = (
        db.Index('idx_user_course', 'user_id', 'course_id'),
    )
    
    def __repr__(self):
        return f'<CourseProgress user:{self.user_id} course:{self.course_id}>'

class CourseReview(db.Model):
    __tablename__ = 'course_reviews'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False, index=True)
    
    # Review content
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    title = db.Column(db.String(200))
    comment = db.Column(db.Text)
    
    # Review metadata
    is_verified = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    helpful_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='reviews')
    
    def __repr__(self):
        return f'<CourseReview {self.rating} stars by {self.user_id}>'

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False, index=True)
    
    # Subscription details
    amount_zar = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='ZAR')
    subscription_type = db.Column(db.String(20), default='one_time')  # one_time, monthly, annual
    payment_method = db.Column(db.String(50))
    
    # Status
    status = db.Column(db.String(20), default='active')  # active, cancelled, expired, paused
    is_recurring = db.Column(db.Boolean, default=False)
    
    # Dates
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    next_billing_date = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Index for efficient queries
    __table_args__ = (
        db.Index('idx_user_subscription', 'user_id', 'status'),
        db.Index('idx_course_subscription', 'course_id', 'status'),
    )
    
    def __repr__(self):
        return f'<Subscription user:{self.user_id} course:{self.course_id}>'

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    subscription_id = db.Column(db.String(36), db.ForeignKey('subscriptions.id'), index=True)
    
    # Payment details
    amount_zar = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='ZAR')
    payment_method = db.Column(db.String(50), nullable=False)
    payment_gateway = db.Column(db.String(50), default='fnb')
    
    # Gateway references
    gateway_transaction_id = db.Column(db.String(100))
    gateway_reference = db.Column(db.String(100))
    fnb_reference = db.Column(db.String(100))
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded, disputed
    failure_reason = db.Column(db.Text)
    
    # Distribution (for FNB accounts)
    distribution = db.Column(db.JSON)  # Store payout distribution to different accounts
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    subscription = db.relationship('Subscription', backref='payments')
    
    def __repr__(self):
        return f'<Payment {self.amount_zar} {self.currency} by {self.user_id}>'

class SupportTicket(db.Model):
    __tablename__ = 'support_tickets'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Ticket details
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))  # technical, billing, content, account, general
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    
    # Status
    status = db.Column(db.String(20), default='open')  # open, in_progress, resolved, closed
    assigned_to = db.Column(db.String(36))  # AI agent or human support agent ID
    resolution_notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    closed_at = db.Column(db.DateTime)
    
    # Relationships
    messages = db.relationship('SupportMessage', backref='ticket', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<SupportTicket {self.subject} - {self.status}>'

class SupportMessage(db.Model):
    __tablename__ = 'support_messages'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    ticket_id = db.Column(db.String(36), db.ForeignKey('support_tickets.id'), nullable=False, index=True)
    
    # Message content
    message = db.Column(db.Text, nullable=False)
    is_from_user = db.Column(db.Boolean, default=True)
    sender_type = db.Column(db.String(20), default='user')  # user, ai_agent, human_agent
    sender_id = db.Column(db.String(36))  # ID of the sender (user or agent)
    
    # Attachments
    attachments = db.Column(db.JSON)  # JSON list of attachment URLs
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SupportMessage ticket:{self.ticket_id} from:{self.sender_type}>'

class ChatConversation(db.Model):
    __tablename__ = 'chat_conversations'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Conversation details
    title = db.Column(db.String(200))
    context = db.Column(db.Text)  # Conversation context or summary
    
    # Status
    status = db.Column(db.String(20), default='active')  # active, closed, archived
    
    # Timestamps
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime)
    
    # Relationships
    messages = db.relationship('ChatMessage', backref='conversation', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ChatConversation user:{self.user_id}>'

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    conversation_id = db.Column(db.String(36), db.ForeignKey('chat_conversations.id'), nullable=False, index=True)
    
    # Message content
    message = db.Column(db.Text, nullable=False)
    is_user = db.Column(db.Boolean, default=True)
    message_type = db.Column(db.String(20), default='text')  # text, image, suggestion, system
    intent = db.Column(db.String(50))  # Detected intent of the message
    
    # Metadata
    suggestions = db.Column(db.JSON)  # JSON list of suggested responses
    confidence = db.Column(db.Numeric(3, 2))  # Confidence score for AI responses
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatMessage conv:{self.conversation_id} user:{self.is_user}>'

class RevenueTracking(db.Model):
    __tablename__ = 'revenue_tracking'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    date = db.Column(db.Date, nullable=False, index=True)
    
    # Revenue metrics
    total_revenue_zar = db.Column(db.Numeric(12, 2), default=0)
    recurring_revenue_zar = db.Column(db.Numeric(12, 2), default=0)
    one_time_revenue_zar = db.Column(db.Numeric(12, 2), default=0)
    
    # Subscription metrics
    new_subscriptions = db.Column(db.Integer, default=0)
    active_subscriptions = db.Column(db.Integer, default=0)
    cancelled_subscriptions = db.Column(db.Integer, default=0)
    churn_rate = db.Column(db.Numeric(5, 4), default=0)
    
    # User metrics
    new_users = db.Column(db.Integer, default=0)
    active_users = db.Column(db.Integer, default=0)
    paying_users = db.Column(db.Integer, default=0)
    
    # Course metrics
    course_enrollments = db.Column(db.Integer, default=0)
    course_completions = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Numeric(3, 2), default=0.0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint on date
    __table_args__ = (
        db.UniqueConstraint('date', name='unique_date'),
    )
    
    def __repr__(self):
        return f'<RevenueTracking {self.date} - ZAR {self.total_revenue_zar}>'

class SystemHealth(db.Model):
    __tablename__ = 'system_health'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    component = db.Column(db.String(50), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False)  # healthy, warning, critical, offline
    status_message = db.Column(db.Text)
    
    # Metrics
    metrics = db.Column(db.JSON)  # JSON object with component-specific metrics
    performance_score = db.Column(db.Numeric(5, 2))  # 0-100 score
    
    # Timestamps
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SystemHealth {self.component} - {self.status}>'

class AIAgentLog(db.Model):
    __tablename__ = 'ai_agent_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    agent_name = db.Column(db.String(50), nullable=False, index=True)
    task_type = db.Column(db.String(50), nullable=False)
    
    # Task details
    task_parameters = db.Column(db.JSON)
    task_result = db.Column(db.JSON)
    status = db.Column(db.String(20), default='completed')  # pending, running, completed, failed
    error_message = db.Column(db.Text)
    
    # Performance metrics
    execution_time_ms = db.Column(db.Integer)
    resource_usage = db.Column(db.JSON)
    
    # Timestamps
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AIAgentLog {self.agent_name} - {self.task_type}>'

# Import all models for easy access
__all__ = [
    'User',
    'Course', 
    'CourseModule',
    'CourseLesson',
    'CourseProgress',
    'CourseReview',
    'Subscription',
    'Payment',
    'SupportTicket',
    'SupportMessage', 
    'ChatConversation',
    'ChatMessage',
    'RevenueTracking',
    'SystemHealth',
    'AIAgentLog'
]
