## Inspiration 
While working on a graph clustering algorithm, I encountered a conundrum where I didn't know whether to store my data in a dictionary or a heap.  The advantage of a dictionary was that the data could be referenced in O(1), but the downside was that it would take O(n) to find the min value.  The advantage of a heap was that the min value could be found in O(logn), but looking up a value by key would be impossible.  I needed a data structure that had all of the benefits of a dictionary and a heap.  Thus, I created the searchHeap.

## Functions
The functions and time complexities of the searchHeap are as follows:
- create		-	O(n)		-	Takes a dictionary, and creates this data structure 
- returnAsDict		-	O(n)		-	Returns the key-value pairs stored in the data structure as a dictionary 
- insert		-	O(logn)		-	Insert key-value pair 
- delete		- 	O(logn)		-	Delete key-value pair by key 
- update		- 	O(logn)		-	Update value in key-value pair 
- pop 		 	- 	O(logn)		-	Returns the min value in the data structure, and maintains all necessary properties (ie. heap property, etc.) 
- getValueFromKey	-	O(1)		-	Returns the value of key 
- keyMembership		-	O(1)		-	Checks the membership of a key within the data structure.  Returns True if key is a member, else returns False

## About the Data
The searchHeap is meant to store key-value pairs where they value is an integer.  The searchHeap will not perform correctly if given non-integer data as a value.

## Other
The code within the main function serves two purposes: 
- 1) To demonstrate how to use the various searchHeap functions outlined above.
- 2) To demonstrate that the search heap is working and is implemented properly.  The outputs are printed to the terminal to show that each individual function's result is correct, and that the internal state of the data structure is also correct.
