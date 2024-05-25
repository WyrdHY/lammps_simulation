import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random 
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

class pair_hunt:
    def __init__(self,filepath):
        self.path = filepath 
        #these two are for loading the simulation coordinates
        self.timestep_data ={}
        self.timesteps = []
        #these two are for sampling the pair correlation inside the box chosen from the chamber
        self.hunting_result = 0#this is a diction, whose key is the key-th sample, and each element is a two-elemen list
                               #the first element is the # of atoms in the box, the second element is a sorted array of the pair distance
        self.hunting_size = 0
        #these two are for the histogram data
        self.hist_stat = 0 #this is a diction, key is the n-th sample
                           #within each key, the first elemetn is hist, the second is bin_edge
        
        self.initialization()

    def initialization(self):
        """Reads data from a LAMMPS trajectory file and organizes it by timestep."""
        with open(self.path, 'r') as file:
            current_timestep = None
            for line in file:
                line = line.strip()
                if 'Timestep:' in line:
                    current_timestep = int(line.split()[-1])
                    self.timestep_data[current_timestep] = []
                elif line.isdigit():
                    continue  # Skip the atom count lines
                else:
                    parts = line.split()
                    if len(parts) == 4:  # Expected format: atom_type x y z
                        atom_type = int(parts[0])
                        x, y, z = map(float, parts[1:])
                        self.timestep_data[current_timestep].append([atom_type, x, y, z])
        
        # Convert lists to pandas DataFrame for easier manipulation
        for timestep, data in self.timestep_data.items():
            self.timestep_data[timestep] = pd.DataFrame(data, columns=['Atom Type', 'x', 'y', 'z'])
        self.timesteps = sorted(self.timestep_data.keys())
        print(f"Initialized Successfully.")
        print(f"initial, final, stepsize: {self.timesteps[0]}, {self.timesteps[-1]}, {self.timesteps[1]-self.timesteps[0]}")
        
    def hunt(self,boxsize,number_of_sample,minimum_prey=0,timestamp=None): #box size, number of samples, time, minimum_atom_number
        #randomly generate the coordinate of the center of the box 
        #as I do not want to touch the edge of the chamber, 
        #I add a safety zone and also manually add 0.1

        if timestamp is None: #the time by defualt is the end of annealing
            timestamp = self.timesteps[-1]

        answer = {}
        flag = 0 
        for i in range(int(10e4)):
            temp_center = self.generate_center(boxsize) 
            number, temp_result = self.pair_distance(temp_center,boxsize,timestamp,minimum_prey) #this is an array
            if temp_result.size == 0: 
                continue 
            
            flag+=1
            answer[flag] = [number,temp_result]
            
            
            if flag >= number_of_sample:
                self.hunting_result = answer
                self.hunting_size = flag
                return answer
    def bin(self,custom_bin = None,to_plot=0):
        if custom_bin==None: 
            custom_bin = np.linspace(0,8,500)
        bin_stat = {}
        for i in range(self.hunting_size):
            temp_hist,temp_edge=np.histogram(self.hunting_result[i+1][1], bins=custom_bin)
            bin_stat[i+1]= [temp_hist,temp_edge]
        self.hist_stat = bin_stat
        

    def generate_center(self,boxsize):
        safe_x = boxsize[0]/2
        safe_y = boxsize[1]/2
        safe_z = boxsize[2]/2
        x_c = random.uniform(safe_x+0.1,12.589462669-safe_x-0.1)
        y_c = random.uniform(safe_y+0.1,12.589462669-safe_y-0.1)
        z_c = random.uniform(safe_z+0.1,13.222095665-safe_z-0.1)
        return [x_c,y_c,z_c]
    
    def pair_distance(self,center,boxsize,timestamp,minimum):
        result = []
        #pick out the one I need to sample
        screenshot = self.timestep_data[timestamp]

        #range for me to choose atom
        xlow,xhigh = center[0] - boxsize[0]/2-0.001, center[0] + boxsize[0]/2+0.001
        ylow,yhigh = center[1] - boxsize[1]/2-0.001, center[1] + boxsize[1]/2+0.001
        zlow,zhigh = center[2] - boxsize[2]/2-0.001, center[2] + boxsize[2]/2+0.001
        
        #filter_x
        filtered_x = screenshot[(screenshot['x'] >= xlow) & (screenshot['x'] <= xhigh)]
        #filtered_y 
        filtered_x_y = filtered_x[(filtered_x['y'] >= ylow) & (filtered_x['y'] <= yhigh)]
        #filtered_z
        filtered_x_y_z = filtered_x_y[(filtered_x_y['z'] >= zlow) & (filtered_x_y['z'] <= zhigh) ]

        if filtered_x_y_z.shape[0]<minimum:
            result = np.array([])
            return 0,result 

        for i in range(filtered_x_y_z.shape[0]):
            for j in range(filtered_x_y_z.shape[0]):
                if i<=j:
                    continue
                v_i = filtered_x_y_z.iloc[i][['x', 'y', 'z']].to_numpy()
                v_j = filtered_x_y_z.iloc[j][['x', 'y', 'z']].to_numpy()
                distance = np.linalg.norm(v_i-v_j)
                result.append(distance)

        #print(f"how many atoms inside your box: {filtered_x_y_z.shape[0]}")
        #print(f"how long is your array: {len(result)}")
        return filtered_x_y_z.shape[0],np.sort(np.array(result))

plt.figure(figsize=(20, 25))

for index in range(20):
    index +=1

    filename = f'C:\\Users\\Eric\\Desktop\\Yb Simulation\\twenty_run\\run{index}\dump.lammpstrj'

    lebron = pair_hunt(filename)
    samplesize = 500
    samples_per_process = (samplesize // size) + (1 if rank < samplesize % size else 0)

    # Each process performs its part of the work
    local_results = lebron.hunt([5, 5, 5], samples_per_process)

    # Gather results at root
    all_results = comm.gather(local_results, root=0)

    if rank == 0:
        # Process and plot results
        lebron.bin()
        hist = np.zeros_like(lebron.hist_stat[1][0])  # Initialize histogram sum

        for i in range(samplesize):
            hist += lebron.hist_stat[i+1][0]

        bin_edges = lebron.hist_stat[1][1]

        # Create subplot in a 4x5 grid
        plt.subplot(4, 5, index)
        plt.bar(bin_edges[:-1], hist / samplesize, width=np.diff(bin_edges), color='blue', edgecolor='none', align='edge')
        plt.title(f'Run{index}')
        plt.xlim([1, 8])
        plt.xlabel("Anstrom")
        plt.ylabel("Sum of the weight")
# Adjust layout to prevent overlap and show the plot
plt.tight_layout()
plt.show()

