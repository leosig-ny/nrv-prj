from typing import List, Dict
from app.strategies import CoalesceStrategy, AverageStrategy, MinStrategy, MaxStrategy, MedianStrategy
from app.config import config

# Mapping of strategy names to their respective classes
STRATEGY_CLASSES = {
    "average": AverageStrategy,
    "min": MinStrategy,
    "max": MaxStrategy,
    "median": MedianStrategy,
}
print("Starting test...")
class DataCoalescer:
    def __init__(self, strategy_name: str = None) -> None:
        # Use default strategy from config if none provided
        if strategy_name is None:
            strategy_name = config.COALESCE_STRATEGY
        strategy_class = STRATEGY_CLASSES.get(strategy_name, AverageStrategy)
        self._strategy = strategy_class()
        print(f"Initialized with strategy: {strategy_name}")  # Debugging output

    def set_strategy(self, strategy_name: str) -> None:
        strategy_class = STRATEGY_CLASSES.get(strategy_name, AverageStrategy)
        self._strategy = strategy_class()
        print(f"Strategy changed to: {strategy_name}")  # Debugging output


    def coalesce_data(self, responses: List[Dict[str, int]]) -> Dict[str, int]:
        print("coalesce_data method called")  # Simple print to check method execution 
        coalesced = {}
        for key in ["oop_max", "remaining_oop_max", "copay"]:
            values = [resp[key] for resp in responses if key in resp]
            print(f"Coalescing {key} with values: {values}")  # Debugging output
            coalesced[key] = self._strategy.apply(values)
        print(f"Coalesced result: {coalesced}")  # Debugging output
        return coalesced

