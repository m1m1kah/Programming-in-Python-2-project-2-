from TreeNode import TreeNode




def inorder(node):
    """This method recursively traverses the left subtree
    then appends the node's key to the results list, and finally recursively traverses
    the rights subtree"""
    if node is None:
        return []
    return inorder(node.left) +[node.key] + inorder(node.right)

def preorder( node):
    """This method starts by appending the node's key to the results list , then recursively traverses the left
    subtree , followed by right subtree"""
    if node is None:
        return []
    return [node.key] +preorder(node.left)+preorder(node.right)

def postorder( node):
    """This method first recursively traverses the left subtree, then the right subtree and finally
    appends the node's key to the result list"""
    if node is None:
        return []
    return postorder(node.left) +postorder(node.right) + [node.key]

# Tree_1 = TreeNode(1)
# Tree_1.left = TreeNode(5)
# print(Tree_1)
# B = BinaryTree()
# print(B.inorder(Tree_1))