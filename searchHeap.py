import heapq
import hashlib
import decimal
import math
import random
import sys


'''
This is a custom data structure that is used to store key-value pairs.  The values must be integers.  The basic functions implemented for this data structure, and their time complexities, are as follows:

create		-	O(n)		-	Takes a dictionary, and creates this data structure
returnAsDict	-	O(n)		-	Returns the key-vaue pairs stored in the data structure as a dictionary
insert		-	O(logn)		-	Insert key-value pair
delete		- 	O(logn)		-	Delete key-value pair by key
update		- 	O(logn)		-	Update value in key-value pair
pop 	 	- 	O(logn)		-	Returns the min value in the data structure, and maintains all necessary properties (ie. heap property, etc.)
getValueFromKey	-	O(1)		-	Returns the value of key
keyMembership	-	O(1)		-	Checks the membership of a key within the data structure.  Returns True if key is a member, else returns False

Testing of each of these functions occurs within the main function of this file.  Outputs of testing are printed to the console to prove that the correct result was returned, as well as that the internal structure of the searchHeap is correct.
'''


class searchHeap:

	# The Constructor
	def __init__(self):
		self.minHeap = []
		self.valueToKey = {}
		self.keyToIndex = {}


	# Assign a Unique Decimal Value to the Value in a Key-Value Pair
	# 	O(1)
	def _uniqueValue(self, key, value):

		# Repeat process until a unique value is found
		while True:

			# Take a hash of the key and turn it into a decimal
			# 	Append some random data to the end of the key before hashing.  This causes a different hash every time
			# 		This makes it equal probability that two keys with the same value will be popped first
			keyWithSalt = key + str(random.randint(0, 1000000000000))
			keyHash = hashlib.sha256(keyWithSalt).hexdigest()
			keyHashAsInt = int(keyHash, 16)
			numDigits = len(str(keyHashAsInt))
			decimal.getcontext().prec = numDigits + 1
			keyHashAsDecimal = decimal.Decimal(keyHashAsInt) / decimal.Decimal(10 ** numDigits)
		
			# Add the decimal to value
			decimal.getcontext().prec = numDigits + 1
			value = decimal.Decimal(value) + decimal.Decimal(keyHashAsDecimal)

			# Check that value is unique
			if value not in self.valueToKey:
				break

			# Append '_' to key to act as an incrementing salt, so that there are technically unlimited possibilities for keyWithSalt value
			else:
				key = key + '_'

		# Return new value
		return value


	# Get Value from Key
	# 	O(1)
	def _getValueFromKey(self, key):
		indexAtKey = self.keyToIndex[key]
		valueAtIndex = self.minHeap[indexAtKey]
		return valueAtIndex


	# Bubble Up
	# 	O(logn)
	def _heapBubbleUp(self, value, valueIndex, valueToUpdatedHeapIndicies):

		# Check if the root has been reached
		# 	This is the base case
		if valueIndex == 0:
			valueToUpdatedHeapIndicies[value] = valueIndex
			return valueToUpdatedHeapIndicies

		# Otherwise, bubble up the heap
		else:

			# Calculate parent node
			parentIndex = (valueIndex - 1) / 2

			# If the heap property is violated
			parentValue = self.minHeap[parentIndex]
			if value < parentValue:

				# Switch value and parent value if necessary, and record new indicies
				self.minHeap[parentIndex] = value
				self.minHeap[valueIndex] = parentValue

				# Record the change in indicies
				valueToUpdatedHeapIndicies[value] = parentIndex
				valueToUpdatedHeapIndicies[parentValue] = valueIndex

				# Recursively call heapBubbleUp() until the heap property is restored
				valueToUpdatedHeapIndicies = self._heapBubbleUp(value, parentIndex, valueToUpdatedHeapIndicies)
				return valueToUpdatedHeapIndicies

			# Otherwise, the heap property has been restored
			else:
				return valueToUpdatedHeapIndicies


	# Heap Insert
	# 	O(logn)
	def _heapInsert(self, value):

		# Append value to end of list and calculate index
		# 	O(1)
		self.minHeap.append(value)

		# Bubble value up until the heap property is restored
		# 	O(logn)
		valueIndex = len(self.minHeap) - 1
		valueToUpdatedHeapIndicies = {value: valueIndex}
		valueToUpdatedHeapIndicies = self._heapBubbleUp(value, valueIndex, valueToUpdatedHeapIndicies)

		# Return indices in heap to be updated in keyToIndex
		return valueToUpdatedHeapIndicies


	# Bubble Down
	# 	O(logn)
	def _heapBubbleDown(self, index, valueToUpdatedHeapIndicies):

		# Calculate the indicies of the child nodes
		leftChildIndex = (2 * index) + 1
		rightChildIndex = (2 * index) + 2

		# Check if a leaf node has been reached
		# 	This is the base case
		minHeapFinalIndex = len(self.minHeap) - 1
		if (minHeapFinalIndex < leftChildIndex) or (minHeapFinalIndex < rightChildIndex):
			return valueToUpdatedHeapIndicies

		# Otherwise, bubble down the heap
		else:

			# Find the child node with the smallest value
			leftChildValue = self.minHeap[leftChildIndex]
			rightChildValue = self.minHeap[rightChildIndex]
			if leftChildValue < rightChildValue:
				smallestChildIndex = leftChildIndex
			else:
				smallestChildIndex = rightChildIndex

			# Switch value of node at index and value of node at smallestChildIndex
			valueAtIndex = self.minHeap[index]
			valueAtSmallestChildIndex = self.minHeap[smallestChildIndex]
			self.minHeap[index] = valueAtSmallestChildIndex
			self.minHeap[smallestChildIndex] = valueAtIndex

			# Record the change in indicies
			valueToUpdatedHeapIndicies[valueAtIndex] = smallestChildIndex
			valueToUpdatedHeapIndicies[valueAtSmallestChildIndex] = index

			# Recursively call heapBubbleDown() until the heap property is restored
			self._heapBubbleDown(smallestChildIndex, valueToUpdatedHeapIndicies)
			return valueToUpdatedHeapIndicies


	# Heap Delete
	# 	O(logn)
	def _heapDelete(self, index):

		# Replace the value at index with the value of the final node in minHeap.  Then pop the final node, as it is now redundant.
		# 	O(1)
		furthestRightNodeIndex = len(self.minHeap) - 1
		furthestRightNodeValue = self.minHeap[furthestRightNodeIndex]
		self.minHeap[index] = furthestRightNodeValue
		self.minHeap.pop()

		# Bubble down from index until heap property is restored
		# 	O(logn)
		valueToUpdatedHeapIndicies = {furthestRightNodeValue: index}
		valueToUpdatedHeapIndicies = self._heapBubbleDown(index, valueToUpdatedHeapIndicies)

		# Return indices in heap to be updated in keyToIndex
		return valueToUpdatedHeapIndicies


	# Get Number of Elements
	# 	O(1)
	def getNumElements(self):
		lenMinHeap = len(self.minHeap)
		lenValueToKey = len(self.valueToKey)
		lenKeyToIndex = len(self.keyToIndex)
		if (lenMinHeap == lenValueToKey) and (lenValueToKey == lenKeyToIndex):
			return lenMinHeap
		else:
			sys.exit('Error: \tinconsistent sizes of internal data structures')

	# Get the Min Value in searchHeap
	# 	O(1)
	def getMinKeyValue(self):
		if self.getNumElements() > 0:
			minValue = self.minHeap[0]
			minKey = self.valueToKey[minValue]
			return (minKey, math.floor(minValue))
		else:
			sys.exit('Error: \tno min key-value when searchHeap is empty')


	# Get Value from Key
	# 	O(1)
	def getValueFromKey(self, key):

		# Check if key already in data structure
		if key not in self.keyToIndex:
			sys.exit('KeyError: \t' + str(key))

		# Otherwise, get the value associated with key
		indexAtKey = self.keyToIndex[key]
		valueAtIndex = math.floor(self.minHeap[indexAtKey])
		return valueAtIndex


	# Check if Key is a Member of the Data Structure
	# 	O(1)
	def keyMembership(self, key):
		if key in self.keyToIndex:
			return True
		else:
			return False


	# Create Data Structure
	# 	O(n)
	def create(self, keyToValue):

		# Call the constructor
		self.__init__()

		# Adjust each value to have "hashed decimal"
		# 	O(n)
		for key in keyToValue:
			value = keyToValue[key]
 			value = self._uniqueValue(key, value)
			keyToValue[key] = value

		# Create valueToKey
		# 	O(n)
		for key in keyToValue:
			value = keyToValue[key]
			self.valueToKey[value] = key

		# Create minHeap
		# 	O(n)
		valueList = keyToValue.values()
		heapq.heapify(valueList)
		self.minHeap = valueList

		# Create keyToIndex
		# 	O(n)
		for index in range(len(self.minHeap)):
			value = self.minHeap[index]
			key = self.valueToKey[value]
			self.keyToIndex[key] = index	


	# Return Key-Value Pairs As Dictionary
	# 	O(n)
	def returnAsDict(self):	
	
		# Iterate through each key and get corresponding value
		# 	O(n)
		keyToValues = {}
		for key in self.keyToIndex:
			value = self._getValueFromKey(key)
			keyToValues[key] = math.floor(value)

		# Return keyToValues
		return keyToValues


	# Insert
	# 	O(logn)
	def insert(self, key, value):

		# Check if key already in data structure
		if key in self.keyToIndex:
			sys.exit('KeyError: \t' + str(key) + ' already in data structure')

		# Adjust value to have "hashed decimal"
		# 	O(1)
 		value = self._uniqueValue(key, value)

		# Add key-value to valueToKey
		# 	O(1)
		self.valueToKey[value] = key

		# Insert value to minHeap
		# 	O(logn)
		valueToUpdatedHeapIndicies = self._heapInsert(value)

		# Add updated key-indices to keyToIndex
		# 	O(logn)
		for value in valueToUpdatedHeapIndicies:

			# Get the new index
			newIndex = valueToUpdatedHeapIndicies[value]

			# Get the key corresponding to the value
			correspondingKey = self.valueToKey[value]

			# Update keyToIndex 
			self.keyToIndex[correspondingKey] = newIndex


	# Delete
	# 	O(logn)
	def delete(self, key):
	
		# Check if key not in data structure
		if key not in self.keyToIndex:
			sys.exit('KeyError: \t' + str(key))

		# Get the value associated with key, before any internal changes are made to the data structure
		# 	O(1)
		originalValue = self._getValueFromKey(key)

		# Remove key-value from minHeap
		# 	O(logn)
		indexToDelete = self.keyToIndex[key]
		valueToUpdatedHeapIndicies = self._heapDelete(indexToDelete)

		# Add updated key-indices to keyToIndex
		# 	O(logn)
		for value in valueToUpdatedHeapIndicies:

			# Get the new index
			newIndex = valueToUpdatedHeapIndicies[value]

			# Get the key corresponding to the value
			correspondingKey = self.valueToKey[value]

			# Update keyToIndex 
			self.keyToIndex[correspondingKey] = newIndex

		# Remove key-value from valueToKey
		# 	O(1)
		del self.valueToKey[originalValue]

		# Remove key-value from keyToValue
		# 	O(1)
		del self.keyToIndex[key]


	# Update
	#	O(logn)
	def update(self, key, value):

		# Check if key not in data structure
		if key not in self.keyToIndex:
			sys.exit('KeyError: \t' + str(key))

		# Adjust value to have "hashed decimal"
		# 	O(1)
 		value = self._uniqueValue(key, value)

		# Delete old key-value from data structure
		# 	O(logn)
		self.delete(key)

		# Insert new key-value to data structure
		# 	O(logn)
		self.insert(key, value)

	# Pop Min
	# 	O(logn)
	def pop(self):

		# Check if minHeap has entries
		if len(self.minHeap) == 0:
			sys.exit('IndexError: \tpop from empty list')

		# Get minimum value in minHeap, and key associated with minValue
		# 	O(1)
		minValue = self.minHeap[0]
		key = self.valueToKey[minValue]

		# Remove minValue and key from data structure
		# 	O(logn)
		self.delete(key)

		# Return the minimum value
		return (key, math.floor(minValue))


if __name__ == '__main__':

	# Initialize data
	idict = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6}

	# Create a test instance of searchHeap()
	test = searchHeap()

	# Test create() and returnAsDict()
	test.create(idict)
	output = test.returnAsDict()
	print "\n\n-----create()-----"
	print "-----returnAsDict()-----"
	print "input: \t\t{'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6}" + '\n'
	print "output: \t" + str(output) + '\n'
	print "minHeap: \t" + str(test.minHeap) + '\n'
	print "valueToKey: \t" + str(test.valueToKey) + '\n'
	print "valueToKey_keys: \t" + str(test.valueToKey.keys()) + '\n'
	print "keyToIndex: \t\t" + str(test.keyToIndex) + '\n'
	print "keyToIndex_keys: \t" + str(test.keyToIndex.keys()) + '\n'

	# Test insert()
	test.insert('seven', 7)
	output = test.returnAsDict()
	print "\n\n-----insert()-----"
	print "input: \t\t{'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6}" + '\n'
	print "output: \t" + str(output) + '\n'
	print "minHeap: \t" + str(test.minHeap) + '\n'
	print "valueToKey: \t" + str(test.valueToKey) + '\n'
	print "valueToKey_keys: \t" + str(test.valueToKey.keys()) + '\n'
	print "keyToIndex: \t\t" + str(test.keyToIndex) + '\n'
	print "keyToIndex_keys: \t" + str(test.keyToIndex.keys()) + '\n'

	# Test delete()
	test.delete('two')
	output = test.returnAsDict()
	print "\n\n-----delete()-----"
	print "input: \t\t{'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7}" + '\n'
	print "output: \t" + str(output) + '\n'
	print "minHeap: \t" + str(test.minHeap) + '\n'
	print "valueToKey: \t" + str(test.valueToKey) + '\n'
	print "valueToKey_keys: \t" + str(test.valueToKey.keys()) + '\n'
	print "keyToIndex: \t\t" + str(test.keyToIndex) + '\n'
	print "keyToIndex_keys: \t" + str(test.keyToIndex.keys()) + '\n'
	print "\n\n-----end delete-----\n\n"

	# Test update()
	test.update('four', 6)
	output = test.returnAsDict()
	print "\n\n-----update()-----"
	print "input: \t\t{'one': 1, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7}" + '\n'
	print "output: \t" + str(output) + '\n'
	print "minHeap: \t" + str(test.minHeap) + '\n'
	print "valueToKey: \t" + str(test.valueToKey) + '\n'
	print "valueToKey_keys: \t" + str(test.valueToKey.keys()) + '\n'
	print "keyToIndex: \t\t" + str(test.keyToIndex) + '\n'
	print "keyToIndex_keys: \t" + str(test.keyToIndex.keys()) + '\n'

	# Test pop()
	minValue = test.pop()
	output = test.returnAsDict()
	print "\n\n-----pop()-----"
	print "poppedValue: \t" + str(minValue)
	print "input: \t\t{'three': 3, 'four': 6, 'five': 5, 'six': 6, 'seven': 7}" + '\n'
	print "output: \t" + str(output) + '\n'
	print "minHeap: \t" + str(test.minHeap) + '\n'
	print "valueToKey: \t" + str(test.valueToKey) + '\n'
	print "valueToKey_keys: \t" + str(test.valueToKey.keys()) + '\n'
	print "keyToIndex: \t\t" + str(test.keyToIndex) + '\n'
	print "keyToIndex_keys: \t" + str(test.keyToIndex.keys()) + '\n'	

	# Test getValueFronKey()
	value = test.getValueFromKey('three')
	print "\n\n-----getValueFronKey()-----"
	print "value: \t" + str(value)

	# Test keyMembership()
	print "\n\n-----keyMembership()-----"
	result = test.keyMembership('three')
	print str(result)
	result = test.keyMembership('zebra')
	print str(result)










