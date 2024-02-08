from datetime import datetime, timedelta
import calendar


# функция для создания срока годности реферального кода равного 1 месяцу
def function_valid_until():
    date = datetime.now()
    days_in_month = calendar.monthrange(date.year, date.month)[1]
    date += timedelta(days=days_in_month)
    print(date)
    return date
