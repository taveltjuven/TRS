calendar_cycle_cache = None

def zellers(year, month, day):
    """
        Calculate the day of the week for a given date using Zeller's congruence.
            Args:
                year (int): The year of the date.
                month (int): The month of the date.
                day (int): The day of the date.
            Returns:
                int: The day of the week where 1 = Monday and 7 = Sunday.
            References:
                http://en.wikipedia.org/wiki/Zeller%27s_congruence:
        """
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


def get_weekdays_in_year_new(leap, dow):
    """
    Calculate the number of weekdays in a year based on whether it is a leap year and the starting day of the week.
        Args:
            leap (bool): Indicates whether it is a leap year (True) or a non-leap year (False).
            dow (int): Day of the week the year starts on (1 = Monday, 7 = Sunday).
        Returns:
            int: Number of weekdays in the year.
    """
    if not leap:
        return 261 if dow in [1, 2, 3, 4, 5] else 260
    else:
        return 262 if dow in [1, 2, 3, 4] else 261 if dow in [5, 7] else 260


def is_leap_year(year):
    """
      Determine whether a given year is a leap year.
          Args:
              year (int): The year to check.
          Returns:
              bool: True if the year is a leap year, False otherwise.
      """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def mapping_days_in_month(year):
    """
      Return a dictionary mapping each month to its number of days for a given year.
          Args:
              year (int): The year for which to calculate the number of days in each month.
          Returns:
              dict: A dictionary mapping month numbers (1-12) to the number of days in each month.
      """
    month_days = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    if is_leap_year(year):
        month_days[2] = 29  # 29 days in Feb if leap year
    return month_days


def weekdays_ytd(dow, days_in_year):
    """
    Transform calendar days year-to-date into weekdays year-to-date.
        Args:
            dow (int): The day of the week (dow) the year starts on (1 = Monday, 7 = Sunday).
            days_in_year (int): The total number of days from the start of the year.
        Returns:
            int: The number of weekdays (Monday to Friday) from the start of the year to the given day.
   """
    full_weeks = days_in_year // 7
    full_weeks_in_days = full_weeks * 7
    rest = days_in_year - full_weeks_in_days
    rest_list = [(i % 7) if (i % 7) != 0 else 7 for i in range(dow, dow + rest)]
    weekdays_ytd_transformed = full_weeks * 5 + sum(1 for day in rest_list if day in [1, 2, 3, 4, 5])

    return weekdays_ytd_transformed


def calendar_cycle():
    """
     Generate a lookup table over a 400-year period, the Gregorian calendar cycle

     This function calculates the total number of weekdays (Monday to Friday) for each year in a 400-year cycle
     based on the day of the week the year starts and whether the year is a leap year. It also accumulates the number
     of weekdays for each year and stores the results in a dictionary. The accumulated years are then used as a building
     block to calculate the weekdays between two days. The 400 year calendar cycle is saved globally after  first run.
         Returns:
             dict: A dictionary where the keys are years (0 to 399) in the 400-year cycle and the values are the
                   accumulated number of weekdays from the start of the cycle to that year.
     """
    # check if the lookup dict is already saved globally
    global calendar_cycle_cache
    if calendar_cycle_cache is not None:
        return calendar_cycle_cache

    # create dict of the 14 different versions of how a year could start regards to day of the week and leap year
    days_in_year_lookup = {(dow, leap): get_weekdays_in_year_new(leap, dow) for dow in range(1, 8) for leap in [False, True]}

    # creation of lookup table of the calendar cycle
    annual_weekdays = {}
    dow = 6
    for i in range(0, 400):
        if i in [100, 200, 300]:
            leap = False
        elif i % 4 == 0:
            leap = True
        else:
            leap = False

        annual_weekdays[i] = days_in_year_lookup.get((dow, leap))

        if leap:
            dow = (dow + 2) % 7
        else:
            dow = (dow + 1) % 7

        if dow == 0:
            dow = 7

    annual_accumulated = {}
    accumulated_days = 0

    # create a dict of accumulated days
    for key in sorted(annual_weekdays):
        accumulated_days += annual_weekdays[key]
        annual_accumulated[key] = accumulated_days

    calendar_cycle_cache = annual_accumulated
    return annual_accumulated


def weekdays(user_start_date, user_end_date):
    """
      Calculate the total number of weekdays (Monday to Friday) between two dates.

      This function determines the number of weekdays between two given dates. It accounts for leap years,
      the starting day of the week for each year, and uses a precomputed 400-year calendar cycle to optimize
      the calculation.
          Args:
              user_start_date (str): The start date in 'YYYY-MM-DD' format.
              user_end_date (str): The end date in 'YYYY-MM-DD' format.
          Returns:
              int: The total number of weekdays (Monday to Friday) between the two dates, inclusive.
      """
    start_year, start_month, start_day = map(int, user_start_date.split('-'))
    end_year, end_month, end_day = map(int, user_end_date.split('-'))

    if (start_year, start_month, start_day) > (end_year, end_month, end_day):
        return 0

    # anchoring point for day of week for the start year and end year in an inclusive closed  interval, ie [a,b]
    dow_a = zellers(start_year, 1, 1)
    dow_b = zellers(end_year, 1, 1)

    # get the correct calendar for start and end year
    start_year_dict = mapping_days_in_month(start_year)
    end_year_dict = mapping_days_in_month(end_year)

    # summing up days in year to date using correct calendar (leap year or not)
    ytd_a = sum(start_year_dict[x] for x in range(1, start_month)) + start_day
    ytd_b = sum(end_year_dict[x] for x in range(1, end_month)) + end_day

    # amount of weekdays from calendar days in year to date
    ytd_weekdays_a = weekdays_ytd(dow_a, ytd_a - 1)
    ytd_weekdays_b = weekdays_ytd(dow_b, ytd_b)

    # get the calendar dict as lookup table for years in the 400 year Gregorian calendar cycle
    calendar_400 = calendar_cycle()

    # what 400 year period is start-date (a) and end*date (b) are belonging to, eg 1600 or 2000, or 2400 etc
    period_block_a = start_year // 400 * 400
    period_block_b = end_year // 400 * 400

    # 400 year cycle blocks in terms of weekdays
    period_cycle_diff = ((period_block_b - period_block_a) // 400 * calendar_400[len(calendar_400) - 1])

    # key to get right value in the 400 year calendar dict of accumulated years
    period_a_key = start_year - period_block_a - 1
    period_b_key = end_year - period_block_b - 1

    # accumulated annual weekdays, from its respective block to the start year, eg 2002-01-01, then year 00 and 01
    cum_weekdays_a = calendar_400[period_a_key] if period_a_key >= 0 else 0
    cum_weekdays_b = calendar_400[period_b_key] if period_b_key >= 0 else 0

    # total by: 400y block + net cumulative weekdays to year prior b and a + net ytd for b and a
    total_weekdays = period_cycle_diff + (cum_weekdays_b - cum_weekdays_a) + (ytd_weekdays_b - ytd_weekdays_a)

    return total_weekdays


if __name__ == '__main__':
    """ 
    for a closed interval of dates between a and b, i.e. [a,b]= {x ∈ ℝ: | a ≤ x ≤ b} 
    """
    user_start_date = '1776-7-4'
    user_end_date = '1845-12-29'

    print(f' Between {user_start_date} and {user_end_date} '
          f'there are {weekdays(user_start_date, user_end_date)} weekdays')
