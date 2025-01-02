"""
The following program processes all functionalities for the reservation system
"""
from datetime import datetime, date, time



class Reservation():

    reservations = [
    {
        "id": 1,
        "device_id": 1,
        "user_id": 1,
        "start_time": datetime.combine(date.today(), time(10, 0)),
        "end_time": datetime.combine(date.today(), time(12, 0))
    },
    {
        "id": 2,
        "device_id": 2,
        "user_id": 2,
        "start_time": datetime.combine(date.today(), time(12, 0)),
        "end_time": datetime.combine(date.today(), time(14, 0))
    },
    {
        "id": 3,
        "device_id": 3,
        "user_id": 3,
        "start_time": datetime.combine(date.today(), time(14, 0)),
        "end_time": datetime.combine(date.today(), time(16, 0))
    }
    ]

    def __init__(self, id, device_id, user_id, start_time, end_time) -> None:
        """Create a new reservation based on the given parameters"""
        self.id = id
        self.device_id = device_id
        self.user_id = user_id
        self.start_time = start_time
        self.end_time = end_time
    
    @classmethod
    def get_all_reservations(cls):
        """Return a string representation of the reservation"""
        return cls.reservations
    
    @classmethod
    def add_reservation(cls, device_id, user_id, start_time, end_time):
        """Add the reservation to the database"""
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

        for reservation in cls.reservations:
            if device_id == reservation["device_id"]:
                if start_time < reservation["end_time"] and end_time > reservation["start_time"]:
                    raise ValueError("Dieses Gerät ist zum angegebenen Zeitpunkt bereits reserviert.")



        new_id = max(r["id"] for r in cls.reservations) + 1
        cls.reservations.append({
            "id": new_id,
            "device_id": device_id,
            "user_id": user_id,
            "start_time": start_time,
            "end_time": end_time
        })

    @classmethod
    def delete_reservation(cls, reservation_id):
        """Delete the reservation from the database"""
        cls.reservations = [r for r in cls.reservations if r["id"] != reservation_id]





