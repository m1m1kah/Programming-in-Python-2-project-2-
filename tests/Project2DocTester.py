from DocTester import DocTester
from TesterUtils import single_line, double_line, blank_line
import sys

expected_docstrings = \
    [("TreeNode.py", 
      ["class TreeNode",
       "TreeNode.__init__",
       "TreeNode.remove_leaf"]),
     ("Heap.py",
      ["MinHeap.insert_node",
       "MinHeap.insert",
       "MinHeap.extract",
       "MinHeap.delete_node"]),
     ("PriceTracker.py",
      ["class PriceTracker",
       "PriceTracker.__init__",
       "PriceTracker.add_price",
       "PriceTracker.get_price_data"]),
     ("MarketTracker.py",
      ["class MarketTracker",
       "MarketTracker.__init__",
       "MarketTracker.add_price",
       "MarketTracker.get_price_data"])
]


dt = DocTester()
dt.expected_docstrings=expected_docstrings
dt.check_docstrings()

with sys.stdout as f:
    grade = dt.write_summary(f)

if grade < 10:
    exit(1)
else:
    exit(0)
