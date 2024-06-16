
def timedelta_to_years_months_days(td):
    # Total number of days
    days = td.days

    # Convert days to years
    years = days // 365
    remaining_days = days % 365

    # Convert remaining days to months
    months = remaining_days // 30
    remaining_days = remaining_days % 30

    return years, months, remaining_days