from SQLiteClient import SQLiteClient
from datetime import date, datetime, timedelta
from HourLog import HourLog
import json


class Calendar:

    def generate_full_year(self, start_date, end_date):

        delta = end_date - start_date
        today = datetime.today()
        j = 0
        date_list = []
        projections = None

        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            if j < len(self.logged_dates) and day.date() == self.logged_dates[j].date:
                self.total_hours_logged += self.logged_dates[j].hour_count
                date_list.append(self.logged_dates[j])
                j += 1
            elif day.date() < today.date():
                date_list.append(HourLog(-1, day.strftime("%Y-%m-%d"), self.user.user_id, 0, False))
            else:
                if projections == None:
                    self.remaining_hours = self.user.hour_target - self.total_hours_logged
                    projections = self.calculate_projected_daily_targets(self.remaining_hours, day)
                date_list.append(HourLog(-1, day.strftime("%Y-%m-%d"), self.user.user_id, projections[day.date()], True))

        return date_list

    def calculate_projected_daily_targets(self, remaining_hours, begin_projections, year=date.today().year):
        """
        Function written by David Bowen
        Function to calculate target hours for remaining days in a year
        Return a dictionary with keys of datetimes, i.e. daily_targets[date(2022, 5, 17)]
        Required argument is the remaining hours to distribute amongst the targets.
        Basic example: daily_targets = calculate_daily_targets(1000)
        Option arguments are the year (defaults to current year) and the latest completed date
        Example with optional arguments: daily_targets = calculate_daily_targets(target = 872, year = 2021,
        completed_date=date(2021, 5, 12)). Any dates including and prior to the provided completed date will not
        be included in the returned dictionary
        """
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        delta = end_date - start_date
        days = []
        for i in range(delta.days + 1):
            days.append((start_date + timedelta(days=i)))

        day_hopper = [[] for _ in range(5)]
        day_hopper[0].append(days[len(days) // 2])
        for i in range(1, len(days) // 2 + 1):
            if (len(days) // 2 + i) < len(days):
                day = days[len(days) // 2 + i]
                if day.month in [6, 7]:
                    day_hopper[0].append(day)
                elif day.month in [5, 8]:
                    day_hopper[1].append(day)
                elif day.month in [4, 9]:
                    day_hopper[2].append(day)
                elif day.month in [5, 10, 11]:
                    day_hopper[3].append(day)
                else:
                    day_hopper[4].append(day)

            if (len(days) // 2 - i) >= 0:
                day = days[len(days) // 2 - i]
                if day.month in [6, 7]:
                    day_hopper[0].append(day)
                elif day.month in [5, 8]:
                    day_hopper[1].append(day)
                elif day.month in [4, 9]:
                    day_hopper[2].append(day)
                elif day.month in [3, 10, 11]:
                    day_hopper[3].append(day)
                else:
                    day_hopper[4].append(day)

        daily_target_hours = {}
        allocated_hours = 0
        allocation_round = 0
        while allocated_hours < remaining_hours:
            for i in range(len(day_hopper) - (allocation_round % 5)):
                for j in range(len(day_hopper[i])):
                    if day_hopper[i][j] < begin_projections.date():
                        continue
                    if day_hopper[i][j] in daily_target_hours:
                        daily_target_hours[day_hopper[i][j]] += 1
                    else:
                        daily_target_hours[day_hopper[i][j]] = 1
                    allocated_hours += 1
                    if allocated_hours >= remaining_hours:
                        break
                if allocated_hours >= remaining_hours:
                    break
            allocation_round += 1
        return daily_target_hours

    def log_day(self, date, hours):
        if self.date_list[int(date.strftime("%j"))-1].log_id == -1:
            self.db.create_hour_log(self.user.user_id, date, hours)

        else:
            self.db.update_hour_log(self.date_list[int(date.strftime("%j"))-1].log_id, hours)
        self.logged_dates = self.db.get_all_hour_logs_range(self.user.user_id, datetime(2022, 1, 1),
                                                            datetime(2022, 12, 31))
        self.date_list = self.generate_full_year(datetime(2022, 1, 1), datetime(2022, 12, 31))

    def get_status(self):
        status_dict = {"Goal": self.user.hour_target, "Completed": self.total_hours_logged, "Remaining": self.remaining_hours}
        return status_dict

    def get_day(self, date):
        return self.date_list[int(date.strftime("%j"))-1]

    def update_goal(self, new_target):
        self.db.update_user_hour_target(self.user.user_id, new_target)

    def render_json(self):
        total = 0
        remaining = self.user.hour_target
        log_data = {self.user.user_id: {"Goal": self.user.hour_target, "Days": {}}}
        for log in self.date_list:
            total += log.hour_count
            remaining -= log.hour_count
            log_data[self.user.user_id]["Days"][log.date.strftime("%x")] = {"Hour Count": log.hour_count, "Projected": log.is_projected, "Completed": total, "Remaining": remaining}
        json_data = json.dumps(log_data)
        return json_data
        # with open("1000-hours-data.json", "w") as file:
        #     file.write(json_data)


    def __init__(self, username, database):
        self.db = SQLiteClient(database)
        self.user = self.db.get_user_by_username(username)
        self.remaining_hours = self.user.hour_target
        self.total_hours_logged = 0
        self.logged_dates = self.db.get_all_hour_logs_range(self.user.user_id, datetime(2022, 1, 1),
                                                    datetime(2022, 12, 31))
        self.date_list = self.generate_full_year(datetime(2022, 1, 1), datetime(2022, 12, 31))









