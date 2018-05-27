import pandas as pd
from scipy.optimize import linprog
from datetime import date,time
import numpy as np

def create_constraint_matrix(x):

    if x == 'Theatre Cleaning' or x == 'Closed: Check @DCM_Lines for Venue Options' or pd.isnull(x):
        return 0
    else:
        return 1


df = pd.read_excel('dcm_schedule.xlsx',index_col='Time')

constraint_matrix_pre = df.applymap(create_constraint_matrix)

num_data_points = len(df)
constraint_vector = []
row_vec = []
counter = 0

for i in range(num_data_points):
    for j in range(num_data_points*11):
        if j in range(i*11,i*11+11):
            row_vec.append(constraint_matrix_pre.values[i][counter])
            counter+=1
        else:
            row_vec.append(0)

    constraint_vector.append(row_vec)
    row_vec = []
    counter = 0

variable_req = np.identity(num_data_points*11)*-1
variable_req_2 = np.identity(num_data_points*11)
a_ub = np.concatenate((variable_req, variable_req_2))
# constraint_matrix.to_excel('constraint_matrix.xlsx')
eq_constraint_vec = [1]*len(constraint_matrix_pre)
objective_func_vec = [-1]*(len(constraint_vector[0]))
ub_constraint_vec = [0]*len(constraint_vector[0])
ub_constraint_vec_2 = [1]*len(constraint_vector[0])

b_ub = np.concatenate((ub_constraint_vec, ub_constraint_vec_2))

final_solution = linprog(objective_func_vec,A_eq=constraint_vector,b_eq=eq_constraint_vec,A_ub=a_ub,b_ub=b_ub)
print(final_solution.x)