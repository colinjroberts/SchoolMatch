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


rs_raw_df = pd.read_csv('RSSchoolList2.csv', usecols=[0,1,2,3,4])
rs_ind_df = rs_raw_df[rs_raw_df.Type != "Public"].copy()
rs_pub_df = rs_raw_df[rs_raw_df.Type == "Public"].copy()



#clean all of the city names as they are obviously variable among sources
ospi_raw_pub_df.City = clean_title(ospi_raw_pub_df.City) 
ospi_raw_ind_df.City = clean_title(ospi_raw_ind_df.City)

rs_pub_df.City = clean_title(rs_pub_df.City)
rs_ind_df.City = clean_title(rs_ind_df.City)

def clean_title(text):
    """
    Takes a pandas series of strings, and returns a pandas series of strings
    that have been stripped and each word capitalized
    """
    text = text.str.lower()
    text = text.str.title()
    text = text.str.strip()
    return text


def string_truncate(strings_to_truncate, words_to_remove):
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


def school_match(school_type, output_type, rs_df, ospi_df):
    '''
    Takes the type of school (public or independent) as a string, a string 
    "matched" or "unmatched" that determines whether the output is the schools 
    that matched or those that didn't, the processed dataframe from 
    Rainier Scholars, and the processed dataframe from OPSI using only the 
    code, name, and city columns in that order and looks for matches by 
    comparing the truncated names.
    '''
    ospi_code = []
    ospi_name = []
    ospi_city = []
    ospi_type = []

    for rs_idx, school in enumerate(rs_df.TruncName):
        getcity = rs_df.iloc[rs_idx,2]
        ospi_df_bycity = ospi_df[ospi_df.City == getcity] 
        
        best_school_so_far = np.nan
        
        for ospi_idx, item in enumerate(ospi_df_bycity.TruncName):
            if school == item:
                best_school_so_far = 0
                best_school_so_far = ospi_idx
                
        if pd.isnull(best_school_so_far):
            ospi_code.append(np.nan)
            ospi_name.append(np.nan)
            ospi_city.append(np.nan)
            
        else:
            ospi_code.append(ospi_df_bycity.iloc[best_school_so_far,0])
            ospi_name.append(ospi_df_bycity.iloc[best_school_so_far,1])
            ospi_city.append(ospi_df_bycity.iloc[best_school_so_far,2])
            ospi_type.append(school_type)
    
    ospi_matched_df = pd.DataFrame({"OSPI School Code": ospi_code,
                                   "OSPI School School Name": ospi_name,
                                   "OSPI City": ospi_city}, index = range(0,len(ospi_code)), 
        columns=["OSPI School Code", "OSPI School School Name", "OSPI City"])
    
    rs_df.reset_index(drop=True, inplace=True)
    ospi_matched_df.reset_index(drop=True, inplace=True)
    
    all_df = pd.concat([rs_df, ospi_matched_df], axis=1)
    all_unmatched_df = all_df[all_df["OSPI City"].isnull()]
    all_matched_df = all_df[all_df["OSPI City"].notnull()]

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
    if output_type == "matched":
        return all_matched_df
    
    elif output_type == "unmatched":
        return all_unmatched_df
    
    else:
        print("output_type must be a string, either 'matched' or 'unmatched'.")


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
all_ind_unmatched_df = all_ind_matched_df[all_ind_matched_df["OSPI City"].isnull()]

#Join public and private schools
all_matched_df = pd.concat([all_pub_matched_df, all_ind_matched_df], axis=0)


#Join public and private missing schools
all_unmatched_df = pd.concat([all_pub_unmatched_df, all_ind_unmatched_df], axis=0)

all_matched_df.to_csv('all_matched_schools.csv')
all_unmatched_df.to_csv('all_unmatched_schools')
#read in all csvs and create relevant dataframes
ospi_raw_pub_df = pd.read_csv('Washington_School_Directory_20171201.csv')
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

removablewords = ["Elementary", "Middle", "High", "School"]

rs_pub_df["TruncName"] = string_truncate(rs_pub_df.Name, removablewords)
rs_ind_df["TruncName"] = string_truncate(rs_ind_df.Name, removablewords)
ospi_raw_pub_df["TruncName"] = string_truncate(ospi_raw_pub_df["SchoolName"], removablewords)
ospi_raw_ind_df["TruncName"] = string_truncate(ospi_raw_ind_df["SchoolName"], removablewords)

### PUBLIC ###
all_pub_matched_df = school_match("public", "matched", rs_pub_df, ospi_raw_pub_df[["SchoolCode", "SchoolName", "City", "TruncName"]])
all_pub_unmatched_df = school_match("public", "unmatched", rs_pub_df, ospi_raw_pub_df[["SchoolCode", "SchoolName", "City", "TruncName"]])

#### NOT PUBLIC ###
all_ind_matched_df = school_match("independent", "matched", rs_ind_df, ospi_raw_ind_df[["SchoolBldgNumber","SchoolName","City", "TruncName"]])
all_ind_unmatched_df = school_match("independent", "unmatched", rs_ind_df, ospi_raw_ind_df[["SchoolBldgNumber","SchoolName","City", "TruncName"]])

all_pub_matched_df.to_csv('all_pub_matched_schools.csv')
all_pub_unmatched_df.to_csv('all_pub_unmatched_schools.csv')
all_ind_matched_df.to_csv('all_ind_matched_schools.csv')
all_ind_unmatched_df.to_csv('all_ind_unmatched_schools.csv')
