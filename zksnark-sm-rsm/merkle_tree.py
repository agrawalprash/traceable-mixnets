 # Merkle tree code adapted from the code contributed by Pranay Arora (TSEC-2023) 
 # on GeeksForGeeks.


from utils import timed
from math import log, ceil

class Node:
    def __init__(self, left, right, value, content):
        self.left = left
        self.right = right
        self.value = value
        self.content = content
       
class MerkleTree:
    @timed
    def __init__(self, contents, hashfuncleaves, hashfuncinternal, padelem):
        depth = ceil(log(len(contents), 2))
        cnodes = [Node(None, None, hashfuncleaves(c), c) for c in contents]
        padding = [Node(None, None, hashfuncleaves(padelem), padelem) 
                   for i in range(2**depth - len(cnodes))]
        leaves = cnodes + padding
        self.contents = contents
        self.depth = depth
        self.hashfuncleaves = hashfuncleaves
        self.hashfuncinternal = hashfuncinternal
        self.padelem = padelem
        self.root = self._buildTreeRec(leaves)
 
    def _buildTreeRec(self, nodes):
        if len(nodes) == 2:
            return Node(nodes[0], nodes[1], self.hashfuncinternal(nodes[0].value, nodes[1].value), None)        
        half = len(nodes) // 2
        left = self._buildTreeRec(nodes[:half])
        right = self._buildTreeRec(nodes[half:])
        value = self.hashfuncinternal(left.value, right.value)
        content = None
        return Node(left, right, value, content)
 
    def getRootHash(self):
      return self.root.value

    def getnode(self, address):
        """ Return node at a given address. """
        node = self.root
        for addressBit in address:
            node = node.left if addressBit==0 else node.right
        return node

    @timed
    def get_auth_path(self, address):
        """ Return Merkle authentication path for the leaf at the given address, as an array of (valsibling, dirsibling) pairs from leaf to root. """
        auth_path = []
        node = self.root
        for addressBit in address:              # if addressBit is 0 then take the left child else take the right child to reach the leaf
            if addressBit == 0:                 
                valsibling = node.right.value   # path to the leaf is towards the left child, so the sibling is towards right.
                dirsibling = 1                  # 1 encodes that the sibling is towards the right
                node       = node.left          # hop one step along the path as per the address (i.e., go to the left child)
            else:                   
                valsibling = node.left.value    # path to the leaf is towards the right child, so the sibling is towards left.
                dirsibling = 0                  # 0 encodes that the sibling is towards the left
                node       = node.right         # hop one step along the path as per the address (i.e., go to the right child)
            auth_path.insert(0, (valsibling, dirsibling))
  
        return auth_path

    @timed
    def check_auth_path(self, content, auth_path):
        """ Check if the given authentication path for a given content is correct with respect to the current root. """
        print("init content is", content)
        nodeVal = self.hashfuncleaves(content)
        import bitstring
        print("init nodeval is", nodeVal)
        for (valsibling, dirsibling) in auth_path:
            if dirsibling == 0:
                nodeVal = self.hashfuncinternal(valsibling, nodeVal)
            else:
                nodeVal = self.hashfuncinternal(nodeVal, valsibling)
        assert(nodeVal == self.root.value)

    def address(self, index):
        """ Address in the Merkle tree of the element with given index in the
        corresponding array representation.  """
        fmt = '0%sb' % str(self.depth)
        return [int(s) for s in format(index, fmt)]
