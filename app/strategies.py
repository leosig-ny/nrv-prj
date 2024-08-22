# app/strategies.py

from abc import ABC, abstractmethod
from typing import List, Dict, Type

"""
classtrategies (average, min, max, and median) were chosen based on
common statistical methods used to aggregate data. These strategies are useful
in scenarios where you need to consolidate multiple values into a single representative value,
especially when the data comes from different sources or APIs. Here's why each was chosen:

    1. Average (Mean):
        The average (or mean) is a widely used measure of central tendency that provides
        a single value representing the center of a data set. It is calculated by
        summing all values and dividing by the number of values.
        This strategy is useful when you want to smooth out variations
        between different data sources and get a general sense of the overall trend.
        If multiple APIs provide slightly different estimates for the same metric
        (e.g., estimated costs), averaging can give a balanced, overall estimate.

    2. Minimum (Min):
        The minimum strategy selects the smallest value from the data set.
        It’s often used when you want to identify the least costly or most conservative estimate.
        This strategy is useful in scenarios where you want to minimize risk,
        such as choosing the least expensive option or the smallest reported value among several sources.
        If you're aggregating costs from different providers, you might want to go with the lowest quote.

    3. Maximum (Max):
        The maximum strategy selects the largest value from the data set.
        It’s often used when you want to identify the most expensive or most aggressive estimate.
        This strategy is useful when you need to account for the worst-case 
        scenario or the highest value reported among several sources.
        If you're assessing potential liabilities, you might want to consider the highest cost reported.

     4. Median:
         The median is the middle value when the data set is sorted in
         ascending or descending order. It is a robust measure of central tendency
         that is less affected by outliers than the average.
         The median is useful when you want a central value that isn't skewed
         by extreme values, making it a good choice when the data might contain outliers.
         If multiple APIs provide values where some are significantly higher or lower
         than others, the median can give a better sense of the "typical" value.
"""                    
class CoalesceStrategy(ABC):
    @abstractmethod
    def apply(self, values: List[int]) -> int:
        pass

class AverageStrategy(CoalesceStrategy):
    def apply(self, values: List[int]) -> int:
        print(f"Calculating average for values: {values}")  # Debugging output
        return sum(values) // len(values)

class MinStrategy(CoalesceStrategy):
    def apply(self, values: List[int]) -> int:
        return min(values)

class MaxStrategy(CoalesceStrategy):
    def apply(self, values: List[int]) -> int:
        return max(values)

class MedianStrategy(CoalesceStrategy):
    def apply(self, values: List[int]) -> int:
        sorted_values = sorted(values)
        n = len(sorted_values)
        if n % 2 == 1:
            return sorted_values[n // 2]
        else:
            mid1 = n // 2
            mid2 = mid1 - 1
            return (sorted_values[mid1] + sorted_values[mid2]) // 2

STRATEGY_CLASSES: Dict[str, Type[CoalesceStrategy]] = {
    "average": AverageStrategy,
    "min": MinStrategy,
    "max": MaxStrategy,
    "median": MedianStrategy,
}

def get_strategy(strategy_name: str) -> CoalesceStrategy:
    strategy_class = STRATEGY_CLASSES.get(strategy_name)
    if not strategy_class:
        raise ValueError(f"Unknown coalescing strategy: {strategy_name}")
    return strategy_class()

