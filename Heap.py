from TreeNode import TreeNode
from TreePrinter import print_tree


class MinHeap:
    """This class implements a linked binary min-heap.

    The heap will support insertion, extraction of the minimum element,
    and dynamic deletion of nodes by reference. The heap is a binary tree
    with nodes of type TreeNode.

    Attributes:
        root: Optional[TreeNode] the root node of the heap. If the heap
            is empty, this is None.
    """

    def __init__(self):
        """Creates a new, empty heap"""
        self.root: TreeNode = None

        # We use a protected attribute to store the current size
        # of the heap. This keeps us from needing to recompute the size.
        # Any delete or insert operations must update this protected
        # attribute to ensure the size remains correct!
        self._size = 0


    def __len__(self):
        """Return the number of nodes stored in the heap.

        Returns:
            int: the number of nodes in the heap.
        """
        return self._size

    def _swap_node_with_parent(self, x: TreeNode):
        """Swaps the given node with its parent in the heap.

        This method will actually swap the TreeNodes for a node
        and its parent, rather than simply swapping the values. As part
        of the swap, all links to parents and children will be altered
        so that afterwards the given node assumes the role of its parent
        and vice-versa in the linked tree structure. This means that
        all references to the node x should still refer to x after the swap.

        Args:
             x: a TreeNode object that should be swapped with its parent.

        Raises:
             ValueError: if x does not have a parent.
        """
        p = x.parent
        if p is None:
            raise ValueError("Node {x} has no parent")

        # Save the left and right children of p and x then break these
        # links from p to its children (including x)
        pr, pl = p.right, p.left
        p.right, p.left = None, None

        # Now we put x into the correct position with respect to p's
        # parent p2:
        p2 = p.parent
        # If p was the root, make x the root instead
        if p2 is None:
            self.root = x
        # If p was a left child of its parent, make x the left child
        # of this parent instead
        elif p2.left is p:
            p2.left = x
        # If p was a right child of its parent, make x a right child
        # instead
        else:
            p2.right = x

        # Next we need to exchange x and p's children One of these
        # will be x so we need to put that in the position that p was
        # in:

        # First, save x's old left and right children, then break
        # these links
        xl, xr = x.left, x.right
        x.left, x.right = None, None
        # Next, set x's new children to be p's old children, except...
        # ...if x was a left child of p, then p should be a left
        # child of x
        if x is pl:
            x.left = p
            x.right = pr
        # ...if x was a right child of p, then p should be a right
        # child of x
        else:
            x.left = pl
            x.right = p
        # Finally, make p's new children x's old children
        p.left = xl
        p.right = xr

    def _replace_node_with_leaf(self, node: TreeNode, leaf: TreeNode):
        """Replaces the given node with the given leaf node.

        This method will first remove the leaf node from the linked
        structure. It will then rearrange the linked structure so that
        the given leaf node takes the role of node: all of node's children
        will be made children of the leaf node, and node's parent will
        become the parent of the leaf node. After the operation, node will
        have no parent or children.

        Args:
             node: a TreeNode object that is the node we wish to replace.
             leaf: a TreeNode object that is a leaf node that we will
                 replace node with. This node should not have any children
                 and should have a parent. That is, it should be a leaf
                 and also not the root of the heap.

        Returns:
             TreeNode: the node that was replaced. This node will have
                 no children and no parent after the replacement operation.

        Raises:
             ValueError: if leaf has any children or has no parent.
        """
        # Make sure leaf is a leaf and has a parent:
        if (leaf.left is not None) or (leaf.right is not None):
            raise ValueError("The specified node is not a leaf")
        if leaf.parent is None:
            raise ValueError("The specified node has no parent")
        # Remove the leaf node from its parent
        leaf.parent.remove_leaf(leaf)
        # Remove the children from the replaced node, and then assign them
        # as children to the leaf that is replacing node.
        nl, nr = node.left, node.right
        node.left, node.right = None, None
        leaf.left, leaf.right = nl, nr

        # Insert the leaf node into the same position as the removed
        # node:

        # Check if the removed node is the root. If so, we make
        # replacement leaf the root:
        if node.parent is None:
            self.root = leaf
        # Otherwise, make the leaf the left or right child of the replaced
        # node's parent, as appropriate:
        elif node is node.parent.left:
            node.parent.left = leaf
        else:
            node.parent.right = leaf
        return node

    def _get_node_at(self, ix: int) -> TreeNode:
        """Returns the node at the given index in the heap, following the binary path.

        Args:
            ix: The index of the node to retrieve.

        Returns:
            TreeNode: The node at the given index in the heap.

        Raises:
            KeyError: If ix is not valid (e.g., ix is out of bounds or non-positive).
        """
        # Raise an error if the index is not valid
        if ix <= 0 or ix > self._size:
            raise KeyError(f"Index {ix} is out of bounds.")

        # Convert the index to a binary list, slicing off the '0b' prefix
        bin_path = [int(bit) for bit in bin(ix)[3:]]  # binary path, ignore '0b'

        # Start from the root of the heap
        current_node = self.root

        # Traverse the heap following the binary path
        for direction in bin_path:
            if direction == 0:
                # Move to the left child
                if current_node.left is None:
                    raise KeyError(f"Node at index {ix} does not exist.")
                current_node = current_node.left
            else:  # direction == 1:
                # Move to the right child
                if current_node.right is None:
                    raise KeyError(f"Node at index {ix} does not exist.")
                current_node = current_node.right

        return current_node

    def _add_leaf(self, leaf):
        """
        Adds a leaf node to the heap in the correct location.

        Args:
            leaf (TreeNode): The new node to be inserted.

        Returns:
            TreeNode: The inserted node.
        """
        if self.root is None:
            # If the heap is empty, make this node the root
            self.root = leaf
            self._size = 1
            return leaf

        # Find the parent node for the new node
        new_index = self._size + 1  # Index where the new node will be inserted
        parent_index = new_index // 2  # Parent index in binary heap
        parent = self._get_node_at(parent_index)  # Get parent node using helper

        # Attach new node as left or right child
        if new_index % 2 == 0:  # If even, it's a left child
            parent.left = leaf
        else:  # If odd, it's a right child
            parent.right = leaf

        leaf._parent = parent
        self._size += 1  # Update heap size

        return leaf  # Return the node so key and value can be set later

    def _sift_up(self, node):
        """
        Moves a node upward to maintain heap order.

        Args:
            node (TreeNode): The node to be sifted upward.
        """
        while node.parent and node.key < node.parent.key:
            # Swap node with its parent
            self._swap_node_with_parent(node)


    def _sift_down(self, node):
        """
        Moves a node downward to maintain heap order.

        Args:
            node (TreeNode): The node to be sifted downward.
        """
        while node:
            smallest = node

            # Check if left child exists and is smaller
            if node.left and node.left.key < smallest.key:
                smallest = node.left

            # Check if right child exists and is smaller
            if node.right and node.right.key < smallest.key:
                smallest = node.right

            # If the smallest node is not the current node, swap them
            if smallest != node:
                self._swap_node_with_parent(smallest)
            else:
                break  # Stop when the node is in the correct position

    def insert_node(self, node):
        """
        Inserts an already created TreeNode into the heap. The node is added as a
        leaf at the next available position in the heap and then sifted up to maintain
        the heap property.

        Args:
            node (TreeNode): A TreeNode instance to be inserted into the heap.

        Returns:
            TreeNode: The newly inserted node.

        Raises:
            TypeError: If `node` is not an instance of TreeNode.
        """
        if self.root is None:
            # If the heap is empty, the node becomes the root
            self.root = node
            self._size = 1
            return node

            # Step 1: Add the node as a leaf at the next available position
        new_index = self._size + 1  # Index where the new node will be inserted
        parent_index = new_index // 2  # Parent index in binary heap
        parent = self._get_node_at(parent_index)  # Get parent node using helper

        # Attach new node as left or right child
        if new_index % 2 == 0:  # If even, it's a left child
            parent.left = node  # Left child
        else:  # If odd, it's a right child
            parent.right = node  # Right child


        # Increment size
        self._size += 1

        # Step 2: Sift the new node up to maintain heap property
        self._sift_up(node)

        # Step 3: Return the newly added node
        return node

    def insert(self, key, value=None):
        """
        Creates a new TreeNode with the given key and value, inserts it into the heap,
        and returns the inserted node.

        Args:
            key (Comparable): The key used to maintain heap ordering.
            value (Any, optional): Optional data associated with the key. Defaults to None.

        Returns:
            TreeNode: The newly inserted TreeNode.
        """
        new_node = TreeNode(key, value)  # Assuming TreeNode is imported
        # If the heap is not empty, find the correct place for the new node

        return self.insert_node(new_node) # Return the newly inserted node for testing

    def extract(self):
        """
        Removes and returns the root node (minimum key node) from the heap. After
        removal, rebalances the heap to maintain the heap property.

        Returns:
            TreeNode: The node that was removed from the root of the heap.

        Raises:
            KeyError: If the heap is empty.
        """
        if self._size == 0:
            raise KeyError("Heap is empty")

        if self._size == 1:
            # If there's only one node, return the root and empty the heap
            min_node = self.root
            self.root = None
            self._size = 0  # Reset size
            return min_node

        last_leaf = self._get_node_at(self._size)
        # Step 1: Swap the root (min element) with the last leaf node
        old_root = self._replace_node_with_leaf(self.root, last_leaf) #replace root with last element
        self._size -= 1  # Decrease heap size

        # Step 2: Sift down the new root to maintain heap property
        if self._size > 0:  # Only sift down if there are elements left in the heap
            self._sift_down(self.root)

        # Step 3: Return the original root
        return old_root

    def delete_node(self, node):
        """
        Deletes an arbitrary node from the heap by swapping it with the last node,
        reducing the size of the heap, and rebalancing it as necessary.

        Args:
            node (TreeNode): The node to be deleted from the heap.

        Returns:
            TreeNode: The node that was logically deleted (after potential key swap).

        Raises:
            KeyError: If the heap is empty.
        """

        if self._size == 0:
            raise KeyError("Heap is empty.")
        if self._size == 1:
            self.root = None
        else:
            last_leaf = self._get_node_at(self._size)
            if last_leaf == node:
                node.parent.remove_leaf(last_leaf)
            else:
                node = self._replace_node_with_leaf(node, last_leaf)
                if last_leaf.parent and last_leaf.key < last_leaf.parent.key:
                    self._sift_up(last_leaf)
                else:
                    self._sift_down(last_leaf)
        self._size -= 1
        return node



