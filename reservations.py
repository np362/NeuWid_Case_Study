"""
The following program processes all functionalities for the reservation system
"""

class Reservation():
    def __init__(self, id, device_id, user_id, start_time, end_time) -> None:
        """Create a new reservation based on the given parameters"""
        self.id = id
        self.device_id = device_id
        self.user_id = user_id
        self.start_time = start_time
        self.end_time = end_time
    
    def show_reservation(self) -> str:
        """Return a string representation of the reservation"""
        return f"Reservation {self.id} - {self.device_id} - {self.user_id} - {self.start_time} - {self.end_time}"
    
    def record_reservation(self):
        """Save the reservation to the database"""
        pass

    def delete_reservation(self):
        """Delete the reservation from the database"""
        pass





