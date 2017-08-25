import numpy as np
import matplotlib.pyplot as plt
import math

x = range(10)
a = []
for item in x:
  	a.append(1/(1+math.exp(-item)))


plt.plot(x,a)
plt.show()

	 
    
