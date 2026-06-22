import json
from dataclasses import dataclass
from datetime import datetime

@dataclass
class RevenueData:
    revenue: float
    user_id: int
    timestamp: str

class AuthLicence:
    def __init__(self):
        self.revenue_data = []

    def track_revenue(self, revenue: float, user_id: int):
        self.revenue_data.append(RevenueData(revenue, user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def get_analytics(self):
        total_revenue = sum(data.revenue for data in self.revenue_data)
        user_activity = {data.user_id: sum(d.revenue for d in self.revenue_data if d.user_id == data.user_id) for data in self.revenue_data}
        return total_revenue, user_activity

    def detect_fraud(self):
        # Simple fraud detection: if a user has more than 10 transactions in the last minute
        recent_transactions = [data for data in self.revenue_data if (datetime.now() - datetime.strptime(data.timestamp, "%Y-%m-%d %H:%M:%S")).total_seconds() < 60]
        user_transactions = {data.user_id: sum(1 for d in recent_transactions if d.user_id == data.user_id) for data in recent_transactions}
        return {user_id: count for user_id, count in user_transactions.items() if count > 10}
