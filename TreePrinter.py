from Node import Node

def get_height(n: Node):
    l_height = 0 if n.left is None else get_height(n.left)
    r_height = 0 if n.right is None else get_height(n.right)
    return 1 + max(l_height, r_height)

def print_tree(root: Node, total_width=80):
    if root is None:
        print("(Empty)")
        return
    h = get_height(root)
    w = total_width//(2**(h+1))
    levels = ["" for i in range(h)]
    def print_rec(node: Node, i: int):
        # Each subtree "block" at level i (where root is level 0)
        # should occupy (2**(h-i+1))*w columns of output.
        block_width = (2**(h-i+1))*w
        # If the current node is empty, we need to pad this block
        # in this level and all future levels.
        if node is None:
            for j in range(i, h):
                levels[j] += block_width*' '
            return
        # Otherwise, we draw this part of the tree:
        # First, print all left children
        print_rec(node.left, i+1)
        # Then, we need to decide whether to print a conencting line for 
        # the left and right subchildren. These will occupy the 2nd and 3rd
        # quarters of the current block:
        sub_width = block_width//4
        # Pad the 1st quarter of the block
        line = sub_width*' '
        # Draw or pad the 2nd quarter of the block
        if node.left is not None:
            line += '┌'.ljust(sub_width, '─')
        else:
            line += ' '*sub_width
        # Print the node and draw or pad the 3rd quarter of the block. 
        # Since each node value is printed left-aligned in a block of columns,
        # we need the elbows to prtin as the first character of the
        # *next* block to appear correctly. To keep computations simple,
        # We do the same for the padding if there is no line.
        if node.right is not None:
            line += str(node.key).ljust(sub_width, '─') + '┐'
        else:
            line += str(node.key).ljust(sub_width+1, ' ')
        # Pad the last quarter of the block, minus one character for
        # the connecting elbow or extra padding added above.
        line += (sub_width-1)*' '
        # Append the drawing to the current level
        levels[i] += line
        # Finally, print all right children
        print_rec(node.right, i+1)
    print_rec(root, 0)
    print('\n'.join(levels))
