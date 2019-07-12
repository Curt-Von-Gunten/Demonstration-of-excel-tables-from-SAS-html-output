# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:31:57 2019

@author: cv85
"""

from bs4 import BeautifulSoup as soup 
import os
import numpy as np 
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP

path = "S:/IRB/Wu/VonGunten_2018/NSDUH Projects/Multiple SUD and Treatment Project/Output/Pythong Parsing/Table 5"
os.chdir(path)

############################################################File 1################################################
HtmlFile = open("Table 5_Any.html", 'r', encoding='utf-8')
content = HtmlFile.read() 
HtmlFile.close()
page_soup = soup(content, "html.parser")
AllCrossTables = page_soup.find_all(summary="Procedure Surveyfreq: CrossTabulation Table")
TableNumber = len(AllCrossTables)
DrugAmountDF = pd.DataFrame(columns = ("Row Percent", "Std Err of Row Percent"))

newListAnyPerc = []
newListAnyCI = []
for x in range(1, len(AllCrossTables), 2):
    temp = AllCrossTables[x]
    tempText = temp.find_all('td', class_="r data")
    tempValues = [pt.get_text() for pt in tempText]
    tempDF = pd.DataFrame(np.array(tempValues).reshape(int(len(tempValues)/11),11), 
                              columns = ("Frequency", "Weighted Frequency", "Std Err of Wgt Freq", 
                                  "Percent", "Std Err of Percent", "Percent Lower CI", "Percent Upper  CI",
                                  "Row Percent", "Std Err of Row Percent", "Row Percent Lower CI", "Row Percent Upper CI"))
   
##############Treatment Percent##############
    tempPerElem = tempDF.iloc[4,7]
    tempPerElem = Decimal(str(tempPerElem)).quantize(Decimal('11.1'), rounding=ROUND_HALF_UP)
    tempPerStr = str(tempPerElem)
    newListAnyPerc.append(tempPerStr)    

    #CIs
    tempCIElem = tempDF.iloc[4,[9,10]]
    tempCIElem = [Decimal(str(CI)).quantize(Decimal('11.1'), rounding=ROUND_HALF_UP) for CI in tempCIElem]
    tempCIString = str('[' + str(tempCIElem[0]) + "-" + str(tempCIElem[1]) + "]")
    newListAnyCI .append(tempCIString)


############################################################File 2################################################
HtmlFile = open("Table 5_AlcOnly.html", 'r', encoding='utf-8')
content = HtmlFile.read() 
HtmlFile.close()
page_soup = soup(content, "html.parser")
AllCrossTables = page_soup.find_all(summary="Procedure Surveyfreq: CrossTabulation Table")
TableNumber = len(AllCrossTables)
DrugAmountDF = pd.DataFrame(columns = ("Row Percent", "Std Err of Row Percent"))

newListAlcOnlyPerc = []
newListAlcOnlyCI = []
for x in range(1, len(AllCrossTables), 2):
    temp = AllCrossTables[x]
    tempText = temp.find_all('td', class_="r data")
    tempValues = [pt.get_text() for pt in tempText]
    tempDF = pd.DataFrame(np.array(tempValues).reshape(int(len(tempValues)/11),11), 
                              columns = ("Frequency", "Weighted Frequency", "Std Err of Wgt Freq", 
                                  "Percent", "Std Err of Percent", "Percent Lower CI", "Percent Upper  CI",
                                  "Row Percent", "Std Err of Row Percent", "Row Percent Lower CI", "Row Percent Upper CI"))
   
##############Treatment Percent##############
    tempPerElem = tempDF.iloc[4,7]
    tempPerElem = Decimal(str(tempPerElem)).quantize(Decimal('11.1'), rounding=ROUND_HALF_UP)
    tempPerStr = str(tempPerElem)
    newListAlcOnlyPerc.append(tempPerStr)    

    #CIs
    tempCIElem = tempDF.iloc[4,[9,10]]
    tempCIElem = [Decimal(str(CI)).quantize(Decimal('11.1'), rounding=ROUND_HALF_UP) for CI in tempCIElem]
    tempCIString = str('[' + str(tempCIElem[0]) + "-" + str(tempCIElem[1]) + "]")
    newListAlcOnlyCI .append(tempCIString)


############################################################File 3################################################
HtmlFile = open("Table 5_IllicitOnly.html", 'r', encoding='utf-8')
content = HtmlFile.read() 
HtmlFile.close()
page_soup = soup(content, "html.parser")
AllCrossTables = page_soup.find_all(summary="Procedure Surveyfreq: CrossTabulation Table")
TableNumber = len(AllCrossTables)
DrugAmountDF = pd.DataFrame(columns = ("Row Percent", "Std Err of Row Percent"))

newListIllicitOnlyPerc = []
newListIllicitOnlyCI = []
#Note had to ignore the final table because the value is 0.
for x in range(1, len(AllCrossTables)-2, 2):
    temp = AllCrossTables[x]
    tempText = temp.find_all('td', class_="r data")
    tempValues = [pt.get_text() for pt in tempText]
    tempDF = pd.DataFrame(np.array(tempValues).reshape(int(len(tempValues)/11),11), 
                              columns = ("Frequency", "Weighted Frequency", "Std Err of Wgt Freq", 
                                  "Percent", "Std Err of Percent", "Percent Lower CI", "Percent Upper  CI",
                                  "Row Percent", "Std Err of Row Percent", "Row Percent Lower CI", "Row Percent Upper CI"))
   
##############Treatment Percent##############
    tempPerElem = tempDF.iloc[4,7]
    tempPerElem = Decimal(str(tempPerElem)).quantize(Decimal('11.1'), rounding=ROUND_HALF_UP)
    tempPerStr = str(tempPerElem)
    newListIllicitOnlyPerc.append(tempPerStr)    
       
    #CIs
    tempCIElem = tempDF.iloc[4,[9,10]]
    tempCIElem = [Decimal(str(CI)).quantize(Decimal('11.1'), rounding=ROUND_HALF_UP) for CI in tempCIElem]
    tempCIString = str('[' + str(tempCIElem[0]) + "-" + str(tempCIElem[1]) + "]")
    newListIllicitOnlyCI .append(tempCIString)
       
newListIllicitOnlyPerc.append(np.nan)
newListIllicitOnlyCI .append(np.nan)


############################################################File 4################################################
HtmlFile = open("Both.html", 'r', encoding='utf-8')
content = HtmlFile.read() 
HtmlFile.close()
page_soup = soup(content, "html.parser")
AllCrossTables = page_soup.find_all(summary="Procedure Surveyfreq: CrossTabulation Table")
TableNumber = len(AllCrossTables)
DrugAmountDF = pd.DataFrame(columns = ("Row Percent", "Std Err of Row Percent"))

newListBothPerc = []
newListBothCI = []
for x in range(1, len(AllCrossTables), 2):
    temp = AllCrossTables[x]
    tempText = temp.find_all('td', class_="r data")
    tempValues = [pt.get_text() for pt in tempText]
    tempDF = pd.DataFrame(np.array(tempValues).reshape(int(len(tempValues)/11),11), 
                              columns = ("Frequency", "Weighted Frequency", "Std Err of Wgt Freq", 
                                  "Percent", "Std Err of Percent", "Percent Lower CI", "Percent Upper  CI",
                                  "Row Percent", "Std Err of Row Percent", "Row Percent Lower CI", "Row Percent Upper CI"))
   
##############Treatment Percent##############
    tempPerElem = tempDF.iloc[4,7]
    tempPerElem = Decimal(str(tempPerElem)).quantize(Decimal('11.1'), rounding=ROUND_HALF_UP)
    tempPerStr = str(tempPerElem)
    newListBothPerc.append(tempPerStr)    

    #CIs
    tempCIElem = tempDF.iloc[4,[9,10]]
    tempCIElem = [Decimal(str(CI)).quantize(Decimal('11.1'), rounding=ROUND_HALF_UP) for CI in tempCIElem]
    tempCIString = str('[' + str(tempCIElem[0]) + "-" + str(tempCIElem[1]) + "]")
    newListBothCI .append(tempCIString)


############################################################File 5################################################
HtmlFile = open("Table 5_PercAlcOnly.html", 'r', encoding='utf-8')
content = HtmlFile.read() 
HtmlFile.close()
page_soup = soup(content, "html.parser")
AllCrossTables = page_soup.find_all(summary="Procedure Surveyfreq: CrossTabulation Table")
TableNumber = len(AllCrossTables)
DrugAmountDF = pd.DataFrame(columns = ("Row Percent", "Std Err of Row Percent"))

newListPercAlcOnlyPerc = []
newListPercAlcOnlyCI = []
for x in range(0, len(AllCrossTables)):
    temp = AllCrossTables[x]
    tempText = temp.find_all('td', class_="r data")
    tempValues = [pt.get_text() for pt in tempText]
    tempDF = pd.DataFrame(np.array(tempValues).reshape(int(len(tempValues)/11),11), 
                              columns = ("Frequency", "Weighted Frequency", "Std Err of Wgt Freq", 
                                  "Percent", "Std Err of Percent", "Percent Lower CI", "Percent Upper  CI",
                                  "Row Percent", "Std Err of Row Percent", "Row Percent Lower CI", "Row Percent Upper CI"))
   
##############Treatment Percent##############
    tempPerElem = tempDF.iloc[4,7]
    tempPerElem = Decimal(str(tempPerElem)).quantize(Decimal('11.1'), rounding=ROUND_HALF_UP)
    tempPerStr = str(tempPerElem)
    newListPercAlcOnlyPerc.append(tempPerStr)    

    #CIs
    tempCIElem = tempDF.iloc[4,[9,10]]
    tempCIElem = [Decimal(str(CI)).quantize(Decimal('11.1'), rounding=ROUND_HALF_UP) for CI in tempCIElem]
    tempCIString = str('[' + str(tempCIElem[0]) + "-" + str(tempCIElem[1]) + "]")
    newListPercAlcOnlyCI .append(tempCIString)
    
    
    
##################################################################################################################       
############################################################Final Table###########################################    
##################################################################################################################       
variableList = [
'Alcohol and Marijuana',
'Alcohol and opiates',
'Alcohol and cocaine',
'Alcohol and stimulants']

Table5_df = pd.DataFrame(columns=['Variables', 'Any %', 'Any CI', 'Alcohol Only %', 'Alcohol Only CI', 'Illicit Only %', 'Illicit Only CI',
                                  'Both %', 'Both CI', 'Percentage Alcohol Only %', 'Percentage Alcohol Only CI'])          
Table5_df['Variables'] = variableList
Table5_df['Any %'] = newListAnyPerc
Table5_df['Any CI'] = newListAnyCI
Table5_df['Alcohol Only %'] = newListAlcOnlyPerc
Table5_df['Alcohol Only CI']  = newListAlcOnlyCI
Table5_df['Illicit Only %'] = newListIllicitOnlyPerc
Table5_df['Illicit Only CI'] = newListIllicitOnlyCI
Table5_df['Both %'] = newListBothPerc
Table5_df['Both CI']  = newListBothCI
Table5_df['Percentage Alcohol Only %'] = newListPercAlcOnlyPerc
Table5_df['Percentage Alcohol Only CI']  = newListPercAlcOnlyCI
Table5_df['Percentage Alcohol Only %_v2'] = Table5_df['Alcohol Only %'].astype(float) / Table5_df['Any %'].astype(float)
Table5_df['Percentage Alcohol Only %_v2']  = Table5_df['Percentage Alcohol Only %_v2']  * 100
Table5_df['Percentage Alcohol Only %_v2'] = [Decimal(str(elem)).quantize(Decimal('11.1'), rounding=ROUND_HALF_UP) for elem in Table5_df['Percentage Alcohol Only %_v2']]
Table5_df['Percentage Alcohol Only %_v3'] = Table5_df['Alcohol Only %'].astype(float) / (Table5_df['Alcohol Only %'].astype(float) + Table5_df['Illicit Only %'].astype(float) + Table5_df['Both %'].astype(float))
Table5_df['Percentage Alcohol Only %_v3'] = Table5_df['Percentage Alcohol Only %_v3'] * 100
Table5_df['Percentage Alcohol Only %_v3'] = [Decimal(str(elem)).quantize(Decimal('11.1'), rounding=ROUND_HALF_UP) for elem in Table5_df['Percentage Alcohol Only %_v3']]

Table5_df.drop(columns=['Percentage Alcohol Only %', 'Percentage Alcohol Only CI', 'Percentage Alcohol Only %_v2'], inplace = True)
