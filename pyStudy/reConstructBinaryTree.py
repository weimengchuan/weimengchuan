class TreeNode:
    def __init__(self, x):
          self.val = x
          self.left = None
          self.right = None
class Solution:
    # 返回构造的TreeNode根节点
    def reConstructBinaryTree(self, pre, tin):
        # write code here
        if pre and tin:
            Node = TreeNode(pre.pop(0))
            idx = tin.index(Node.val)
            Node.left = self.reConstructBinaryTree(pre, tin[:idx])
            Node.right = self.reConstructBinaryTree(pre, tin[idx+1:])
            return Node

class Solution:
    # 返回构造的TreeNode根节点
    def reConstructBinaryTree(self, pre, tin):
        # write code here
        def genTree(Node, pre, tin):
            if pre:
                idx = tin.index(pre[0])
                pre_l = pre[1:idx+1]
                pre_r = pre[idx+1:]
                tin_l = tin[:idx]
                tin_r = tin[idx+1:]
                if pre_l:
                    Node.left = TreeNode(pre_l[0])
                    genTree(Node.left, pre_l, tin_l)
                if pre_r:
                    Node.right = TreeNode(pre_r[0])
                    genTree(Node.right, pre_r, tin_r)
        if pre and tin and len(pre) == len(tin):
            Node = TreeNode(pre[0])
            genTree(Node, pre, tin)
            return Node