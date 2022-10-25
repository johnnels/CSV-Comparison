import csv

prepCSV = 'Prep Checklist-03.csv'
inventoryCSV = 'Current Active Inventory B.csv'
decomCSV = 'decommed001.csv'
prepFile = open(prepCSV,'r',encoding='utf-8')
inventoryFile = open(inventoryCSV,'r',encoding='utf-8')
decomFile = open(decomCSV,'r',encoding='utf-8')
inventoryReader = list(csv.reader(inventoryFile))
prepReader = list(csv.reader(prepFile))
decomReader = list(csv.reader(decomFile))
decomList = []
for x in range(len(decomReader)):
    decomList.append(decomReader[x][0])

missingCount = 0
missingMon = 0
missingPC = 0
missingLap = 0
missingDock = 0
notRelevant = 0
officeCount = 0
distroCount = 0
decomCount = 0
distroMark = 'Office'
distroModels = ['v19', 'V19', 'V227Q', 'Pro Desk','ProDesk','G5','G2' 'EliteBook','ProBook' ]
distroMark = ''

missingPCStore = []
def appendPCStore():
    missingPCStore.append([inventoryReader[inventoryCount][2], inventoryReader[inventoryCount][8],inventoryReader[inventoryCount][3],
                           inventoryReader[inventoryCount][13],inventoryReader[inventoryCount][14], inventoryReader[inventoryCount][19],
                           inventoryReader[inventoryCount][4],inventoryReader[inventoryCount][7]])
def deptMarker():
    global distroMark
    distroMark = 'Office'
    for x in  range(len(distroModels)):
        if distroModels[x] in inventoryReader[inventoryCount][13]:
            distroMark = 'Distro'
            global distroCount
            distroCount +=1
            break
    if (distroMark == 'Office'):
        global officeCount
        officeCount += 1

def appendStorage(devName):
    user = 'UNASSIGNED'
    if prepReader[prepCount][0] != '':
        user = prepReader[prepCount][0]
    deptMarker()        
    writeStorage.append([
                        inventoryReader[inventoryCount][2], inventoryReader[inventoryCount][8],user,
                        inventoryReader[inventoryCount][3],devName,inventoryReader[inventoryCount][19],
                        inventoryReader[inventoryCount][14],inventoryReader[inventoryCount][13],distroMark,
                        inventoryReader[inventoryCount][4],inventoryReader[inventoryCount][7]
                        ])

writeStorage = []
runSep = False
loadingBar = 1


print('Running!')
print('|         |')
print('|', end="")
for inventoryCount in range(len(inventoryReader)):
    if str(inventoryReader[inventoryCount][2]) in decomList:
        decomCount +=1
        continue
    if inventoryCount >= (len(inventoryReader) / 10) * loadingBar:
        print('-', end="")
        loadingBar +=1
    for prepCount in range(len(prepReader)):
        if prepReader[prepCount][2] == 'n/a' or inventoryReader[inventoryCount][2] == '':
            break
        if inventoryReader[inventoryCount][3] != 'Monitor' and inventoryReader[inventoryCount][3] != 'Laptop' and inventoryReader[inventoryCount][3] != 'Docking Station' and inventoryReader[inventoryCount][3] != 'Workstation':
            notRelevant += 1
            break
                
        if inventoryReader[inventoryCount][2] == prepReader[prepCount][1] and inventoryReader[inventoryCount][3] != 'Monitor':
            appendStorage(prepReader[prepCount][2])
            break
        if inventoryReader[inventoryCount][2] == prepReader[prepCount][1] and inventoryReader[inventoryCount][3] == 'Monitor':
            appendStorage('n/a')
            break
        if inventoryReader[inventoryCount][2] == prepReader[prepCount][5] or inventoryReader[inventoryCount][2] == prepReader[prepCount][6]:
            appendStorage('n/a')
            break
        
        elif (prepCount == (len(prepReader)-1)):
            deptMarker()
            if (distroMark == 'Distro'):
                missingCount += 1
                if inventoryReader[inventoryCount][3] == 'Workstation':
                    appendPCStore()
                    missingPC += 1
                if inventoryReader[inventoryCount][3] == 'Monitor':
                    appendPCStore()
                    missingMon += 1
                if inventoryReader[inventoryCount][3] == 'Laptop':
                    missingLap += 1
                if inventoryReader[inventoryCount][3] == 'Docking Station':
                    missingDock += 1 
            writeStorage.append([
                                inventoryReader[inventoryCount][2], inventoryReader[inventoryCount][8],'UNASSIGNED',
                                inventoryReader[inventoryCount][3],'n/a',inventoryReader[inventoryCount][19],
                                inventoryReader[inventoryCount][14],inventoryReader[inventoryCount][13],distroMark,
                                inventoryReader[inventoryCount][4], inventoryReader[inventoryCount][7]
                                ])
print('|')
print('total irrelevant items: ' + str(notRelevant))
print('Total Missing: ' + str(missingCount))
print('Missing PCs: ' + str(missingPC))
print('Missing monitors: ' + str(missingMon))
print('Missing docks: ' + str(missingDock))
print('Missing laptops: ' + str(missingLap))
print('office items: ' + str(officeCount))
print('distro items: ' + str(distroCount))
print('decommed items: ' + str(decomCount))
print('Finished!')            
with open('inventoryControl-out.csv','w',encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(writeStorage)
with open('missingPC-out.csv','w',encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(missingPCStore)

