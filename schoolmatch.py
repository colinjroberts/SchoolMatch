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



#read in all csvs and create relevant dataframes
OSPI_df = pd.read_csv('Washington_School_Directory_20171121.csv')
OSPI_Ind_df = pd.read_csv('ApprovedPrivateSchoolsList.csv')
OSPI_Ind_df.dropna(how='all', axis=1, inplace=True)
OSPI_Ind_df.dropna(how='all', axis=0, inplace=True)


RS_df_pre = pd.read_csv('RSSchoolList2.csv', usecols=[0,1,2,3,4])
RS_df_NotPub = RS_df_pre[RS_df_pre.Type != "Public"].copy()
RS_df = RS_df_pre[RS_df_pre.Type == "Public"].copy()



#clean all of the city names as they are obviously variable among sources
OSPI_df.City = clean_title(OSPI_df.City) 
OSPI_Ind_df.City = clean_title(OSPI_Ind_df.City)

RS_df.City = clean_title(RS_df.City)
RS_df_NotPub.City = clean_title(RS_df_NotPub.City)



#Initialize empty variables to be used later
RSSchoolListTruncated = []
RSIndSchoolListTruncated = []
OSPITruncatedSchools = []
OSPIIndTruncatedSchools = []
RelevantOSPISchoolsTruncated = []
RelevantOSPIIndSchoolsTruncated = []
OSPIcode = []
OSPIname = []
OSPIcity = []
OSPIIndcode = []
OSPIIndname = []
OSPIIndcity = []



#initialize vairbales of names
RSSchoolList = RS_df.Name.tolist()
RSIndSchoolList = RS_df_NotPub.Name.tolist()
OSPISchoolList = OSPI_df.SchoolName.tolist()
OSPIIndSchoolList = OSPI_Ind_df.SchoolName.tolist()

removablewords = ["Elementary", "Middle", "High", "School"]

RSSchoolListTruncated = string_truncate(RSSchoolList,removablewords,RSSchoolListTruncated)  
RSIndSchoolListTruncated = string_truncate(RSIndSchoolList,removablewords,RSIndSchoolListTruncated)
OSPITruncatedSchools = string_truncate(OSPISchoolList,removablewords, OSPITruncatedSchools)
OSPIIndTruncatedSchools = string_truncate(OSPIIndSchoolList,removablewords, OSPIIndTruncatedSchools)

OSPITruncatedSchools = pd.Series(OSPITruncatedSchools)
OSPI_df['TruncName'] = OSPITruncatedSchools
OSPIIndTruncatedSchools = pd.Series(OSPIIndTruncatedSchools)
OSPI_Ind_df['TruncName'] = OSPIIndTruncatedSchools



### PUBLIC ###
for RSidx, school in enumerate(RSSchoolListTruncated):
    getcity = RS_df.iloc[RSidx,2]
    RelevantOSPISchoolsList = []
    RelevantOSPISchools = OSPI_df[OSPI_df.City == getcity] 
    RelevantOSPISchoolsList = RelevantOSPISchools.SchoolName.tolist()
    RelevantOSPISchoolsTruncated = RelevantOSPISchools.TruncName.tolist()
    
    bestschoolsofar = np.nan
    
    for OSPIindex, item in enumerate(RelevantOSPISchoolsTruncated):
        if school == item:
            bestschoolsofar = 0
            bestschoolsofar = OSPIindex
            
    if pd.isnull(bestschoolsofar):
        OSPIcode.append(np.nan)
        OSPIname.append(np.nan)
        OSPIcity.append(np.nan)
    else:
        OSPIcode.append(RelevantOSPISchools.iloc[bestschoolsofar,4])
        OSPIname.append(RelevantOSPISchools.iloc[bestschoolsofar,5])
        OSPIcity.append(RelevantOSPISchools.iloc[bestschoolsofar,10])

OSPI_df_fin = pd.DataFrame({"OSPI School Code": OSPIcode,
                               "OSPI School School Name": OSPIname,
                               "OSPI City": OSPIcity}, index = range(0,len(OSPIcode)), columns=["OSPI School Code", "OSPI School School Name", "OSPI City"])

RS_df.reset_index(drop=True, inplace=True)
OSPI_df_fin.reset_index(drop=True, inplace=True)

print(RS_df.tail(10))
print(OSPI_df_fin.tail(10))    
bothschools_pub_df = pd.concat([RS_df, OSPI_df_fin], axis=1)            
        



### NOT PUBLIC ###
for RSindex, school in enumerate(RSIndSchoolListTruncated):
    getcity = RS_df_NotPub.iloc[RSindex,2]
    RelevantOSPIIndSchoolsList = []
    RelevantOSPIIndSchools = OSPI_Ind_df[OSPI_Ind_df.City == getcity] 
    RelevantOSPIIndSchoolsList = RelevantOSPIIndSchools.SchoolName.tolist()
    RelevantOSPIIndSchoolsTruncated = RelevantOSPIIndSchools.TruncName.tolist()
    bestschoolsofar = np.nan
    
    for OSPIindex, item in enumerate(RelevantOSPIIndSchoolsTruncated):
        if school == item:
            bestschoolsofar = 0
            bestschoolsofar = OSPIindex
            
    if pd.isnull(bestschoolsofar):
        OSPIIndcode.append(np.nan)
        OSPIIndname.append(np.nan)
        OSPIIndcity.append(np.nan)
    else:
        OSPIIndcode.append(RelevantOSPIIndSchools.iloc[bestschoolsofar,3])
        OSPIIndname.append(RelevantOSPIIndSchools.iloc[bestschoolsofar,2])
        OSPIIndcity.append(RelevantOSPIIndSchools.iloc[bestschoolsofar,6])

OSPI_Ind_df_fin = pd.DataFrame({"OSPI School Code": OSPIIndcode,
                               "OSPI School School Name": OSPIIndname,
                               "OSPI City": OSPIIndcity}, index = range(0,len(OSPIIndcode)), columns=["OSPI School Code", "OSPI School School Name", "OSPI City"])

RS_df_NotPub.reset_index(drop=True, inplace=True)
OSPI_Ind_df_fin.reset_index(drop=True, inplace=True)
  

#Join public and private
bothschoolsInd_df = pd.concat([RS_df_NotPub, OSPI_Ind_df_fin], axis=1)
bothschools_df = pd.concat([bothschools_pub_df, bothschoolsInd_df], axis=0)

print(bothschools_pub_df.head(10))
print(bothschoolsInd_df.head(10))
print(bothschools_df.head(10))

bothschools_df.to_csv('both_schools.csv')