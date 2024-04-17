
import openpyxl
from openpyxl import Workbook
import random


nif_check = ['a','b','c','e','f','g','h','j','p','q','r','s','u','v' , 'w' , 'n']

excel = openpyxl.load_workbook("recursos\\NACE.xlsx")

wb = Workbook()

data = []
row = []
nace = []
nif = ['0','1','2','3','4','5','6','7','8','9']
employees =  [" < 10" , "10 - 50" , "50 - 250" , " > 250"]
alias = 1

for x in excel["Hoja 1"]:
    nace.append(x[0].value)
    
    
for data_row in range(20):
    row.append("Company".lower() + str(alias))
    row.append(random.choice(nif_check).capitalize() + "".join(random.choices(nif , k=8)))
    row.append(f"adress{str(alias)}-{str(alias)}-{str(alias + int(random.choice(nif)))}")
    row.append(f"www.web{str(alias)}.com")  
    row.append(f"{row[0]}@{row[3][4:]}")
    row.append(int("9" + ''.join(random.choices(nif , k = 8)) )) 
    row.append("")
    row.append(random.choice(nace))
    row.append(0)
    row.append(0)
    row.append("Pool")
    row.append(random.choice(employees))
    data.append(row)
    
      
    