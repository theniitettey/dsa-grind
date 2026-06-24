from collections import deque

class TreeNode:
    # for an n-ary tree, there are only two data members, the value and the children
    # def __init__(self, val):
    #     self.val = val
    #     self.children = []

    # however for simplicity, we would use a binary tree, which has a value, a left child and a right child
    # most traversal algorithms are usually written in most resources for binary trees, so we would use a binary tree for simplicity
    # however for all traversal algorithms except inorder
    # inorder is the exception because it only makes sense when a node has exactly two children
    # the definition is visit left, then root, then right
    # with n-ary trees there is no clear middle, so the concept itself breaks down, not just the implementation
    # the same algorithm can be used for n-ary trees, with a slight modification to the recursive calls
    # instead of calling the recursive function on the left and right child, we would call it on just the children of the current node, which is a list of nodes who may have their own children, and so on
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    
    # Traversal methods
    # Pre-Order (Root -> Left -> Right)

    def preorder(self, node):
        if not node:
            return
        
        print("Value: ", node.val)
        self.preorder(node.left)
        self.preorder(node.right)

    # Post Order (Left -> Right -> Root)
    def postorder(self, node):
        if not node:
            return

        self.postorder(node.left)
        self.postorder(node.right)
        print("Value: ", node.val)

    # In Order (Left -> Root -> Right)
    def inorder(self, node):
        if not node:
            return
        
        self.inorder(node.left)
        print("Value: ", node.val)
        self.inorder(node.right)

    
    # NB: In-order, Pre-order, and Post-order traversals are all depth-first traversals of a binary tree. (DFS)
    # A base implementation of DFS traversal is provided below, which can be used to implement the three traversals above.

    # Usually the recursive approach is common
    # The iterative approach invloves simulating the call stack yourself
    def dfs(self, node):
        if not node:
            return
        
        print("Value: ", node.val)

        self.dfs(node.left)
        self.dfs(node.right)

    def dfs_iterative(self, node):
        if not node:
            return

        stack = [node]

        while stack:
            node = stack.pop()
            print(node.data)

            # Since Preorder involves left first before right
            # The pop operation pops the last element so we can't append the left first else we later add the right and the pop returns the right to be processed
            # to fix this we append the right first, then left
            # this way when we pop left comes of first

            if node.right:
                stack.append(node.right)
            
            if node.left:
                stack.append(node.left)


    # from the above, you can see this is similar to preorder traversal

    # Level Order Traversal: (Breadth First Search)
    # Since BFS is level order, it is not natural to recursively do it
    # Or immitate the call stack
    # The idea in itself is kind of iterative, however i would add the recursive implementation for the curious minds
    # The idea is to use a queue to track the levels
    # Then we process from front to back
    # Eg: when we take a root, we put the immediate left and right in the queue
    # but we popLeft (remove from front), this actually pops of a level
    # consider this tree
    #
    #   Level 0:        root
    #                   /  \
    #   Level 1:       1    2
    #                 / \  / \
    #   Level 2:     3   4 5   6
    #
    # on first iteration we would have [root], this is level 0
    # when we run popLeft, we pop root
    # now we add left and right to the queue
    # [1, 2] -> this is now level 1
    # we pop 1, add its children, but 2 is still sitting in the queue
    # [2, 3, 4] -> still draining level 1, level 2 building up behind it
    # we pop 2, add its children
    # [3, 4, 5, 6] -> level 1 is done, we are now fully on level 2
    # we pop 3, 4, 5, 6 one by one, none have children
    # [] -> queue is empty, we are done
    #
    # the key insight is that children always join the back of the queue
    # so by the time we reach them, everything from the current level is already gone
    # that is what gives us the level by level ordering naturally


    # now you go back up to the first line of code
    # you'll notice we imported deque from collections, this is a double ended queue
    # it allows us to pop from the front and back in O(1) time
    # you don't need to implement a double ended queue yourself, just use deque from collections
    # however if you want to implement your own double ended queue, you can do so using a linked list
    # but a specific type of linked list called a doubly linked list, where each node has a pointer to the next and previous node
    # and you need to keep track of the head and tail of the list, so you can pop from both ends in O(1) time
    def bfs(self, node):
        if not node:
            return
        
        queue = deque([node])

        while queue:
            node = queue.popleft()
            print(node.val)

            if node.left:
                queue.append(node.left)
            
            if node.right:
                queue.append(node.right)

    
    def bfs_recursive(self, queue=None, node=None):
        if node and queue is None:
            queue = deque([node])
        
        if not queue:
            return
        
        node = queue.popleft()
        print(node.val)

        if node.left:
            queue.append(node.left)
        
        if node.right:
            queue.append(node.right)

        self.bfs_recursive(queue)
        
