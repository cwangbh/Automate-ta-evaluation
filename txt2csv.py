# -*- coding: utf-8 -*-
import os
import pandas as pd
import re
from pandas import ExcelWriter

# set up regular expressions
# use https://regexper.com to visualise these if required
rx_dict = {
    'Survey': re.compile(r'Survey ;[\d.]+\n'),
    'NA': re.compile(r'NA.*  ;\d+'),
    'Total': re.compile(r'Total;'),
}



def _parse_line(line):
    """
    Do a regex search against all defined regexes and
    return the key and match result of the first matching regex

    """
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None

def txt_to_csv(currentfile,data):
    SurveyList = []
    NAList = []
    with open(currentfile,'r') as file_object:
        for line in file_object:
            if line.startswith(' ;Survey period:'):
                TA_Name = next(file_object , '').strip()
                CourseCode = next(file_object , '').strip().split(' ')#re.compile(r'CIVL-\d*-L\d')
                print(TA_Name, CourseCode[0])
            if 'Percentage of enrolled ' in line:
                # split the line by space (\xc2) and ; (\xa0)
                ResponseRateLine = line.split('\xc2\xa0')
                #extract  re.findall('\d+', str1 )
                ResponseRate = float(re.findall(r'\d+.\d', ResponseRateLine[-2] )[0])
                ClassSize = int(re.findall(r'\d+',ResponseRateLine[-1].split('/')[-1] )[0])
                NumberOfRespondent = int(re.findall(r'\d+',ResponseRateLine[-1].split('/')[-2])[0])
                print ResponseRate,ClassSize, NumberOfRespondent
            
            key,match = _parse_line(line)
            if key == 'Survey':
                Survey = float(re.findall(r'\d{2}[.]\d{1}', match.string.split(';')[-1])[-2])
                SurveyList.append(Survey)
                print Survey

            if key == 'NA':
                #NA = re.findall(r'\d{1-3}[.]\d{1-3}',match.string.split('\xc2\xa0')[7])[0]
                print match.string
                NA = re.findall(r'\d+[.]\d+%',match.string)
                print NA
                NA = re.findall(r'\d+[.]\d+',NA[0])
                print NA
                NAList.append(float(NA[0]))
                

    print SurveyList
    print NAList

 
    row1 = {'CourseCode': CourseCode[0],
        'TA_Name':TA_Name,
        'ClassSize':ClassSize,
        'NumberOfRespondent':NumberOfRespondent,
        'ResponseRate': ResponseRate,    
        'Q1':SurveyList[0],'Q1_Active':1-NAList[0]/100.,
        'Q2':SurveyList[1],'Q2_Active':1-NAList[1]/100.,
        'Q3':SurveyList[2],'Q3_Active':1-NAList[2]/100.,
        'Q4':SurveyList[3],'Q4_Active':1-NAList[3]/100.,
        'Q5':SurveyList[4],'Q5_Active':1-NAList[4]/100.,
        'Q6':SurveyList[5],'Q6_Active':1-NAList[5]/100.,
        'Score':sum(SurveyList)/len(SurveyList)
        }
    print row1
            
    data.append(row1)
    # create a pandas DataFrame from the list of dicts
    data = pd.DataFrame(data)
    '''
    data.set_index(['CourseCode', 'TA_Name', 'ClassSize','NumberOfRespondent',
    'ResponseRate','Q1','Q1_Active','Q2','Q2_Active','Q3','Q3_Active',
    'Q4','Q4_Active','Q5','Q5_Active','Q6','Q6_Active',
    'Score'], inplace=True)
    '''
    #print data
    return 0

if __name__ == '__main__':
    path = 'txt\\summer\\'  # change to the folder containing the pdfs
    # the separator to use with the CSV
    # the distance multiplier after which a character is considered part of a new word/column/block. Usually 1.5 works quite well
    data = []
    for file in os.listdir(path):
        current_file = os.path.join(path, file)
        print txt_to_csv(current_file,data)
    
    data = pd.DataFrame(data)
    data= data[['CourseCode', 'TA_Name', 'ClassSize','NumberOfRespondent',
    'ResponseRate','Q1','Q1_Active','Q2','Q2_Active','Q3','Q3_Active',
    'Q4','Q4_Active','Q5','Q5_Active','Q6','Q6_Active',
    'Score']]
    print data.head()
    print data.columns 
    #writer = ExcelWriter('outputspring.xlsx')
    data.to_csv('summer.csv')
    #writer.save()
    #txt_to_csv('Instructor_Report-CIVL-1100-L1-bwuag_20190614_111537.pdf.txt')