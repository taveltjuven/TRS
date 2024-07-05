Take Home Assessment:
"Given two dates (inclusive), determine the number of weekdays between the two. You'll be allowed and expected to use all available resources to accomplish the task. However, your solution should not use third-party libraries, e.g. pandas. Built-in libraries such as collections are allowed, but we ask that you don't use built-in implementations. Please write your own implementation"

Solution commentary:
Using a while-loop to iterate through the current day in a closed date interval while checking if the day is a weekday or a weekend. The day of the week number is given by Zeller's algorithm (from Wikipedia). A dictionary is generated to keep track of the number of days in each month, including leap years.

Unit testing with pandas.

I was expecting the while loop to be faster (nested for-loop might be a faster implementation).
