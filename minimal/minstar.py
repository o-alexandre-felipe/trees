"""
  This script implements min* function using
  using different strategies, and makes it possible to
  easily count the number of muxes and comparators
  required for that particular implementation, for
  different input sizes.

  the above mentioned min* function is defined as follows
    min(l[k] for k in xrange(len(l)) if k != i) for i in xrange(len(l))
"""

import random;

class instances:
  muxes = 0;
  comparators = 0;

def min2(a, b):
  """ min2(a,b)
      the minimum binary function
  """
  instances.muxes += 1; 
  instances.comparators += 1;
  return a if a < b else b;

def minl(l):
  """
    minl(l)
      Divide and conquer aproach:
      Retrieve the minimum of a list by successively
      dividing the input list in two list (one with the 
      elements on the even positions and one with the
      elements on the odd positions) and call it recursively
      until it reduces to the trivial case (a list with one element)
      or a list with two elements that may be passed to a binary
      minimum function
  """
  if len(l) == 1:
    return l[0];
  elif len(l) == 2:
    return min2(*l);
  elif len(l) > 2:
    return min2(minl(l[0::2]), minl(l[1::2]))
  else: return []

class ImplementationError(Exception):
  def __init__(self, msg, arg, ret, ref):
    self.value = msg;
    self.arg = arg;
    self.ret = ret;
    self.ref = ref;
  def __str__(self):
    return "\n%s\n Arguments: %s\n Returned: %s\n Expected: %s\n" % (
      self.value, self.arg, self.ret, self.ref);

def minstar_ref(l):
  """
    minstar_ref(l)
      Retrieve a list with minimum for each set of elements
      formed by excluding one element from the the original list.
  """
  return [min(l[0:i] + l[i+1:]) for i,_ in enumerate(l)], min(l);

def minstar_naive(l):
  """
    minstar_naive(l)
      Retrieve a list with minimum for each set of elements
      formed by excluding one element from the the original list.
      The problem is approached by calculating the minimum of 
      each set separatedly
  """
  return [minl(l[0:i] + l[i+1:]) for i,_ in enumerate(l)], min(l);

def minstar_rec(l):
  """
    minstar_rec(l)
      Retrieve a list with the minimum for each set of elements
      formed by excluding one element from the original list,
      
      The problem is solved with the divide and conquer approach

      The function return the minimum of the input list and 
      the list with the minimum of the sublists with size len(l)-1
      
  """
  if len(l) == 2:
    return [l[1],l[0]], min2(l[0], l[1]);
  elif len(l) == 3:
    t = [min2(l[1],l[2]), min2(l[0], l[2]), min2(l[0], l[1])];
    return t, min2(t[0], l[0]);
  elif len(l) > 3:
    lhs, lhsm = minstar_rec(l[:len(l)/2]);
    rhs, rhsm = minstar_rec(l[len(l)/2:]);
    return ([min2(l, rhsm) for l in lhs] + 
            [min2(r, lhsm) for r in rhs],
            min2(lhsm, rhsm));

def minstar_flags(l, top=1):
  """
    minstar_flags(l)

      This is a more sophisticated approach approach that takes
      advantage of the fact that the output list will have at 
      most two different values, the two smallest values in the
      list.

      It is only required to calculate the minimum of the list
      obtaining excluding the minimum, all other entries
      will have the same minimum value that the complete list.

      This function uses the divide and conquer approach with
      the difference that only the two least values and the position
      of the minimum value are returned.
  """

  if top:
    first, second, flags = minstar_flags(l, 0);
    return ([second if f else first for f in flags],);
  else:
    if len(l) == 2:
      instances.comparators += 1;
      instances.muxes += 2;
      if(l[0] < l[1]):
        return l[0], l[1], [1, 0];
      else:
        return l[1], l[0], [0, 1];
    if len(l) % 2 == 1:
      first, second, flags = minstar_flags(l[1:], 0);
      second_ = min2(second, l[0]);
      instances.comparators += 1;
      instances.muxes += 2;
      if first < l[0]:
        return first, second_, [0] + flags;
      else:
        return l[0], first, [1] + [0] * (len(l)-1);
    else:
      first_lhs, second_lhs, flags_lhs = minstar_flags(l[:len(l)/2], 0);
      first_rhs, second_rhs, flags_rhs = minstar_flags(l[len(l)/2:], 0);
      instances.comparators += 1;
      instances.muxes += 2;
      if first_lhs < first_rhs:
        first = first_lhs;
        max_first = first_rhs;
        flags = flags_lhs + [0 for _ in flags_rhs];
      else:
        first = first_rhs;
        max_first = first_lhs;
        flags = [0 for _ in flags_lhs] + flags_rhs;
      min_second = min2(second_lhs, second_rhs);
      second = min2(max_first, min_second);
      return first, second, flags;

def minstar_cascade(l):
  """
    minstar_cascade(l)
      
      This function is calculated by two auxiliary
      lists, one has the minimum of the sublist before the 
      corresponding position, and the other has the minimum
      of the sublist after the corresponding position.
      The minimum of the sublist obtained excluding one element
      is the minimum of the corresponding elements in the two
      auxiliary lists.

      The advantage of this approach for sequential calculation
      is that the auxiliary lists may be calculated recursively
      using (n-2) binary minimum functions, the total complexity
      is 3*n-6 invocations to a binary binimum function.
  """
  l1 = [l[0]];
  l2 = [l[-1]];
  for i in xrange(1, len(l)-1):
    l1.append(min2(l1[-1], l[i]));
    l2.append(min2(l2[-1], l[len(l)-i-1]));
  return ([l2[-1]] + [min2(l1i,l2i) 
      for l1i, l2i in zip(l1[0:-1], (l2[0:-1])[::-1])] + [l1[-1]],)

def check_implementation(fun, d_in, d_out):
  """
    Routine for checking the correctness of the implementations
  """
  instances.muxes = 0;
  instances.comparators = 0;
  ans = fun(d_in);
  if ans != d_out:
    e = ImplementationError("%s is not working as expected." %
          fun.__name__, d_in, ans, d_out)
    raise e;
  return ans + (instances.comparators,instances.muxes);

if __name__ == '__main__':
  complexity = [];
  for i in xrange(3, 60):
    u = [random.randint(0, 100) for _ in xrange(i)]
    ref_output = minstar_ref(u);
    _,_,m1,c1 = check_implementation(minstar_rec, u, ref_output);
    _,m2,c2 = check_implementation(minstar_flags, u, ref_output[0:1]);
    _,m3,c3 = check_implementation(minstar_cascade, u, ref_output[0:1]);
    _,_,m4,c4 = check_implementation(minstar_naive, u, ref_output);
    complexity.append([i, c1-1, m1-1, c2, m2, c3, m3, c4, m4])
  headers = ['Recursive', 
             '1st, 2nd, 1st index', 
             'Cascade', 
             'Separated Evaluation']
  header_text = '|%12s|%s|'% ('Input', '|'.join('%25s' % s for s in headers));
  print '_' * len(header_text);
  hline = ''.join('+' if c == '|' else '-' for c in header_text);
  print header_text;
  print hline;
  print '|%12s|%s' % ('Size', ('%12s|%12s|' % ('Muxes', 'Comparators')) * 4);
  print hline;
  print '|%s|'% ('|\n|'.join('|'.join("%11d " % c for c in row) 
        for row in complexity));
  print hline
  import matplotlib.pyplot as plt;
  import numpy as np;
  ns = np.array(complexity);
  plt.plot(ns[:,0], ns[:,1::2] + ns[:,2::2]);
  plt.ylabel('Muxes + Comparators');
  plt.xlabel("Ones in the row");
  plt.grid(True);
  plt.legend(headers, 'best');
  plt.show();
