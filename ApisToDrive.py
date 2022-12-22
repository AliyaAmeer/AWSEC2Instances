from googleapiclient.discovery import build
from ec2 import ec2_instance_types, ec2_offerings_setup, ec2_attributes, ec2_instances_and_attributes
from sheets import create,add_sheet
import pandas as pd
import pygsheets

file = pygsheets.authorize(service_file='cred.json')

instancesResult=ec2_instance_types('us-east-1')
offeringsResult=ec2_offerings_setup('us-east-1')
attributesResult=ec2_attributes()
outputResult=ec2_instances_and_attributes('us-east-1')

df = pd.DataFrame(instancesResult)
df1 = pd.DataFrame(outputResult)
print('Attr&Values with instances')
# print(df1)
df2 = pd.DataFrame(attributesResult)
print('Offerings & attr codes with instances')
# print(df2)
df3 = pd.DataFrame(offeringsResult)
print('Offering details')
# print(df3)

sheetId=create() #Create new spreadsheet
res=add_sheet('sheets',sheetId,'Attribute Assignments') #Add new worksheet to the spreadsheet

wSheet = file.open_by_key(sheetId) #open sheet
#print(wSheet.id)     # Returns id of spreadsheet
print(wSheet.title) # Returns title of spreadsheet
print(wSheet.url) # Returns url of spreadsheet

wks1 = wSheet[0] #Open first worksheet of spreadsheet
wks1.title = 'Offerings' #Rename the 1st worksheet name
wks1.set_dataframe(df3,(1,1), extend=True, escape_formulae=True) #Add dataframe to the worksheet

wks2 = wSheet[1] #Open second worksheet of spreadsheet
wks2.set_dataframe(df1,(1,1), extend=True, escape_formulae=True)