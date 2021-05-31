from datetime import datetime as dt, timedelta 


from datetime import timezone
now = dt.now(timezone.utc)
now1 = dt.now(timezone.utc)+timedelta(days=2)

print(now<now1)

