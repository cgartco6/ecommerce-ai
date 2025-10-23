# ai_core/marketing_automation.py (Enhanced)
class SocialMediaTracker:
    def __init__(self):
        self.campaign_metrics = {}
        self.performance_analyzer = PerformanceAnalyzer()
    
    async def track_campaign_performance(self, campaign_id: str) -> Dict:
        """Track real-time performance across all platforms"""
        platform_metrics = {}
        
        for platform_name in self.platforms.keys():
            metrics = await self._get_platform_metrics(platform_name, campaign_id)
            platform_metrics[platform_name] = metrics
        
        # Analyze overall performance
        analysis = self.performance_analyzer.analyze_campaign(platform_metrics)
        
        # Store metrics
        self.campaign_metrics[campaign_id] = {
            "timestamp": datetime.now(),
            "metrics": platform_metrics,
            "analysis": analysis
        }
        
        return analysis
    
    async def _get_platform_metrics(self, platform: str, campaign_id: str) -> Dict:
        """Get metrics from specific platform API"""
        # Simulated metrics - in production, integrate with platform APIs
        return {
            "impressions": random.randint(10000, 500000),
            "engagement_rate": random.uniform(0.03, 0.15),
            "click_through_rate": random.uniform(0.02, 0.08),
            "conversions": random.randint(50, 2000),
            "cost_per_conversion": random.uniform(5, 25),
            "roi": random.uniform(2.0, 8.0)
        }

class PerformanceAnalyzer:
    def analyze_campaign(self, platform_metrics: Dict) -> Dict:
        """Deep analysis of campaign performance"""
        total_conversions = sum(metrics['conversions'] for metrics in platform_metrics.values())
        total_impressions = sum(metrics['impressions'] for metrics in platform_metrics.values())
        
        return {
            "total_conversions": total_conversions,
            "total_impressions": total_conversions,
            "overall_roi": sum(metrics['roi'] for metrics in platform_metrics.values()) / len(platform_metrics),
            "best_performing_platform": max(platform_metrics.items(), key=lambda x: x[1]['conversions'])[0],
            "recommendations": self._generate_recommendations(platform_metrics),
            "conversion_trend": "increasing" if total_conversions > 100 else "stable"
        }
    
    def _generate_recommendations(self, metrics: Dict) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        for platform, data in metrics.items():
            if data['engagement_rate'] < 0.05:
                recommendations.append(f"Boost {platform} content creativity")
            if data['cost_per_conversion'] > 15:
                recommendations.append(f"Optimize {platform} targeting")
        
        return recommendations
