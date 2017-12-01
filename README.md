# SchoolMatch

Goal:
The goal is to write a program to match a list of schools we have created with an officially published list provided by the Washington OSPI. The matches don't need to be perfect, but it is meant to reduce the number of changes we need to make by hand.

Process:
The program reads in tables of schools to compare, creates lists of those removing the words "Elementary", "Middle", "High", "School", selects schools by city and compares the truncated names. If a school from our list does not match a school from the OSPI list, our list gets a row of NaN added, if it does match, the OSPI school's school code, name, and city are added. 

Data Sources:
Washington_School_Directory_20171201.csv - File as downloaded from OSPI at http://www.k12.wa.us/PrivateEd/PrivateSchools/ 
Washington_School_Directory_20171201csv.csv - converted to a csv by exporting from excel to remove some formatting issues
ApprovedPrivateSchoolsList.xlsx - File as downloaded from OSPI at https://eds.ospi.k12.wa.us/DirectoryEDS.aspx 
ApprovedPrivateSchoolsListcsv.csv - deleted first three rows and convert to a csv by exporting from excel
