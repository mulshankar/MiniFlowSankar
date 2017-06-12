import numpy

class Node(object):
	def __init__(self, inbound_nodes=[]):
		# Node(s) from which this Node receives values
		self.inbound_nodes = inbound_nodes
		# Node(s) to which this Node passes values
		self.outbound_nodes = []
		# For each inbound Node here, add this Node as an outbound Node to _that_ Node.
		for n in self.inbound_nodes:
			n.outbound_nodes.append(self)
		self.value = None
	def forward(self):
		"""
		Forward propagation.

		Compute the output value based on `inbound_nodes` and
		store the result in self.value.
		"""
		raise NotImplemented
		
class Input(Node):
    def __init__(self):
		# An Input node has no inbound nodes,
		# so no need to pass anything to the Node instantiator.
		Node.__init__(self)

		# NOTE: Input node is the only node where the value
		# may be passed as an argument to forward().
		#
		# All other node implementations should get the value
		# of the previous node from self.inbound_nodes
		#
		# Example:
		# val0 = self.inbound_nodes[0].value
	def forward(self, value=None):
		# Overwrite the value if one is passed in.
		if value is not None:
			self.value = value

class Add(Node):
	def __init__(self, x, y):
		Node.__init__(self, [x, y])

	def forward(self):
		self.value=self.inbound_nodes[0].value+self.inbound_nodes[1].value

def topological_sort(feed_dict):
	"""
	Sort generic nodes in topological order using Kahn's Algorithm.

	`feed_dict`: A dictionary where the key is a `Input` node and the value is the respective value feed to that node.

	Returns a list of sorted nodes.
	"""

	input_nodes = [n for n in feed_dict.keys()]

	G = {}
	nodes = [n for n in input_nodes]
	while len(nodes) > 0:
		n = nodes.pop(0)
		if n not in G:
			G[n] = {'in': set(), 'out': set()}
		for m in n.outbound_nodes:
			if m not in G:
				G[m] = {'in': set(), 'out': set()}
			G[n]['out'].add(m)
			G[m]['in'].add(n)
			nodes.append(m)

	L = []
	S = set(input_nodes)
	while len(S) > 0:
		n = S.pop()

		if isinstance(n, Input):
			n.value = feed_dict[n]

		L.append(n)
		for m in n.outbound_nodes:
			G[n]['out'].remove(m)
			G[m]['in'].remove(n)
			# if no other incoming edges add to S
			if len(G[m]['in']) == 0:
				S.add(m)
	return L


def forward_pass(output_node, sorted_nodes):
	"""
	Performs a forward pass through a list of sorted nodes.

	Arguments:

		`output_node`: A node in the graph, should be the output node (have no outgoing edges).
		`sorted_nodes`: A topologically sorted list of nodes.

	Returns the output Node's value
	"""

	for n in sorted_nodes:
		n.forward()

	return output_node.value

############################################ BASE ALGO ############################

"""
This script builds and runs a graph with miniflow.

There is no need to change anything to solve this quiz!

However, feel free to play with the network! Can you also
build a network that solves the equation below?

(x + y) + y
"""

from miniflow import *

x, y = Input(), Input()

f = Add(x, y)

feed_dict = {x: 10, y: 5}

sorted_nodes = topological_sort(feed_dict)
output = forward_pass(f, sorted_nodes)

# NOTE: because topological_sort set the values for the `Input` nodes we could also access
# the value for x with x.value (same goes for y).
print("{} + {} = {} (according to miniflow)".format(feed_dict[x], feed_dict[y], output))

