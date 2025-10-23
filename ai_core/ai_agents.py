# ai_core/ai_agents.py
import asyncio
from typing import Dict, List, Callable
import random
from datetime import datetime, timedelta

class AIAgent:
    def __init__(self, name: str, role: str, capabilities: List[str]):
        self.name = name
        self.role = role
        self.capabilities = capabilities
        self.performance_metrics = {}
        self.task_history = []
        
    async def execute_task(self, task: Dict) -> Dict:
        """Execute assigned task"""
        task_start = datetime.now()
        
        try:
            if task['type'] == 'course_creation':
                result = await self.create_course(task['parameters'])
            elif task['type'] == 'marketing':
                result = await self.run_marketing_campaign(task['parameters'])
            elif task['type'] == 'content_creation':
                result = await self.create_content(task['parameters'])
            elif task['type'] == 'analysis':
                result = await self.analyze_data(task['parameters'])
            elif task['type'] == 'support':
                result = await self.handle_support(task['parameters'])
            else:
                result = {"status": "error", "message": f"Unknown task type: {task['type']}"}
            
            # Track performance
            task_duration = (datetime.now() - task_start).total_seconds()
            self._track_performance(task['type'], 'success', task_duration)
            
            self.task_history.append({
                "task": task,
                "result": result,
                "duration": task_duration,
                "timestamp": datetime.now()
            })
            
            return result
            
        except Exception as e:
            self._track_performance(task['type'], 'error', 0)
            return {"status": "error", "message": str(e)}
        
    async def create_course(self, parameters: Dict) -> Dict:
        """AI agent for course creation"""
        course_data = {
            "title": f"AI-Generated Course: {parameters['topic']}",
            "description": self._generate_course_description(parameters['topic']),
            "modules": self._generate_course_modules(parameters['topic']),
            "difficulty": parameters.get('difficulty', 'beginner'),
            "estimated_duration": random.randint(8, 25),
            "learning_objectives": self._generate_learning_objectives(parameters['topic']),
            "target_audience": parameters.get('target_audience', 'beginners'),
            "prerequisites": parameters.get('prerequisites', ['basic computer skills']),
            "price_tier": parameters.get('price_tier', 'premium')
        }
        return {"status": "success", "course": course_data}
    
    async def run_marketing_campaign(self, parameters: Dict) -> Dict:
        """Execute marketing campaign"""
        campaign_data = {
            "campaign_name": f"AI-Driven Campaign: {parameters['product']}",
            "platforms": parameters.get('platforms', ['facebook', 'instagram', 'tiktok']),
            "budget": parameters.get('budget', 10000),
            "target_audience": parameters.get('target_audience', 'tech_enthusiasts'),
            "duration_days": parameters.get('duration', 14),
            "expected_reach": parameters['budget'] * 100,  # $1 = 100 reach
            "expected_conversions": parameters['budget'] * 0.05,  # 5% conversion
            "creative_assets": await self._generate_creative_assets(parameters)
        }
        return {"status": "success", "campaign": campaign_data}
    
    async def create_content(self, parameters: Dict) -> Dict:
        """Create marketing and educational content"""
        content_type = parameters.get('content_type', 'blog_post')
        
        if content_type == 'blog_post':
            content = self._generate_blog_post(parameters)
        elif content_type == 'social_media':
            content = self._generate_social_media_post(parameters)
        elif content_type == 'email':
            content = self._generate_email_content(parameters)
        else:
            content = {"error": f"Unsupported content type: {content_type}"}
        
        return {"status": "success", "content": content}
    
    def _generate_course_description(self, topic: str) -> str:
        descriptions = {
            'ai': f"Master Artificial Intelligence and Machine Learning with hands-on projects. Learn from industry experts and build real-world AI applications.",
            'programming': f"Comprehensive programming course covering fundamental concepts and advanced techniques. Perfect for beginners and experienced developers alike.",
            'data_science': f"Become a data science expert with this intensive course. Learn Python, statistics, machine learning, and data visualization.",
            'digital_marketing': f"Digital marketing mastery course covering SEO, social media, content marketing, and analytics. Grow your business online."
        }
        return descriptions.get(topic.lower(), f"Comprehensive course on {topic} covering essential skills and practical applications.")
    
    def _generate_course_modules(self, topic: str) -> List[Dict]:
        base_modules = [
            {"title": f"Introduction to {topic}", "duration": 2, "content_type": "video"},
            {"title": f"Fundamental Concepts", "duration": 3, "content_type": "video+quiz"},
            {"title": f"Practical Applications", "duration": 4, "content_type": "project"},
            {"title": f"Advanced Techniques", "duration": 3, "content_type": "video+assignment"},
            {"title": f"Real-world Project", "duration": 5, "content_type": "capstone"}
        ]
        return base_modules
    
    def _generate_learning_objectives(self, topic: str) -> List[str]:
        return [
            f"Understand core concepts of {topic}",
            f"Apply {topic} techniques to real problems",
            f"Build practical projects using {topic}",
            f"Prepare for {topic} related careers",
            f"Develop advanced {topic} skills"
        ]
    
    async def _generate_creative_assets(self, parameters: Dict) -> List[Dict]:
        return [
            {
                "type": "image",
                "platform": "instagram",
                "specs": {"format": "square", "size": "1080x1080"},
                "content": f"Promotional image for {parameters['product']}"
            },
            {
                "type": "video",
                "platform": "tiktok",
                "specs": {"format": "vertical", "duration": "30s"},
                "content": f"Short promotional video for {parameters['product']}"
            }
        ]
    
    def _generate_blog_post(self, parameters: Dict) -> Dict:
        return {
            "title": f"The Ultimate Guide to {parameters['topic']} in 2024",
            "content": f"Comprehensive article about {parameters['topic']} covering latest trends and best practices...",
            "keywords": [parameters['topic'], "guide", "2024", "tutorial"],
            "read_time": "8 min",
            "seo_optimized": True
        }
    
    def _generate_social_media_post(self, parameters: Dict) -> Dict:
        platforms = parameters.get('platforms', ['instagram'])
        posts = {}
        
        for platform in platforms:
            if platform == 'instagram':
                posts[platform] = {
                    "caption": f"🚀 Amazing insights about {parameters['topic']}! 👇\n\nLearn more in our latest course! 🔥",
                    "hashtags": ["#" + parameters['topic'].replace(' ', ''), "#learning", "#education"],
                    "image_required": True
                }
            elif platform == 'twitter':
                posts[platform] = {
                    "content": f"Just published: The complete guide to {parameters['topic']}! 🚀\n\nEssential reading for anyone in tech! 👇",
                    "hashtags": ["#" + parameters['topic'].replace(' ', ''), "#tech", "#AI"],
                    "thread_possible": True
                }
        
        return posts
    
    def _generate_email_content(self, parameters: Dict) -> Dict:
        return {
            "subject": f"Unlock Your Potential in {parameters['topic']}",
            "preheader": f"Start your journey to mastering {parameters['topic']} today",
            "body": f"Dear learner,\n\nWe're excited to help you master {parameters['topic']}...",
            "cta": "Start Learning Now",
            "personalization_fields": ["first_name", "skill_level"]
        }
    
    def _track_performance(self, task_type: str, status: str, duration: float):
        """Track agent performance metrics"""
        if task_type not in self.performance_metrics:
            self.performance_metrics[task_type] = {
                "total_tasks": 0,
                "successful_tasks": 0,
                "failed_tasks": 0,
                "average_duration": 0,
                "total_duration": 0
            }
        
        metrics = self.performance_metrics[task_type]
        metrics["total_tasks"] += 1
        metrics["total_duration"] += duration
        
        if status == 'success':
            metrics["successful_tasks"] += 1
        else:
            metrics["failed_tasks"] += 1
        
        metrics["average_duration"] = metrics["total_duration"] / metrics["total_tasks"]
        
    def get_performance_report(self) -> Dict:
        """Generate performance report"""
        return {
            "agent_name": self.name,
            "role": self.role,
            "total_tasks_completed": sum(m["total_tasks"] for m in self.performance_metrics.values()),
            "success_rate": self._calculate_success_rate(),
            "average_task_duration": self._calculate_average_duration(),
            "capabilities_utilized": list(self.performance_metrics.keys()),
            "recent_activity": self.task_history[-10:] if self.task_history else []
        }
    
    def _calculate_success_rate(self) -> float:
        """Calculate overall success rate"""
        if not self.performance_metrics:
            return 0.0
        
        total_tasks = sum(m["total_tasks"] for m in self.performance_metrics.values())
        successful_tasks = sum(m["successful_tasks"] for m in self.performance_metrics.values())
        
        return successful_tasks / total_tasks if total_tasks > 0 else 0.0
    
    def _calculate_average_duration(self) -> float:
        """Calculate average task duration"""
        if not self.performance_metrics:
            return 0.0
        
        total_duration = sum(m["total_duration"] for m in self.performance_metrics.values())
        total_tasks = sum(m["total_tasks"] for m in self.performance_metrics.values())
        
        return total_duration / total_tasks if total_tasks > 0 else 0.0

class CourseCreationAgent(AIAgent):
    def __init__(self):
        super().__init__("CourseCreator Pro", "course_development", 
                        ["content_generation", "curriculum_design", "assessment_creation", "quality_assurance"])
        
    async def create_comprehensive_course(self, topic: str, level: str = 'beginner') -> Dict:
        """Create a comprehensive course with all components"""
        course_parameters = {
            "topic": topic,
            "difficulty": level,
            "target_audience": self._determine_audience(level),
            "price_tier": self._determine_price_tier(level)
        }
        
        return await self.create_course(course_parameters)
    
    def _determine_audience(self, level: str) -> str:
        audiences = {
            'beginner': 'absolute beginners with no prior experience',
            'intermediate': 'learners with basic knowledge looking to advance',
            'advanced': 'experienced professionals seeking mastery'
        }
        return audiences.get(level, 'learners at all levels')
    
    def _determine_price_tier(self, level: str) -> str:
        tiers = {
            'beginner': 'standard',
            'intermediate': 'premium', 
            'advanced': 'enterprise'
        }
        return tiers.get(level, 'premium')

class MarketingAgent(AIAgent):
    def __init__(self):
        super().__init__("Marketing Pro", "digital_marketing",
                        ["campaign_management", "audience_targeting", "performance_analysis", "content_creation"])
        
    async def launch_viral_campaign(self, product: str, budget: float) -> Dict:
        """Launch viral marketing campaign"""
        parameters = {
            "product": product,
            "budget": budget,
            "platforms": ['tiktok', 'instagram', 'youtube', 'facebook'],
            "target_audience": 'viral_content_consumers',
            "duration": 7
        }
        
        return await self.run_marketing_campaign(parameters)

class AnalyticsAgent(AIAgent):
    def __init__(self):
        super().__init__("Data Analyst Pro", "business_analytics",
                        ["data_analysis", "trend_identification", "performance_reporting", "predictive_modeling"])
        
    async def analyze_business_performance(self, timeframe: str = 'weekly') -> Dict:
        """Analyze overall business performance"""
        # Simulated analysis - in production, connect to actual data
        return {
            "timeframe": timeframe,
            "revenue_growth": random.uniform(0.05, 0.25),
            "subscriber_growth": random.uniform(0.08, 0.35),
            "conversion_rate": random.uniform(0.03, 0.12),
            "churn_rate": random.uniform(0.02, 0.08),
            "top_performing_courses": ["AI Fundamentals", "Web Development", "Data Science"],
            "recommendations": [
                "Increase marketing spend on top-performing courses",
                "Improve onboarding for new subscribers",
                "Develop more advanced course content"
            ]
        }

class SupportAgent(AIAgent):
    def __init__(self):
        super().__init__("Support Assistant", "customer_support",
                        ["ticket_management", "issue_resolution", "customer_satisfaction", "knowledge_base"])
        
    async def handle_support(self, parameters: Dict) -> Dict:
        """Handle customer support requests"""
        issue_type = parameters.get('issue_type', 'general')
        user_message = parameters.get('message', '')
        
        responses = {
            'technical': "I can help with technical issues. Please try clearing your browser cache or using a different browser.",
            'billing': "For billing questions, please check your account settings or contact our billing department.",
            'content': "I can help with course content questions. Which specific course are you having trouble with?",
            'general': "Thank you for reaching out! How can I assist you today?"
        }
        
        response = responses.get(issue_type, responses['general'])
        
        return {
            "status": "success",
            "response": response,
            "resolution_confidence": random.uniform(0.7, 0.95),
            "follow_up_actions": ["Monitor ticket", "Escalate if needed", "Update knowledge base"]
        }

class AIAgentOrchestrator:
    def __init__(self):
        self.agents = {
            'course_creator': CourseCreationAgent(),
            'marketing': MarketingAgent(),
            'analytics': AnalyticsAgent(),
            'support': SupportAgent()
        }
        self.coordination_log = []
        
    async def coordinate_agents(self, business_plan: Dict) -> Dict:
        """Coordinate multiple AI agents to execute business plan"""
        coordination_id = f"coordination_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        tasks = self._create_agent_tasks(business_plan)
        results = {}
        
        # Execute tasks in parallel
        agent_tasks = []
        for agent_name, task in tasks.items():
            if agent_name in self.agents:
                agent_tasks.append(
                    self._execute_agent_task(agent_name, task, coordination_id)
                )
        
        # Wait for all tasks to complete
        task_results = await asyncio.gather(*agent_tasks, return_exceptions=True)
        
        # Process results
        for agent_name, result in zip(tasks.keys(), task_results):
            if isinstance(result, Exception):
                results[agent_name] = {"status": "error", "message": str(result)}
            else:
                results[agent_name] = result
        
        # Synthesize overall results
        final_result = self._synthesize_results(results, coordination_id)
        
        # Log coordination
        self.coordination_log.append({
            "coordination_id": coordination_id,
            "timestamp": datetime.now(),
            "business_plan": business_plan,
            "results": final_result
        })
        
        return final_result
    
    async def _execute_agent_task(self, agent_name: str, task: Dict, coordination_id: str) -> Dict:
        """Execute a single agent task with error handling"""
        try:
            agent = self.agents[agent_name]
            result = await agent.execute_task(task)
            return result
        except Exception as e:
            return {"status": "error", "message": f"Agent {agent_name} failed: {str(e)}"}
    
    def _create_agent_tasks(self, business_plan: Dict) -> Dict:
        """Create tasks for each agent based on business plan"""
        tasks = {}
        
        # Course creation tasks
        if 'course_development' in business_plan:
            tasks['course_creator'] = {
                'type': 'course_creation',
                'parameters': {
                    'topic': 'Artificial Intelligence',
                    'difficulty': 'beginner',
                    'target_audience': 'working professionals'
                }
            }
        
        # Marketing tasks
        if 'marketing_approach' in business_plan:
            tasks['marketing'] = {
                'type': 'marketing',
                'parameters': {
                    'product': 'AI Learning Platform',
                    'budget': 50000,
                    'platforms': ['facebook', 'instagram', 'linkedin'],
                    'duration': 30
                }
            }
        
        # Analytics tasks
        tasks['analytics'] = {
            'type': 'analysis',
            'parameters': {
                'timeframe': 'weekly',
                'metrics': ['revenue', 'subscribers', 'engagement']
            }
        }
        
        # Support tasks
        tasks['support'] = {
            'type': 'support',
            'parameters': {
                'issue_type': 'general',
                'message': 'Platform overview request'
            }
        }
        
        return tasks
    
    def _synthesize_results(self, results: Dict, coordination_id: str) -> Dict:
        """Synthesize results from all agents"""
        successful_tasks = sum(1 for r in results.values() if r.get('status') == 'success')
        total_tasks = len(results)
        
        return {
            "coordination_id": coordination_id,
            "overall_status": "completed" if successful_tasks == total_tasks else "partial",
            "success_rate": successful_tasks / total_tasks,
            "agent_results": results,
            "summary": f"Completed {successful_tasks} of {total_tasks} tasks successfully",
            "next_steps": self._generate_next_steps(results),
            "timestamp": datetime.now()
        }
    
    def _generate_next_steps(self, results: Dict) -> List[str]:
        """Generate next steps based on agent results"""
        next_steps = []
        
        if 'course_creator' in results and results['course_creator'].get('status') == 'success':
            next_steps.append("Review and publish new course content")
        
        if 'marketing' in results and results['marketing'].get('status') == 'success':
            next_steps.append("Monitor marketing campaign performance")
        
        if 'analytics' in results and results['analytics'].get('status') == 'success':
            next_steps.append("Implement analytics recommendations")
        
        next_steps.append("Schedule next coordination cycle")
        
        return next_steps
    
    def get_coordination_report(self) -> Dict:
        """Generate coordination performance report"""
        total_coordinations = len(self.coordination_log)
        successful_coordinations = sum(1 for log in self.coordination_log 
                                    if log['results']['overall_status'] == 'completed')
        
        return {
            "total_coordinations": total_coordinations,
            "success_rate": successful_coordinations / total_coordinations if total_coordinations > 0 else 0,
            "agent_performance": {name: agent.get_performance_report() for name, agent in self.agents.items()},
            "recent_activities": self.coordination_log[-5:] if self.coordination_log else []
        }
