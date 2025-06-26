from BST import BST
from Node import Node
from TreePrinter import print_tree
import random

class AVLNode(Node):
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self._left = None
        self._right = None
        self._parent = None
        self._height = 1

    def __repr__(self):
        l_key = None if self.left is None else self.left.key
        r_key = None if self.right is None else self.right.key
        p_key = None if self.parent is None else self.parent.key
        return f"AVLNode(key={self.key}, " + \
                   f"left={l_key}, right={r_key}, "+ \
                   f"parent={p_key})"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self,value):
        self._value = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self,key):
        self._key = key

    @property
    def parent(self):
        return self._parent

    @property 
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        if not (isinstance(node, AVLNode) or node is None):
            raise TypeError(f"{node} is not of type AVLNode)")
        # If node is currently attached to another parent,
        # we need to remove it:
        if node is not None and node.parent is not None:
            if node is node.parent.left:
                node._parent._left = None
            else:
                node._parent._right = None
            node._parent = None
        # If self has a current left child we must remove it:
        if self._left is not None:
            self._left._parent = None
        # Finally, assign the new node and its parent
        self._left = node
        if node is not None:
            node._parent = self
        self._update_height()

    @property 
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        if not (isinstance(node, AVLNode) or node is None):
            raise TypeError(f"{node} is not of type AVLNode)")
        # If node is currently attached to another parent,
        # we need to remove it
        if node is not None and node.parent is not None:
            if node is node.parent.left:
                node._parent._left = None
            else:
                node._parent._right = None
            node._parent = None
        # If self has a current right child we must remove it:
        if self._right is not None:
            self._right._parent = None
        self._right = node
        # Finally, assign the new node and its parent
        if node is not None:
            node._parent = self
        self._update_height()

    @property
    def height(self):
        return self._height

    def _update_height(self):
        l_height = 0 if self.left is None else self.left._height
        r_height = 0 if self.right is None else self.right._height
        self._height = 1 + max(l_height, r_height)

    @property
    def balance(self):
        l_height = 0 if self.left is None else self.left.height
        r_height = 0 if self.right is None else self.right.height
        return l_height - r_height


    def remove_leaf(self,node):
        if not (isinstance(node, AVLNode) or node is None):
            raise TypeError(f"{node} is not of type AVLNode)")

        if node.has_child():
            raise ValueError(f"{node} is not a leaf")

        if node is self.left:
            self.left = None
            return node.value
        elif node is self.right:
            self.right = None
            return node.value
        else:
            raise ValueError(f"{node} is not a child of {self}")
        self._update_height()

    def has_child(self):
        if self.left or self.right:
            return True
        else:
            return False


class AVLTree(BST):
    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    @property
    def height(self):
        return self.root.height

    def search(self, key):
        x = self.root
        while x is not None:
            if x.key > key:
                x = x.left
            elif x.key < key:
                x = x.right
            else:
                return x
        raise KeyError

    def get_value(self, key):
        return self.search(key).value

    def insert(self, key, value=None):
        """Insert a new key/value pair into the tree.

        Args: 
            key: the key at which the new entry should be inserted.
            value: the value which should be inserted at this key 
                (Default: None) 
        """
        # Perform insertion:
        node = self.root
        prev = None
        while node is not None:
            prev = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                # We found the key, so update the value. This does not
                # affect the balance or size so return immediately.
                node.value = value
                return
        new_node = AVLNode(key, value)
        # If prev is still none, we are at the root, and this is the first
        # node inserted into the tree.
        if prev is None:
            self.root = new_node
            self._size += 1
            return
        # Figure out which child of the previous node we should insert 
        # the new node at
        if key < prev.key:
            prev.left = new_node
        else:
            prev.right = new_node
        # Rebalance the tree starting and the parent of the newly
        # inserted node
        self._restore_balance_from(prev)
        # Update size
        self._size += 1

    def delete(self, key):
        """Delete an entry from the tree by key.

        Args: 
            key: the key of the entry that should be deleted.
        """
        self._remove_node(self.search(key))

    def _rot_right(self, n):
        x = n.left
        n.left = x.right
        x.right = n
        return x

    def _rot_left(self, n):
        x = n.right
        n.right = x.left
        x.left = n
        return x

    def _rebalance(self, node):
        """Rebalance the subtree rooted at the given node.

        Args: 
            node: an AVLNode whose subtree should be checked and
                rebalanced if necessary.

        Returns:
            AVLNode: the root of the rebalanced subtree.
        """
        b = node.balance
        if abs(b) <= 1:
            return node
        if b > 1:
            if node.left.balance < 0:
                node.left = self._rot_left(node.left)
            x = self._rot_right(node)
        else: # b < -1
            if node.right.balance > 0:
                node.right = self._rot_right(node.right)
            x = self._rot_left(node)
        return x


    def _restore_balance_from(self, node):
        """Rebalance all nodes on the path from the given node to the root.
        
        Args: 
            node: The node from which to start the rebalancing.
        """
        if node is None:
            raise ValueError
        cur = node
        p = node.parent
        while p is not None:
            if cur is p.left:
                p.left = self._rebalance(cur)
            else:
                p.right = self._rebalance(cur)
            cur = p
            p = p.parent
        # We have now reached the root
        self.root = self._rebalance(cur)

    def _get_successor(self, node: AVLNode):
        if node is None or node.right is None:
            raise ValueError
        s = node.right
        while s.left is not None:
            s = s.left
        return s

    def _remove_leaf(self, node: AVLNode):
        # If this is the root, then we must empty the tree since the root
        # is then a leaf
        if node.parent is None:
            self.root = None
            self._size -= 1
            return None
        # Otherwise, remove the leaf and then rebalance from its parent
        p = node.parent
        p.remove_leaf(node)
        self._restore_balance_from(p)
        self._size -= 1

    def _remove_single(self, node: AVLNode):
        # Find out if the single child of this node is a left or right
        # child
        if node.left is None:
            new_node = node.right
        else:
            new_node = node.left
        # Remove the node and promote its child to its position
        if node.parent is None:
            node.left = None
            node.right = None
            self.root = new_node
        elif node is node.parent.left:
            node.parent.left = new_node
        else:
            node.parent.right = new_node
        # Restore balance from the newly promoted node
        self._restore_balance_from(new_node)
        self._size -= 1

    def _remove_node(self, node: AVLNode):
        # If this is a leaf, remove acccordingly
        if node.left is None and node.right is None:
            self._remove_leaf(node)
        # If this node has a single child, remove accordingly
        elif node.left is None or node.right is None:
            self._remove_single(node)
        # Otherwise, copy inorder successor's data to this node and
        # then delete the inorder successor. Since the successor
        # cannot have a right child, the second call to _remove_node
        # must be one of the above cases, which each trigger a
        # rebalancing. Thus, we don't need to rebalance or update
        # the size here.
        else:
            s = self._get_successor(node)
            node.value = s.value
            node.key = s.key
            self._remove_node(s)
