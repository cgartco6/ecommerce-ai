# ai_core/ai_helpers.py
import re
from typing import Dict, List, Optional
from datetime import datetime
import random

class AIHelper:
    def __init__(self, helper_type: str):
        self.helper_type = helper_type
        self.interaction_history = []
        self.helpfulness_score = 0.0
        
    def provide_assistance(self, request: str, context: Dict = None) -> Dict:
        """Provide AI-powered assistance"""
        assistance_start = datetime.now()
        
        self.interaction_history.append({
            "request": request, 
            "context": context,
            "timestamp": assistance_start
        })
        
        # Analyze request and provide appropriate assistance
        if "course" in request.lower() and "create" in request.lower():
            assistance = self._help_course_creation(request, context)
        elif "market" in request.lower() or "promote" in request.lower():
            assistance = self._help_marketing(request, context)
        elif "analyze" in request.lower() or "report" in request.lower():
            assistance = self._help_analysis(request, context)
        elif "support" in request.lower() or "help" in request.lower():
            assistance = self._help_support(request, context)
        elif "content" in request.lower():
            assistance = self._help_content_creation(request, context)
        else:
            assistance = self._general_assistance(request, context)
        
        # Calculate helpfulness
        assistance_duration = (datetime.now() - assistance_start).total_seconds()
        self._update_helpfulness_score(assistance, assistance_duration)
        
        return assistance
    
    def _help_course_creation(self, request: str, context: Dict) -> Dict:
        """Assist with course creation"""
        return {
            "suggestions": [
                "Define clear learning objectives for each module",
                "Structure content in progressive difficulty levels",
                "Include practical exercises and projects",
                "Add assessment quizzes for knowledge checks",
                "Provide supplementary resources and reading materials"
            ],
            "templates": [
                "course_structure_template",
                "learning_objective_template", 
                "assessment_creation_template"
            ],
            "best_practices": [
                "Start with fundamentals before advancing",
                "Use real-world examples and case studies",
                "Incorporate interactive elements",
                "Provide certificate of completion",
                "Include community discussion forums"
            ],
            "tools": [
                "Content outline generator",
                "Learning objective formulator",
                "Assessment creator",
                "Progress tracker setup"
            ]
        }
    
    def _help_marketing(self, request: str, context: Dict) -> Dict:
        """Assist with marketing activities"""
        return {
            "channels": [
                "Social media (TikTok, Instagram, Facebook, LinkedIn)",
                "Email marketing campaigns",
                "Content marketing (blog, YouTube)",
                "Search engine optimization (SEO)",
                "Partnerships and affiliates"
            ],
            "strategies": [
                "Create viral content with educational value",
                "Implement referral programs with incentives",
                "Use influencer partnerships for credibility",
                "Run targeted advertising campaigns",
                "Develop email nurture sequences"
            ],
            "metrics_to_track": [
                "Conversion rates by channel",
                "Customer acquisition cost (CAC)",
                "Lifetime value (LTV)",
                "Engagement rates on social media",
                "Email open and click-through rates"
            ],
            "content_ideas": [
                "Student success stories and testimonials",
                "Behind-the-scenes course creation process",
                "Free mini-courses or workshops",
                "Industry expert interviews",
                "Trend analysis in education technology"
            ]
        }
    
    def _help_analysis(self, request: str, context: Dict) -> Dict:
        """Assist with data analysis and reporting"""
        return {
            "key_metrics": [
                "Subscriber growth rate",
                "Course completion rates",
                "Revenue per user",
                "Customer satisfaction scores",
                "Platform engagement metrics"
            ],
            "analysis_techniques": [
                "Trend analysis over time",
                "Cohort analysis for user behavior",
                "A/B testing for optimization",
                "Predictive modeling for growth",
                "Correlation analysis for insights"
            ],
            "reporting_templates": [
                "Weekly performance dashboard",
                "Monthly business review",
                "Course performance deep-dive",
                "Marketing ROI analysis",
                "Customer satisfaction report"
            ],
            "tools_recommendations": [
                "Google Analytics for web traffic",
                "Mixpanel for user behavior",
                "Tableau for visualization",
                "Python pandas for data analysis",
                "SQL for database queries"
            ]
        }
    
    def _help_support(self, request: str, context: Dict) -> Dict:
        """Assist with customer support"""
        return {
            "common_issues": [
                "Login and account access problems",
                "Payment and billing questions",
                "Course content access issues",
                "Technical platform problems",
                "Certificate and completion queries"
            ],
            "resolution_guidelines": [
                "Always verify user identity first",
                "Provide step-by-step solutions",
                "Escalate complex issues promptly",
                "Follow up to ensure resolution",
                "Document solutions for knowledge base"
            ],
            "communication_tips": [
                "Use empathetic and understanding language",
                "Provide clear timelines for resolution",
                "Offer multiple contact channels",
                "Personalize responses when possible",
                "Set proper expectations"
            ],
            "escalation_procedures": [
                "Technical issues to engineering team",
                "Billing disputes to finance team",
                "Content errors to course creators",
                "Platform outages to operations team",
                "Legal concerns to compliance team"
            ]
        }
    
    def _help_content_creation(self, request: str, context: Dict) -> Dict:
        """Assist with content creation"""
        return {
            "content_types": [
                "Educational blog posts and articles",
                "Social media posts and stories",
                "Email newsletters and campaigns",
                "Video tutorials and demonstrations",
                "Interactive quizzes and assessments"
            ],
            "creation_tools": [
                "Canva for graphic design",
                "Descript for video editing",
                "Grammarly for writing assistance",
                "Loom for screen recording",
                "Notion for content planning"
            ],
            "quality_guidelines": [
                "Ensure accuracy and fact-checking",
                "Maintain consistent brand voice",
                "Optimize for mobile viewing",
                "Include clear calls-to-action",
                "Add alt-text for accessibility"
            ],
            "seo_recommendations": [
                "Research relevant keywords",
                "Optimize meta descriptions",
                "Use descriptive file names",
                "Build internal linking structure",
                "Monitor search performance"
            ]
        }
    
    def _general_assistance(self, request: str, context: Dict) -> Dict:
        """Provide general assistance"""
        return {
            "welcome_message": "Hello! I'm your AI assistant. I can help you with:",
            "capabilities": [
                "Course creation and curriculum design",
                "Marketing strategy and campaign planning",
                "Data analysis and performance reporting",
                "Customer support and issue resolution",
                "Content creation and optimization"
            ],
            "quick_actions": [
                "Generate course outline",
                "Create marketing plan",
                "Analyze performance data",
                "Set up support system",
                "Plan content calendar"
            ],
            "getting_started": [
                "Tell me what you'd like to accomplish",
                "Provide context about your current project",
                "Specify any constraints or requirements",
                "Let me know your timeline",
                "Share your target audience details"
            ]
        }
    
    def _update_helpfulness_score(self, assistance: Dict, duration: float):
        """Update the helper's helpfulness score"""
        # Simple scoring based on response completeness and speed
        completeness_score = min(1.0, len(str(assistance)) / 1000)  # More content is better
        speed_score = max(0, 1 - (duration / 10))  # Faster is better, max 10 seconds expected
        
        assistance_score = (completeness_score + speed_score) / 2
        self.helpfulness_score = 0.9 * self.helpfulness_score + 0.1 * assistance_score
    
    def get_performance_stats(self) -> Dict:
        """Get helper performance statistics"""
        return {
            "helper_type": self.helper_type,
            "total_assistance_provided": len(self.interaction_history),
            "helpfulness_score": round(self.helpfulness_score, 3),
            "average_response_time": self._calculate_average_response_time(),
            "recent_requests": [hist["request"] for hist in self.interaction_history[-5:]]
        }
    
    def _calculate_average_response_time(self) -> float:
        """Calculate average response time"""
        if len(self.interaction_history) < 2:
            return 0.0
        
        total_time = 0
        for i in range(1, len(self.interaction_history)):
            time_diff = (self.interaction_history[i]["timestamp"] - self.interaction_history[i-1]["timestamp"]).total_seconds()
            total_time += time_diff
        
        return total_time / (len(self.interaction_history) - 1) if len(self.interaction_history) > 1 else 0.0

class CourseCreationHelper(AIHelper):
    def __init__(self):
        super().__init__("course_creation")
        self.course_templates = self._load_course_templates()
    
    def generate_course_ideas(self, topic: str, target_audience: str) -> List[str]:
        """Generate course ideas based on topic and audience"""
        ideas = [
            f"Complete {topic} Bootcamp for {target_audience}",
            f"Advanced {topic} Masterclass: From Beginner to Expert",
            f"{topic} Practical Projects: Build Real-World Applications",
            f"{topic} for Career Advancement: Industry-Focused Training",
            f"The Ultimate {topic} Guide: Theory and Practice Combined"
        ]
        return ideas
    
    def _load_course_templates(self) -> Dict:
        """Load predefined course templates"""
        return {
            "beginner": {
                "duration": "4-6 weeks",
                "modules": 5,
                "assessment_frequency": "weekly",
                "project_required": True
            },
            "intermediate": {
                "duration": "6-8 weeks", 
                "modules": 8,
                "assessment_frequency": "bi-weekly",
                "project_required": True
            },
            "advanced": {
                "duration": "8-12 weeks",
                "modules": 12,
                "assessment_frequency": "per_module",
                "project_required": True
            }
        }

class MarketingHelper(AIHelper):
    def __init__(self):
        super().__init__("marketing")
        self.campaign_templates = self._load_campaign_templates()
    
    def generate_ad_copy(self, product: str, platform: str, tone: str = "professional") -> Dict:
        """Generate advertising copy for different platforms"""
        copy_templates = {
            "facebook": {
                "professional": f"Transform your career with our {product} course. Industry experts. Real projects. 🚀",
                "casual": f"Ready to level up? Learn {product} the fun way! 😎",
                "urgent": f"LAST CHANCE: Master {product} before prices increase! ⏰"
            },
            "instagram": {
                "professional": f"Become a {product} expert 💼\n\nJoin 10,000+ successful students 👇",
                "casual": f"PSA: Learning {product} can change your life 🌟",
                "urgent": f"🚨 Flash sale: {product} course 75% OFF today only!"
            },
            "linkedin": {
                "professional": f"Advance your career with professional {product} training. Industry-recognized certification.",
                "casual": f"Looking to upskill? Our {product} course has you covered.",
                "urgent": f"Limited seats available for our {product} certification program."
            }
        }
        
        return {
            "headline": copy_templates.get(platform, {}).get(tone, f"Learn {product} effectively"),
            "body": f"Comprehensive {product} training with hands-on projects and expert guidance.",
            "cta": "Enroll Now" if tone == "urgent" else "Learn More",
            "hashtags": ["#" + product.replace(" ", ""), "#learning", "#education"]
        }
    
    def _load_campaign_templates(self) -> Dict:
        """Load marketing campaign templates"""
        return {
            "launch": {
                "duration": "30 days",
                "channels": ["social_media", "email", "content"],
                "budget_allocation": {"ads": 0.6, "content": 0.3, "partnerships": 0.1},
                "success_metrics": ["subscriber_growth", "conversion_rate", "brand_awareness"]
            },
            "growth": {
                "duration": "90 days", 
                "channels": ["social_media", "seo", "affiliate"],
                "budget_allocation": {"ads": 0.4, "content": 0.4, "partnerships": 0.2},
                "success_metrics": ["revenue_growth", "customer_lifetime_value", "market_share"]
            }
        }

class AnalyticsHelper(AIHelper):
    def __init__(self):
        super().__init__("analytics")
        self.metric_definitions = self._load_metric_definitions()
    
    def generate_dashboard_metrics(self, timeframe: str = "weekly") -> Dict:
        """Generate key metrics for business dashboard"""
        return {
            "subscriber_metrics": {
                "new_subscribers": random.randint(50, 500),
                "total_subscribers": random.randint(1000, 10000),
                "growth_rate": random.uniform(0.05, 0.25),
                "churn_rate": random.uniform(0.02, 0.08)
            },
            "revenue_metrics": {
                "total_revenue": random.randint(50000, 500000),
                "recurring_revenue": random.randint(40000, 400000),
                "average_revenue_per_user": random.uniform(500, 2000),
                "revenue_growth": random.uniform(0.08, 0.35)
            },
            "engagement_metrics": {
                "course_completion_rate": random.uniform(0.6, 0.9),
                "average_time_on_platform": random.randint(30, 120),
                "active_users_daily": random.randint(500, 5000),
                "satisfaction_score": random.uniform(4.0, 5.0)
            }
        }
    
    def _load_metric_definitions(self) -> Dict:
        """Load metric definitions and calculations"""
        return {
            "conversion_rate": {
                "formula": "(Conversions / Total Visitors) * 100",
                "benchmark": "2-5% for education platforms",
                "improvement_tips": ["Optimize landing pages", "Simplify signup process"]
            },
            "customer_acquisition_cost": {
                "formula": "Total Marketing Spend / New Customers Acquired",
                "benchmark": "ZAR 500-2000 for education",
                "improvement_tips": ["Refine targeting", "Improve conversion rates"]
            },
            "lifetime_value": {
                "formula": "Average Revenue Per User * Average Customer Lifespan", 
                "benchmark": "3x CAC for healthy business",
                "improvement_tips": ["Increase retention", "Upsell additional courses"]
            }
        }

class HelperOrchestrator:
    def __init__(self):
        self.helpers = {
            'course_creation': CourseCreationHelper(),
            'marketing': MarketingHelper(),
            'analytics': AnalyticsHelper(),
            'general': AIHelper("general")
        }
        self.assistance_log = []
        
    def get_assistance(self, helper_type: str, request: str, context: Dict = None) -> Dict:
        """Get assistance from appropriate helper"""
        if helper_type in self.helpers:
            helper = self.helpers[helper_type]
            assistance = helper.provide_assistance(request, context)
        else:
            helper = self.helpers['general']
            assistance = helper.provide_assistance(request, context)
        
        # Log assistance
        self.assistance_log.append({
            "helper_type": helper_type,
            "request": request,
            "assistance": assistance,
            "timestamp": datetime.now()
        })
        
        return assistance
    
    def get_helper_performance(self) -> Dict:
        """Get performance of all helpers"""
        return {
            helper_type: helper.get_performance_stats()
            for helper_type, helper in self.helpers.items()
        }
    
    def get_popular_requests(self) -> List[Dict]:
        """Get most popular assistance requests"""
        request_counts = {}
        for log in self.assistance_log:
            request = log["request"][:50]  # First 50 chars
            request_counts[request] = request_counts.get(request, 0) + 1
        
        return sorted(request_counts.items(), key=lambda x: x[1], reverse=True)[:10]
