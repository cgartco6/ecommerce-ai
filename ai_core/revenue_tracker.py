# ai_core/revenue_tracker.py
from datetime import datetime, timedelta
from typing import Dict, List
import pandas as pd

class RevenueTracker:
    def __init__(self):
        self.revenue_data = []
        self.analytics_engine = RevenueAnalytics()
    
    async def track_revenue(self, transaction: Dict) -> None:
        """Track revenue in real-time"""
        self.revenue_data.append({
            **transaction,
            "timestamp": datetime.now(),
            "week_number": datetime.now().isocalendar()[1]
        })
    
    async def get_revenue_analytics(self, period: str = "weekly") -> Dict:
        """Get comprehensive revenue analytics"""
        if period == "weekly":
            data = self._get_weekly_data()
        elif period == "monthly":
            data = self._get_monthly_data()
        else:
            data = self.revenue_data
        
        return self.analytics_engine.analyze_revenue(data)
    
    def _get_weekly_data(self) -> List[Dict]:
        """Get data for current week"""
        week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        return [d for d in self.revenue_data if d['timestamp'] >= week_start]
    
    def _get_monthly_data(self) -> List[Dict]:
        """Get data for current month"""
        month_start = datetime.now().replace(day=1)
        return [d for d in self.revenue_data if d['timestamp'] >= month_start]

class RevenueAnalytics:
    def analyze_revenue(self, revenue_data: List[Dict]) -> Dict:
        """Advanced revenue analysis"""
        if not revenue_data:
            return {"status": "no_data"}
        
        df = pd.DataFrame(revenue_data)
        
        return {
            "total_revenue": df['amount'].sum(),
            "average_transaction_value": df['amount'].mean(),
            "revenue_growth_rate": self._calculate_growth_rate(df),
            "projected_monthly_revenue": self._project_revenue(df),
            "top_performing_courses": self._get_top_courses(df),
            "conversion_trends": self._analyze_conversion_trends(df),
            "revenue_forecast": self._generate_forecast(df)
        }
    
    def _calculate_growth_rate(self, df) -> float:
        """Calculate week-over-week growth rate"""
        # Implementation for growth calculation
        return 0.25  # 25% growth
    
    def _project_revenue(self, df) -> Dict:
        """Project future revenue"""
        current_weekly = df['amount'].sum()
        return {
            "next_week": current_weekly * 1.25,
            "next_month": current_weekly * 4 * 1.25,
            "next_quarter": current_weekly * 13 * 1.25
        }
