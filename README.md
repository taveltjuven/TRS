## Take Home Assessment
"Given two dates (inclusive), determine the number of weekdays between the two. You'll be allowed and expected to use all available resources to accomplish the task. However, your solution should not use third-party libraries, e.g., pandas. Built-in libraries such as collections are allowed, but we ask that you don't use built-in implementations. Please write your own implementation." 

## Solution Commentary
The solution iterates through the current day in a closed date interval while checking if the day is a weekday or a weekend. The day of the week number is determined by Zeller's algorithm (from Wikipedia). A dictionary is generated to keep track of the number of days in each month, including leap years. 

## Recent Updates

### Improved Asymptotic Computational Complexity
- Improved the asymptotic computational complexity. The function get_weekdays_in_year calculates the number of weekdays in a given year, accounting for different start days of the week and leap years.

### General Updates
- Refactored code for better readability and maintainability.
