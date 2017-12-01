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

OSPI_df = pd.read_csv('Washington_School_Directory_20171121.csv')
OSPI_Ind_df = pd.read_csv('ApprovedPrivateSchoolsList.csv')

RS_df_pre = pd.read_csv('RSSchoolList2.csv', usecols=[0,1,2,3,4])
RS_df_NotPub = RS_df_pre[RS_df_pre.Type != "Public"]
RS_df = RS_df_pre[RS_df_pre.Type == "Public"]



RSSchoolList = RS_df.Name.tolist()
RSSchoolListStrip = []
RSSchoolListBones = []

RSIndSchoolList = RS_df_NotPub.Name.tolist()
RSIndSchoolListStrip = []
RSIndSchoolListBones = []

RelevantOSPISchoolsBones = []
RelevantOSPIIndSchoolsBones = []
removablewords = ["Elementary", "Middle", "High", "School"]


#for z in RSSchoolList:
#    y = str.strip(z)
#    RSSchoolListStrip.append(y)
#RSSchoolList = RSSchoolListStrip

for z in RSSchoolList:
    modWA = z
    for w in removablewords:
        modWA = modWA.replace(w, "")
        modWA = modWA.strip()
    RSSchoolListBones.append(modWA)
    
for z in RSIndSchoolList:
    modWA = z
    for w in removablewords:
        modWA = modWA.replace(w, "")
        modWA = modWA.strip()
    RSIndSchoolListBones.append(modWA)    

#Create a new dataframe to hold OSPI school info
OSPIcode = []
OSPIname = []
OSPIcity = []

OSPIIndcode = []
OSPIIndname = []
OSPIIndcity = []

### PUBLIC ###
for RSindex, school in enumerate(RSSchoolListBones):
    RS_df.City = RS_df.City.str.upper()
    RS_df.City = RS_df.City.str.strip()
    getcity = RS_df.iloc[RSindex,2]
    bestschoolsofarcounter = 0
    bestschoolsofar = np.nan
    RelevantOSPISchoolsLiST = []
    OSPI_df.City = OSPI_df.City.str.upper()
    RelevantOSPISchools = OSPI_df[OSPI_df.City == getcity] 
    RelevantOSPISchoolsList = RelevantOSPISchools.SchoolName.tolist()
    
    #Remove the words from OSPI
    RelevantOSPISchoolsBones = []
    for z in RelevantOSPISchoolsList:
        modOSPI = z
        for w in removablewords:
            modOSPI = modOSPI.replace(w, "")
            modOSPI = modOSPI.strip()
        RelevantOSPISchoolsBones.append(modOSPI)

    for OSPIindex, item in enumerate(RelevantOSPISchoolsBones):
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
for RSindex, school in enumerate(RSIndSchoolListBones):
    RS_df_NotPub.City = RS_df_NotPub.City.str.upper()
    RS_df_NotPub.City = RS_df_NotPub.City.str.strip()    
    getcity = RS_df_NotPub.iloc[RSindex,2]
    bestschoolsofarcounter = 0
    bestschoolsofar = np.nan
    RelevantOSPIIndSchoolsLiST = []
    OSPI_Ind_df.City = OSPI_Ind_df.City.str.upper()
    RelevantOSPIIndSchools = OSPI_Ind_df[OSPI_Ind_df.City == getcity] 
    RelevantOSPIIndSchoolsList = RelevantOSPIIndSchools.SchoolName.tolist()
    
    #Remove the words from OSPI
    RelevantOSPIIndSchoolsBones = []
    for z in RelevantOSPIIndSchoolsList:
        modOSPI = z
        for w in removablewords:
            modOSPI = modOSPI.replace(w, "")
            modOSPI = modOSPI.strip()
        RelevantOSPIIndSchoolsBones.append(modOSPI)

    for OSPIindex, item in enumerate(RelevantOSPIIndSchoolsBones):
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

#print(RS_df_NotPub.tail(10))
#print(OSPI_df_fin.tail(10))    
bothschoolsInd_df = pd.concat([RS_df_NotPub, OSPI_Ind_df_fin], axis=1)

bothschools_df = pd.concat([bothschools_pub_df, bothschoolsInd_df], axis=0)

#print parts of the dataframe to check
print(bothschools_pub_df.head(10))
print(bothschoolsInd_df.head(10))
print(bothschools_df.head(10))
bothschools_df.to_csv('both_schools.csv')
