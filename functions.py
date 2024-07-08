import pandas as pd
import numpy as np
import random


def increasing(length, first_element=None, extreme:bool=False):
    if first_element is None:
        first_element = random.randint(1, 1000)
    
    list_of_numbers = [first_element]

    if extreme:
        rand_num = 500
    else:
        rand_num = 50
    for _ in range(1, length):
        next_number = list_of_numbers[-1]*(1+random.randint(1, 50)/rand_num)  
        list_of_numbers.append(round(next_number,2))

    return list_of_numbers


def decreasing(length, first_element=None, extreme:bool=False):
    if first_element is None:
        first_element = random.randint(1, 1000)
    
    list_of_numbers = [first_element]

    if extreme:
        rand_num = 500
    else:
        rand_num = 50
        
    for _ in range(1, length):
        next_number = list_of_numbers[-1]/(1+random.randint(1, 50)/rand_num)  
        list_of_numbers.append(round(next_number,2))

    return list_of_numbers


def random_cols(data:pd.DataFrame, rows, length_col):
    for row in rows:
        data.loc[row] = np.random.rand(length_col) * 1000
    return data


def summarize_row(data:pd.DataFrame, sum_dict:dict):
    for key, value in sum_dict.items():
        data.loc[key] = data.loc[value].sum()
    
    return data


def create_dataframe(columns, rows, sum_dict:dict=None, params:dict=None, first_element:int=1000):
    data = pd.DataFrame(index=rows, columns=columns)

    data = random_cols(data, rows, len(columns))
    if params["extreme_increasing"]:
        for item in params["extreme_increasing"]:
            data.loc[item] = increasing(len(columns), extreme=True)
    
    if params["extreme_decreasing"]:
        for item in params["extreme_decreasing"]:
            data.loc[item] = decreasing(len(columns), extreme=True)

    if params["increasing"]:
        for item in params["increasing"]:
            data.loc[item] = increasing(len(columns), extreme=False)

    if params["decreasing"]:
        for item in params["decreasing"]:
            data.loc[item] = decreasing(len(columns), extreme=False)

    data = summarize_row(data, sum_dict)
    data = data.apply(pd.to_numeric, errors='coerce')
    data = data.round(2)


    columns_to_sum = data.filter(like='2024').columns
    data['This Year'] = data[columns_to_sum].sum(axis=1)

    columns_to_sum = data.filter(like='2024').columns
    data['Monthly Changes'] = data[columns[-1]] - data[columns[-2]] 
    data['This Year'] = data[columns_to_sum].sum(axis=1)
    data['Last Year'] = data['2023 December']*12*random.randint(0, 3)
    return data
    
    