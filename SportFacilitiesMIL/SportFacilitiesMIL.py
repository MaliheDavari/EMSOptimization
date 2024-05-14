from gurobipy import *

#sets and data

facility=['s','t','a','g']              #a swimming pool, a tennis center, an athletic field, and a gymnasium
# data for each facility (number of people per day, instalation cost, required land area)
facilityData={'s':{'People': 300 ,'Cost':35,'Land':4},
              't':{'People':90,'Cost':10,'Land':2},
              'a':{'People':400,'Cost':25,'Land':7},
              'g':{'People':150,'Cost':90,'Land':3}}
budget=120
AvailableLand=12

########################################################################################################################
# Create model
m=Model('ExcerciseFacilities')

# Variables
SwimmingPool=m.addVar(vtype=GRB.BINARY,name='SwimmingPoo')
TennisCenter=m.addVar(vtype=GRB.BINARY, name='TennisCenter')
AthelicField=m.addVar(vtype=GRB.BINARY, name='AthelicField')
Gymnasium=m.addVar(vtype=GRB.BINARY, name='Gymnasium')
PeopleNumber=m.addVar(vtype=GRB.CONTINUOUS, name='PeopleNumber')
LandArea=m.addVar(vtype=GRB.CONTINUOUS, name='LandArea')
Cost=m.addVar(vtype=GRB.CONTINUOUS, name='Cost')
my_variables=[SwimmingPool,TennisCenter,AthelicField,Gymnasium]
# Constraints

People_const = m.addConstr(PeopleNumber == quicksum(facilityData[facility[i]]['People']* my_variables[i] for i in
                                                     range(len(facility))), name='People_const')
Land_const = m.addConstr(LandArea == quicksum(facilityData[facility[i]]['Land']* my_variables[i] for i in
                                               range(len(facility))), name='Land_const')
Cost_const = m.addConstr(Cost == quicksum(facilityData[facility[i]]['Cost']* my_variables[i] for i in
                                           range(len(facility))), name='Cost_const')
Cost_limit_const = m.addConstr(Cost <= budget, name='Cost_limit_const')
Land_limit_const = m.addConstr(LandArea <= AvailableLand, name='Land_limit_const')
tenis_swimming_const = m.addConstr(SwimmingPool + TennisCenter <= 1, name='tenis_swimming_const')

########################################################################################################################

# Objective
m.setObjective(PeopleNumber,GRB.MAXIMIZE)
#Solve
m.optimize()

#Results
# FacilitiesResult=[[[SwimmingPool].x,'Swimming Pool'],[[TennisCenter].x,'Tennis Center'],[[AthelicField].x,'Athelic Field'],
#                   [Gymnasium.x,'Gymnasium']]
# for i in range(len(FacilitiesResult)):
#     if FacilitiesResult[i][0]==1:
#         print (FacilitiesResult[i][1])


