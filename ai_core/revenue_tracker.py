# ai_core/revenue_tracker.py
from datetime import datetime, timedelta
from typing import Dict, List
import pandas as pd
import random

class RevenueTracker:
    def __init__(self):
        self.revenue_data = []
        self.analytics_engine = RevenueAnalytics()
        self.daily_targets = {
            "subscribers": 715,  # 5000 per week
            "revenue_zar": 3570000,  # 25M per week
            "conversion_rate": 0.08
        }
    
    async def track_revenue(self, transaction: Dict) -> None:
        """Track revenue in real-time"""
        tracked_transaction = {
            **transaction,
            "timestamp": datetime.now(),
            "week_number": datetime.now().isocalendar()[1],
            "month_number": datetime.now().month,
            "year": datetime.now().year
        }
        
        self.revenue_data.append(tracked_transaction)
        print(f"💰 Revenue tracked: ZAR {transaction.get('amount', 0):,}")
    
    async def get_revenue_analytics(self, period: str = "weekly") -> Dict:
        """Get comprehensive revenue analytics"""
        if period == "weekly":
            data = self._get_weekly_data()
        elif period == "monthly":
            data = self._get_monthly_data()
        elif period == "daily":
            data = self._get_daily_data()
        else:
            data = self.revenue_data
        
        return self.analytics_engine.analyze_revenue(data, self.daily_targets)
    
    def _get_weekly_data(self) -> List[Dict]:
        """Get data for current week"""
        week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        return [d for d in self.revenue_data if d['timestamp'] >= week_start]
    
    def _get_monthly_data(self) -> List[Dict]:
        """Get data for current month"""
        month_start = datetime.now().replace(day=1)
        return [d for d in self.revenue_data if d['timestamp'] >= month_start]
    
    def _get_daily_data(self) -> List[Dict]:
        """Get data for current day"""
        day_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return [d for d in self.revenue_data if d['timestamp'] >= day_start]
    
    def get_revenue_targets(self) -> Dict:
        """Get current revenue targets"""
        return {
            "daily_targets": self.daily_targets,
            "weekly_targets": {
                "subscribers": self.daily_targets["subscribers"] * 7,
                "revenue_zar": self.daily_targets["revenue_zar"] * 7
            },
            "monthly_targets": {
                "subscribers": self.daily_targets["subscribers"] * 30,
                "revenue_zar": self.daily_targets["revenue_zar"] * 30
            }
        }
    
    def update_targets(self, new_targets: Dict):
        """Update revenue targets"""
        self.daily_targets.update(new_targets)
        print("🎯 Revenue targets updated")

class RevenueAnalytics:
    def analyze_revenue(self, revenue_data: List[Dict], targets: Dict) -> Dict:
        """Advanced revenue analysis"""
        if not revenue_data:
            return {"status": "no_data", "message": "No revenue data available"}
        
        df = pd.DataFrame(revenue_data)
        
        # Calculate key metrics
        total_revenue = df['amount'].sum()
        total_subscribers = len(df)
        avg_transaction_value = df['amount'].mean()
        
        # Time-based analysis
        daily_revenue = self._calculate_daily_revenue(df)
        weekly_trend = self._calculate_weekly_trend(df)
        
        # Target performance
        target_performance = self._calculate_target_performance(total_revenue, total_subscribers, targets)
        
        # Predictive analytics
        revenue_forecast = self._generate_forecast(df)
        
        return {
            "summary_metrics": {
                "total_revenue": total_revenue,
                "total_subscribers": total_subscribers,
                "average_transaction_value": avg_transaction_value,
                "revenue_growth_rate": self._calculate_growth_rate(df),
                "customer_acquisition_cost": self._estimate_cac(df)
            },
            "time_analysis": {
                "daily_revenue": daily_revenue,
                "weekly_trend": weekly_trend,
                "best_performing_day": self._get_best_performing_day(df),
                "revenue_momentum": self._assess_momentum(df)
            },
            "target_performance": target_performance,
            "predictive_insights": revenue_forecast,
            "optimization_recommendations": self._generate_recommendations(df, target_performance)
        }
    
    def _calculate_daily_revenue(self, df) -> List[Dict]:
        """Calculate daily revenue breakdown"""
        if 'timestamp' not in df.columns:
            return []
        
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        daily = df.groupby('date').agg({
            'amount': 'sum',
            'id': 'count'  # Assuming 'id' represents transactions
        }).reset_index()
        
        return daily.to_dict('records')
    
    def _calculate_weekly_trend(self, df) -> Dict:
        """Calculate weekly revenue trends"""
        if 'week_number' not in df.columns:
            return {"trend": "stable", "confidence": "low"}
        
        weekly = df.groupby('week_number')['amount'].sum()
        
        if len(weekly) < 2:
            return {"trend": "insufficient_data", "confidence": "low"}
        
        # Simple trend calculation
        recent_weeks = weekly.tail(4)  # Last 4 weeks
        if len(recent_weeks) >= 2:
            trend = "growing" if recent_weeks.iloc[-1] > recent_weeks.iloc[-2] else "declining"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "weekly_growth": self._calculate_weekly_growth(weekly),
            "confidence": "medium"
        }
    
    def _calculate_target_performance(self, total_revenue: float, total_subscribers: int, targets: Dict) -> Dict:
        """Calculate performance against targets"""
        daily_revenue_target = targets.get("revenue_zar", 1000000)
        daily_subscriber_target = targets.get("subscribers", 100)
        
        revenue_performance = (total_revenue / daily_revenue_target) * 100
        subscriber_performance = (total_subscribers / daily_subscriber_target) * 100
        
        return {
            "revenue_target_achievement": min(revenue_performance, 100),
            "subscriber_target_achievement": min(subscriber_performance, 100),
            "overall_performance": (revenue_performance + subscriber_performance) / 2,
            "status": "on_track" if revenue_performance >= 80 and subscriber_performance >= 80 else "needs_attention"
        }
    
    def _generate_forecast(self, df) -> Dict:
        """Generate revenue forecast"""
        if len(df) < 7:  # Need at least 7 days of data
            return {
                "next_week_forecast": "insufficient_data",
                "next_month_forecast": "insufficient_data",
                "confidence": "low"
            }
        
        # Simple forecasting based on recent trend
        recent_revenue = df['amount'].tail(7).sum()
        growth_rate = self._calculate_growth_rate(df)
        
        next_week_forecast = recent_revenue * (1 + growth_rate)
        next_month_forecast = recent_revenue * 4 * (1 + growth_rate) ** 4
        
        return {
            "next_week_forecast": next_week_forecast,
            "next_month_forecast": next_month_forecast,
            "confidence": "medium",
            "assumptions": ["Current growth rate continues", "No major market changes"]
        }
    
    def _calculate_growth_rate(self, df) -> float:
        """Calculate week-over-week growth rate"""
        if 'week_number' not in df.columns or len(df) < 14:  # Need 2 weeks of data
            return 0.1  # Default 10% growth
        
        weekly_revenue = df.groupby('week_number')['amount'].sum()
        if len(weekly_revenue) < 2:
            return 0.1
        
        current_week = weekly_revenue.iloc[-1]
        previous_week = weekly_revenue.iloc[-2]
        
        return (current_week - previous_week) / previous_week if previous_week > 0 else 0.1
    
    def _estimate_cac(self, df) -> float:
        """Estimate customer acquisition cost"""
        # This would normally come from marketing data
        # For simulation, using industry averages
        return random.uniform(500, 2000)  # ZAR 500-2000 per customer
    
    def _get_best_performing_day(self, df) -> str:
        """Identify best performing day of week"""
        if 'timestamp' not in df.columns:
            return "unknown"
        
        df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.day_name()
        daily_performance = df.groupby('day_of_week')['amount'].sum()
        
        return daily_performance.idxmax() if not daily_performance.empty else "unknown"
    
    def _assess_momentum(self, df) -> str:
        """Assess revenue momentum"""
        if len(df) < 2:
            return "starting"
        
        recent_days = df.tail(7)
        if len(recent_days) < 2:
            return "stable"
        
        current_revenue = recent_days['amount'].sum()
        previous_revenue = df['amount'].head(7).sum() if len(df) >= 14 else current_revenue * 0.8
        
        momentum = (current_revenue - previous_revenue) / previous_revenue
        
        if momentum > 0.1:
            return "accelerating"
        elif momentum > 0:
            return "growing"
        elif momentum > -0.1:
            return "stable"
        else:
            return "slowing"
    
    def _calculate_weekly_growth(self, weekly_series) -> float:
        """Calculate specific weekly growth rates"""
        if len(weekly_series) < 2:
            return 0.0
        
        growth_rates = []
        for i in range(1, len(weekly_series)):
            growth = (weekly_series.iloc[i] - weekly_series.iloc[i-1]) / weekly_series.iloc[i-1]
            growth_rates.append(growth)
        
        return sum(growth_rates) / len(growth_rates) if growth_rates else 0.0
    
    def _generate_recommendations(self, df, target_performance: Dict) -> List[str]:
        """Generate revenue optimization recommendations"""
        recommendations = []
        
        if target_performance['revenue_target_achievement'] < 80:
            recommendations.extend([
                "Increase marketing spend on high-converting channels",
                "Optimize pricing strategy for better conversion",
                "Launch limited-time promotion to boost sales"
            ])
        
        if target_performance['subscriber_target_achievement'] < 80:
            recommendations.extend([
                "Improve onboarding experience for new users",
                "Enhance free trial to paid conversion funnel",
                "Implement referral program to leverage existing users"
            ])
        
        # Always include general recommendations
        recommendations.extend([
            "Analyze customer lifetime value by acquisition channel",
            "Test different pricing tiers and packages",
            "Optimize checkout process for higher completion rates"
        ])
        
        return recommendations
