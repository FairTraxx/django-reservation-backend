from datetime import datetime
todaysdate=datetime.today().date()
requested_start_date = datetime.strptime(
            '2021-05-27T18:00:00Z', '%Y-%m-%dT%H:%M:%S%z')
print(requested_start_date.replace(hour = 12, minute =0, second =0,microsecond = 0))
