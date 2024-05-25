import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

for i in range(20):
    file_path = f'C:\\Users\\Eric\\Desktop\\Yb Simulation\\twenty_run\\run{i+1}\\dump.lammpstrj' ####################
    file_path_coord=r'C:\Users\Eric\Desktop\Yb Simulation\Zihagn_good_tool\Classical_MD_coord_visual\cart_coordinates.txt' ####################
    file_path_temp=f'C:\\Users\\Eric\Desktop\\Yb Simulation\\twenty_run\\run{i+1}\\temperature.dat' ####################


    classical_name_list=['Si','O'] # the coord number represents the type in the classical MD
    init_name_arry= np.loadtxt(file_path_coord,dtype='str' )[:,0]
    init_coord_arry=np.genfromtxt(file_path_coord )[:,1:4]
    data_size=len(init_name_arry)
    data_size=96
    temp_array=np.genfromtxt(file_path_temp )[:,1].tolist()

    x_max, y_max, z_max = 12.589462669, 12.589462669, 13.222095665
    unit_step_structure_size = 96

    def read_atom_num(line):
        try: 
            parts = line.split()
            if int(parts[0])==data_size:
                return True
                
        except:
            return False
    def read_time(line,time_array):
        if 'Timestep' in line and 'Atoms' in line:
            # Split the line by spaces and extract the numerical part
            parts = line.split()
            for part in parts:
                try:
                    # Try to convert the part to a float
                    time_value = float(part)

                    time_array.append(time_value)
                    
                    break  # Stop searching after finding the numerical value
                except ValueError:
                    pass  # Ignore non-numeric parts
        return time_array
    def atomic_position(line):
        S=line.strip() 
        return S
    time_array=[]
    total_atom_coord_arry=np.zeros(3) # changed to target sorted 
    total_atom_name_arry = np.array(['start'])  # changed to target sorted 
    atom_name_arry=[]
    atom_coord_arry=[]
    global_count=0
    with open(file_path, 'r') as file:
        counter=0
        for line in file:
            bool_head=read_atom_num(line)
            #print(bool_head)
            if bool_head:
                counter=1
                #print('SSS')

            elif counter==1:
                time_array=read_time(line,time_array)
                counter=2
                atom_name_arry=[]
                atom_coord_arry=[]
                
                
            elif counter<data_size+1:
                parts = line.split()
                #print(counter)
                #print(parts)
                #print(parts[0])
                atom_name = classical_name_list[int(parts[0])-1]  # First part is the atom
                # print(int(parts[0]))
                coordinates = np.array([float(coord) for coord in parts[1:]]) 
                
                atom_coord_arry.append(coordinates)
                atom_name_arry.append(atom_name)
                
                counter+=1
            

            elif counter==data_size+1:
                counter=0
                #print(atom_coord_arry)
                #print(np.array(atom_name_arry))
                
                total_atom_name_arry=np.hstack([total_atom_name_arry,np.array(atom_name_arry)])
                #print(total_atom_name_arry)
                total_atom_coord_arry=np.vstack([total_atom_coord_arry,np.array(atom_coord_arry)])
                #print(total_atom_coord_arry)
            global_count+=1

    #####
    #Above code produces these two arrays
    #total_atom_coord_arry 
    #total_atom_name_arry

    time_length=int(len(total_atom_coord_arry)/unit_step_structure_size)


    # Assuming you want to plot the structure at the first time step
    current_structure_coord = total_atom_coord_arry[(time_length-1)*96:time_length*96]
    labels = total_atom_name_arry[(time_length-1)*96:time_length*96]

    # Setup figure and 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Color map and label settings
    label_color_map = {'Si': 'blue', 'O': 'red', 'Yb': 'green'}
    unique_labels = np.unique(labels)

    # Plot each type of atom with a different color
    for label in unique_labels:
        label_mask = labels == label
        ax.scatter(
            current_structure_coord[:, 0][label_mask],
            current_structure_coord[:, 1][label_mask],
            current_structure_coord[:, 2][label_mask],
            color=label_color_map[label],
            label=label,
            s=10  # Size of the points
        )

    # Setting the limits of the plot
    ax.set_xlim(0, x_max)
    ax.set_ylim(0, y_max)
    ax.set_zlim(0, z_max)

    # Labeling the axes
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Y coordinate')
    ax.set_zlabel('Z coordinate')
    ax.set_title(f'run{i+1}')

    # Adding a legend to differentiate atom types
    ax.legend()

    # Show plot
    plt.show()


