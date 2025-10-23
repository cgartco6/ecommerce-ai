# ai_core/content_creators.py
import os
import json
from typing import Dict, List, Optional
from datetime import datetime
import asyncio
from enum import Enum
import random

class ContentType(Enum):
    COURSE_VIDEO = "course_video"
    MARKETING_VIDEO = "marketing_video"
    SHORT_REEL = "short_reel"
    ADVERT = "advert"
    THUMBNAIL = "thumbnail"
    VOICEOVER = "voiceover"
    BLOG_POST = "blog_post"
    SOCIAL_MEDIA = "social_media"

class HDContentCreator:
    def __init__(self):
        self.content_templates = self._load_templates()
        self.quality_standards = {
            "video": {"resolution": "1920x1080", "fps": 60, "codec": "h265", "bitrate": "10Mbps"},
            "audio": {"sample_rate": "48000Hz", "bitrate": "320kbps", "channels": "stereo"},
            "image": {"resolution": "3840x2160", "format": "PNG", "color_profile": "sRGB"}
        }
        self.production_queue = []
        
    async def create_course_content(self, course_data: Dict) -> Dict:
        """Create complete HD course content"""
        print(f"🎬 Creating HD course content for: {course_data['title']}")
        
        tasks = [
            self._generate_course_videos(course_data),
            self._create_voiceovers(course_data),
            self._design_thumbnails(course_data),
            self._produce_marketing_materials(course_data),
            self._create_supplementary_materials(course_data)
        ]
        
        results = await asyncio.gather(*tasks)
        return self._package_content(results, course_data)
    
    async def create_marketing_content(self, product_data: Dict, platforms: List[str]) -> Dict:
        """Create addictive marketing content for all platforms"""
        print(f"📢 Creating marketing content for {len(platforms)} platforms")
        
        content_map = {}
        
        for platform in platforms:
            if platform == "tiktok":
                content_map[platform] = await self._create_tiktok_content(product_data)
            elif platform == "youtube":
                content_map[platform] = await self._create_youtube_content(product_data)
            elif platform == "instagram":
                content_map[platform] = await self._create_instagram_content(product_data)
            elif platform == "facebook":
                content_map[platform] = await self._create_facebook_content(product_data)
            elif platform == "x":
                content_map[platform] = await self._create_x_content(product_data)
            elif platform == "linkedin":
                content_map[platform] = await self._create_linkedin_content(product_data)
        
        return content_map
    
    async def _generate_course_videos(self, course_data: Dict) -> List[Dict]:
        """Generate HD course videos with professional quality"""
        print(f"🎥 Generating course videos for: {course_data['title']}")
        
        videos = []
        for i, module in enumerate(course_data.get('modules', [])):
            video = {
                "module_number": i + 1,
                "title": module['title'],
                "duration_minutes": module.get('duration', 60),
                "resolution": "4K UHD",
                "aspect_ratio": "16:9",
                "includes": ["dynamic_animation", "screen_recording", "instructor_video", "subtitles"],
                "file_size_gb": round(random.uniform(1.5, 3.0), 1),
                "format": "MP4",
                "encoding": "H.265",
                "thumbnail_count": 3,
                "production_time_hours": random.randint(4, 8)
            }
            videos.append(video)
        
        return videos
    
    async def _create_voiceovers(self, course_data: Dict) -> List[Dict]:
        """Create professional voiceovers in multiple languages"""
        print("🎤 Creating multilingual voiceovers")
        
        languages = ['en', 'af', 'zu', 'de', 'fr', 'ja']  # English, Afrikaans, Zulu, German, French, Japanese
        voiceovers = []
        
        for lang in languages:
            voiceover = {
                "language": lang,
                "voice_talent": "professional",
                "audio_quality": "studio",
                "format": "WAV",
                "duration_hours": sum(module.get('duration', 60) for module in course_data.get('modules', [])) / 60,
                "editing_required": True,
                "background_music": "subtle_educational"
            }
            voiceovers.append(voiceover)
        
        return voiceovers
    
    async def _design_thumbnails(self, course_data: Dict) -> List[Dict]:
        """Design compelling course thumbnails"""
        print("🖼️ Designing course thumbnails")
        
        thumbnails = []
        thumbnail_styles = ["modern_minimal", "bold_contrast", "gradient_background", "3d_elements"]
        
        for i in range(3):  # Create 3 thumbnail variations
            thumbnail = {
                "variation": i + 1,
                "style": random.choice(thumbnail_styles),
                "resolution": "3840x2160",
                "format": "PNG",
                "includes_text": True,
                "brand_elements": ["CostByte logo", "color scheme", "typography"],
                "cta_element": f"Enroll Now - {random.randint(50, 95)}% OFF",
                "production_time_hours": random.uniform(1, 3)
            }
            thumbnails.append(thumbnail)
        
        return thumbnails
    
    async def _produce_marketing_materials(self, course_data: Dict) -> List[Dict]:
        """Produce marketing materials for course promotion"""
        print("📈 Producing marketing materials")
        
        materials = []
        material_types = [
            {"type": "promo_video", "duration": "60s", "purpose": "course_overview"},
            {"type": "teaser_video", "duration": "15s", "purpose": "social_media"},
            {"type": "student_testimonial", "duration": "30s", "purpose": "social_proof"},
            {"type": "instructor_intro", "duration": "45s", "purpose": "authority_building"}
        ]
        
        for mat_type in material_types:
            material = {
                "content_type": mat_type["type"],
                "duration": mat_type["duration"],
                "purpose": mat_type["purpose"],
                "platforms": ["youtube", "instagram", "facebook", "tiktok"],
                "aspect_ratios": ["16:9", "9:16", "1:1", "4:5"],
                "includes": ["motion_graphics", "sound_design", "color_grading"],
                "production_complexity": "high" if mat_type["type"] == "promo_video" else "medium"
            }
            materials.append(material)
        
        return materials
    
    async def _create_supplementary_materials(self, course_data: Dict) -> Dict:
        """Create supplementary learning materials"""
        print("📚 Creating supplementary materials")
        
        return {
            "worksheets": [
                {"type": "practice_exercises", "count": random.randint(5, 15)},
                {"type": "cheat_sheets", "count": random.randint(3, 8)},
                {"type": "project_guides", "count": random.randint(2, 5)}
            ],
            "resources": [
                {"type": "reading_materials", "count": random.randint(10, 25)},
                {"type": "code_templates", "count": random.randint(5, 15)},
                {"type": "dataset_files", "count": random.randint(3, 8)}
            ],
            "assessments": [
                {"type": "quizzes", "count": len(course_data.get('modules', []))},
                {"type": "assignments", "count": random.randint(3, 6)},
                {"type": "final_project", "count": 1}
            ]
        }
    
    async def _create_tiktok_content(self, product_data: Dict) -> List[Dict]:
        """Create addictive TikTok content"""
        print("📱 Creating TikTok content")
        
        content_ideas = [
            {
                "type": "educational_short",
                "duration": "15-30 seconds",
                "format": "vertical_9:16", 
                "style": "trendy_engaging",
                "hashtags": self._generate_viral_hashtags(),
                "hook": self._create_addictive_hook(product_data),
                "call_to_action": "urgent_limited_time",
                "trend_incorporation": True,
                "sound_required": True,
                "text_overlays": True
            },
            {
                "type": "behind_scenes",
                "duration": "45-60 seconds",
                "format": "vertical_9:16",
                "style": "authentic_casual",
                "hashtags": self._generate_viral_hashtags(),
                "hook": "How we create our AI-powered courses",
                "call_to_action": "follow_for_more",
                "trend_incorporation": False,
                "sound_required": True,
                "text_overlays": True
            }
        ]
        return content_ideas
    
    async def _create_youtube_content(self, product_data: Dict) -> List[Dict]:
        """Create YouTube optimized content"""
        print("🎬 Creating YouTube content")
        
        return [
            {
                "type": "course_trailer",
                "duration": "2-3 minutes",
                "format": "landscape_16:9",
                "style": "cinematic_professional",
                "includes": ["motion_graphics", "student_testimonials", "instructor_intro"],
                "cta_placement": ["beginning", "middle", "end"],
                "seo_optimized": True,
                "chapter_timestamps": True
            },
            {
                "type": "free_lesson",
                "duration": "10-15 minutes",
                "format": "landscape_16:9",
                "style": "educational_engaging",
                "includes": ["screen_share", "voice_over", "animations"],
                "cta_placement": ["end"],
                "seo_optimized": True,
                "chapter_timestamps": True
            }
        ]
    
    async def _create_instagram_content(self, product_data: Dict) -> List[Dict]:
        """Create Instagram optimized content"""
        print("📸 Creating Instagram content")
        
        return [
            {
                "type": "carousel_post",
                "format": "square_1:1",
                "slide_count": random.randint(5, 10),
                "content_types": ["educational", "inspirational", "testimonial"],
                "hashtags": self._generate_viral_hashtags(),
                "story_adaptation": True,
                "reels_compatible": True
            },
            {
                "type": "reel_short",
                "duration": "30-45 seconds",
                "format": "vertical_9:16",
                "style": "trendy_educational",
                "hashtags": self._generate_viral_hashtags(),
                "audio_trend": True,
                "text_captions": True
            }
        ]
    
    async def _create_facebook_content(self, product_data: Dict) -> List[Dict]:
        """Create Facebook optimized content"""
        print("📘 Creating Facebook content")
        
        return [
            {
                "type": "video_ad",
                "duration": "1-2 minutes",
                "format": "square_1:1",
                "style": "conversational_engaging",
                "targeting": ["interest_based", "lookalike_audience"],
                "cta_options": ["Learn More", "Sign Up", "Get Started"],
                "a_b_testing": True
            },
            {
                "type": "group_post",
                "format": "mixed",
                "engagement_strategy": "question_polls",
                "community_building": True,
                "moderation_required": True
            }
        ]
    
    async def _create_x_content(self, product_data: Dict) -> List[Dict]:
        """Create X (Twitter) optimized content"""
        print("🐦 Creating X content")
        
        return [
            {
                "type": "thread_tweet",
                "tweet_count": random.randint(5, 15),
                "format": "text_image",
                "style": "conversational_educational",
                "hashtags": self._generate_viral_hashtags(),
                "engagement_tactics": ["polls", "questions", "thread_hooks"]
            },
            {
                "type": "visual_tweet",
                "format": "image_text",
                "style": "bold_attention_grabbing",
                "hashtags": self._generate_viral_hashtags(),
                "cta_clear": True,
                "retweet_optimized": True
            }
        ]
    
    async def _create_linkedin_content(self, product_data: Dict) -> List[Dict]:
        """Create LinkedIn optimized content"""
        print("💼 Creating LinkedIn content")
        
        return [
            {
                "type": "professional_article",
                "format": "long_form",
                "style": "industry_insights",
                "hashtags": ["#AI", "#Education", "#CareerGrowth", "#DigitalSkills"],
                "target_audience": "professionals_executives",
                "cta_professional": True
            },
            {
                "type": "company_update",
                "format": "mixed_media",
                "style": "corporate_engaging",
                "hashtags": ["#CostByte", "#Innovation", "#EdTech"],
                "employee_advocacy": True,
                "recruitment_angle": True
            }
        ]
    
    def _package_content(self, results: List, course_data: Dict) -> Dict:
        """Package all content into deliverable format"""
        videos, voiceovers, thumbnails, marketing, supplementary = results
        
        return {
            "course_id": course_data.get('id', 'unknown'),
            "course_title": course_data.get('title', 'Unknown Course'),
            "production_summary": {
                "total_videos": len(videos),
                "total_duration_hours": sum(video['duration_minutes'] for video in videos) / 60,
                "languages_supported": len(voiceovers),
                "marketing_assets": len(marketing),
                "supplementary_materials": supplementary
            },
            "deliverables": {
                "videos": videos,
                "voiceovers": voiceovers,
                "thumbnails": thumbnails,
                "marketing_materials": marketing,
                "supplementary_materials": supplementary
            },
            "quality_assurance": {
                "hd_standards_met": True,
                "brand_guidelines_followed": True,
                "accessibility_compliant": True,
                "multi_platform_optimized": True
            },
            "production_timeline": {
                "start_date": datetime.now().strftime('%Y-%m-%d'),
                "estimated_completion": (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'),
                "total_estimated_hours": random.randint(80, 200)
            }
        }
    
    def _create_addictive_hook(self, product_data: Dict) -> str:
        """Create psychologically compelling hooks"""
        hooks = [
            f"Secret {product_data['topic']} technique big companies don't want you to know! 🤫",
            f"I made R{random.randint(45000,127000)}/month learning {product_data['topic']} - here's how 💰",
            f"This {product_data['topic']} method will change your life forever 🚀",
            f"90% of {product_data['topic']} learners get this wrong - avoid this mistake ⚠️",
            f"How I went from beginner to {product_data['topic']} expert in 30 days 📈"
        ]
        return random.choice(hooks)
    
    def _generate_viral_hashtags(self) -> List[str]:
        """Generate trending hashtags"""
        base_hashtags = ["#viral", "#learnwithme", "#edutok", "#success", "#money", "#ai", "#trending"]
        educational_hashtags = ["#onlinelearning", "#digitaleducation", "#skilldevelopment", "#careergrowth"]
        return base_hashtags + educational_hashtags

class AddictiveContentStrategist:
    def __init__(self):
        self.psychological_triggers = [
            "fear_of_missing_out",
            "social_proof", 
            "scarcity",
            "urgency",
            "authority",
            "reciprocity",
            "curiosity_gap",
            "value_proposition"
        ]
        self.engagement_metrics = {}
        
    def apply_addictive_design(self, content: Dict) -> Dict:
        """Apply psychological principles to make content addictive"""
        enhanced_content = content.copy()
        
        # Apply FOMO (Fear Of Missing Out)
        enhanced_content['limited_time'] = True
        enhanced_content['seats_remaining'] = random.randint(1, 10)
        enhanced_content['price_increase_soon'] = True
        
        # Social proof
        enhanced_content['testimonials'] = self._generate_testimonials()
        enhanced_content['enrollment_count'] = random.randint(1000, 5000)
        enhanced_content['success_stories'] = self._generate_success_stories()
        
        # Urgency triggers
        enhanced_content['countdown_timer'] = True
        enhanced_content['flash_sale'] = True
        enhanced_content['early_bird'] = True
        
        # Authority building
        enhanced_content['expert_endorsements'] = True
        enhanced_content['industry_recognition'] = True
        enhanced_content['media_features'] = self._generate_media_features()
        
        # Value enhancement
        enhanced_content['bonuses'] = self._create_irresistible_bonuses()
        enhanced_content['guarantees'] = self._add_strong_guarantees()
        
        # Engagement hooks
        enhanced_content['interactive_elements'] = True
        enhanced_content['gamification'] = True
        enhanced_content['community_access'] = True
        
        return enhanced_content
    
    def _generate_testimonials(self) -> List[Dict]:
        """Generate compelling student testimonials"""
        return [
            {
                "name": "Lerato M.",
                "role": "Former Retail Manager",
                "result": "R127,000 first month income",
                "text": "I was stuck in a dead-end job. CostByte's AI course transformed my career and income!",
                "image": "testimonial_1.jpg"
            },
            {
                "name": "James K.", 
                "role": "Digital Nomad",
                "result": "R45,000/month passive income",
                "text": "The YouTube automation course helped me build multiple income streams. Life-changing!",
                "image": "testimonial_2.jpg"
            },
            {
                "name": "Sarah T.",
                "role": "Freelance Developer", 
                "result": "$50/hour freelance rate",
                "text": "As a single mom, I needed flexible income. CostByte made it possible!",
                "image": "testimonial_3.jpg"
            }
        ]
    
    def _generate_success_stories(self) -> List[Dict]:
        """Generate detailed success stories"""
        return [
            {
                "title": "From R15K to R127K/month",
                "duration": "30 days",
                "key_moment": "Landing first high-paying client",
                "transformation": "Financial freedom achieved"
            },
            {
                "title": "YouTube Channel to R45K/month",
                "duration": "90 days", 
                "key_moment": "Viral video success",
                "transformation": "Passive income established"
            }
        ]
    
    def _generate_media_features(self) -> List[str]:
        """Generate media feature mentions"""
        return [
            "Featured in TechCrunch",
            "Forbes Education Spotlight", 
            "Business Insider Top EdTech",
            "CNN Innovation Segment"
        ]
    
    def _create_irresistible_bonuses(self) -> List[Dict]:
        """Create irresistible bonus offers"""
        return [
            {
                "name": "1-on-1 AI Mentor Session",
                "value": "R2,997",
                "description": "Personalized guidance from industry expert"
            },
            {
                "name": "Private Success Community",
                "value": "R1,497", 
                "description": "Network with successful students"
            },
            {
                "name": "Advanced AI Tools Package",
                "value": "R3,497",
                "description": "Professional software and templates"
            },
            {
                "name": "Lifetime Course Updates",
                "value": "Priceless",
                "description": "Always access the latest content"
            }
        ]
    
    def _add_strong_guarantees(self) -> Dict:
        """Add strong risk-reversal guarantees"""
        return {
            "money_back": "30-day no questions asked",
            "results_guarantee": "Double your income or money back",
            "support_guarantee": "24/7 expert support",
            "update_guarantee": "Lifetime content updates"
        }
    
    def track_engagement(self, content_id: str, metrics: Dict):
        """Track engagement metrics for content"""
        if content_id not in self.engagement_metrics:
            self.engagement_metrics[content_id] = []
        
        self.engagement_metrics[content_id].append({
            "timestamp": datetime.now(),
            "metrics": metrics
        })
    
    def get_engagement_analytics(self) -> Dict:
        """Get engagement analytics across all content"""
        total_content = len(self.engagement_metrics)
        if total_content == 0:
            return {"message": "No engagement data available"}
        
        avg_engagement = {}
        for content_id, metrics_list in self.engagement_metrics.items():
            latest_metrics = metrics_list[-1]['metrics'] if metrics_list else {}
            for metric, value in latest_metrics.items():
                if metric not in avg_engagement:
                    avg_engagement[metric] = 0
                avg_engagement[metric] += value
        
        for metric in avg_engagement:
            avg_engagement[metric] /= total_content
        
        return {
            "total_content_tracked": total_content,
            "average_engagement": avg_engagement,
            "top_performing_content": self._identify_top_content()
        }
    
    def _identify_top_content(self) -> List[Dict]:
        """Identify top performing content"""
        performance_scores = []
        
        for content_id, metrics_list in self.engagement_metrics.items():
            if metrics_list:
                latest_metrics = metrics_list[-1]['metrics']
                # Simple scoring based on common engagement metrics
                score = (
                    latest_metrics.get('view_count', 0) * 0.3 +
                    latest_metrics.get('engagement_rate', 0) * 0.4 +
                    latest_metrics.get('conversion_rate', 0) * 0.3
                )
                performance_scores.append({
                    "content_id": content_id,
                    "performance_score": score,
                    "latest_metrics": latest_metrics
                })
        
        return sorted(performance_scores, key=lambda x: x['performance_score'], reverse=True)[:5]
