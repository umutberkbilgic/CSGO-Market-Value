import matplotlib.pyplot as plt
import numpy as np

with open('report.txt', 'r') as file :
  data = str(file.read())

data = data.split('Page sum: $')

for i in range(1, len(data)):
  data[i] = float(data[i][:data[i].find('\n')])

  print(data[i])

x1 = [x for x in range(0, 160) if x % 5 == 0]
y1 = [y for y in range(0, 300000) if y % 50000]

plt.plot(data[1:], 'o-')
plt.ylabel('lowest listing price * quantity ($)')
plt.xlabel('Page (100 items per page, 152 pages)')
plt.title('Cumulative price*quantity graph of every batch of 100 items')
plt.xticks(x1)
plt.xticks(rotation=45)
plt.yticks(y1)
plt.grid()
plt.show()