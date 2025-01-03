"""
This module contains the maintenance functions for the database.
"""

from datetime import datetime, date, time

class Maintenance:

    maintenances = [
        {
            "id": 1,
            "device_id": 1,
            "start_time": datetime.combine(date.today(), time(10, 0)),
            "end_time": datetime.combine(date.today(), time(12, 0)),
            "cost": 100
        },
        {
            "id": 2,
            "device_id": 2,
            "start_time": datetime.combine(date.today(), time(12, 0)),
            "end_time": datetime.combine(date.today(), time(14, 0)),
            "cost": 200
        },
        {
            "id": 3,
            "device_id": 3,
            "start_time": datetime.combine(date.today(), time(14, 0)),
            "end_time": datetime.combine(date.today(), time(16, 0)),
            "cost": 150
        }
    ]

    def __init__(self, id: int, device_id: int, start_time: datetime, end_time: datetime) -> None:
        """Create a new maintenance based on the given parameters"""
        self.id = id
        self.device_id = device_id
        self.start_time = start_time
        self.end_time = end_time

    @classmethod
    def show_maintenance(cls) -> str:
        """Return a string representation of the maintenance"""
        return cls.maintenances
    
    @classmethod
    def configure_maintenance(cls, device_id, start_time, end_time, cost):
        """Configure the maintenance from the database"""
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

        maintenance_found = False

        for maintenance in cls.maintenances:
            if device_id == maintenance["device_id"]:
                maintenance["end_time"] = end_time
                maintenance["start_time"] = start_time
                maintenance["cost"] = cost
                maintenance_found = True
                break
            
        if not maintenance_found: 
            new_id = max(m["id"] for m in cls.maintenances) + 1
            cls.maintenances.append({
                "id": new_id,
                "device_id": device_id,
                "start_time": start_time,
                "end_time": end_time,
                "cost": cost
        })
    
    @classmethod
    def calculate_quarterly_costs(cls):
        """Calculate maintenance costs per quarter"""
        cost = 0
        for maintenance in cls.maintenances:
            cost += maintenance["cost"]
        return cost