# ai_core/__init__.py (Updated)
from .synthetic_intelligence import SyntheticIntelligence, StrategicDecision
from .strategic_intelligence import StrategicIntelligence
from .ai_agents import AIAgent, CourseCreationAgent, MarketingAgent, AnalyticsAgent, SupportAgent, AIAgentOrchestrator
from .ai_helpers import AIHelper, CourseCreationHelper, MarketingHelper, AnalyticsHelper, HelperOrchestrator
from .content_creators import HDContentCreator, AddictiveContentStrategist, ContentType
from .marketing_automation import SocialMediaMarketingAgent, SocialMediaTracker, PerformanceAnalyzer
from .compliance_manager import GlobalComplianceManager, CountryCode
from .security_monitoring import MilitaryGradeSecurity, ThreatDetectionSystem
from .auto_poster import SocialMediaAutoPoster
from .revenue_tracker import RevenueTracker, RevenueAnalytics
from .revenue_optimizer import RevenueOptimizer
from .payment_processor import FNBPaymentProcessor, RevenueDistributor
from .self_healing import SelfHealingSystem, SystemHealthMonitor, RepairAgents
from .llm_chatbot import MeganChatbot, CustomerSupportSystem

__all__ = [
    # Synthetic Intelligence
    'SyntheticIntelligence',
    'StrategicDecision',
    
    # Strategic Intelligence  
    'StrategicIntelligence',
    
    # AI Agents
    'AIAgent',
    'CourseCreationAgent', 
    'MarketingAgent',
    'AnalyticsAgent',
    'SupportAgent',
    'AIAgentOrchestrator',
    
    # AI Helpers
    'AIHelper',
    'CourseCreationHelper',
    'MarketingHelper', 
    'AnalyticsHelper',
    'HelperOrchestrator',
    
    # Content Creation
    'HDContentCreator',
    'AddictiveContentStrategist',
    'ContentType',
    
    # Marketing Automation
    'SocialMediaMarketingAgent', 
    'SocialMediaTracker',
    'PerformanceAnalyzer',
    
    # Compliance
    'GlobalComplianceManager',
    'CountryCode',
    
    # Security
    'MilitaryGradeSecurity',
    'ThreatDetectionSystem',
    
    # Auto Posting
    'SocialMediaAutoPoster',
    
    # Revenue Tracking & Optimization
    'RevenueTracker', 
    'RevenueAnalytics',
    'RevenueOptimizer',
    
    # Payment Processing
    'FNBPaymentProcessor',
    'RevenueDistributor',
    
    # Self Healing
    'SelfHealingSystem',
    'SystemHealthMonitor', 
    'RepairAgents',
    
    # LLM Chatbot
    'MeganChatbot',
    'CustomerSupportSystem'
]

# CostByte AI Core Version
__version__ = "1.0.0"
__author__ = "CostByte AI Team"
__description__ = "Advanced AI-Powered E-Learning Platform Core System"
