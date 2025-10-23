# ai_core/self_healing.py
import asyncio
from typing import Dict, List
import logging
from datetime import datetime, timedelta
import random

class SelfHealingSystem:
    def __init__(self):
        self.health_monitor = SystemHealthMonitor()
        self.repair_agents = RepairAgents()
        self.incident_log = []
        self.healing_active = False
        self.performance_metrics = {
            "issues_detected": 0,
            "issues_resolved": 0,
            "auto_healing_success_rate": 0.0,
            "average_resolution_time": 0.0
        }
    
    async def monitor_and_heal(self):
        """Continuous monitoring and self-healing"""
        self.healing_active = True
        print("⚡ Starting self-healing system...")
        
        while self.healing_active:
            try:
                # Check system health
                health_status = await self.health_monitor.check_system_health()
                
                if health_status['overall_health'] < 0.8:
                    # System needs healing
                    healing_result = await self._trigger_healing_procedures(health_status)
                    
                    # Log the incident and healing attempt
                    incident_record = {
                        "timestamp": datetime.now(),
                        "health_status": health_status,
                        "healing_actions": healing_result,
                        "resolution_status": healing_result['overall_status']
                    }
                    self.incident_log.append(incident_record)
                    
                    # Update performance metrics
                    self._update_performance_metrics(healing_result)
                
                # Wait before next check
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logging.error(f"Self-healing system error: {e}")
                await self._emergency_recovery()
                await asyncio.sleep(30)  # Wait 30 seconds before retrying
    
    async def _trigger_healing_procedures(self, health_status: Dict) -> Dict:
        """Trigger appropriate healing procedures"""
        print("🛠️ Triggering self-healing procedures...")
        
        healing_actions = []
        issues_detected = []
        
        # Check each component and trigger appropriate healing
        if health_status['database_health'] < 0.7:
            issues_detected.append("database_performance")
            healing_actions.append(await self.repair_agents.fix_database_issues())
        
        if health_status['api_health'] < 0.7:
            issues_detected.append("api_connectivity")
            healing_actions.append(await self.repair_agents.restart_api_services())
        
        if health_status['performance_health'] < 0.7:
            issues_detected.append("system_performance")
            healing_actions.append(await self.repair_agents.optimize_performance())
        
        if health_status['security_health'] < 0.8:
            issues_detected.append("security_concerns")
            healing_actions.append(await self.repair_agents.enhance_security())
        
        if health_status['revenue_health'] < 0.7:
            issues_detected.append("revenue_system")
            healing_actions.append(await self.repair_agents.optimize_revenue_systems())
        
        # Determine overall status
        successful_actions = sum(1 for action in healing_actions if action['status'] == 'success')
        overall_status = "resolved" if successful_actions == len(healing_actions) else "partial"
        
        return {
            "issues_detected": issues_detected,
            "actions_taken": healing_actions,
            "overall_status": overall_status,
            "successful_actions": successful_actions,
            "total_actions": len(healing_actions),
            "estimated_recovery_time": self._estimate_recovery_time(healing_actions),
            "timestamp": datetime.now()
        }
    
    async def _emergency_recovery(self):
        """Emergency recovery procedures"""
        print("🚨 Executing emergency recovery procedures...")
        
        emergency_actions = [
            await self.repair_agents.emergency_restart(),
            await self.repair_agents.rollback_to_backup(),
            await self.repair_agents.notify_administrators()
        ]
        
        self.incident_log.append({
            "timestamp": datetime.now(),
            "type": "emergency_recovery",
            "actions": emergency_actions,
            "status": "executed"
        })
    
    def _estimate_recovery_time(self, healing_actions: List[Dict]) -> str:
        """Estimate recovery time based on actions taken"""
        total_time = sum(action.get('estimated_duration_minutes', 5) for action in healing_actions)
        
        if total_time <= 5:
            return "1-5 minutes"
        elif total_time <= 15:
            return "5-15 minutes"
        elif total_time <= 30:
            return "15-30 minutes"
        else:
            return "30+ minutes"
    
    def _update_performance_metrics(self, healing_result: Dict):
        """Update performance metrics after healing attempt"""
        self.performance_metrics["issues_detected"] += len(healing_result["issues_detected"])
        
        if healing_result["overall_status"] == "resolved":
            self.performance_metrics["issues_resolved"] += len(healing_result["issues_detected"])
        
        # Calculate success rate
        total_attempts = self.performance_metrics["issues_detected"]
        successful_resolutions = self.performance_metrics["issues_resolved"]
        
        if total_attempts > 0:
            self.performance_metrics["auto_healing_success_rate"] = successful_resolutions / total_attempts
    
    def get_system_health_report(self) -> Dict:
        """Get comprehensive system health report"""
        recent_incidents = [inc for inc in self.incident_log 
                           if (datetime.now() - inc['timestamp']).days < 7]
        
        return {
            "monitoring_status": "active" if self.healing_active else "inactive",
            "recent_incidents_7d": len(recent_incidents),
            "performance_metrics": self.performance_metrics,
            "current_health_status": self.health_monitor.get_current_status(),
            "preventive_measures": self._get_preventive_measures(),
            "recommendations": self._generate_health_recommendations()
        }
    
    def _get_preventive_measures(self) -> List[str]:
        """Get current preventive measures in place"""
        return [
            "Regular system health checks",
            "Automated backup procedures",
            "Performance monitoring",
            "Security vulnerability scanning",
            "Resource usage optimization"
        ]
    
    def _generate_health_recommendations(self) -> List[str]:
        """Generate health improvement recommendations"""
        recommendations = []
        
        if self.performance_metrics["auto_healing_success_rate"] < 0.8:
            recommendations.append("Improve healing procedure success rates")
        
        if len(self.incident_log) > 10:
            recommendations.append("Investigate recurring issues for permanent fixes")
        
        recommendations.extend([
            "Implement additional monitoring for critical components",
            "Schedule regular maintenance windows",
            "Enhance logging for better issue diagnosis"
        ])
        
        return recommendations
    
    def stop_monitoring(self):
        """Stop the self-healing monitoring"""
        self.healing_active = False
        print("🛑 Self-healing system stopped")

class SystemHealthMonitor:
    def __init__(self):
        self.health_metrics = {}
        self.health_history = []
    
    async def check_system_health(self) -> Dict:
        """Comprehensive system health check"""
        health_metrics = {
            "database_health": await self._check_database_health(),
            "api_health": await self._check_api_health(),
            "performance_health": await self._check_performance_health(),
            "security_health": await self._check_security_health(),
            "revenue_health": await self._check_revenue_health(),
            "user_experience_health": await self._check_user_experience_health()
        }
        
        overall_health = sum(health_metrics.values()) / len(health_metrics)
        
        health_status = {
            "timestamp": datetime.now(),
            "overall_health": overall_health,
            "component_health": health_metrics,
            "status": "healthy" if overall_health >= 0.8 else "needs_attention"
        }
        
        self.health_history.append(health_status)
        
        # Keep only last 1000 records
        if len(self.health_history) > 1000:
            self.health_history = self.health_history[-1000:]
        
        return health_status
    
    async def _check_database_health(self) -> float:
        """Check database health and performance"""
        # Simulate database health check
        base_health = 0.9
        issues = random.random() < 0.1  # 10% chance of minor issues
        
        if issues:
            return base_health - random.uniform(0.1, 0.3)
        return base_health
    
    async def _check_api_health(self) -> float:
        """Check API health and responsiveness"""
        # Simulate API health check
        base_health = 0.95
        issues = random.random() < 0.05  # 5% chance of API issues
        
        if issues:
            return base_health - random.uniform(0.1, 0.4)
        return base_health
    
    async def _check_performance_health(self) -> float:
        """Check system performance"""
        # Simulate performance check
        base_health = 0.85
        performance_issues = random.random() < 0.15  # 15% chance of performance issues
        
        if performance_issues:
            return base_health - random.uniform(0.1, 0.35)
        return base_health
    
    async def _check_security_health(self) -> float:
        """Check security health"""
        # Simulate security check
        base_health = 0.92
        security_concerns = random.random() < 0.03  # 3% chance of security concerns
        
        if security_concerns:
            return base_health - random.uniform(0.2, 0.5)
        return base_health
    
    async def _check_revenue_health(self) -> float:
        """Check revenue system health"""
        # Simulate revenue system check
        base_health = 0.88
        revenue_issues = random.random() < 0.08  # 8% chance of revenue system issues
        
        if revenue_issues:
            return base_health - random.uniform(0.1, 0.4)
        return base_health
    
    async def _check_user_experience_health(self) -> float:
        """Check user experience health"""
        # Simulate UX health check
        base_health = 0.87
        ux_issues = random.random() < 0.12  # 12% chance of UX issues
        
        if ux_issues:
            return base_health - random.uniform(0.1, 0.3)
        return base_health
    
    def get_current_status(self) -> Dict:
        """Get current system status"""
        if not self.health_history:
            return {"status": "unknown", "message": "No health data available"}
        
        latest_health = self.health_history[-1]
        
        return {
            "status": latest_health["status"],
            "overall_score": latest_health["overall_health"],
            " weakest_component": min(latest_health["component_health"].items(), key=lambda x: x[1])[0],
            "trend": self._calculate_health_trend()
        }
    
    def _calculate_health_trend(self) -> str:
        """Calculate health trend over time"""
        if len(self.health_history) < 2:
            return "stable"
        
        recent_scores = [h["overall_health"] for h in self.health_history[-5:]]
        if len(recent_scores) < 2:
            return "stable"
        
        current = recent_scores[-1]
        previous = recent_scores[-2]
        
        if current > previous + 0.05:
            return "improving"
        elif current < previous - 0.05:
            return "declining"
        else:
            return "stable"

class RepairAgents:
    async def fix_database_issues(self) -> Dict:
        """Fix database performance and connectivity issues"""
        print("🗄️ Repairing database issues...")
        await asyncio.sleep(2)  # Simulate repair time
        
        return {
            "action": "database_optimization",
            "status": "success",
            "details": "Database indexes optimized, connections pooled",
            "estimated_duration_minutes": 5,
            "impact": "improved_performance"
        }
    
    async def restart_api_services(self) -> Dict:
        """Restart API services"""
        print("🔌 Restarting API services...")
        await asyncio.sleep(3)
        
        return {
            "action": "api_service_restart",
            "status": "success",
            "details": "API services restarted, load balanced",
            "estimated_duration_minutes": 3,
            "impact": "restored_connectivity"
        }
    
    async def optimize_performance(self) -> Dict:
        """Optimize system performance"""
        print("⚡ Optimizing system performance...")
        await asyncio.sleep(4)
        
        return {
            "action": "performance_optimization",
            "status": "success",
            "details": "Cache optimized, resources reallocated",
            "estimated_duration_minutes": 8,
            "impact": "faster_response_times"
        }
    
    async def enhance_security(self) -> Dict:
        """Enhance security measures"""
        print("🛡️ Enhancing security...")
        await asyncio.sleep(2)
        
        return {
            "action": "security_enhancement",
            "status": "success",
            "details": "Security protocols updated, monitoring enhanced",
            "estimated_duration_minutes": 10,
            "impact": "improved_security_posture"
        }
    
    async def optimize_revenue_systems(self) -> Dict:
        """Optimize revenue-related systems"""
        print("💰 Optimizing revenue systems...")
        await asyncio.sleep(3)
        
        return {
            "action": "revenue_system_optimization",
            "status": "success",
            "details": "Payment processing optimized, reporting enhanced",
            "estimated_duration_minutes": 7,
            "impact": "improved_revenue_flow"
        }
    
    async def emergency_restart(self) -> Dict:
        """Emergency system restart"""
        print("🚨 Executing emergency restart...")
        await asyncio.sleep(5)
        
        return {
            "action": "emergency_restart",
            "status": "success",
            "details": "Critical systems restarted in safe mode",
            "estimated_duration_minutes": 15,
            "impact": "system_recovery"
        }
    
    async def rollback_to_backup(self) -> Dict:
        """Rollback to latest backup"""
        print("💾 Rolling back to backup...")
        await asyncio.sleep(10)
        
        return {
            "action": "backup_rollback",
            "status": "success",
            "details": "System rolled back to last stable backup",
            "estimated_duration_minutes": 20,
            "impact": "data_recovery"
        }
    
    async def notify_administrators(self) -> Dict:
        """Notify system administrators"""
        print("📧 Notifying administrators...")
        await asyncio.sleep(1)
        
        return {
            "action": "admin_notification",
            "status": "success",
            "details": "Administrators notified of emergency situation",
            "estimated_duration_minutes": 2,
            "impact": "human_intervention_triggered"
        }
