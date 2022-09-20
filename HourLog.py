from datetime import *

class HourLog:

    def __init__(self, log_id, date, user_id, hour_count, is_projected: bool):

        self.log_id = log_id
        self.user_id = user_id
        self.date = datetime.strptime(date, "%Y-%m-%d").date()
        self.hour_count = hour_count
        self.is_projected = is_projected

    def __str__(self):
        return f'''Log ID: {self.log_id}\nDate: {self.date}\nUser ID: {self.user_id}\nHour Count: {self.hour_count}\nIs projected: {self.is_projected}\n'''
