from abc import ABC, abstractmethod


class Node(ABC):
    @abstractmethod
    def __init__(self, key):
        """
        Create a new node with the specififed key..

        This will creates an "isolated" node, initialised with
        no parent or children. Children can be set using
        the left and right properties, and the parent will be 
        set when the node is added as a child of some other node.

        Args:
            key: The value to be stored in the node.
        """
        pass

    @property
    @abstractmethod
    def key(self) -> any:
        """
        any: the value stored in this node."""
        pass

    @key.setter
    @abstractmethod
    def key(self, key):
        pass

    @property
    @abstractmethod
    def parent(self) -> 'Node':
        """Node: the parent of this node. None if this node is a root."""
        pass

    @property
    @abstractmethod
    def left(self) -> 'Node':
        """Node: the left child of this node. None if this node has no left child.
        Assigning the left child of a node will update the new child's
        parent to this node and also remove this node as the parent of
        any existing left child.

        Attempting to set a left child that is not a Node or None will
        raise a TypeError.
        """
        pass

    @left.setter
    @abstractmethod
    def left(self, node: 'Node'):
        pass

    @property
    @abstractmethod
    def right(self) -> 'Node':
        """Node: the right child of this node. None if this node has no right child.
        Assigning the right child of a node will update the new child's
        parent to this node and also remove this node as the parent of
        any existing right child.

        Attempting to set a right child that is not a Node or None will
        raise a TypeError.
        """
        pass

    @right.setter
    @abstractmethod
    def right(self, node: 'Node'):
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        Return a string representation of the node.

        Returns:
            str: A string representation of the node.
        """
        pass

    @abstractmethod
    def remove_leaf(self, node:'Node') -> 'Node':
        """
        Remove a child node from this node's children if it is a leaf node.

        Args:
            node (Node): The node to be removed.

        Returns:
            Node: the node that was removed.
        
        Raises:
            ValueError: if node is not a child of this node or 
                node is not a leaf node.
        """
        pass


