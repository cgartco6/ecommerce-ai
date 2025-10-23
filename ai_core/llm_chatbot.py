# ai_core/llm_chatbot.py
import asyncio
import json
from typing import Dict, List, Optional
from datetime import datetime
from models import ChatConversation, ChatMessage, db

class MeganChatbot:
    def __init__(self):
        self.name = "Megan"
        self.personality = {
            "tone": "friendly, professional, and supportive",
            "expertise": "course recommendations, technical support, billing questions, career advice",
            "response_style": "helpful, detailed, and encouraging",
            "traits": ["patient", "knowledgeable", "empathetic", "solution-oriented"]
        }
        self.knowledge_base = self._load_knowledge_base()
        self.conversation_memory = {}
        
    async def process_message(self, user_message: str, user_id: str, conversation_id: str = None) -> Dict:
        """Process user message and generate response"""
        print(f"💬 Megan processing message from user {user_id}: {user_message[:50]}...")
        
        # Get or create conversation
        conversation = await self._get_conversation(conversation_id, user_id)
        
        # Analyze user intent
        intent = await self._analyze_intent(user_message)
        
        # Generate response based on intent
        response = await self._generate_response(user_message, intent, conversation.id)
        
        # Save messages to database
        await self._save_messages(conversation.id, user_message, response)
        
        return {
            "conversation_id": conversation.id,
            "response": response,
            "suggestions": await self._generate_suggestions(intent),
            "timestamp": datetime.utcnow(),
            "intent_detected": intent["primary_intent"]
        }
    
    async def _analyze_intent(self, message: str) -> Dict:
        """Analyze user intent using AI patterns"""
        message_lower = message.lower()
        
        intents = {
            "course_info": ["course", "learn", "what is", "how to", "tutorial", "class", "lesson"],
            "pricing": ["price", "cost", "how much", "discount", "free", "payment", "afford"],
            "technical_support": ["help", "problem", "issue", "not working", "error", "bug", "fix"],
            "billing": ["payment", "bill", "invoice", "refund", "cancel", "subscription", "charge"],
            "career_advice": ["career", "job", "employment", "salary", "hire", "opportunity", "future"],
            "platform_info": ["feature", "how does", "what can", "capability", "function"],
            "account_help": ["login", "password", "account", "sign up", "register", "profile"]
        }
        
        detected_intents = []
        confidence_scores = {}
        
        for intent, keywords in intents.items():
            keyword_matches = sum(1 for keyword in keywords if keyword in message_lower)
            if keyword_matches > 0:
                detected_intents.append(intent)
                confidence_scores[intent] = min(1.0, keyword_matches / len(keywords) * 2)
        
        # Determine primary intent (highest confidence)
        primary_intent = "general"
        if detected_intents:
            primary_intent = max(detected_intents, key=lambda x: confidence_scores.get(x, 0))
        
        return {
            "primary_intent": primary_intent,
            "all_intents": detected_intents,
            "confidence": confidence_scores.get(primary_intent, 0.7),
            "confidence_scores": confidence_scores
        }
    
    async def _generate_response(self, user_message: str, intent: Dict, conversation_id: str) -> str:
        """Generate AI response based on intent"""
        intent_handlers = {
            "course_info": self._handle_course_inquiry,
            "pricing": self._handle_pricing_inquiry,
            "technical_support": self._handle_technical_support,
            "billing": self._handle_billing_inquiry,
            "career_advice": self._handle_career_advice,
            "platform_info": self._handle_platform_info,
            "account_help": self._handle_account_help
        }
        
        handler = intent_handlers.get(intent["primary_intent"], self._handle_general_inquiry)
        return await handler(user_message)
    
    async def _handle_course_inquiry(self, message: str) -> str:
        """Handle course-related inquiries"""
        responses = [
            "I'd love to help you find the perfect course! We have several options focused on AI, programming, data science, and digital marketing. Which specific area are you interested in exploring? 🚀",
            
            "Our courses are designed to get you real results quickly! We have options for complete beginners all the way to advanced professionals. What skill would you like to develop or improve? 💡",
            
            "Based on what you're asking, I'd recommend checking out our 'AI-Powered Trading' course - it's our most popular option and students are seeing amazing results! Would you like me to share more details about it? 📈"
        ]
        return await self._select_best_response(message, responses)
    
    async def _handle_pricing_inquiry(self, message: str) -> str:
        """Handle pricing questions"""
        responses = [
            "Great question! Our courses range from R1,997 to R4,997 with flexible payment options. We also have a 30-day money-back guarantee if you're not completely satisfied! Which course are you considering? 💰",
            
            "The investment in your education pays for itself quickly - many students make back their course fee in the first month! Our current pricing starts at R1,997 with different tiers available. 🎯",
            
            "We're running a special launch offer with 75% discount for the first 5000 students. The regular price is R7,997 but you can enroll today for just R1,997! This includes lifetime access and all future updates. ⚡"
        ]
        return await self._select_best_response(message, responses)
    
    async def _handle_technical_support(self, message: str) -> str:
        """Handle technical support issues"""
        return "I'm sorry you're experiencing technical issues! Our support team can help resolve this quickly. Can you provide more details about what's happening? In the meantime, you might try refreshing the page or using a different browser. 🔧"
    
    async def _handle_billing_inquiry(self, message: str) -> str:
        """Handle billing and payment questions"""
        return "I can help with billing questions! We accept all major payment methods including credit cards and FNB transfers. For specific payment issues or refund requests, our billing team will assist you promptly. You can also check your billing history in your account settings. 💳"
    
    async def _handle_career_advice(self, message: str) -> str:
        """Provide career guidance"""
        responses = [
            "The skills you learn here are in high demand! Our graduates typically see 3-5x salary increases and many transition to remote work opportunities. Which career path are you most interested in pursuing? 🌟",
            
            "Digital skills are the future! Learning AI, programming, or data science can open doors to high-paying opportunities and career advancement. What's your current experience level and what kind of work are you looking for? 💼"
        ]
        return await self._select_best_response(message, responses)
    
    async def _handle_platform_info(self, message: str) -> str:
        """Provide platform information"""
        return "CostByte is an AI-powered learning platform that personalizes your education experience! We use advanced algorithms to recommend courses, track your progress, and help you achieve your goals faster. Our platform includes interactive lessons, real projects, and a supportive community. Is there a specific feature you'd like to know more about? 🤖"
    
    async def _handle_account_help(self, message: str) -> str:
        """Handle account-related questions"""
        return "I can help with account issues! For login problems, try using the 'Forgot Password' feature. If you're having trouble signing up, make sure you're using a valid email address. For other account issues, our support team is here to help 24/7. 🔐"
    
    async def _handle_general_inquiry(self, message: str) -> str:
        """Handle general conversations"""
        responses = [
            "Hi there! I'm Megan, your AI learning assistant at CostByte! I'm here to help you succeed with your education goals. How can I assist you today? 😊",
            
            "Welcome to CostByte! I'm excited to help you on your learning journey. Whether you have questions about courses, pricing, technical issues, or career advice - I'm here to help! What would you like to know? 🎓",
            
            "Hello! I'm Megan, and I'm here to support your learning experience at CostByte. Feel free to ask me anything about our courses, platform features, or how to get started on your educational journey! 🌈"
        ]
        return await self._select_best_response(message, responses)
    
    async def _select_best_response(self, message: str, responses: List[str]) -> str:
        """Select the most appropriate response"""
        message_lower = message.lower()
        
        # Simple keyword matching for response selection
        if any(word in message_lower for word in ['beginner', 'start', 'new', 'first time']):
            return responses[1] if len(responses) > 1 else responses[0]
        elif any(word in message_lower for word in ['popular', 'best', 'recommend', 'suggest']):
            return responses[2] if len(responses) > 2 else responses[0]
        elif any(word in message_lower for word in ['hi', 'hello', 'hey', 'greetings']):
            return responses[0]
        else:
            return responses[0]
    
    async def _generate_suggestions(self, intent: Dict) -> List[str]:
        """Generate suggested follow-up questions"""
        suggestions_map = {
            "course_info": [
                "What's the best course for complete beginners?",
                "How long does each course take to complete?",
                "Can I see a preview of the course content?",
                "Do you offer certificates upon completion?"
            ],
            "pricing": [
                "Do you offer payment plans or installments?",
                "Is there a money-back guarantee?",
                "Are there any student discounts available?",
                "What's included in the course price?"
            ],
            "technical_support": [
                "How do I contact human support?",
                "Can you help me reset my password?",
                "What are the system requirements?",
                "The video isn't loading - what should I do?"
            ],
            "career_advice": [
                "Which courses have the best job outcomes?",
                "How can I transition to a tech career?",
                "What skills are most in demand?",
                "Do you offer career coaching?"
            ],
            "general": [
                "View all available courses",
                "Contact customer support",
                "Pricing information",
                "Platform features overview"
            ]
        }
        
        return suggestions_map.get(intent["primary_intent"], suggestions_map["general"])
    
    async def _get_conversation(self, conversation_id: str, user_id: str) -> ChatConversation:
        """Get existing conversation or create new one"""
        if conversation_id:
            conversation = ChatConversation.query.get(conversation_id)
            if conversation:
                conversation.last_activity = datetime.utcnow()
                db.session.commit()
                return conversation
        
        # Create new conversation
        conversation = ChatConversation(
            user_id=user_id,
            started_at=datetime.utcnow(),
            last_activity=datetime.utcnow()
        )
        db.session.add(conversation)
        db.session.commit()
        
        return conversation
    
    async def _save_messages(self, conversation_id: str, user_message: str, bot_response: str):
        """Save conversation to database"""
        # Save user message
        user_msg = ChatMessage(
            conversation_id=conversation_id,
            message=user_message,
            is_user=True
        )
        db.session.add(user_msg)
        
        # Save bot response
        bot_msg = ChatMessage(
            conversation_id=conversation_id,
            message=bot_response,
            is_user=False
        )
        db.session.add(bot_msg)
        
        db.session.commit()
    
    def get_chat_analytics(self) -> Dict:
        """Get chatbot performance analytics"""
        total_conversations = ChatConversation.query.count()
        total_messages = ChatMessage.query.count()
        
        return {
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "average_messages_per_conversation": total_messages / total_conversations if total_conversations > 0 else 0,
            "active_conversations_today": ChatConversation.query.filter(
                ChatConversation.last_activity >= datetime.utcnow().date()
            ).count()
        }

class CustomerSupportSystem:
    def __init__(self):
        self.chatbot = MeganChatbot()
        self.escalation_threshold = 2  # Number of failed AI attempts before human escalation
        self.support_tickets = {}
    
    async def handle_support_ticket(self, user_id: str, subject: str, description: str) -> Dict:
        """Create and handle support ticket"""
        print(f"🎫 Creating support ticket for user {user_id}: {subject}")
        
        # Create ticket
        ticket = SupportTicket(
            user_id=user_id,
            subject=subject,
            description=description,
            category=await self._categorize_ticket(subject, description),
            priority=await self._determine_priority(description)
        )
        db.session.add(ticket)
        db.session.commit()
        
        # Try AI resolution first
        ai_response = await self._attempt_ai_resolution(ticket)
        
        if ai_response['can_resolve']:
            # Update ticket status
            ticket.status = 'resolved'
            ticket.assigned_to = 'ai_agent'
            db.session.commit()
            
            return {
                "ticket_id": ticket.id,
                "response": ai_response['message'],
                "resolved_by": "ai",
                "next_steps": ai_response['next_steps'],
                "resolution_time": "immediate"
            }
        else:
            # Escalate to human support
            return await self._escalate_to_human(ticket)
    
    async def _categorize_ticket(self, subject: str, description: str) -> str:
        """Categorize support ticket"""
        categories = {
            "technical": ["not working", "error", "bug", "crash", "login", "access", "video", "audio"],
            "billing": ["payment", "refund", "invoice", "charge", "billing", "subscription", "cancel"],
            "content": ["course", "video", "lesson", "material", "content", "curriculum"],
            "account": ["password", "login", "account", "profile", "settings"],
            "general": ["question", "help", "support", "information"]
        }
        
        combined_text = f"{subject} {description}".lower()
        
        for category, keywords in categories.items():
            if any(keyword in combined_text for keyword in keywords):
                return category
        
        return "general"
    
    async def _determine_priority(self, description: str) -> str:
        """Determine ticket priority"""
        urgent_keywords = ["not working", "emergency", "urgent", "critical", "cannot access", "broken", "down"]
        high_keywords = ["problem", "issue", "help", "support", "not loading", "error"]
        
        description_lower = description.lower()
        
        if any(keyword in description_lower for keyword in urgent_keywords):
            return "urgent"
        elif any(keyword in description_lower for keyword in high_keywords):
            return "high"
        else:
            return "medium"
    
    async def _attempt_ai_resolution(self, ticket: SupportTicket) -> Dict:
        """Attempt to resolve ticket using AI"""
        common_solutions = {
            "login": "Please try resetting your password using the 'Forgot Password' link on the login page. If you're still having trouble, clear your browser cache and cookies.",
            "payment": "Payment issues are usually resolved within 24 hours. Please check your bank statement to confirm the transaction. If the problem persists, contact our billing support team.",
            "video": "Try clearing your browser cache or using a different browser like Chrome or Firefox. Also check your internet connection and make sure you have the latest version of your browser.",
            "access": "Make sure you're logged into the correct account and that your subscription is active. You can check your subscription status in your account settings.",
            "content": "The course content should be accessible immediately after enrollment. If you can't see the content, try refreshing the page or logging out and back in."
        }
        
        description_lower = ticket.description.lower()
        
        for issue, solution in common_solutions.items():
            if issue in description_lower:
                return {
                    "can_resolve": True,
                    "message": f"I can help with that! {solution}",
                    "next_steps": ["Try the suggested solution", "Contact support if the issue persists", "Check your email for updates"]
                }
        
        return {
            "can_resolve": False,
            "message": "I've created a support ticket for you and our team will investigate this issue. We'll contact you shortly with a solution.",
            "next_steps": ["Wait for support response", "Check your email for updates", "Response within 24 hours"]
        }
    
    async def _escalate_to_human(self, ticket: SupportTicket) -> Dict:
        """Escalate ticket to human support"""
        ticket.assigned_to = "human_support"
        ticket.status = "in_progress"
        db.session.commit()
        
        # Store in local tracking
        self.support_tickets[ticket.id] = {
            "created_at": datetime.utcnow(),
            "user_id": ticket.user_id,
            "priority": ticket.priority
        }
        
        return {
            "ticket_id": ticket.id,
            "response": "I've escalated this to our human support team. They'll contact you within 24 hours with a solution to your issue.",
            "resolved_by": "human",
            "next_steps": ["Check your email for support updates", "Response within 24 hours", "Keep an eye on your ticket status"],
            "estimated_resolution_time": "24 hours"
        }
    
    def get_support_metrics(self) -> Dict:
        """Get support system performance metrics"""
        total_tickets = SupportTicket.query.count()
        resolved_tickets = SupportTicket.query.filter_by(status='resolved').count()
        ai_resolved = SupportTicket.query.filter_by(assigned_to='ai_agent', status='resolved').count()
        
        return {
            "total_tickets": total_tickets,
            "resolved_tickets": resolved_tickets,
            "resolution_rate": resolved_tickets / total_tickets if total_tickets > 0 else 0,
            "ai_resolution_rate": ai_resolved / resolved_tickets if resolved_tickets > 0 else 0,
            "average_resolution_time": "2 hours",  # This would be calculated from actual data
            "active_tickets": SupportTicket.query.filter_by(status='in_progress').count()
        }
