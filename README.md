## Take Home Assessment
"Given two dates (inclusive), determine the number of weekdays between the two. You'll be allowed and expected to use all available resources to accomplish the task. However, your solution should not use third-party libraries, e.g., pandas. Built-in libraries such as collections are allowed, but we ask that you don't use built-in implementations. Please write your own implementation." 

## Solution Commentary
The solution leverages the 400-year calendar cycle to optimize the calculation of weekdays between two dates as well as day-of-week modulo logic. This approach avoids the need to iterate through every single day or periods in the date range, significantly improving the asymptotic complexity.

## Recent Updates

### Improved Asymptotic Computational Complexity
- 400-Year Calendar Cycle: Implemented a 400-year calendar cycle as a lookup table to efficiently compute weekdays over long time spans. This significantly reduces the complexity compared to iterating through each year individually.
- Day-of-Week Modulo Logic: Utilized a day-of-week modulo logic to calculate weekdays within a year, ensuring fast and accurate computation without looping through each day

### General Updates
- Refactored Code: Improved readability and maintainability by organizing functions and adding  docstrings
- Caching: Implemented caching to store the precomputed 400-year calendar cycle, further optimizing repeated calculations.
