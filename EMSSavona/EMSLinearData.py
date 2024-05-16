from gurobipy import *
import numpy as np


# Define Sets
T=list(range(1,96))             # 95 time intervals, each 15 minutes
SN=list(range(1,12))            # supply nodes in supply network
RN=list(range(1,12))            # return nodes in return network
B=list(range(1,7))              # Buildings in DHN
pipes=list(range(1,21))         # all of the pipes in DHN
NodeType=['p','s']                  # predecessor and successor pipes of nodes
N=list(range(1,17))
# connection between nodes and their predecessor and successor pipes
NodePipes= {
    1: {'p': [], 's': [1]},
    2: {'p': [1], 's': [2, 5]},
    3: {'p': [2], 's': [3, 6, 7]},
    4: {'p': [3], 's': [4, 8]},
    5: {'p': [4], 's': [9, 10]},
    6: {'p': [5], 's': [11]},
    7: {'p': [6], 's': [12]},
    8: {'p': [7], 's': [13]},
    9: {'p': [8], 's': [14]},
    10: {'p': [9], 's': [15]},
    11: {'p': [10], 's': [16]},
    12: {'p': [15, 16], 's': [17]},
    13: {'p': [14, 17], 's': [18]},
    14: {'p': [12, 13, 18], 's': [19]},
    15: {'p': [11, 19], 's': [20]},
    16: {'p': [20], 's': []}
}

# Data (constants)
C_H2O= 4.186                       #specific heat of the water [kj/kg K]
# campus pipe thermal resistance data (k/kW) for average 40 meter for pipe length
R_p = {i: (2.3 * 1000 / 40) for i in range(1, 21)}

T_g = 4                             # ground temperature
eff_b = 0.92                        # efficiency of the heat exchanger in building
# the internal volume of the buildings
V_build = {
    1: 20817,
    2: 9328.32,
    3: 9328.32,
    4: 5684.1,
    5: 11808,
    6: 11808
}

N_dot = 1.1 / 3600                  # The average air changes per hour 1.1 [1/s]

air_density = 1.293                 # The density of air [kg/m^3]
C_air_build = 700 / 1000            # The heat capacity of air at constant pressure [kJ/(kg.K)]

# The external air temperature
T_ext = {
    i + 1: temp for i, temp in enumerate(
        [6.30, 5.90, 5.90, 5.90, 5.80, 6.00, 6.00, 5.60, 5.60, 5.60, 
         5.80, 5.70, 5.50, 5.60, 5.50, 5.50, 5.40, 5.40, 5.00, 5.20, 
         5.20, 5.30, 5.60, 6.10, 6.60, 6.90, 7.20, 7.10, 6.70, 6.10, 
         6.30, 6.80, 7.10, 7.00, 7.20, 7.50, 9.00, 11.20, 14.60, 14.10, 
         11.30, 10.80, 10.80, 11.10, 11.30, 11.60, 11.70, 11.90, 11.90, 
         11.90, 12.00, 12.00, 12.10, 12.10, 12.10, 12.10, 12.20, 12.00, 
         11.80, 11.60, 11.30, 10.80, 10.10, 9.70, 9.20, 8.80, 8.40, 
         8.20, 7.90, 7.70, 7.40, 7.50, 7.70, 7.80, 7.80, 7.40, 7.30, 
         7.60, 7.50, 7.30, 6.90, 6.80, 6.50, 6.30, 6.40, 6.50, 6.50, 
         6.70, 6.80, 6.70, 6.30, 6.30, 7.40, 7.10, 7.70])}

# Renewable power production in kW (PV)
P_RES = {
    i + 1: power for i, power in enumerate(
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 
         20, 23, 25, 28, 30, 31, 34, 35, 36, 36, 38, 40, 41, 42, 40, 
         40, 40, 38, 36, 34, 33, 31, 28, 23, 21, 15, 8, 0, 0, 0, 0, 
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
         0, 0, 0, 0, 0, 0, 0, 0])}

U_walls_build=0.32/1000                 #[(kW/m2K)] website
#Area of walls [m^2]
A_walls_build = {
    1: 2448.5418,
    2: 1172.439,
    3: 1172.439,
    4: 900.0576,
    5: 1484.1,
    6: 1484.1}

U_win_build=2/1000    #[(kW/m2K)] website
#Area of windows [m^2]
A_win_build = {
    1: 272.0602,
    2: 130.271,
    3: 130.271,
    4: 100,
    5: 164.9,
    6: 164.9}
Beta=0.9                           #
sol_trans=0.634                    # The fraction of solar transmitted (prof Priarone paper)
sol_abs=0.2                        # The fraction of solar radiation absorbed by the surface
h_ext=1/1000                       #The outdoor convection coefficient [kW/ (m^2.K)]

G_tot={}
for t in T:
    if P_RES[t]>0:
        G_tot[t]=0.08
    else:
        G_tot[t]=0

U_roof_build=0.27/1000              #[(KW/m2K)] website

# roof area of buildings
A_roof_build = {
    1: 2635.121,
    2: 1180.8,
    3: 1180.8,
    4: 962.51,
    5: 1180.8,
    6: 1180.8}

T_build_0 = 19                      # the initial building temperature
delta = 0.25                        # the time interval 15 min
C_ext_mass_build = 0.84             # edit [KJ/(kg.K)]
wall_tick = 0.56                    # [m]
density_wall = 1200                 # [kg/m3]
mass_ext_mass_build = [density_wall * wall_tick * A_walls_build[i] for i in B]  # edit [kg]
T_build_min = 18                    # The min internal temperature [K]
T_build_max = 24                    # The max internal temperature [K]
T_fill = 25                         # the filling flow temperature[K]


#the ideal internal temperature [C]
T_idl_build = {
    i + 1: temp for i, temp in enumerate(
        [19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 20, 20, 20, 20, 20, 20, 20, 20, 
         20, 20, 20, 20, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 
         21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 
         21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 20, 20, 20, 20, 20, 20, 20, 
         20, 20, 20, 20, 20, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19])}

# SEB data
V_SEB = 3627                        # correct data [m^3]
U_walls_SEB = 0.095 / 1000          # correct data: overall transmittance of Ventilated facade
A_walls_SEB = 858                   # Area of walls [m^2]
U_win_SEB = 1.4 / 1000              # correct data: overall transmittance of windows [KW/m2K]
A_win_SEB = 157                     # Area of windows [m^2]
U_roof_SEB = 0.191 / 1000           # [KW/m2K]
A_roof_SEB = 506
T_SEB_0 = T_build_0                 # the initial building temperature
C_ext_mass_SEB = 0.85               # I've assumed the building's external walls are concrete [KJ/(kg.K)]
density_wall_SEB = 140              # kg/m3
wall_tick_SEB = 0.55
mass_ext_mass_SEB = density_wall_SEB * wall_tick_SEB * A_walls_SEB  # the mass of external walls [kg]
T_SEB_min = 18                      # The min internal temperature [K]
T_SEB_max = 27                      # The max internal temperature [K]
COP_GHP = 4.4
COP_AHU = 5.8                       # edit with the real number
C_air_SEB = 700 / 1000              # The heat capacity of air at constant pressure [kJ/(kg.K)]

#source node
Q_GB_max=2*450                      #kW
Q_MT_max=112                        #kW
eff_MT_el=0.29
eff_MT_th=0.5
eff_boiler=0.85                    # I assumed 85% efficiency for boiler- I could not find the exact amount
T_source_in_min=60
T_source_in_max=90
T_network_min=50


P_el ={
    i+1: load for i, load in enumerate (
        [101.533641600000, 100.638230700000, 96.4305766900000, 89.2338954800000, 
         91.7989978200000, 87.5878185000000, 102.394659800000, 88.2697917300000, 
         87.2955386200000, 102.497758800000, 103.599918100000, 100.508542800000, 
         100.516506700000, 101.167656300000, 105.204356000000, 95.8153732300000, 
         92.3108805300000, 101.591723300000, 95.8470850000000, 96.7494124100000, 
         94.5773545600000, 94.5615068400000, 93.5222457900000, 89.9633766700000, 
         92.2908040400000, 101.678418500000, 94.3102572100000, 102.192028600000, 
         116.567579400000, 120.138802800000, 120.586695400000, 115.165207700000, 
         101.372492500000, 121.793880500000, 128.400306700000, 148.522096500000, 
         156.383351000000, 159.361512000000, 173.736467100000, 185.986400800000, 
         192.549654000000, 192.145901300000, 191.245965700000, 182.422197000000, 
         181.510819600000, 197.154790500000, 190.910094200000, 207.061481700000, 
         206.138461200000, 195.711329300000, 202.916048100000, 192.109665800000, 
         186.558315300000, 187.817036300000, 182.689772000000, 176.029039500000, 
         174.270232600000, 166.892686300000, 170.317699800000, 159.815460800000, 
         157.370502500000, 154.141092700000, 139.371390600000, 136.973314300000, 
         128.568023600000, 134.030719100000, 129.818099100000, 127.780599200000, 
         124.543909000000, 121.854240200000, 125.391414100000, 131.588761300000, 
         117.814662800000, 110.431497900000, 104.448310600000, 101.931775200000, 
         117.865646400000, 108.456793600000, 98.6867225200000, 102.490629100000, 
         115.819101700000, 108.505739700000, 110.963530900000, 109.841397100000, 
         109.830357700000, 106.229952400000, 107.529909100000, 102.363573200000, 
         99.3140783900000, 103.450976100000, 95.3500443600000, 93.7988789200000, 
         97.9335478500000, 90.5191924100000, 93.7919988600000])}

#per_unit_prices
per_unit_price_MT=0.1060;                           #euro/kWh
per_unit_price_GB=0.0853;                           #euro/kWh
per_unit_price_grid_sell = [0.08] * len(T)          #euro/kWh
per_unit_price_grid_buy = [0.3] * len(T)            #euro/kWh

# storage
CAP_s=141;                                          #capacity of storage
W_s_min=0.1;                                        #min state of the storage
W_s_max=0.9;                                        #max state of the storage
eff_s_ch=0.95;                                      #storage charging efficiency
eff_s_disch=1.05;                                   #storage discharging efficiency
P_s_max=36;                                         #max power that storage can charge or release

# Nodes mass
m_n_in = {
    1: 26.5,
    2: 26.5,
    3: 18.5,
    4: 10.5,
    5: 8,
    6: 8,
    7: 4,
    8: 4,
    9: 2.5,
    10: 4,
    11: 4,
    12: 8,
    13: 10.5,
    14: 18.5,
    15: 26.5,
    16: 26.5}
m_n_out=m_n_in
# Nodes mass
m_p_in = {
    1: 26.5,
    2: 18.5,
    3: 10.5,
    4: 8,
    5: 8,
    6: 4,
    7: 4,
    8: 2.5,
    9: 4,
    10: 4,
    11: 8,
    12: 4,
    13: 4,
    14: 2.5,
    15: 4,
    16: 4,
    17: 8,
    18: 10.5,
    19: 18.5,
    20: 26.5}
m_p_out=m_p_in                      # there is no loss in pipes
SHGC_tot_build=sol_trans+sol_abs*U_win_build/h_ext
# the wondows solar heat gain [kW]
Q_win_sol_build = {}
for t in T:
    Q_win_sol_build[t] = {}
    for b in B:
        Q_win_sol_build[t][b] = Beta * A_win_build[b] * G_tot[t]

# temperature of air considering irradiation
T_sol_air={}
for t in T:
    T_sol_air[t]=T_ext[t]+G_tot[t]*sol_abs/h_ext

#Solar heat gain coefficient of the building
SHGC_tot_SEB=0.701                  # data from campus building
Q_win_sol_SEB={}
for t in T:
    Q_win_sol_SEB[t]=Beta*A_win_SEB*SHGC_tot_SEB*G_tot[t]

