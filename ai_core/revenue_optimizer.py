# Revenue optimization
class RevenueOptimizer:
    def __init__(self):
        self.conversion_funnels = {}
    
    def project_revenue(self, current_subscribers: int) -> Dict:
        """Project revenue growth based on current metrics"""
        weekly_growth_rate = 0.25  # 25% weekly growth
        
        projections = {
            "week_1": current_subscribers,
            "week_2": int(current_subscribers * (1 + weekly_growth_rate)),
            "week_3": int(current_subscribers * (1 + weekly_growth_rate) ** 2),
            "month_1": int(current_subscribers * (1 + weekly_growth_rate) ** 4),
            "month_3": int(current_subscribers * (1 + weekly_growth_rate) ** 12)
        }
        
        # Convert to revenue (average course price R2,497)
        revenue_projections = {k: v * 2497 for k, v in projections.items()}
        
        return revenue_projections
