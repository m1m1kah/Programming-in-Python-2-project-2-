from datetime import datetime, timedelta
from collections import defaultdict
from PriceTracker import PriceTracker  # Importing the PriceTracker class, assuming it's implemented


class MarketTracker:
    """
    A class to manage and track multiple assets' price data over time.

    This class maintains a collection of `PriceTracker` instances for different assets.
    It allows adding new assets, updating their prices, and retrieving price data for
    specific assets within a given time range.

    Attributes:
        market_data (defaultdict): A dictionary that stores `PriceTracker` instances,
                                   indexed by asset names. If an asset name doesn't exist,
                                   a new `PriceTracker` is created automatically.
    """
    def __init__(self):
        """
        Initializes a MarketTracker instance, which tracks multiple assets using individual PriceTracker instances.

        Attributes:
            market_data (defaultdict): A dictionary mapping asset names to their corresponding PriceTracker objects.
        """
        # Dictionary to store PriceTracker instances for each asset
        self.market_data = defaultdict(PriceTracker)  # Default to a new PriceTracker if the asset doesn't exist

    def add_price(self, name: str, time: datetime, price: float):
        """
        Adds a new price entry for a specific asset at a given time.

        Args:
            name (str): The name of the asset.
            time (datetime): The timestamp when the price was recorded.
            price (float): The price of the asset at the given time.

        Raises:
            KeyError: If the asset has not been added to the market using `add_asset()`.
        """
        if name not in self.market_data: #if the asset name is not found - key error is raised
            raise KeyError(f"Asset '{name}' not found in market.")

        # Get the PriceTracker for the asset and add the price data
        asset_tracker = self.market_data[name]
        asset_tracker.add_price(time, price)

    def get_price_data(self, name: str, start: datetime, end: datetime):
        """
        Retrieves a list of price statistics for a specific asset within the given time range.

        Each entry includes the original price and the 10-day minimum, maximum, and average prices
        as of that time point.

        Args:
            name (str): The name of the asset.
            start (datetime): The start time of the desired range (inclusive).
            end (datetime): The end time of the desired range (inclusive).

        Returns:
            list[tuple[datetime, tuple[float, float, float, float]]]:
                A list of tuples where each contains:
                - datetime: The timestamp of the data point.
                - (float, float, float, float): Tuple of (price, 10-day min, 10-day max, 10-day average).

        Raises:
            KeyError: If the asset does not exist in the market.
        """
        if name not in self.market_data: #if the asset name is not found - KeyError raised
            raise KeyError(f"Asset '{name}' not found in market.")

        # Get the PriceTracker for the asset
        asset_tracker = self.market_data[name]

        # Get the price data within the specified range
        data_in_range = asset_tracker.get_price_data(start, end)

        # List to store the result
        result_list = []

        for time, price in data_in_range:
            # Calculate the 10-day statistics for the current price
            ten_day_min = self.calculate_min(data_in_range, time)
            ten_day_max = self.calculate_max(data_in_range, time)
            ten_day_avg = self.calculate_avg(data_in_range, time)

            # Append the result as a tuple
            result_list.append((time, (price, ten_day_min, ten_day_max, ten_day_avg)))

        return result_list

    def add_asset(self, name: str):
        """
        Adds a new asset to the market and initializes its PriceTracker.

        Args:
            name (str): The name of the asset to be added.
        """
        if name not in self.market_data:
            self.market_data[name] = PriceTracker()

    def calculate_min(self, data, time):
        """
        Calculates the minimum price in the 10-day window ending at the given time.

        Args:
            data (list[tuple[float, datetime]]): A list of tuples containing (price, timestamp).
            time (datetime): The reference time for the 10-day window.

        Returns:
            float or None: The minimum price in the last 10 days, or None if no data is found.
        """
        #dp[0] = price of asset , dp[1] = time of asset being recorded

        # Create an empty list to store prices within the 10-day window
        prices_in_window = []

        # Loop through each data point in 'data'
        for dp in data:
            # If the time of the data point is within the 10-day window
            if time - timedelta(days=10) <= dp[1] <= time:
                # Add the price to the list
                prices_in_window.append(dp[0])

        # Calculate the minimum price from the list of prices in the window
        min_price = min(prices_in_window) if prices_in_window else None  # Handle the case where no prices are found
        return min_price

    def calculate_max(self, data, time):
        """
        Calculates the maximum price in the 10-day window ending at the given time.

        Args:
            data (list[tuple[float, datetime]]): A list of tuples containing (price, timestamp).
            time (datetime): The reference time for the 10-day window.

        Returns:
            float or None: The maximum price in the last 10 days, or None if no data is found.
        """
        prices_in_window = []

        # Loop through each data point in 'data'
        for dp in data:
            # If the time of the data point is within the 10-day window
            if time - timedelta(days=10) <= dp[1] <= time:
                # Add the price to the list
                prices_in_window.append(dp[0])

        # Calculate the maximum price from the list of prices in the window
        max_price = max(prices_in_window) if prices_in_window else None  # Handle the case where no prices are found
        return max_price

    def calculate_avg(self, data, time):
        """
        Calculates the average price in the 10-day window ending at the given time.

        Args:
            data (list[tuple[float, datetime]]): A list of tuples containing (price, timestamp).
            time (datetime): The reference time for the 10-day window.

        Returns:
            float: The average price in the last 10 days. Returns 0 if no data is found.
        """
        prices_in_window = []

        # Loop through each data point in 'data'
        for dp in data:
            # If the time of the data point is within the 10-day window
            if time - timedelta(days=10) <= dp[1] <= time:
                # Add the price to the list
                prices_in_window.append(dp[0])

        # Calculate the average price from the list of prices in the window
        if prices_in_window:
            avg_price = sum(prices_in_window) / len(prices_in_window)  # Calculate the average
        else:
            avg_price = 0  #Return 0 if no prices are found

        return avg_price