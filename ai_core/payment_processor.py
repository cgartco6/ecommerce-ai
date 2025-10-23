# ai_core/payment_processor.py
import hashlib
from typing import Dict
from decimal import Decimal
from datetime import datetime
import random

class FNBPaymentProcessor:
    def __init__(self):
        self.accounts = {
            "owner_account": "6212345678901",  # FNB Main Account
            "ai_operations_account": "6212345678902",  # FNB AI Account
            "reserve_account": "6212345678903"  # FNB Reserve Account
        }
        self.payout_distribution = {
            "owner": Decimal('0.60'),  # 60%
            "ai_operations": Decimal('0.20'),  # 20%
            "reserve": Decimal('0.20')  # 20%
        }
        self.transaction_history = []
    
    async def process_payment(self, amount: Decimal, customer_data: Dict) -> Dict:
        """Process payment and distribute to FNB accounts"""
        print(f"💳 Processing payment: ZAR {amount}")
        
        # Process payment (simulate FNB integration)
        payment_result = await self._fnb_payment_gateway(amount, customer_data)
        
        if payment_result['status'] == 'success':
            # Distribute funds according to allocation
            distribution = self._distribute_funds(amount)
            
            # Execute payouts
            payout_results = await self._execute_payouts(distribution)
            
            # Record transaction
            transaction_record = {
                "transaction_id": payment_result['transaction_id'],
                "amount": amount,
                "customer_email": customer_data.get('email'),
                "distribution": distribution,
                "payouts": payout_results,
                "timestamp": datetime.now(),
                "status": "completed"
            }
            self.transaction_history.append(transaction_record)
            
            return {
                "payment_status": "completed",
                "amount": amount,
                "distribution": distribution,
                "payouts": payout_results,
                "transaction_id": payment_result['transaction_id']
            }
        
        return {"payment_status": "failed", "error": payment_result['error']}
    
    def _distribute_funds(self, amount: Decimal) -> Dict:
        """Distribute funds to various FNB accounts"""
        return {
            "owner_amount": amount * self.payout_distribution['owner'],
            "ai_operations_amount": amount * self.payout_distribution['ai_operations'],
            "reserve_amount": amount * self.payout_distribution['reserve'],
            "distribution_breakdown": {
                "owner_percentage": float(self.payout_distribution['owner'] * 100),
                "ai_operations_percentage": float(self.payout_distribution['ai_operations'] * 100),
                "reserve_percentage": float(self.payout_distribution['reserve'] * 100)
            }
        }
    
    async def _execute_payouts(self, distribution: Dict) -> Dict:
        """Execute payouts to FNB accounts"""
        payouts = {}
        
        for account_type, amount in [(k, v) for k, v in distribution.items() if k.endswith('_amount')]:
            base_type = account_type.replace('_amount', '')
            account_number = self.accounts[f"{base_type}_account"]
            
            payout_result = await self._fnb_transfer(account_number, amount)
            payouts[base_type] = payout_result
        
        return payouts
    
    async def _fnb_payment_gateway(self, amount: Decimal, customer_data: Dict) -> Dict:
        """Simulate FNB payment gateway integration"""
        # Simulate processing delay
        await asyncio.sleep(1)
        
        # Simulate random failures (2% failure rate)
        if random.random() < 0.02:
            return {
                "status": "failed",
                "error": "Payment processing failed - please try again",
                "transaction_id": None
            }
        
        # Successful payment
        return {
            "status": "success",
            "transaction_id": f"FNB_{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:16]}",
            "amount": amount,
            "currency": "ZAR",
            "processed_at": datetime.now().isoformat()
        }
    
    async def _fnb_transfer(self, account_number: str, amount: Decimal) -> Dict:
        """Simulate FNB bank transfer"""
        # Simulate transfer processing
        await asyncio.sleep(0.5)
        
        return {
            "status": "completed",
            "to_account": account_number,
            "amount": amount,
            "reference": f"COSTBYTE_{datetime.now().strftime('%Y%m%d')}",
            "timestamp": datetime.now(),
            "transfer_id": f"TRF_{hashlib.md5((account_number + str(datetime.now())).encode()).hexdigest()[:12]}"
        }
    
    def get_transaction_history(self, days: int = 7) -> List[Dict]:
        """Get transaction history for specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        return [t for t in self.transaction_history if t['timestamp'] >= cutoff_date]
    
    def get_revenue_summary(self) -> Dict:
        """Get revenue summary"""
        recent_transactions = self.get_transaction_history(30)  # Last 30 days
        
        total_revenue = sum(Decimal(str(t['amount'])) for t in recent_transactions)
        total_transactions = len(recent_transactions)
        
        distribution_totals = {
            "owner": Decimal('0'),
            "ai_operations": Decimal('0'),
            "reserve": Decimal('0')
        }
        
        for transaction in recent_transactions:
            dist = transaction['distribution']
            distribution_totals['owner'] += dist['owner_amount']
            distribution_totals['ai_operations'] += dist['ai_operations_amount']
            distribution_totals['reserve'] += dist['reserve_amount']
        
        return {
            "period": "last_30_days",
            "total_revenue": total_revenue,
            "total_transactions": total_transactions,
            "average_transaction_value": total_revenue / total_transactions if total_transactions > 0 else Decimal('0'),
            "distribution_summary": distribution_totals,
            "success_rate": len([t for t in recent_transactions if t['status'] == 'completed']) / total_transactions if total_transactions > 0 else 0
        }

class RevenueDistributor:
    def __init__(self):
        self.payment_processor = FNBPaymentProcessor()
        self.daily_distributions = []
    
    async def distribute_daily_revenue(self) -> Dict:
        """Distribute daily revenue to FNB accounts"""
        print("💰 Executing daily revenue distribution...")
        
        daily_revenue = await self._calculate_daily_revenue()
        distribution_results = {}
        
        for transaction in daily_revenue['transactions']:
            result = await self.payment_processor.process_payment(
                Decimal(str(transaction['amount'])),
                transaction['customer_data']
            )
            distribution_results[transaction['id']] = result
        
        # Record daily distribution
        distribution_record = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "total_distributed": daily_revenue['total'],
            "transaction_count": len(daily_revenue['transactions']),
            "distribution_details": distribution_results,
            "timestamp": datetime.now()
        }
        self.daily_distributions.append(distribution_record)
        
        return {
            "daily_revenue": daily_revenue['total'],
            "distributions": distribution_results,
            "date": datetime.now().strftime('%Y-%m-%d'),
            "status": "completed"
        }
    
    async def _calculate_daily_revenue(self) -> Dict:
        """Calculate daily revenue for distribution"""
        # In production, this would query the database for today's transactions
        # For simulation, generate mock data
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Mock transactions for simulation
        mock_transactions = [
            {
                "id": f"txn_{i}",
                "amount": random.randint(1997, 4997),
                "customer_data": {
                    "email": f"customer{i}@example.com",
                    "name": f"Customer {i}"
                },
                "timestamp": today_start + timedelta(hours=random.randint(0, 23))
            }
            for i in range(random.randint(50, 200))  # 50-200 transactions per day
        ]
        
        total_revenue = sum(t['amount'] for t in mock_transactions)
        
        return {
            "total": total_revenue,
            "transactions": mock_transactions,
            "transaction_count": len(mock_transactions)
        }
    
    def get_distribution_history(self, days: int = 7) -> List[Dict]:
        """Get distribution history"""
        cutoff_date = datetime.now() - timedelta(days=days)
        return [d for d in self.daily_distributions if d['timestamp'] >= cutoff_date]
    
    def generate_financial_report(self) -> Dict:
        """Generate comprehensive financial report"""
        recent_distributions = self.get_distribution_history(30)
        
        total_distributed = sum(d['total_distributed'] for d in recent_distributions)
        average_daily_revenue = total_distributed / len(recent_distributions) if recent_distributions else 0
        
        return {
            "report_period": "last_30_days",
            "total_revenue_distributed": total_distributed,
            "average_daily_revenue": average_daily_revenue,
            "total_transactions": sum(d['transaction_count'] for d in recent_distributions),
            "account_balances": self._estimate_account_balances(recent_distributions),
            "growth_metrics": self._calculate_growth_metrics(recent_distributions),
            "compliance_status": "fully_compliant"
        }
    
    def _estimate_account_balances(self, distributions: List[Dict]) -> Dict:
        """Estimate current account balances"""
        # This would normally come from bank API
        # For simulation, calculate based on distributions
        total_distributed = sum(d['total_distributed'] for d in distributions)
        
        return {
            "owner_account": total_distributed * 0.60,
            "ai_operations_account": total_distributed * 0.20,
            "reserve_account": total_distributed * 0.20
        }
    
    def _calculate_growth_metrics(self, distributions: List[Dict]) -> Dict:
        """Calculate revenue growth metrics"""
        if len(distributions) < 2:
            return {"weekly_growth": 0, "monthly_growth": 0, "trend": "insufficient_data"}
        
        # Calculate weekly growth
        recent_week = distributions[-7:] if len(distributions) >= 7 else distributions
        previous_week = distributions[-14:-7] if len(distributions) >= 14 else recent_week
        
        recent_week_revenue = sum(d['total_distributed'] for d in recent_week)
        previous_week_revenue = sum(d['total_distributed'] for d in previous_week)
        
        weekly_growth = (recent_week_revenue - previous_week_revenue) / previous_week_revenue if previous_week_revenue > 0 else 0
        
        return {
            "weekly_growth": weekly_growth,
            "monthly_growth": weekly_growth * 4,  # Simplified projection
            "trend": "growing" if weekly_growth > 0 else "stable",
            "momentum": "strong" if weekly_growth > 0.1 else "moderate"
        }
