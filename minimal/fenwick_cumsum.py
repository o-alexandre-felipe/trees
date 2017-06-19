

def BIT(s = ' 0123456789abcdefghijklmnopqrstuv'):
"""
  This function calculate cumulative sums over the semigroup of the 
  strings with concatenation as the binary operation, using the 
  Fenwick Tree [1]. This serves as reference for RTL implementation
  as well as a guide for verification, it may be used to produce
  a list of assertions in order to formally verify one implementation.
  
  
  1. Peter M. Fenwick (1994). 
     "A new data structure for cumulative frequency tables"
"""
  w = [''] * (len(s) + 1);
  y = [''] * (len(s) + 1);
  n = len(s);
  for i in xrange(1, n):
    p = (i | (i-1)) + 1;
    r = (i & (i-1)); 
    if p == i:
      w[i] = s[i];
    else:
      w[i] = w[i] + s[i];
    if p < n:
      if p == 2*i-1:
        w[p] = w[i];
      else:
        w[p] = w[p] + w[i];
    if r > 0:
      y[i] = y[r] + w[i];
    else:
      y[i] = w[i];
  
  for wi in w:
    print wi;
  z = '';
  for i in xrange(1, n):
    z += s[i];
    print z;
    assert y[i] == z;


if __name__ == '__main__':
  BIT();

