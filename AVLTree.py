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
		self.height = 0

	def __repr__(self):
		return f"Node(k={self.key}, v={self.value}, h={self.height})"

	"""returns the Balance Factor of a node
	@rtype: int
	"""
	def BF(self):
		# treat missing children as virtual nodes with height = -1
		left_height = self.left.height if (self.left is not None and self.left.is_real_node()) else -1
		right_height = self.right.height if (self.right is not None and self.right.is_real_node()) else -1
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
		# a single shared virtual node with height -1
		self.virtual_node = AVLNode(None, None)  # virtual node for easier handling
		self.virtual_node.height = -1
		
		#start with a virtual root
		self.root = self.virtual_node  # virtual root
		self._size = 0
		self._max_node = self.virtual_node  # virtual max_node


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
		if self._max_node is None or not self._max_node.is_real_node():
			return None, 1

		finger = self._max_node
		edges = 1

    	# going up the tree until we find a node with key <= search key
		while finger.parent is not None and finger.parent.is_real_node() and key < finger.key:
			finger = finger.parent
			edges += 1

    	# going down the tree to find the key
		while finger is not None and finger.is_real_node():
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
		
		parent = self.virtual_node
		current = self.root
		edges = 0
		height_changes = 0

		if self.root is None or not self.root.is_real_node(): # Tree was empty
			self.root = new_node
			self._max_node = self.root
			new_node.parent = self.virtual_node

		else:
			# Binary search to find place to insert
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
				if new_node.key > self._max_node.key:
					self._max_node = new_node
			
			# Rebalance the tree
			height_changes += self.rebalance_tree(parent)

		self._size += 1
		return new_node, edges, height_changes
	
	"""rebalances the tree starting from parent node
	@type parent: AVLNode
	@pre: parent is a real pointer to a node in self
	@rtype: int
	@returns: number of height changes during rebalancing
	@param parent: the node to start rebalancing from"""
	
	def rebalance_tree(self, node):
		# Rebalance the tree
		height_changes = 0
		while node is not None and node.is_real_node():
			bf = node.BF()
			if abs(bf) < 2:
				# Update height if needed
				old_height = node.height
				left_height = node.left.height if node.left is not None else -1
				right_height = node.right.height if node.right is not None else -1
				node.height = 1 + max(left_height, right_height)

				if node.height != old_height:
					height_changes += 1
					node = node.parent
				else:
					break
			else: #|bf| == 2 - will only happen once
				# Perform rotations
				new_root = self.rotate(node, bf)
				node = new_root.parent
				
		return height_changes

	"""performs a rotation on node depending on its balance factor
	"""
	def rotate(self, node, bf):  # node's |balance factor| would be 2  
		new_root = self.virtual_node
        # keep references to children that may need explicit height updates
		left_child = self.virtual_node
		right_child = self.virtual_node
	
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
		if node.parent is None or not node.parent.is_real_node(): #node is root
			self.root = new_root
		else:
			if node == node.parent.left:
				node.parent.left = new_root
			else:
				node.parent.right = new_root
		node.parent = new_root

		# update heights for directly affected nodes
		def get_h(node):
			if node is not None and node.is_real_node():
				return node.height
			return -1
        
		# LR: left_child changed -> update left_child first
		if left_child is not None and left_child.is_real_node():
			left_child.height = 1 + max(get_h(left_child.left), get_h(left_child.right))
        # RL: right_child changed -> update right_child first
		if right_child is not None and right_child.is_real_node():
			right_child.height = 1 + max(get_h(right_child.left) ,get_h(right_child.right))
        # node was moved down -> update it
		node.height = 1 + max(get_h(node.left), get_h(node.right))

    	# then new_root
		new_root.height = 1 + max(get_h(new_root.left), get_h(new_root.right))

		return new_root
	

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
		new_node = AVLNode(key, val)
		new_node.height = 0
		new_node.left = self.virtual_node
		new_node.right = self.virtual_node
		new_node.parent = self.virtual_node
		
		current = self._max_node
		parent = self.virtual_node
		edges = 0
		height_changes = 0
		
		#empty tree case
		if self._max_node is None or not self._max_node.is_real_node():
			self.root = new_node
			self._max_node = self.root
			new_node.parent = self.virtual_node
		else:
			# going up the tree until we find a node with key <= insert key
			while current.parent is not None and current.parent.is_real_node() and key < current.key:
				current = current.parent
				edges += 1

			# going down the tree to find the key
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
				if new_node.key > self._max_node.key:
					self._max_node = new_node

			# Rebalance the tree
			height_changes += self.rebalance_tree(parent)

		self._size += 1

		return new_node, edges, height_changes

	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		if node is None or not node.is_real_node():
			return
		
		# Case 1: node is a leaf
		if (node.left is None or not node.left.is_real_node()) and (node.right is None or not node.right.is_real_node()):
			if node.parent is None or not node.parent.is_real_node(): # node is root
				self.root = self.virtual_node
				self._max_node = self.virtual_node
			else: # node has a parent 
				if node == node.parent.left:
					node.parent.left = self.virtual_node
				else:
					node.parent.right = self.virtual_node
				# update max_node if needed
				if node == self._max_node:
					self.update_max()
			parent_for_rebalance = node.parent
			node.parent = self.virtual_node  # help garbage collection
		
		# Case 2: node has one child
		elif (node.left is None or not node.left.is_real_node()) or (node.right is None or not node.right.is_real_node()):
			child = node.left if node.left.is_real_node() else node.right
			if node.parent is None or not node.parent.is_real_node(): # node is root
				self.root = child
				child.parent = self.virtual_node
			else: # node has a parent
				if node == node.parent.left:
					node.parent.left = child
				else:
					node.parent.right = child
				child.parent = node.parent
			
			# update max_node if needed
			if node == self._max_node: #check for duplicates in other cases??? check w GPT that child is always new max!!!!!!!!!!!!!!!!!!
				self._max_node = child if child.is_real_node() else self.virtual_node
			parent_for_rebalance = node.parent
			node.parent = self.virtual_node  # help garbage collection

		# Case 3: node has two children
		else:
			succ = self.successor(node) # we know succ has at most one child (right)
			parent_for_rebalance = succ.parent
			if succ == node.right:
				parent_for_rebalance = succ  # since succ will move to node's place

			# delete successor
			if succ.parent.left == succ:
				succ.parent.left = succ.right
			else:
				succ.parent.right = succ.right
			if succ.right.is_real_node():
				succ.right.parent = succ.parent
			
			#replace node with successor
			succ.parent = node.parent
			if node.parent is None or not node.parent.is_real_node(): # node is root
				self.root = succ
			else:
				if node == node.parent.left:
					node.parent.left = succ
				else:
					node.parent.right = succ
			succ.left = node.left
			succ.right = node.right
			if node.left is not None and node.left.is_real_node():
				node.left.parent = succ
			if node.right is not None and node.right.is_real_node():
				node.right.parent = succ
			
			succ.height = node.height  # successor takes node's height
			node.parent = self.virtual_node  # help garbage collection
		
		self._size -= 1
			
		# Rebalance the tree
		self.rebalance_tree(parent_for_rebalance)

		return None

	""" finds the in-order successor of a given node
	@type node: AVLNode
	@param node: the node to find the successor of
	@pre: node is a real pointer to a node in self
	@rtype: AVLNode
	"""
	def successor(self, node):
		if (node is None) or (not node.is_real_node()) or (self._size == 1) or (node is self._max_node):
			return None
		elif node.right is not None and node.right.is_real_node():
			# go to leftmost node in right subtree
			current = node.right
			while current.left is not None and current.left.is_real_node():
				current = current.left
			return current
		else:
			# go up until we find a node that is a left child
			current = node
			while current.parent is not None and current.parent.is_real_node() and current == current.parent.right:
				current = current.parent
			return current.parent if current.parent is not None and current.parent.is_real_node() else None

	
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
		new_node = AVLNode(key, val)
		h1 = self.root.height if self.root.is_real_node() else -1
		h2 = tree2.root.height if tree2.root.is_real_node() else -1
		parent_for_rebalance = self.virtual_node
		
		self_empty = self.root is None or not self.root.is_real_node()
		tree2_empty = tree2.root is None or not tree2.root.is_real_node()
		if self_empty or tree2_empty:
			if self_empty and tree2_empty:
				self.root = new_node
				new_node.left = self.virtual_node
				new_node.right = self.virtual_node
				self._max_node = new_node
				self._size = 1
			elif self_empty:
				tree2.insert(key, val)  # insert into tree2
				self.root = tree2.root
				self._max_node = tree2._max_node
				self._size = tree2._size
			else:  # tree2 is empty
				self.insert(key, val)  # insert into self
			tree2.root = tree2.virtual_node  # empty tree2
			return

		if self._max_node.key < key:  # self's keys are smaller than tree2's keys
			if h1 == h2:
				# heights are equal
				new_node.left = self.root
				new_node.right = tree2.root
				if self.root.is_real_node():
					self.root.parent = new_node
				if tree2.root.is_real_node():
					tree2.root.parent = new_node
				self.root = new_node
				parent_for_rebalance = new_node
			
			elif h1 > h2:
				# self is taller
				current = self.root
				while current.height > h2:
					current = current.right
				
				original_parent = current.parent
				if original_parent is None:
					original_parent = self.virtual_node
				
				# insert new_node here
				new_node.parent = original_parent
				if original_parent is None or not original_parent.is_real_node():
					self.root = new_node
				else:
					original_parent.right = new_node
				new_node.left = current
				new_node.right = tree2.root
				current.parent = new_node
				if tree2.root.is_real_node():
					tree2.root.parent = new_node
				parent_for_rebalance = original_parent
				if not parent_for_rebalance.is_real_node():
					parent_for_rebalance = new_node
			
			else:
				# tree2 is taller
				current = tree2.root
				while current.height > h1:
					current = current.left
				
				original_parent = current.parent
				if original_parent is None:
					original_parent = self.virtual_node
				
				# insert new_node here
				new_node.parent = original_parent
				if original_parent is None or not original_parent.is_real_node():
					self.root = new_node
				else:
					original_parent.left = new_node
				new_node.right = current
				new_node.left = self.root
				current.parent = new_node
				if self.root.is_real_node():
					self.root.parent = new_node
				if current.parent is not None and current.parent.is_real_node():
					self.root = tree2.root
				parent_for_rebalance = original_parent
				if not parent_for_rebalance.is_real_node():
					parent_for_rebalance = new_node

			self._max_node = tree2._max_node
			
		else:  # tree2's keys are smaller than self's keys
			if h2 == h1:
				# heights are equal
				new_node.left = tree2.root
				new_node.right = self.root
				if tree2.root.is_real_node():
					tree2.root.parent = new_node
				if self.root.is_real_node():
					self.root.parent = new_node
				self.root = new_node
				parent_for_rebalance = new_node
			
			elif h2 > h1:
				# tree2 is taller
				current = tree2.root
				while current.height > h1:
					current = current.right
				
				original_parent = current.parent
				if original_parent is None:
					original_parent = self.virtual_node
				
				# insert new_node here
				new_node.parent = original_parent
				if original_parent is None or not original_parent.is_real_node():
					self.root = new_node
				else:
					original_parent.right = new_node
				new_node.left = current
				new_node.right = self.root
				current.parent = new_node
				if self.root.is_real_node():
					self.root.parent = new_node
				if current.parent is not None and current.parent.is_real_node():
					self.root = tree2.root
				parent_for_rebalance = original_parent
				if not parent_for_rebalance.is_real_node():
					parent_for_rebalance = new_node
			
			else:
				# self is taller
				current = self.root
				while current.height > h2:
					current = current.left
				
				original_parent = current.parent
				if original_parent is None:
					original_parent = self.virtual_node
				# insert new_node here
				new_node.parent = original_parent
				if original_parent is None or not original_parent.is_real_node():
					self.root = new_node
				else:
					original_parent.left = new_node
				new_node.right = current
				new_node.left = tree2.root
				current.parent = new_node
				if tree2.root.is_real_node():
					tree2.root.parent = new_node
				parent_for_rebalance = original_parent
				if not parent_for_rebalance.is_real_node():
					parent_for_rebalance = new_node
		
		
		def get_h(node):
			if node is not None and node.is_real_node():
				return node.height
			return -1
		new_node.height = 1 + max(get_h(new_node.left), get_h(new_node.right))
		
		tree2.root = tree2.virtual_node  # empty tree2		
		self._size += tree2._size + 1
		
		# Rebalance the tree
		self.rebalance_tree(parent_for_rebalance)
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
		left_tree = AVLTree()
		right_tree = AVLTree()
		
		# special case: split at max
		if node == self._max_node:
			if self.root.is_real_node():
				left_tree.root = self.root
				left_tree.root.parent = left_tree.virtual_node
				left_tree.delete(node)
				left_tree.update_max()
			return left_tree, AVLTree()

		# left subtree of node
		if node.left is not None and node.left.is_real_node():
			left_tree.root = node.left
			# node.left = self.virtual_node
			left_tree.root.parent = left_tree.virtual_node
			left_tree.update_max()

		# right subtree of node
		if node.right is not None and node.right.is_real_node():
			right_tree.root = node.right
			# node.right = self.virtual_node
			right_tree.root.parent = right_tree.virtual_node
			right_tree.update_max()

		# node.height = 0   # node is now a leaf
		# go up the tree from node to root
		current = node.parent
		prev = node
		while current is not None and current.is_real_node():	
			# original_parent = current.parent

			if prev == current.left:
				# prev was left child -> current and its right subtree go to right_tree
				# right_subtree = current.right
				# current.right = self.virtual_node

				temp_tree = AVLTree()
				
				if current.right is not None and current.right.is_real_node():
					temp_tree.root = current.right
					temp_tree.root.parent = temp_tree.virtual_node
					temp_tree.update_max()
				
				# current.left = self.virtual_node
				# current.height = 0  # current is now a leaf
				right_tree.join(temp_tree, current.key, current.value)
			
			else:
				# prev was right child -> current and its left subtree go to left_tree
				# left_subtree = current.left
				# current.left = self.virtual_node

				temp_tree = AVLTree()
				if current.left is not None and current.left.is_real_node():
					temp_tree.root = current.left
					temp_tree.root.parent = temp_tree.virtual_node
					temp_tree.update_max()
				
				# current.right = self.virtual_node
				# current.height = 0  # current is now a leaf
				temp_tree.join(left_tree, current.key, current.value)
				left_tree = temp_tree
			
			prev = current
			current = current.parent
		
		# if not self.root.is_real_node():
		# 	self._max_node = self.virtual_node
		
		return left_tree, right_tree

	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		result = []

		def in_order(node):
			if node is None or not node.is_real_node():
				return
			in_order(node.left)
			result.append((node.key, node.value))
			in_order(node.right)
		
		in_order(self.root)
		return result

	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self):
		return None if (self.root is None or not self.root.is_real_node()) else self._max_node

	"""updates the max_node field of the AVLTree
	@rtype: None
	"""
	def update_max(self):
		# recompute max_node (rightmost)
		node = self.root
		if node is None or not node.is_real_node():
			self._max_node = self.virtual_node
			return None
		while node.right is not None and node.right.is_real_node():
			node = node.right
		self._max_node = node
		return None
	
	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return self._size	


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root if self._size > 0 else None
	
