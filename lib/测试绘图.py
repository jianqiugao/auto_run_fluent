import matplotlib.pyplot as plt
import numpy as np

time = np.linspace(0,1,100)
x0 = 1.5**time*time - 2*time
x1 = 5**time*time - 2*time
x2 = 3**time*time - 1.5*time
plt.xlabel("time")
plt.ylabel('tem')
plt.plot(time,x0)
plt.plot(time,x1)
plt.plot(time,x2)
plt.legend(['x0','x1','x2'])
plt.show()