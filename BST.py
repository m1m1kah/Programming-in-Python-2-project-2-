from abc import abstractmethod, ABC
from TreeNode import TreeNode


class BST(ABC):
    @abstractmethod
    def __init__(self):
        """
        Initializes a binary search tree.

        This method creates an empty binary search tree, with
        root set to None.
        """
        self.root = None


    @abstractmethod
    def insert(self,key,value=None):
        """
        Inserts a key-value pair into the binary search tree.

        If the key already exists in the tree, the associated value is updated.

        Args:
            key: The key to be inserted into the tree.
            value: The value associated with the key, optional.
        """
        pass

    @abstractmethod
    def search(self, key):
        """
        Finds the value associated with a given key in the binary search tree.

        Args:
            key: The key to search for in the tree.

        Returns:
            The node associated with the key 
        
        Raises:
            KeyError: If the key is not found in the tree.
        """
        pass

    @abstractmethod
    def get_value(self,key):
        """
        Finds the value associated with a given key in the binary search tree.

        Args:
            key: The key to search for in the tree.

        Returns:
            The value associated with the key 
        
        Raises:
            KeyError: If the key is not found in the tree.
        """
        pass
    
    
    @abstractmethod
    def delete(self, key):
        """
        Removes a key-value pair from the binary search tree.

        Args:
            key: The key of the node to be deleted.
        
        Raises:
            KeyError: If the key is not found in the tree.
        """
        pass

def range_query(tree : BST, low, high):
    """Return all key-value pairs in a BST with keys in the specified range.
    
    This searches the entire given BST, and returns all (key, value)
    pairs stored in the subtree whose keys are greater than or equal to
    low and less than or equal to high.

    Args:
        tree: A BST in which we want to search.
        low: The lowest key to include in the query.
        high: The highest key to include in the query.

    Returns:
        A list of tuples, where each tuple contains a key and its associated value.
    """
    # TODO: implement this method
    result = []


    def _range_query_helper(node, low, high):
        """Helper function to perform the range query."""
        if node is None:
            return

        # If the current node's key is greater than low, check the left subtree.
        if node._key > low:
            _range_query_helper(node._left, low, high)

        # If the current node's key is within the range, add it to the result.
        if low <= node._key <= high:
            result.append((node._key, node._value))

        # If the current node's key is less than high, check the right subtree.
        if node._key < high:
            _range_query_helper(node._right, low, high)


    # Start the range query from the root node of the tree.
    _range_query_helper(tree.root, low, high)

    return result







