import datetime

def is_in_next_7_days(date_to_check, today) -> bool:
  return date_to_check >= today and date_to_check <= today + datetime.timedelta(days=7)