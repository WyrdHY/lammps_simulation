#this script is used to generated
# 100 begin_i.in file
# and then they will be executed in linux 
# each of the bgin_i_seed should be formatted as i as the i-th run, and seed as the random number
# I need to first prepare 100 different seed

import numpy as np
import os


#generate the 100 seeds for once and then load it for future use 

#seeds = np.random.choice(range(10000, 60001), 100, replace=False)
#filepath = r"C:\Users\Eric\Desktop\Yb Simulation\100_direct_cool\init\seeds.npy"
#np.save(filepath, seeds)
#print(seeds)

filepath = r"C:\Users\Eric\Desktop\Yb Simulation\100_direct_cool\init\seeds.npy"
seeds = np.load(filepath)
print(seeds)

base_directory = r'C:\Users\Eric\Desktop\Yb Simulation\100_direct_cool\simulation_data'
for i in range(100):
    folder_name = f"run_{i+1}"
    folder_path = os.path.join(base_directory, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    lammps_content = f"""
    units metal
boundary p p p
atom_style full
pair_style tersoff 
neighbor 2.0 bin
neigh_modify delay 1

 


read_data /root/Desktop/host/100_direct_cool/init/SiO.data
replicate 1 1 1

pair_coeff * *  /root/Desktop/host/job1/SiO.tersoff Si O  



group Si type 1 
group O type 2
#create_bonds many SiO SiO 1 0.5 10

dump dmp all xyz 2000 dump.lammpstrj
 


variable apot equal pe
# first number: number of steps to get current temp
# second number: calculate average n number of temp read above.
# third number: temp record (this must be larger than the one above )

variable atemp equal temp
fix temp_info all ave/time 10 200 2000 v_atemp file parameters/temperature.dat

#The cutoff used for pairwise computation (any pair style) and the
#associated neighbor list is the maximum cutoff that any compute
#can use. Atoms don't know any info about their neighbors
#further away than that.

# compute coord number
compute coor12 Si coord/atom cutoff 2.5 group O
compute coor11 Si coord/atom cutoff 2.5 group Si
compute coor22 O coord/atom cutoff 2.0 group O

compute sumcoor12 all reduce ave c_coor12
compute sumcoor11 all reduce ave c_coor11
compute sumcoor22 all reduce ave c_coor22


fix 12coord all ave/time  10 200 2000 c_sumcoor12 file parameters/Si-O_coord_number.dat  
fix 11coord all ave/time  10 200 2000  c_sumcoor11 file parameters/Si-Si_coord_number.dat  
fix 22coord all ave/time  10 200 2000  c_sumcoor22 file parameters/O-O_coord_number.dat  




# unit cell information
variable avol equal vol
variable alx equal lx
variable aly equal ly
variable alz equal lz
fix cell_info all ave/time 10 200 2000 v_avol v_alx v_aly v_alz file parameters/cell_volume.dat


fix potential_info all ave/time 10 200 2000 v_apot file parameters/potential-energy.dat
thermo 1000



velocity all create 6000 {seeds[i]} mom yes rot no dist gaussian
fix npt1 all npt temp 6000 10 0.1 iso 0 0  1
timestep 0.001

run 100000 #fuck 10W times


write_data parameters/amorphousSiO.data  


    """
    with open(os.path.join(folder_path, f"cool_{i+1}.in"), "w") as file:
        file.write(lammps_content)
    parameters_folder = os.path.join(folder_path, "parameters")
    os.makedirs(parameters_folder, exist_ok=True)
    parameters_folder = os.path.join(folder_path, f"seed_{seeds[i]}")
    os.makedirs(parameters_folder, exist_ok=True)