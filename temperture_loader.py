import pandas as pd
import matplotlib.pyplot as plt
i=9
filepath = f'C:\\Users\\Eric\\Desktop\\Yb Simulation\\twenty_run\\run{i}\\temperature.dat'
df = pd.read_csv(filepath, delim_whitespace=True, skiprows=2, names=['TimeStep', 'v_atemp'])
time = df['TimeStep']
temperature = df['v_atemp']
plt.figure(dpi=200)
plt.plot(df['TimeStep'], df['v_atemp'], marker='o', linestyle='-', color='b',markersize=0.3)  
plt.title(filepath)  
plt.xlabel('TimeStep') 
plt.ylabel('Temperature')  

plt.show()  
print(df)