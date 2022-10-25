import csv

invoiceCSV = 'CDW20210101-20210420.csv'
inventoryCSV = 'Inventory-full-2021-04.csv'
invoiceFile = open(invoiceCSV,'r',encoding='utf-8')
inventoryFile = open(inventoryCSV,'r',encoding='utf-8')
inventoryReader = list(csv.reader(inventoryFile))
invoiceReader = list(csv.reader(invoiceFile))
print(len(invoiceReader))
print(invoiceReader[1][27])
missingCount = 0
writeStorage = []
runSep = False


for inventoryCount in range(len(inventoryReader)):
    for invoiceCount in range(len(invoiceReader)):
        if inventoryReader[inventoryCount][0] in invoiceReader[invoiceCount][27]:
            if runSep == False:
                runSep = True
                print('\n------------------------\n')
                
            print('Inventory# ' + str(inventoryCount) + ' Found in row ' + str(invoiceCount))
            
            writeStorage.append([
                                inventoryReader[inventoryCount][0],inventoryReader[inventoryCount][1],
                                invoiceReader[invoiceCount][10],invoiceReader[invoiceCount][28],
                                invoiceReader[invoiceCount][12], invoiceReader[invoiceCount][11],
                                'Atlanta',invoiceReader[invoiceCount][14],invoiceReader[invoiceCount][2],
                                'CDW', invoiceReader[invoiceCount][6],'1'
                                ])
            break
        elif (invoiceCount == (len(invoiceReader)-1)):
            if runSep == True:
                runSep = False
                print('\n------------------------\n')
            missingCount += 1
 
            print('Serial ' + inventoryReader[inventoryCount][0] + ' is missing')
            print('Line#: ' + str(inventoryCount + 1))
            writeStorage.append([inventoryReader[inventoryCount][0],inventoryReader[inventoryCount][1]])
print('total missing: ' + str(missingCount))
with open('invjoiner-out.csv','w',encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(writeStorage)

