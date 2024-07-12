def zellers(year, month, day):
    """ Zeller's congruence  http://en.wikipedia.org/wiki/Zeller%27s_congruence ,1 = Monday to 7 = Sunday , """
    if month in [1, 2]:
        month += 12
        year -= 1

    K = year % 100  # K the year of the century
    J = year // 100  # J the zero base century (floor division)
    z = (day + int(13 * (month + 1) / 5.0) + K + int(K / 4.0))
    z_greg = z + int(J / 4.0) - 2 * J
    z_jul = z + 5 - J

    h = (z_greg % 7) if year > 1582 else (z_jul % 7)
    h = 7 if h == 0 else h

    return (h + 5) % 7 + 1


def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def mapping_days_in_month(year):
    month_days = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    if is_leap_year(year):
        month_days[2] = 29  # 29 days in Feb if leap year
    return month_days


def get_weekdays_in_year(year):
    dow = zellers(year, 1, 1)
    if not is_leap_year(year):
        return 261 if dow in [1, 2, 3, 4, 5] else 260
    else:
        return 262 if dow in [1, 2, 3, 4] else 261 if dow in [5, 7] else 260


def get_count_daily(dow, count, current_year, current_month, current_day, days_in_month_dict):
    count += 1 if dow in [1, 2, 3, 4, 5] else 0

    dow = dow + 1 if dow < 7 else 1

    current_day += 1

    if current_day > days_in_month_dict[current_year][current_month]:
        current_day = 1
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1

    return dow, count, current_year, current_month, current_day


def get_count_annually(current_year, count):
    count += get_weekdays_in_year(current_year)
    current_year += 1

    return count, current_year


def weekdays(start_date, end_date):
    start_year, start_month, start_day = map(int, start_date.split('-'))
    end_year, end_month, end_day = map(int, end_date.split('-'))

    # dict to handle days in a month and leap years
    days_in_month_dict = {year: mapping_days_in_month(year) for year in range(start_year, end_year + 1)}

    # getting the first day of the week to count from
    dow = zellers(start_year, start_month, start_day)

    # count weekdays
    count = 0

    current_year = start_year
    current_month = start_month
    current_day = start_day

    # handling input mistake if start-date later than end-date
    if (current_year, current_month, current_day) > (end_year, end_month, end_day):
        return 0

    # partial first calendar
    while current_year < end_year and (current_month != 1 or current_day != 1):
        dow, count, current_year, current_month, current_day = (
            get_count_daily(dow, count, current_year, current_month, current_day, days_in_month_dict))

    # complete calendar year(s)
    while (current_year < end_year and (current_month == 1 and current_day == 1) or
           current_year == end_year and (end_month == 12 and end_day == 31)):
        count, current_year = get_count_annually(current_year, count)

    # partial last calendar year
    dow = zellers(current_year, current_month, current_day)
    while (current_year, current_month, current_day) <= (end_year, end_month, end_day):
        dow, count, current_year, current_month, current_day = (
            get_count_daily(dow, count, current_year, current_month, current_day, days_in_month_dict))

    return count


if __name__ == '__main__':

    user_start_date = '1776-7-4'
    user_end_date = '2024-7-12'

    print(f'Between {user_start_date} and {user_end_date} '
          f'there are {weekdays(user_start_date, user_end_date)} weekdays')
