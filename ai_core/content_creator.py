# ai_core/content_creators.py (Enhanced)
class AddictiveContentFactory:
    def __init__(self):
        self.psychological_triggers = [
            "fear_of_missing_out", "social_proof", "scarcity", 
            "urgency", "authority", "reciprocity", "curiosity_gap"
        ]
        self.content_templates = self._load_addictive_templates()
    
    async def create_addictive_marketing_content(self, product_data: Dict) -> Dict:
        """Create highly addictive marketing content in HD quality"""
        content_batch = {}
        
        for platform in ["linkedin", "tiktok", "instagram", "facebook", "youtube", "x"]:
            platform_content = []
            
            # Create multiple content variations
            for i in range(5):  # 5 pieces per platform
                content = await self._create_platform_specific_content(platform, product_data, i)
                platform_content.append(content)
            
            content_batch[platform] = platform_content
        
        return content_batch
    
    async def _create_platform_specific_content(self, platform: str, product_data: Dict, variation: int) -> Dict:
        """Create platform-optimized addictive content"""
        base_content = {
            "platform": platform,
            "quality": "HD_4K",
            "psychological_triggers": random.sample(self.psychological_triggers, 3),
            "addictiveness_score": random.uniform(0.8, 0.95),
            "call_to_action": self._create_urgent_cta(),
            "visual_elements": ["dynamic_animation", "professional_graphics", "human_faces"]
        }
        
        if platform == "linkedin":
            return {
                **base_content,
                "format": "professional_carousel",
                "hook": f"How I made R{random.randint(50000, 500000)} with {product_data['topic']}",
                "content_length": "300-500 words",
                "hashtags": ["#careergrowth", "#success", "#entrepreneurship"]
            }
        elif platform == "tiktok":
            return {
                **base_content,
                "format": "viral_short",
                "hook": f"Secret {product_data['topic']} method they don't teach in school!",
                "duration": "15-45 seconds",
                "trending_audio": True,
                "hashtags": ["#viral", "#learnwithme", "#moneytok"]
            }
        
        # Add other platform-specific content creation logic
    
    def _create_urgent_cta(self) -> str:
        """Create urgent call-to-action"""
        ctas = [
            "🔥 LIMITED SPOTS: Enroll Now Before Price Increases!",
            "🚨 Only 7 Seats Left at This Price!",
            "⏰ Flash Sale Ending in 24 Hours - Don't Miss Out!",
            "💎 Join 4,327 Successful Students - Your Turn!"
        ]
        return random.choice(ctas)
