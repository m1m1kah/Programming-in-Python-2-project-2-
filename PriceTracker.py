from AVLTree import AVLTree
from TreeNode import TreeNode
# assuming TreeNode is correctly imported
from Heap import MinHeap
from datetime  import datetime, timedelta
from BST import range_query
from TreePrinter import print_tree
  # Importing the range_query function


class PriceTracker:
    """
        A class to track asset prices over time and manage 10-day minimum price calculations.

        This class stores price data for a given asset, maintains an AVL tree to store all prices
        recorded, and uses a MinHeap to track the 10-day minimum price for each new data point.
        The class also provides functionality to retrieve price data within a specified time range.

        Attributes:
            price_data (dict): A dictionary mapping timestamps to TreeNode objects in the MinHeap.
            time_data (AVLTree): An AVL tree containing all price data recorded so far.
            price_heap (MinHeap): A MinHeap used to track prices for the 10 days preceding the most recent data point.
            last_time (datetime): Tracks the most recent time a price was added.

        Methods:
            add_price(time: datetime, price: float):
                Adds a new price point to the system and updates the 10-day minimum.

            get_price_data(start: datetime, end: datetime):
                Returns a list of price data within the specified time range, including the 10-day minimum.

        """
    def __init__(self):
        """
        A class to track and manage price data over time using multiple data structures.

        Attributes:
            price_data (dict): Maps timestamps or data identifiers to corresponding TreeNode objects
                             stored in the MinHeap.
            time_data (AVLTree): An AVL tree that stores all historical price data, ordered by time.
            price_heap (MinHeap): A min-heap that stores prices for the 10 most recent data points
                                prior to the latest one.
            last_time (Any): Tracks the timestamp or identifier of the most recently added data point.
        """
        self._price_data = {}  # Dictionary to map price data points to TreeNode objects in MinHeap
        self._time_data = AVLTree()  # AVL tree containing all price data so far.
        self._price_heap = MinHeap()
        self._max_heap = MinHeap()# MinHeap containing prices for the 10 days before most recent data point
        self._last_time = None  # To track the last added time

        self._price_sum = 0.0
        self._price_count = 0

    def add_price(self, time: datetime, price: float):
        """
        Adds a new price data point for the given time and updates the internal data structures.
        Maintains a 10-day rolling window of prices in a min-heap to compute the 10-day minimum.
        Stores the price and 10-day minimum in an AVL tree for efficient range queries.

        Args:
            time (datetime): The timestamp of the price data point.
            price (float): The price of the asset at the given time.
            
        Raises:
            TypeError: If `time` is not a datetime object or `price` is not a float.
        """
        if self._last_time is not None:
            # 1. Compute the start time for the 10-day window.

            start_time = self._last_time - timedelta(days=10)
            end_time = time - timedelta(days=10) - timedelta.resolution

            # 2. Query the AVLTree to get a list of times that are older than the start_time
            # but within the 10-day window for the current price (range query).
            old_prices = range_query(self._time_data, start_time, end_time)
        else:
            old_prices = []
            # 3. For each time in old_prices, do the following:
        for price_time in old_prices:
            timestamp = price_time[0]
            min_node, max_node, old_price = self._price_data.get(timestamp)

            self._price_heap.delete_node(min_node)
            self._max_heap.delete_node(max_node)

            self._price_sum -= old_price  # Update sum
            self._price_count -= 1  #Update count

            del self._price_data[timestamp]

            # Insert into min-heap
        min_node = self._price_heap.insert(price, price)

        # Insert into max-heap (as negative key)
        max_node = self._max_heap.insert(-price, price)

        self._price_data[time] = (min_node, max_node, price)

        self._price_sum += price  #Update sum
        self._price_count += 1  #Update count

        ten_day_min = self._price_heap.root.value
        ten_day_max = self._max_heap.root.value  # max value is stored as positive
        ten_day_avg = self._price_sum / self._price_count if self._price_count else price

        #New format: (price, min, max, avg)
        self._time_data.insert(time, (price, ten_day_min, ten_day_max, ten_day_avg))
        self._last_time = time

    def get_price_data(self, start: datetime, end: datetime):
        """
        Retrieves all price data (price and 10-day minimum) stored in the AVL tree
        within the specified datetime range (inclusive).

        Args:
            start (datetime): The start of the time range (inclusive).
            end (datetime): The end of the time range (inclusive).

        Returns:
            list[tuple[datetime, tuple[float, float]]]: A list of tuples where each tuple contains:
                - datetime: Timestamp of the data point.
                - (float, float): A tuple containing the price and the corresponding 10-day minimum price.

        Raises:
            ValueError: If `start` is after `end`.
        """

        return range_query(self._time_data,start, end)




