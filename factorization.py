import math
def split(x):
  k = math.floor(math.sqrt(x))
  while float(x)/k != math.floor(float(x)/k):
      k = k+1
      print(k)
  print(k,x/k)

split(12288)
