#!/usr/bin/env python
# coding: utf-8

# In[60]:


import pandas as pd
import numpy as np


# In[3]:


##
#This file aims to read the dump.lummps data to load the 
#positions of different atoms at different t
#at each time t, i can have a table telling me the 3D location of each atom
##
#After that, I will calculate the distance correlation defined as
#for x= Si, y=O
#for x= Si, y = Si
#for x= O, y = O


# $$
# \sum_i \sum_j x_i y_j
# $$
# 

# In[5]:


#Current position data are obtained using an absolute reference frame
#instead of a relateive body frame


# #This is simply importing all of the 
# #infomation as a table, same as 
# #the one you see when you open the .lammpstr file
# def read_lammps_data(filename):
#     data = []  # to store the data temporarily
#     current_timestep = None
#     
#     with open(filename, 'r') as file:
#         for line in file:
#             line = line.strip()
#             if 'Timestep:' in line:
#                 current_timestep = int(line.split()[-1])  # extract timestep
#             elif line.isdigit():
#                 continue  # this is just the number of atoms, skip it
#             else:
#                 parts = line.split()
#                 if len(parts) == 4:  # make sure it's the right format
#                     atom_type = int(parts[0])
#                     x, y, z = map(float, parts[1:])
#                     data.append([current_timestep, atom_type, x, y, z])
#     
#     # Create a DataFrame
#     columns = ['Timestep', 'Atom Type', 'x', 'y', 'z']
#     df = pd.DataFrame(data, columns=columns)
#     return df

# #The data I will read
# filename = r'C:\Users\Eric\Desktop\Yb Simulation\Zihagn_good_tool\Classical_MD_coord_visual\dump.lammpstrj'
# df = read_lammps_data(filename)
# print(df.head())  # show the first few rows

# In[66]:


#This uses diction to store the data
#at each time, there is a table describing the 
#3D location of each atom
def read_lammps_data_partitioned(filename):
    timestep_data = {}  # Dictionary to store data by timestep
    current_timestep = None
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if 'Timestep:' in line:
                current_timestep = int(line.split()[-1])  # extract timestep
                timestep_data[current_timestep] = []  # Initialize an empty list for this timestep
            elif line.isdigit():
                continue  # this is just the number of atoms, skip it
            else:
                parts = line.split()
                if len(parts) == 4:  # make sure it's the right format
                    atom_type = int(parts[0])
                    x, y, z = map(float, parts[1:])
                    timestep_data[current_timestep].append([atom_type, x, y, z])
    
    # Convert lists to DataFrames
    for timestep, data in timestep_data.items():
        columns = ['Atom Type', 'x', 'y', 'z']
        timestep_data[timestep] = pd.DataFrame(data, columns=columns)
    
    return timestep_data


# In[67]:


#The data I will read
filename = r'C:\Users\Eric\Desktop\Yb Simulation\Zihagn_good_tool\Classical_MD_coord_visual\dump.lammpstrj'
df = read_lammps_data(filename)
print(df.head())  # show the first few rows


# In[68]:


#This is to read the data as dictionary
filename = r'C:\Users\Eric\Desktop\Yb Simulation\Zihagn_good_tool\Classical_MD_coord_visual\dump.lammpstrj'
timestep_tables = read_lammps_data_partitioned(filename)


# In[43]:


timestep_tables[3000]


# In[96]:


class correlate:
    def __init__(self,dick):
        self.diction = dick
        keys_list = list(self.diction.keys())
        stepsize = np.abs(keys_list[0]-keys_list[1])
        print(f"Initialized successfully. Use x.run(atom, atom, time) to get correlation.\n"
      f"atom = 1 means Si. atom = 0 means O.\n"
      f"Available time steps range from: {keys_list[0]} to {keys_list[-1]}, stepsize: {stepsize}")

    def run(self,fucker1,fucker2,time):
        #fucker means the type of atoms
        # 1 means Si
        # 2 means o
        hibertsapce = self.diction[time]
        fuckerspace1 = hibertsapce[hibertsapce['Atom Type'] == fucker1]
        fuckerspace2 = hibertsapce[hibertsapce['Atom Type'] == fucker2]
        result = 0 
        #calculate the sum: Sum_{i,j} x_i * x_j
        for i in range(fuckerspace1.shape[0]):
            for j in range(fuckerspace2.shape[0]):
                v_i = fuckerspace1.iloc[i][['x', 'y', 'z']].to_numpy()
                v_j = fuckerspace2.iloc[j][['x', 'y', 'z']].to_numpy()
                result += np.dot(v_i, v_j)
        return result
                
        


# In[97]:


test = correlate(timestep_tables)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




