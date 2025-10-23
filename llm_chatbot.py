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
            "expertise": "course recommendations, technical support, billing questions",
            "response_style": "helpful, detailed, and encouraging"
        }
        self.knowledge_base = self._load_knowledge_base()
        
    async def process_message(self, user_message: str, user_id: str, conversation_id: str = None) -> Dict:
        """Process user message and generate response"""
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
            "timestamp": datetime.utcnow()
        }
    
    async def _analyze_intent(self, message: str) -> Dict:
        """Analyze user intent using AI"""
        intents = {
            "course_info": ["course", "learn", "what is", "how to", "tutorial"],
            "pricing": ["price", "cost", "how much", "discount", "free"],
            "technical_support": ["help", "problem", "issue", "not working", "error"],
            "billing": ["payment", "bill", "invoice", "refund", "cancel"],
            "career_advice": ["career", "job", "employment", "salary", "hire"]
        }
        
        message_lower = message.lower()
        detected_intents = []
        
        for intent, keywords in intents.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_intents.append(intent)
        
        return {
            "primary_intent": detected_intents[0] if detected_intents else "general",
            "all_intents": detected_intents,
            "confidence": 0.85
        }
    
    async def _generate_response(self, user_message: str, intent: Dict, conversation_id: str) -> str:
        """Generate AI response based on intent"""
        if intent["primary_intent"] == "course_info":
            return await self._handle_course_inquiry(user_message)
        elif intent["primary_intent"] == "pricing":
            return await self._handle_pricing_inquiry(user_message)
        elif intent["primary_intent"] == "technical_support":
            return await self._handle_technical_support(user_message)
        elif intent["primary_intent"] == "billing":
            return await self._handle_billing_inquiry(user_message)
        elif intent["primary_intent"] == "career_advice":
            return await self._handle_career_advice(user_message)
        else:
            return await self._handle_general_inquiry(user_message)
    
    async def _handle_course_inquiry(self, message: str) -> str:
        """Handle course-related inquiries"""
        responses = [
            "I'd love to help you find the perfect course! We have several options focused on AI, programming, and digital marketing. Which specific area are you interested in?",
            "Our courses are designed to get you real results quickly. We have options for beginners to advanced learners. What skill would you like to develop?",
            "Based on what you're asking, I recommend our 'AI-Powered Trading' course - it's our most popular and students are seeing amazing results! Would you like more details?"
        ]
        return await self._select_best_response(message, responses)
    
    async def _handle_pricing_inquiry(self, message: str) -> str:
        """Handle pricing questions"""
        responses = [
            "Our courses range from R1,997 to R4,997 with flexible payment options. We also have a 30-day money-back guarantee! Which course are you considering?",
            "The investment in your education pays for itself quickly - many students make back their course fee in the first month! Current pricing starts at R1,997.",
            "We're running a special launch offer with 75% discount for the first 5000 students. The regular price is R7,997 but you can enroll today for just R1,997!"
        ]
        return await self._select_best_response(message, responses)
    
    async def _handle_technical_support(self, message: str) -> str:
        """Handle technical support issues"""
        return "I'm sorry you're experiencing technical issues! Our support team can help resolve this quickly. Can you provide more details about what's happening?"
    
    async def _handle_billing_inquiry(self, message: str) -> str:
        """Handle billing and payment questions"""
        return "I can help with billing questions! We accept all major payment methods including FNB transfers. For specific payment issues, our billing team will assist you promptly."
    
    async def _handle_career_advice(self, message: str) -> str:
        """Provide career guidance"""
        responses = [
            "The skills you learn here are in high demand! Our graduates typically see 3-5x salary increases. Which career path interests you?",
            "Digital skills are the future! Learning AI and programming can open doors to remote work and high-paying opportunities. What's your current experience level?"
        ]
        return await self._select_best_response(message, responses)
    
    async def _handle_general_inquiry(self, message: str) -> str:
        """Handle general conversations"""
        responses = [
            "I'm Megan, your AI learning assistant! I'm here to help you succeed with your education goals. How can I assist you today?",
            "Welcome! I'm excited to help you on your learning journey. What would you like to know about our courses or platform?",
            "Hello! I'm here to support your learning experience. Feel free to ask me anything about courses, pricing, or technical support!"
        ]
        return await self._select_best_response(message, responses)
    
    async def _select_best_response(self, message: str, responses: List[str]) -> str:
        """Select the most appropriate response (simplified - in production use AI)"""
        # Simple keyword matching - in production, use proper NLP
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['beginner', 'start', 'new']):
            return responses[1] if len(responses) > 1 else responses[0]
        elif any(word in message_lower for word in ['popular', 'best', 'recommend']):
            return responses[2] if len(responses) > 2 else responses[0]
        else:
            return responses[0]
    
    async def _generate_suggestions(self, intent: Dict) -> List[str]:
        """Generate suggested follow-up questions"""
        suggestions_map = {
            "course_info": [
                "What's the best course for beginners?",
                "How long does each course take?",
                "Can I see a course preview?"
            ],
            "pricing": [
                "Do you offer payment plans?",
                "Is there a money-back guarantee?",
                "Are there any discounts available?"
            ],
            "technical_support": [
                "Contact human support",
                "Reset my password",
                "Technical requirements"
            ],
            "general": [
                "View all courses",
                "Contact support",
                "Pricing information"
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

class CustomerSupportSystem:
    def __init__(self):
        self.chatbot = MeganChatbot()
        self.escalation_threshold = 2  # Number of failed AI attempts before human escalation
    
    async def handle_support_ticket(self, user_id: str, subject: str, description: str) -> Dict:
        """Create and handle support ticket"""
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
            return {
                "ticket_id": ticket.id,
                "response": ai_response['message'],
                "resolved_by": "ai",
                "next_steps": ai_response['next_steps']
            }
        else:
            # Escalate to human support
            return await self._escalate_to_human(ticket)
    
    async def _categorize_ticket(self, subject: str, description: str) -> str:
        """Categorize support ticket"""
        categories = {
            "technical": ["not working", "error", "bug", "crash", "login"],
            "billing": ["payment", "refund", "invoice", "charge"],
            "content": ["course", "video", "lesson", "material"],
            "general": ["question", "help", "support"]
        }
        
        combined_text = f"{subject} {description}".lower()
        
        for category, keywords in categories.items():
            if any(keyword in combined_text for keyword in keywords):
                return category
        
        return "general"
    
    async def _determine_priority(self, description: str) -> str:
        """Determine ticket priority"""
        urgent_keywords = ["not working", "emergency", "urgent", "critical", "cannot access"]
        high_keywords = ["problem", "issue", "help", "support"]
        
        description_lower = description.lower()
        
        if any(keyword in description_lower for keyword in urgent_keywords):
            return "urgent"
        elif any(keyword in description_lower for keyword in high_keywords):
            return "high"
        else:
            return "medium"
    
    async def _attempt_ai_resolution(self, ticket: SupportTicket) -> Dict:
        """Attempt to resolve ticket using AI"""
        # Simple rule-based resolution - in production, use proper AI
        common_solutions = {
            "login": "Please try resetting your password using the 'Forgot Password' link.",
            "payment": "Payment issues are usually resolved within 24 hours. Check your bank statement or contact billing support.",
            "video": "Try clearing your browser cache or using a different browser. Videos work best on Chrome or Firefox."
        }
        
        description_lower = ticket.description.lower()
        
        for issue, solution in common_solutions.items():
            if issue in description_lower:
                return {
                    "can_resolve": True,
                    "message": f"I can help with that! {solution}",
                    "next_steps": ["Try the suggested solution", "Contact support if issue persists"]
                }
        
        return {
            "can_resolve": False,
            "message": "I've created a support ticket for you. Our team will contact you shortly.",
            "next_steps": ["Wait for support response", "Check your email for updates"]
        }
    
    async def _escalate_to_human(self, ticket: SupportTicket) -> Dict:
        """Escalate ticket to human support"""
        ticket.assigned_to = "human_support"
        ticket.status = "in_progress"
        db.session.commit()
        
        return {
            "ticket_id": ticket.id,
            "response": "I've escalated this to our human support team. They'll contact you within 24 hours.",
            "resolved_by": "human",
            "next_steps": ["Check your email", "Response within 24 hours"]
        }
