# simple example with datetime module

from datetime import datetime
now = datetime.now()
print(now.year, now.strftime("%A"))


# creating date objects

from datetime import datetime
data = datetime(2020, 5, 17)
print(data)  


# date formatting

drugaya_data = datetime(2018, 6, 1)
print(drugaya_data.strftime("%B %d, %Y")) 


# calculating time differences

from datetime import datetime, timedelta
data1 = datetime(2023, 1, 1)
data2 = datetime(2023, 12, 31)
print(data2 - data1) 


# working with timezones

from datetime import datetime, timezone
print(datetime.now(timezone.utc))

