# SchoolMatch

Goal:

The problem is that my organization has a list of schools with a variety of naming schemes, spelling errors, and some duplicates (exact and as a results of scemes/spelling). The goal is to both identify duplicates and  match schools on our list with an officially published list provided by the Washington Office of Superintendent of Public Instruction (OSPI). The matches don't need to be perfect, but it is meant to reduce the number of changes we need to make by hand.

Process:

The program reads in our tables and the OSPI tables of schools to compare; converts them to to lists removing the words "Elementary", "Middle", "High", and "School"; subsets schools from both lists by city; then compares the truncated names. If a school from our list does not match a school from the OSPI list, our list gets a row of NaN added, if it does match, the OSPI school's school code, name, and city are added. 

Results:

After a few tweaks here and there, this program helped us identify handful of duplicates, quite a few schools with names slightly different than the official ones, and a few cases of different schools with identical or very similar names differentiated only by location or time.

Data Sources:

Washington_School_Directory_20171201.csv - File as downloaded from OSPI at http://www.k12.wa.us/PrivateEd/PrivateSchools/ 

Washington_School_Directory_20171201csv.csv - converted to a csv by exporting from excel to remove some formatting issues

ApprovedPrivateSchoolsList.xlsx - File as downloaded from OSPI at https://eds.ospi.k12.wa.us/DirectoryEDS.aspx 

ApprovedPrivateSchoolsListcsv.csv - deleted first three rows and convert to a csv by exporting from excel
