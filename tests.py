import openpyxl


excel = openpyxl.load_workbook("recursos\\NACE.xlsx")

nace = excel['Hoja 1']['A']

lista_nace = []

for x in nace:
    valor = x.value.split(" - ")
    
    if len(valor[0]) > 1:
        lista_nace.append( valor[0] + " " + valor[1])
    
        
for x in lista_nace:
    print(x)
    
