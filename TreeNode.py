from Node import Node

class TreeNode(Node):
    """
    A TreeNode represents a node in a binary tree, inheriting from the Node class.

    Attributes:
        key (int): The key used for comparisons or identification.
        value (Any): The data stored in the node.
        left (TreeNode): Reference to the left child node.
        right (TreeNode): Reference to the right child node.
        parent (TreeNode): Reference to the parent node.
    """

    def __init__(self, key=None, value =None ):
        """
        Initializes a TreeNode with optional key and value, and no children or parent.

        Args:
            key (int, optional): The key associated with the node.
            value (Any, optional): The value stored in the node.
        """
        self._key = key
        self._value = value
        self._left = None
        self._right = None
        self._parent = None


    @property
    def key(self):
        """
        Gets the key of the node.

        Returns:
            int: The key value.
        """
        return self._key

    @key.setter
    def key(self, value):
        """
        Sets the key of the node.

        Args:
            value (int): The new key value.
        """
        self._key = value

    @property
    def left(self):
        """
        Gets the left child node.

        Returns:
            TreeNode: The left child, or None if not set.
        """
        return self._left

    @left.setter
    def left(self, node):
        """
        Sets the left child node and updates parent references.

        Args:
            node (TreeNode): The new left child node.

        Raises:
            TypeError: If the node is not a TreeNode or None.
        """
        if node is not None and not isinstance(node, TreeNode):
            raise TypeError("Left child must be a TreeNode or None")

        if node is not None:
            node._parent = self #setting parent

        if self._left is not None:
            self._left._parent = None #remove previous parent

        self._left = node


    @property
    def right(self) -> 'TreeNode': #this means right return a TreeNode or None
        """
        Gets the right child node.

        Returns:
            TreeNode: The right child, or None if not set.
        """
        return self._right



    @right.setter
    def right(self, node: 'TreeNode'):
        """
        Sets the right child node and updates parent references.

        Args:
            node (TreeNode): The new right child node.

        Raises:
            TypeError: If the node is not a TreeNode or None.
        """
        if node is not None and not isinstance(node, TreeNode):
            raise TypeError("Right child must be a Tree node or None.")
        if node is not None:
            node._parent = self  # Set parent of the new right child

        if self._right is not None:
            self._right._parent = None  # Remove previous parent reference
        self._right = node

    @property
    def value(self):
        """
        Gets the value stored in the node.

        Returns:
            Any: The node's value.
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of the node.

        Args:
            value (Any): The new value to be stored.
        """
        self._value = value


    @property
    def parent(self):
        """
        Gets the parent of the node.

        Returns:
            TreeNode: The parent node, or None if root.
        """
        return self._parent

    @property
    def depth(self):
        """
        Computes the depth of the node in the tree.

        Returns:
            int: Depth of the node (1 for root).
        """
        if self._parent is None:
            return 1 #root node
        else:
            return 1+self._parent.depth


    def remove_leaf(self, n):
        """
        Removes a node from the tree if it is a leaf and a direct child of the current node.

        Args:
            n (TreeNode): The child node to remove.

        Returns:
            TreeNode: The removed node.

        Raises:
            TypeError: If `n` is not a TreeNode.
            ValueError: If `n` is not a leaf or not a child of this node.
        """
        if not isinstance(n, TreeNode):
            raise TypeError("n must be a TreeNode.")

        if n._left is not None or n._right is not None:
            raise ValueError("Cannot remove a non-leaf node.")
        if n is self.left: # check if node is the left child
            self.left = None
        elif n is self._right: #check if the node is a right child
            self.right = None
        else:
            raise ValueError("The node is not a child of this node")
        return n



    def __repr__(self):
        """
        Returns a string representation of the TreeNode, showing key, children, and parent (if any).

        Returns:
            str: String representation of the TreeNode.
        """
        if self._parent is None:
            return f"TreeNode (key={self._key}, left={self._left}, right={self._right})"
        return f"TreeNode (key={self._key}, left={self._left}, right={self._right}, parent={self._parent.key})"

