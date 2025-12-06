#id1: 324207885
#name1: Yael Parzelina
#username1: Parzelina
#id2: 322643297
#name2: Mika Oren
#username2: Mikaoren


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1

	def __repr__(self):
		return f"Node(k={self.key}, v={self.value}, h={self.height})"

	"""returns the Balance Factor of a node

	@rtype: int
	"""
	def BF(self):
		# treat missing children as virtual nodes with height = -1
		left_height = self.left.height if self.left is not None else -1
		right_height = self.right.height if self.right is not None else -1
		return (left_height - right_height)

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return self.height != -1


"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self.virtual_node = AVLNode(None, None)  # virtual node for easier handling
		self.root = self.virtual_node  # virtual root
		self.size = 0
		self.height = -1
		self.max_node = self.virtual_node  # virtual max_node


	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key):
		node = self.root
		edges = 1
		while node is not None and node.is_real_node():
			if key == node.key:
				return node, edges
			elif key < node.key:
				node = node.left
			else:
				node = node.right
			edges += 1
			
		return None, edges

	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def finger_search(self, key):
		#empty tree case
		if self.max_node is None or not self.max_node.is_real_node():
			return None, 1

		finger = self.max_node
		edges = 1

    	# going up the tree until we find a node with key <= search key
		while finger.parent is not None and key < finger.key:
			finger = finger.parent
			edges += 1

    	# going down the tree to find the key
		while finger is not None:
			edges += 1

			if key == finger.key:
				return finger, edges

			elif key < finger.key:
				finger = finger.left
			else:
				finger = finger.right

    	# key not found
		return None, edges


	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def insert(self, key, val):
		new_node = AVLNode(key, val)
		new_node.height = 0
		new_node.left = self.virtual_node
		new_node.right = self.virtual_node
		new_node.parent = self.virtual_node
		
		parent = None
		current = self.root
		edges = 0
		height_changes = 0

		if parent is None or not self.root.is_real_node(): # Tree was empty
			self.root = new_node
			self.max_node = self.root
			new_node.parent = self.virtual_node

		else:
			while current is not None and current.is_real_node():
				parent = current
				edges += 1
				# Binary search to find place to insert
				if key < current.key:
					current = current.left
				else:
					current = current.right
		
			new_node.parent = parent
			
			if key < parent.key:
				parent.left = new_node

			else:
				parent.right = new_node			
				#update max_node if needed
				if new_node.key > self.max_node.key:
					self.max_node = new_node

		self.size += 1

		# Rebalance the tree
		while parent is not None and parent.is_real_node():
			bf = parent.BF()
			if abs(bf) < 2:
				# Update height if needed
				old_height = parent.height
				left_height = parent.left.height if parent.left is not None else -1
				right_height = parent.right.height if parent.right is not None else -1
				parent.height = 1 + max(left_height, right_height)

				if parent.height != old_height:
					height_changes += 1
					parent = parent.parent
				else:
					break
			else: #|bf| == 2
				# Perform rotations
				height_changes += self.rotate(parent, bf, height_changes)
				break

		return new_node, edges, height_changes
		
	"""performs a rotation on node depending on its balance factor
	"""
	def rotate(self, node, bf, height_changes = 0):  # node's |balance factor| would be 2  
		new_root = None
        # keep references to children that may need explicit height updates
		left_child = None
		right_child = None
	
		if bf == 2: # Left heavy
			if node.left.BF() >= 0:
				# Right rotation
				new_root = node.left
				node.left = new_root.right
				if new_root.right is not None and new_root.right.is_real_node():
					new_root.right.parent = node
				new_root.right = node

			else: # Left-Right case
				# Left rotation then right rotation
				left_child = node.left
				new_root = left_child.right
				left_child.right = new_root.left
				if new_root.left is not None and new_root.left.is_real_node():
					new_root.left.parent = left_child
				node.left = new_root.right
				if new_root.right is not None and new_root.right.is_real_node():
					new_root.right.parent = node
				new_root.right = node
				new_root.left = left_child
				left_child.parent = new_root
		
		elif bf == -2: # Right heavy
			if node.right.BF() <= 0:
				# Left rotation
				new_root = node.right
				node.right = new_root.left
				if new_root.left is not None and new_root.left.is_real_node():
					new_root.left.parent = node
				new_root.left = node

			else: # Right-Left case
				# Right rotation then left rotation
				right_child = node.right
				new_root = right_child.left
				right_child.left = new_root.right
				if new_root.right is not None and new_root.right.is_real_node():
					new_root.right.parent = right_child
				node.right = new_root.left
				if new_root.left is not None and new_root.left.is_real_node():
					new_root.left.parent = node
				new_root.left = node
				new_root.right = right_child
				right_child.parent = new_root
		
		# Update parents
		new_root.parent = node.parent
		if not node.parent.is_real_node(): #node is root
			self.root = new_root
		else:
			if node == node.parent.left:
				node.parent.left = new_root
			else:
				node.parent.right = new_root
		node.parent = new_root

		# update heights for directly affected nodes
        # LR: left_child changed -> update left_child first
		if left_child is not None:
			old_LC_height = left_child.height
			left_child.height = 1 + max(left_child.left.height, left_child.right.height)
			if left_child.height != old_LC_height:
				height_changes += 1
        # RL: right_child changed -> update right_child first
		if right_child is not None:
			old_RC_height = right_child.height
			right_child.height = 1 + max(right_child.left.height ,right_child.right.height)
			if right_child.height != old_RC_height:
				height_changes += 1
        # node was moved down -> update it
		old_node_height = node.height
		node.height = 1 + max(node.left.height, node.right.height)
		if node.height != old_node_height:
			height_changes += 1
    	# then new_root
		old_new_root_height = new_root.height
		new_root.height = 1 + max(new_root.left.height, new_root.right.height)
		if new_root.height != old_new_root_height:
			height_changes += 1
		
        # propagate up until no change
		p = new_root.parent
		while p is not None and p.is_real_node():
			old_h = p.height
			p.height = 1 + max(p.left.height, p.right.height)
			if p.height != old_h:
				height_changes += 1
			else:
				break
			p = p.parent

		return height_changes
	

	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def finger_insert(self, key, val):
		return None, -1, -1


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		return	

	
	"""joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""
	def join(self, tree2, key, val):
		return


	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
		return None, None

	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		return None


	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self):
		if self.size == 0:
			return None
		return self.max_node

	"""updates the max_node field of the AVLTree
	@rtype: None
	"""
	#do we need this???? 
	def update_max(self):
		node = self.root
		while node is not None and node.is_real_node():
			if node.right is None or not node.right.is_real_node():
				break
			node = node.right
		self.max_node = node
		return None
	
	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return -1	


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return None
