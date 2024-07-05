def zellers(year, month, day):
    """ Algo from:  http://en.wikipedia.org/wiki/Zeller%27s_congruence
    Zeller's congruence is an algorithm devised by Christian Zeller in the 19th century
    to calculate the day of the week for any Julian or Gregorian calendar date.
    1 = Monday to 7 = Sunday , """
    m = month  # m is the month (3 = March, 4 = April, 5 = May, ..., 14 = February)
    q = day  # q is the day of the month

    if m == 1:
        m = 13
        year -= 1
    elif m == 2:
        m = 14
        year -= 1

    K = year % 100  # K the year of the century
    J = year // 100  # J the zero base century (floor division)
    z = (q + int(13 * (m + 1) / 5.0) + K + int(K / 4.0))
    z_greg = z + int(J / 4.0) - 2 * J
    z_jul = z + 5 - J

    if year > 1582:
        h = z_greg % 7
    else:
        h = z_jul % 7
    if h == 0:
        h = 7

    return (h + 5) % 7 + 1


def is_leap_year(year):
    leap = False
    if year % 4 == 0:
        if year % 100 != 0:
            leap = True
        elif year % 100 == 0 and year % 400 == 0:
            leap = True
    return leap


def mapping_days_in_month(year):
    dict = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

    if is_leap_year(year):
        dict[2] = 29  # 29 days in feb if leap year

    return dict


def weekdays(start_date, end_date):
    start_year, start_month, start_day = map(int, start_date.split('-'))
    end_year, end_month, end_day = map(int, end_date.split('-'))

    # days in months dict
    days_in_month_dict = {year: mapping_days_in_month(year) for year in range(start_year, end_year + 1)}

    # first day of the week (dow)
    dow = zellers(start_year, start_month, start_day)

    current_year = start_year
    current_month = start_month
    current_day = start_day

    # count weekdays
    count = 0

    while (current_year, current_month, current_day) <= (end_year, end_month, end_day):

        # check if dow is a weekday
        if dow in [1, 2, 3, 4, 5]:
            count += 1

        # set increase dow
        dow += 1

        # resetting dow if over 7
        if dow > 7:
            dow = 1

        # stepping forward
        current_day += 1

        # month-end, end-of-year
        if current_day > days_in_month_dict[current_year][current_month]:  # if last day of the month
            current_day = 1  # reset day
            current_month += 1  # next month

            if current_month > 12:  # if next month over 12
                current_month = 1  # reset month
                current_year += 1  # increase year

    return count


if __name__ == '__main__':
    start_date = '1800-06-18'
    end_date = '2100-4-7'

    print(f'{weekdays(start_date, end_date)} weekdays between {start_date} and {end_date}')


