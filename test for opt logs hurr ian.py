# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 16:03:09 2022

@author: xiw
"""

import pandas as pd
import os
# import xlrd

# Setting working directory
os.chdir(r'C:\Users\xiw\Desktop')
os.getcwd()

df_line_up = pd.read_excel('test oct4.xlsx', sheet_name = 'Daily Line-Up')

# for col in df_line_up.columns:
    # print(col)


# In the Daily Line Up tab
end_row = df_line_up[df_line_up['ROUTE']=='PM / DOWN >'].index.values # find the index of 'PM / DOWN >', use it to indicate the last row of record

list_bus_scheduled = df_line_up['BUS #'].tolist() # list of buses scheduled
list_bus_scheduled = list_bus_scheduled[:int(end_row)] # use the end row index to cut off the rest of the list
list_bus_scheduled = [str(item) for item in list_bus_scheduled] # convert number and text elements to text
list_bus_scheduled = [x.strip(' ') for x in list_bus_scheduled] # delete accidental blank entries
list_bus_scheduled = [x for x in list_bus_scheduled if x != 'nan'] # remove nan in the list

# list_bus_scheduled_type = [type(item) for item in list_bus_scheduled]
# print(list_bus_scheduled_type)


# Define a function to only extract fixed route bus number
def first_digit_bus(fixed_route):
    if int(str(fixed_route)[0]) == 4:
        return fixed_route
    if int(str(fixed_route)[0]) == 5:
        return fixed_route
    if int(str(fixed_route)[0]) == 9:
        return fixed_route

fixed_route = [first_digit_bus(num) for num in list_bus_scheduled]

list_bus_scheduled = fixed_route

# Constrain element format into 3-digit bus number format, such as remove time format
list_bus_scheduled_selected_elements = []
for i in range(len(list_bus_scheduled)):
    if len(str(list_bus_scheduled[i])) == 3:
        list_bus_scheduled_selected_elements.append(list_bus_scheduled[i])
list_bus_scheduled = list_bus_scheduled_selected_elements
# len(list_bus_scheduled)

# df_line_up = df_line_up[ (df_line_up['Replaced With Bus #'] == 'FIXED') or (df_line_up['Replaced With Bus #'][0].isdigit())



# drop trailing zero from string
listOfNum = [1.0, 235, 541.0, 560]
listOfNum = [str(item) for item in listOfNum]
listOfNum
list_test = [i.strip('.0') for i in listOfNum]
list_test

