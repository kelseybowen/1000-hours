class User:

    def __init__(self, user_id, username, hour_target):
        self.user_id = user_id
        self.username = username
        self.hour_target = hour_target

    def __str__(self):
        return f'''User ID: {self.user_id}\nUsername: {self.username}\nHour Target: {self.hour_target}\n'''
