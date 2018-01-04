# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 12:44:45 2017

@author: croberts
"""

# -*- coding: utf-8 -*-

# Read in csv of RS school list and create pandas dataframe
# Read in csv list of OSPI list and create pandas dataframe

# For each school on our list 
#   Find all of the schools in the same city
#   Compare words of each school name
#       Not including school words if 0 escape
#       Including school words, find closest match
#       Add the OSPI school name and the OSPI school code to the copy

import pandas as pd
import numpy as np


def clean_title(text):
    """
    Takes a pandas series of strings, and returns a pandas series of strings
    that have been stripped and each word capitalized
    """
    text = text.str.lower()
    text = text.str.title()
    text = text.str.strip()
    return text


def string_truncate(strings_to_truncate, words_to_remove, truncated_list_name):
    """
    Takes a list of strings to modify, a list of words to remove from the first list,
    and an empty list that will be populated with with the new truncated strings.
    """
    truncated_list_name = []
    for string in strings_to_truncate:
        modifying_string = string
        for word in words_to_remove:
            modifying_string = modifying_string.replace(word, "")
            modifying_string = modifying_string.strip()
        truncated_list_name.append(modifying_string)  
    return truncated_list_name
#Will take a look at stop words next


#read in all csvs and create relevant dataframes
ospi_raw_pub_df = pd.read_csv('Washington_School_Directory_20171121.csv')
ospi_raw_ind_df = pd.read_csv('ApprovedPrivateSchoolsList.csv')
ospi_raw_ind_df.dropna(how='all', axis=1, inplace=True)
ospi_raw_ind_df.dropna(how='all', axis=0, inplace=True)


rs_raw_df = pd.read_csv('RSSchoolList3.csv', usecols=[0,1,2,3,4])
rs_ind_df = rs_raw_df[rs_raw_df.Type != "Public"].copy()
rs_pub_df = rs_raw_df[rs_raw_df.Type == "Public"].copy()



#clean all of the city names as they are obviously variable among sources
ospi_raw_pub_df.City = clean_title(ospi_raw_pub_df.City) 
ospi_raw_ind_df.City = clean_title(ospi_raw_ind_df.City)

rs_pub_df.City = clean_title(rs_pub_df.City)
rs_ind_df.City = clean_title(rs_ind_df.City)



#Initialize empty variables to be used later
rs_pub_list_trunc = []
rs_ind_list_trunc = []
ospi_pub_list_trunc = []
ospi_ind_list_trunc = []
ospi_pub_list_bycity_trunc = []
ospi_ind_list_bycity_trunc = []
ospi_pub_code = []
ospi_pub_name = []
ospi_pub_city = []
ospi_ind_code = []
ospi_ind_name = []
ospi_ind_city = []
all_pub_unmatched_df = []
all_ind_unmatched_df = []


#initialize vairbales of names
rs_pub_list = rs_pub_df.Name.tolist()
rs_ind_list = rs_ind_df.Name.tolist()
ospi_pub_list = ospi_raw_pub_df.SchoolName.tolist()
ospi_ind_list = ospi_raw_ind_df.SchoolName.tolist()

removablewords = ["Elementary", "Middle", "High", "School"]

rs_pub_list_trunc = string_truncate(rs_pub_list,removablewords,rs_pub_list_trunc)  
rs_ind_list_trunc = string_truncate(rs_ind_list,removablewords,rs_ind_list_trunc)
ospi_pub_list_trunc = string_truncate(ospi_pub_list,removablewords, ospi_pub_list_trunc)
ospi_ind_list_trunc = string_truncate(ospi_ind_list,removablewords, ospi_ind_list_trunc)

ospi_pub_list_trunc = pd.Series(ospi_pub_list_trunc)
ospi_raw_pub_df['TruncName'] = ospi_pub_list_trunc
ospi_ind_list_trunc = pd.Series(ospi_ind_list_trunc)
ospi_raw_ind_df['TruncName'] = ospi_ind_list_trunc



### PUBLIC ###
for rs_idx, school in enumerate(rs_pub_list_trunc):
    getcity = rs_pub_df.iloc[rs_idx,2]
    ospi_pub_list_bycity = []
    ospi_pub_df_bycity = ospi_raw_pub_df[ospi_raw_pub_df.City == getcity] 
    ospi_pub_list_bycity = ospi_pub_df_bycity.SchoolName.tolist()
    ospi_pub_list_bycity_trunc = ospi_pub_df_bycity.TruncName.tolist()
    
    best_school_so_far = np.nan
    
    for ospi_idx, item in enumerate(ospi_pub_list_bycity_trunc):
        if school == item:
            best_school_so_far = 0
            best_school_so_far = ospi_idx
            
    if pd.isnull(best_school_so_far):
        ospi_pub_code.append(np.nan)
        ospi_pub_name.append(np.nan)
        ospi_pub_city.append(np.nan)
        
    else:
        ospi_pub_code.append(ospi_pub_df_bycity.iloc[best_school_so_far,4])
        ospi_pub_name.append(ospi_pub_df_bycity.iloc[best_school_so_far,5])
        ospi_pub_city.append(ospi_pub_df_bycity.iloc[best_school_so_far,10])

ospi_pub_matched_df = pd.DataFrame({"OSPI School Code": ospi_pub_code,
                               "OSPI School School Name": ospi_pub_name,
                               "OSPI City": ospi_pub_city}, index = range(0,len(ospi_pub_code)), 
    columns=["OSPI School Code", "OSPI School School Name", "OSPI City"])

rs_pub_df.reset_index(drop=True, inplace=True)
ospi_pub_matched_df.reset_index(drop=True, inplace=True)

all_pub_matched_df = pd.concat([rs_pub_df, ospi_pub_matched_df], axis=1)
all_pub_matched_df = all_pub_matched_df[all_pub_matched_df["OSPI City"].notnull()]
all_pub_unmatched_df = all_pub_matched_df[all_pub_matched_df["OSPI City"].isnull()]



### NOT PUBLIC ###
for rs_idx, school in enumerate(rs_ind_list_trunc):
    getcity = rs_ind_df.iloc[rs_idx,2]
    ospi_ind_list_bycity = []
    ospi_ind_df_bycity = ospi_raw_ind_df[ospi_raw_ind_df.City == getcity] 
    ospi_ind_list_bycity = ospi_ind_df_bycity.SchoolName.tolist()
    ospi_ind_list_bycity_trunc = ospi_ind_df_bycity.TruncName.tolist()
    best_school_so_far = np.nan
    
    for ospi_idx, item in enumerate(ospi_ind_list_bycity_trunc):
        if school == item:
            best_school_so_far = 0
            best_school_so_far = ospi_idx
            
    if pd.isnull(best_school_so_far):
        ospi_ind_code.append(np.nan)
        ospi_ind_name.append(np.nan)
        ospi_ind_city.append(np.nan)
    else:
        ospi_ind_code.append(ospi_ind_df_bycity.iloc[best_school_so_far,3])
        ospi_ind_name.append(ospi_ind_df_bycity.iloc[best_school_so_far,2])
        ospi_ind_city.append(ospi_ind_df_bycity.iloc[best_school_so_far,6])

ospi_ind_matched_df = pd.DataFrame({"OSPI School Code": ospi_ind_code,
                               "OSPI School School Name": ospi_ind_name,
                               "OSPI City": ospi_ind_city}, index = range(0,len(ospi_ind_code)), 
    columns=["OSPI School Code", "OSPI School School Name", "OSPI City"])

rs_ind_df.reset_index(drop=True, inplace=True)
ospi_ind_matched_df.reset_index(drop=True, inplace=True)

all_ind_matched_df = pd.concat([rs_ind_df, ospi_ind_matched_df], axis=1)
all_ind_matched_df = all_ind_matched_df[all_ind_matched_df["OSPI City"].notnull()]
all_ind_unmatched_df = all_ind_matched_df[all_ind_matched_df["OSPI City"].isnull()]

#Join public and private schools
all_matched_df = pd.concat([all_pub_matched_df, all_ind_matched_df], axis=0)

#Join public and private missing schools
all_unmatched_df = pd.concat([all_pub_unmatched_df, all_ind_unmatched_df], axis=0)

all_matched_df.to_csv('all_matched_schools.csv')
all_unmatched_df.to_csv('all_unmatched_schools.csv')
