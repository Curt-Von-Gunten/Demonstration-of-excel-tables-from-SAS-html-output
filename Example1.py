# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 16:20:15 2019

@author: cv85
"""

from bs4 import BeautifulSoup as soup 
import os
import numpy as np 
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP

path = "S:/IRB/Wu/VonGunten_2018/NSDUH Projects/Multiple SUD and Treatment Project/Output/Pythong Parsing/Table 4"
os.chdir(path)

############################################################File 1################################################
HtmlFile = open("Table 4_TreatPerc.html", 'r', encoding='utf-8')
content = HtmlFile.read() 
HtmlFile.close()
page_soup = soup(content, "html.parser")
AllCrossTables = page_soup.find_all(summary="Procedure Surveyfreq: CrossTabulation Table")
TableNumber = len(AllCrossTables)

treatmentDF = pd.DataFrame(columns = ("No Treatment", "Treatment"))
for x in range(1, len(AllCrossTables), 2): #Note that I skip every other table, starting with the second table.
    temp = AllCrossTables[x]
    tempText = temp.find_all('td', class_="r data")
    tempValues = [pt.get_text() for pt in tempText]
    tempDF = pd.DataFrame(np.array(tempValues).reshape(int(len(tempValues)/11),11), 
                              columns = ("Frequency", "Weighted Frequency", "Std Err of Wgt Freq", 
                                  "Percent", "Std Err of Percent", "Percent Lower CI", "Percent Upper  CI",
                                  "Row Percent", "Std Err of Row Percent", "Row Percent Lower CI", "Row Percent Upper CI"))
    
    ###Treatment percentages###
    tempDF = tempDF.drop(tempDF.index[-3:]) #Removing extra rows that are there because SAS includes a Total at the end.
    tempDF = tempDF.iloc[:,[7]]  #Grabbing the needed column.
    #I need to delete the "Total" rows. This is a problem because each variable has a different number of rows.
    templist = list(range(1, int((len(tempValues)/11)/3))) #Each variable has a different number of rows, but the number of rows is a multiple of a constant, with that constant being the number of levels of the DV (here 3).
    templist = [(x*3-1) for x in templist] #The previous line provided a sequential list of the number of "Total" rows. Here I need to convert each value in the list to the index of interest. The -1 is because I had to start at 1 in the line above because 0 can't be multiplied.
    tempDF = tempDF.drop(tempDF.index[templist], axis=0) #Dropping "Total" rows. I'm not sure why I need to specify the index. Why can't just [1,2,3,etc.]
    tempDF = tempDF.reset_index(drop=True) #Making a new index, because the step above removed rows of the index (e.g., 1,2,4,5,7,8)
    tempSeries = tempDF.squeeze() #Decimal only seems to work on single elements and series, and not on list or df elements. .squeeze is a shortcut to convert a single column df to a series. You can use df.T.squeeze() for a multiple column df.
    tempSeries = [Decimal(str(elem)).quantize(Decimal('11.1'), rounding=ROUND_HALF_UP) for elem in tempSeries]
    tempDF = pd.DataFrame(np.array(tempSeries).reshape(int(len(tempDF)/2),2), columns = ("No Treatment", "Treatment")) #Reshaping to wide. The 2 is because the DV has two levels.
    treatmentDF = treatmentDF.append(tempDF) 
    treatmentDF = treatmentDF.append(pd.Series([np.nan]), ignore_index = True) #Adding a space for the "ref" of each variable.
treatmentDF =  treatmentDF.iloc[:,[0,1]] #For some reason there is an extra column created from the space step above. Deleting it.



############################################################File 2################################################
###Unadjusted###
varList = ['AlcCategory', 'DNICNSP', 'Sex', 'Age', 'Race', 'Education', 'FamInc', 
      'Work', 'Insurance', 'Mar', 'COUTYP4', 'SurveyYear'  ]

masterDF = pd.DataFrame(columns = ("Odds Ratio", "Lower CI", "Upper CI"))

for var in varList:
    HtmlFile = open(str("Table 4_TreatOdds_" + var + ".html"), 'r', encoding='utf-8')
    content = HtmlFile.read() 
    HtmlFile.close()
    page_soup = soup(content, "html.parser")
    AllOdds = page_soup.find_all(summary="Procedure Surveylogistic: Odds Ratios")
    OddsNumber = len(AllOdds)
    
    for x in range(2,3):
        temp = AllOdds[x] #There's only 1 element, but need to do this in order to apply the 'get_ext' method.
        OddsText = temp.find_all('td', class_="r data")
        OddsValues = [pt.get_text() for pt in OddsText]
        OddsValues = pd.Series(OddsValues)
        OddsValues = [Decimal(str(elem)).quantize(Decimal('11.11'), rounding=ROUND_HALF_UP) for elem in OddsValues]
        tempDF = pd.DataFrame(np.array(OddsValues).reshape(int(len(OddsValues)/3),3), columns = ("Odds Ratio", "Lower CI", "Upper CI"))
        for lower, upper in zip(tempDF['Lower CI'], tempDF['Upper CI']):
            tempDF.loc[(tempDF['Lower CI'] == lower) & (tempDF['Upper CI'] == upper), 'CI'] = str("[" + str(lower) + "-" +  str(upper) + "]")
        tempDF['Variable'] = var
        tempDF = tempDF.append(pd.Series([np.nan]), ignore_index=True)
        tempDF = tempDF.append(pd.Series([np.nan]), ignore_index=True)
        masterDF = masterDF.append(tempDF)
        
        
############################################################File 3################################################       
###Adjusted###
HtmlFile = open("Table 4_TreatOdds_Adjusted.html", 'r', encoding='utf-8')
content = HtmlFile.read() 
HtmlFile.close()
page_soup = soup(content, "html.parser")
AllOdds = page_soup.find_all(summary="Procedure Surveylogistic: Odds Ratios")
OddsNumber = len(AllOdds)

oddsList = []
CIList = []
#Only selecting the final table, which is domain = 'yes'
for x in range(1,2):
    temp = AllOdds[x] #There's only 1 element, but need to do this in order to apply the 'get_ext' method.
    OddsText = temp.find_all('td', class_="r data")
    OddsValues = [pt.get_text() for pt in OddsText]
    OddsValues = [Decimal(str(elem)).quantize(Decimal('11.11'), rounding=ROUND_HALF_UP) for elem in OddsValues]
    for i,j,k in zip(OddsValues[0::3], OddsValues[1::3], OddsValues[2::3]):
        oddsList.append(i)
        tempCIString = str('[' + str(j) + "-" + str(k) + "]")
        CIList.append(tempCIString)
        
Table4_Adj = pd.DataFrame(columns=['Odds', 'CI'])          
Table4_Adj['Odds'] = oddsList   
Table4_Adj['CI'] = CIList        
#Manually adding nans. Unfortunately this replaces the values in each row.  
#for i in (4,5,7,8,10,11,15,16,21,22,26,27,30,31,35,36,38,39,42,43,46,47,50,51):
    #Table4_Adj.loc[i] = [np.nan for n in range(2)]
    #Table4_Adj.index = Table4_Adj.index + 1  # shifting index
    #Table4_Adj = Table4_Adj.sort_index()  # sorting by index
 
Table4_df = pd.DataFrame(columns = ("Variable", "No Treatment", "Treatment", "Unadj_Odds Ratio", "Unadj_CI", "Adj_Odds Ratio", "Adj_CI"))      
Table4_df["Variable"] = masterDF["Variable"]
Table4_df["No Treatment"] = treatmentDF["No Treatment"]
Table4_df["Treatment"] = treatmentDF["Treatment"]
Table4_df["Unadj_Odds Ratio"] = masterDF["Odds Ratio"]
Table4_df["Unadj_CI"] = masterDF["CI"]
Table4_df.reset_index(drop = True, inplace = True)

Table4_df["Adj_Odds Ratio"] = Table4_Adj['Odds']
Table4_df["Adj_CI"] = Table4_Adj['CI']



 
 

