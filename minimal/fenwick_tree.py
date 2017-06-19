class FenwickTree:
  """
    This class implements cumulative sums over groups under addition
    the default group is the integers, but arbitrary objects may be 
    handled. The default null element is 0, and it can be overriden
    by passing a callable that returns the desired null element.
  """
  def __init__(self, n, zero = lambda: 0):
    self.nodes = [zero() for _ in xrange(n)];
    self.zero = zero;
  def Add(self, i, val):
    """
      Add(self, i, val)
        Random update, add a value in the given position of the list
        the value val will be added to the position i of the table
    """
    index = i;
    while (index < len(self.nodes)):
       # Add 'val' to current node of BI Tree
       self.nodes[index] += val;
       # Update index to that of parent in update View
       index |= (index+1);
  def getSum(self, i):
    """
      getSum(self, i)
        Random query function, calculate the sum from the beginning of 
        the table to the position i
    """
    index = i;
    sum = self.zero(); # Iniialize result
    # index in BITree[] is 1 more than the index in arr[]
    # Traverse ancestors of BITree[index]
    while (index>0):
        # Add current element of BITree to sum
        sum += self.nodes[index-1];
        # Move index to parent node in getSum View
        index &= index-1;
    return sum;

if __name__ == '__main__':
  import random;
  s = FenwickTree(16);
  for i in random.sample(range(1, 16), 15):
    s.Add(i, 1);
  for i in xrange(1, 16):
    print s.getSum(i);
