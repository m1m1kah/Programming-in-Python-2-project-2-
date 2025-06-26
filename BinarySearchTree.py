from TreeNode import TreeNode #as we want class binary tree ot inherit from BST
from BST import BST
from TreePrinter import print_tree

#object is an instance of a class
class BinarySearchTree:

    def __init__(self, root=None):
        self.root  =None
        self.size = 0

    def insert(self, key, value=None):
        """This method takes a key and value and inserts it into the tree."""
        if not isinstance(key, int):
            raise ValueError("Key must be an integer.")

        if self.root is None:
            self.root = TreeNode(key, value)
            self.size +=1 #Increase size when a node is inserted
        else:
            self._insert_helper(self.root, key, value)

    def _insert_helper(self, current_node, key, value):
        """this method is a helper method to recursively
        insert a node into the correct place. """
        if key == current_node.key:
            current_node.value = value
        elif key< current_node.key:
            if current_node.left is None:
                current_node.left = TreeNode(key, value)
                self.size +=1 #Increase size when a node is inserted
            else:
                self._insert_helper(current_node.left, key, value)
        else:
            if current_node.right is None:
                current_node.right = TreeNode(key, value)
                self.size+= 1 #Increase size when a node is inserted
            else:
                self._insert_helper(current_node.right, key, value)


    def search(self, key):
        """This method returns the TreeNode if the
        key is in the tree and raise a KeyError if not

        Args:
            key: (int)
            """
        return self._search_helper(self.root, key)

    def _search_helper(self, current_node, key):
        """this is a helper method to recursively search
        for a node with the given key"""
        if current_node is None :
            raise KeyError(f"key {key} not found in the tree.")
        if key == current_node.key:
            return current_node
        elif key < current_node.key:
            return self._search_helper(current_node.left, key)
        else:
            return self._search_helper(current_node.right, key)


    def get_value(self, key):
        """This method return the value if the key is
        in hte tree and raise a KeyError if not

        Args:
            key:

        Raises:
            KeyError : exception where
        """
        node = self.search(key)
        return node.value

    def delete(self, key):
        """This method deletes the node with specified key from the tree."""
        node_to_delete = self.search(key)
        if not isinstance(node_to_delete, TreeNode):
            raise ValueError(f"Node with key {key} is not a TreeNode.")
        self._delete_helper(node_to_delete)
        self.size -=1 #decrease size when a node is deleted

    def _delete_helper(self, node):
        """Helper method for deleting a node."""
        # Case 1: Node has no children (leaf node)
        if node.left is None and node.right is None:
            self._replace_node_in_parent(node, None)

        # Case 2: Node has one child
        elif node.left is None or node.right is None:
            child = node.left if node.left is not None else node.right
            self._replace_node_in_parent(node, child)

        # Case 3: Node has two children
        else:
            # Find the smallest node in the right subtree (in-order successor)
            successor = self._min_value_node(node.right)
            node.key = successor.key
            node.value = successor.value
            # Recursively delete the successor node
            self._delete_helper(successor)

    def _replace_node_in_parent(self, node, new_node):
        """Replace a node with a new node (or None)."""
        if node.parent is None:
            self.root = new_node
        elif node == node.parent.left:
            node.parent.left = new_node
        else:
            node.parent.right = new_node


    def _min_value_node(self, node):
        """Find the node with the minimum key in the subtree."""
        if not isinstance(node, TreeNode):
            raise ValueError("The node passed to _min_value_node is not a TreeNode")

        current = node
        while current.left is not None:
            current = current.left
        return current

    def __len__(self):
        """Return the number of nodes in the tree."""
        return self.size
    
