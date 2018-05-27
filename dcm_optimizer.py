import pandas as pd
import pulp

def create_constraint_matrix(x):

    if x == 'Theatre Cleaning' or x == 'Closed: Check @DCM_Lines for Venue Options' or pd.isnull(x):
        return 0
    else:
        return 1

def compute_going(x):
    if x == 'Theatre Cleaning' or x == 'Closed: Check @DCM_Lines for Venue Options' or pd.isnull(x):
        return (0,0)
    else:
        return (x,vars[x].varValue)


df = pd.read_excel('dcm_schedule.xlsx',index_col='Time')
df = df.iloc[9:]
weight_matrix = df.applymap(create_constraint_matrix)

dcm_lpp = pulp.LpProblem("dcm_lpp",pulp.LpMaximize)

variables = set(df.values.flatten())
variables.pop()

vars = pulp.LpVariable.dicts("value",(i for i in variables),lowBound=0,upBound=1,cat=pulp.LpInteger)

dcm_lpp += (pulp.lpSum([vars[i] for i in vars.keys()]))

# Only computing for a subset of shows while TBD shows remain on the calendar.
for row in range(len(df)-200):
    dcm_lpp += (pulp.lpSum(vars[i] for i in list(df.ix[row]) if type(i) is str and i != 'Theatre Cleaning' and i != 'Closed: Check @DCM_Lines for Venue Options')) == 1

dcm_lpp.solve()
going_df = df.applymap(compute_going)

going_df.to_excel('optimal_dcm.xlsx',index_label="Time")