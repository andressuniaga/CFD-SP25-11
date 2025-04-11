import numpy as np
import matplotlib.pyplot as plt

processors = np.array([1, 2, 4, 8, 16, 32, 56])  # P
actual_speedup = np.array([1.0, 2.150538, 4.223963, 8.039254, 13.36682, 21.37129, 26.80988])

x = np.linspace(1, 60, 200)   
ideal_speedup = x            # Ideal = y = P
speedup_80   = 0.8 * x       # 80% efficient
speedup_60   = 0.6 * x       # 60% efficient

plt.figure(figsize=(8, 6))

# Plot actual
plt.plot(processors, actual_speedup, 'rs-', label='actual (1 M cells)')
# Plot the theoretical lines
plt.plot(x, ideal_speedup, 'k-',  label='ideal')
plt.plot(x, speedup_80,     'k--', label='80% efficient')
plt.plot(x, speedup_60,     'k-.', label='60% efficient')

plt.xlim(0, 60)
plt.ylim(0, 70)
plt.xlabel('# of processors, P')
plt.ylabel('Speed-up, T(1)/T(P)')
plt.title('Speed-up vs. Number of Processors')
plt.grid(True)
plt.legend(loc='upper left')
plt.show()