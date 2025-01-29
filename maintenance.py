"""
This module contains the maintenance functions for the database.
"""
import os
from tinydb import TinyDB
from serializer import serializer
from datetime import datetime, date, time, timedelta

class Maintenance:

    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('devices')
    data = db_connector.all()
    if data:
        maintenances = [
            {
                "id": 1,
                "device_id": 1,
                "start_time": datetime.combine(date.today()+timedelta(days=2), time(10, 0)),
                "end_time": datetime.combine(date.today()+timedelta(days=2), time(12, 0)),
                "cost": 100
            },
            {
                "id": 2,
                "device_id": 2,
                "start_time": datetime.combine(date.today()+timedelta(days=2), time(12, 0)),
                "end_time": datetime.combine(date.today()+timedelta(days=2), time(14, 0)),
                "cost": 200
            },
            {
                "id": 3,
                "device_id": 3,
                "start_time": datetime.combine(date.today()+timedelta(days=2), time(14, 0)),
                "end_time": datetime.combine(date.today()+timedelta(days=2), time(16, 0)),
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
    def calculate_interval_until_maintenance(cls, id: int):
        """Berechnet die Zeit bis zur nächsten Wartung für die angegebene ID."""
        now = datetime.now()
        time_until_maintenance = None
        
        for maintenance in cls.maintenances:
            if maintenance["id"] == id:
                diff = (maintenance["start_time"] - now).days
                if time_until_maintenance is None or diff < time_until_maintenance:
                    time_until_maintenance = diff
        
        return time_until_maintenance

    @classmethod
    def get_maintenance_cost(cls, id: int):
        """Get the maintenance cost for the given id"""
        for maintenance in cls.maintenances:
            if maintenance["id"] == id:
                return maintenance["cost"]
        return None
    
    @classmethod
    def get_maintenance_start_time(cls, id: int):
        """Get the maintenance start time for the given id"""
        for maintenance in cls.maintenances:
            if maintenance["id"] == id:
                return maintenance["start_time"]
        return None

    @classmethod
    def calculate_quarterly_costs(cls):
        """Calculate maintenance costs per quarter"""
        cost = 0
        for maintenance in cls.maintenances:
            cost += maintenance["cost"]
        return cost