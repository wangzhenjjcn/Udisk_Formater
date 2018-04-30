#coding=utf-8
import os,sys,time
    
global  listAllDrivers
global  drivers
global  disks
global  driverList
global  lastDisks
global  lastDriverList
global  originalDriverList
global  originalDiskList
global  diskpartInfo
global  diskPatitonInfo
global  diskType
global  encodenum
diskType="FAT32"
listAllDrivers="fsutil fsinfo drives"
drivers={}
driverList=[]
lastDriverList=[]
originalDriverList=[]
originalDiskList={}
disks={}
diskPatitonInfo={}
encodenum=0
def formartDisk(diskTag):
    global  listAllDrivers
    global  drivers
    global  driverList
    global  lastDriverList
    global  originalDriverList
    print "正在格式化U盘，请稍候".decode('utf-8').encode(sys.getfilesystemencoding())
    listDriverTags="format "+diskTag+": /FS:"+diskType+"/V:/Q/X"
    tagoutput = os.popen(listDriverTags)
    listDriverTagsResault=tagoutput.read()
    if "格式化已完成".decode('utf-8').encode(sys.getfilesystemencoding()) in listDriverTagsResault:
        print "       格式化磁盘".decode('utf-8').encode(sys.getfilesystemencoding())+diskTag+"成功，可以拔出".decode('utf-8').encode(sys.getfilesystemencoding())
        return 1
    else:
        print  "       格式化磁盘".decode('utf-8').encode(sys.getfilesystemencoding())+diskTag+"失败，失败信息如下：".decode('utf-8').encode(sys.getfilesystemencoding())
        print listDriverTagsResault
        return 0
    pass

def isUdisk(diskTag):
    global  listAllDrivers
    global  drivers
    global  disks
    global  driverList
    global  lastDisks
    global  lastDriverList
    global  originalDriverList
    global  originalDiskList
    global  diskpartInfo
    global  diskPatitonInfo
    global  diskType
    print "       正在检测是否为U盘，请稍候".decode('utf-8').encode(sys.getfilesystemencoding())
    readDriversType="fsutil fsinfo driveType "+diskTag+":"
    diskType=os.popen(readDriversType).read()
    drivers[diskTag]=diskType
    if "可移动驱动器".decode('utf-8').encode(sys.getfilesystemencoding()) in diskType:
        return 1
    else:
        return 0
    
def readDrivers():
    global  listAllDrivers
    global  drivers
    global  disks
    global  driverList
    global  lastDisks
    global  lastDriverList
    global  originalDriverList
    global  originalDiskList
    global  diskpartInfo
    global  diskPatitonInfo
    global  diskType
    lastDriverList=driverList
    driverList=[]
    alldriveroutput = os.popen(listAllDrivers)
    allDriversResault=alldriveroutput.read()
    allDriversResault=allDriversResault.split(":")
    for driversname in allDriversResault:
        name=driversname.strip("\\").strip(" ").strip("\n")
        if len(name)==1:
            driverList.append(name)



def readDiskPartitions(diskTag):
    global  listAllDrivers
    global  drivers
    global  disks
    global  driverList
    global  lastDisks
    global  lastDriverList
    global  originalDriverList
    global  originalDiskList
    global  diskpartInfo
    global  diskPatitonInfo
    global  diskType
    diskpatiton_file=open("diskpatiotion"+bytes(diskTag)+".txt","a")
    diskpatiton_file.close()  
    diskpatiton_file=open("diskpatiotion"+bytes(diskTag)+".txt","w")
    diskpatiton_file.write("select disk "+bytes(diskTag)+"\n list partition\nexit\n")
    diskpatiton_file.flush()    
    diskpatiton_file.close()    
    lsAllDiskPatitions="diskpart /s \"diskpatiotion"+bytes(diskTag)+".txt\""
    lsAllDiskPatitionsoutput = os.popen(lsAllDiskPatitions)
    lsAllDiskPatitionsResault=lsAllDiskPatitionsoutput.read()
    diskPatitonInfo[diskTag]=lsAllDiskPatitionsResault
    os.remove("diskpatiotion"+bytes(diskTag)+".txt")
 
def deleteDiskPartitions(diskTag):
    global  listAllDrivers
    global  drivers
    global  disks
    global  driverList
    global  lastDisks
    global  lastDriverList
    global  originalDriverList
    global  originalDiskList
    global  diskpartInfo
    global  diskPatitonInfo
    global  diskType
    readDiskPartitions(diskTag)
    if "这个磁盘上没有显示的分区".decode('utf-8').encode(sys.getfilesystemencoding()) in diskPatitonInfo[diskTag]:
        print ">>>>>>没有检测到分区的存在，可能是新硬盘或者无分区<<<<<<" .decode('utf-8').encode(sys.getfilesystemencoding())
        return 1
    num=0;
    diskPatitonInfos=diskPatitonInfo[diskTag].split("-")[len(diskPatitonInfo[diskTag].split("-"))-1]
    diskPatitonInfos=diskPatitonInfos.split("\n")
    for i in range(0,len(diskPatitonInfos)):
        if "分区".decode('utf-8').encode(sys.getfilesystemencoding()) in diskPatitonInfos[i]:
            adiskInfo=diskPatitonInfos[i].split("分区".decode('utf-8').encode(sys.getfilesystemencoding()))[1]
            adiskInfo=adiskInfo.split(" ".decode('utf-8').encode(sys.getfilesystemencoding()))
            for k in range(0,len(adiskInfo)):
                if len(adiskInfo[k])>0:
                    num=adiskInfo[k].strip("\n").strip(" ")
                    break  
                else:
                    pass
                    continue
            if "扩展的".decode('utf-8').encode(sys.getfilesystemencoding()) in diskPatitonInfos[i]:
                msg= diskPatitonInfos[i]
            else:
                deleteDiskPatiton_file=open("deleteDisk"+bytes(diskTag)+"Partition"+bytes(num)+".txt","a")
                deleteDiskPatiton_file.close()  
                deleteDiskPatiton_file=open("deleteDisk"+bytes(diskTag)+"Partition"+bytes(num)+".txt","w")
                deleteDiskPatiton_file.write("select disk "+bytes(diskTag)+"\n")
                deleteDiskPatiton_file.write("select partition "+bytes(num)+"\n")
                deleteDiskPatiton_file.write("delete partition override\nexit\n")
                deleteDiskPatiton_file.flush()    
                deleteDiskPatiton_file.close() 
                deleteDiskPatiton="diskpart /s \"deleteDisk"+bytes(diskTag)+"Partition"+bytes(num)+".txt\""
                deleteDiskPatitonoutput = os.popen(deleteDiskPatiton)
                deleteDiskPatitonResault=deleteDiskPatitonoutput.read()
                os.remove("deleteDisk"+bytes(diskTag)+"Partition"+bytes(num)+".txt")
                if "成功地删除了所选分区" .decode('utf-8').encode(sys.getfilesystemencoding()) in deleteDiskPatitonResault:
                    print ">>>>>>成功地删除了" .decode('utf-8').encode(sys.getfilesystemencoding())+diskPatitonInfos[i]
                else:
                    print "====================删除失败======================="
                    print deleteDiskPatitonResault
                    print diskPatitonInfos[i]
                    print "====================删除失败======================="
                    deleteDiskPartitions(diskTag)
    for j in range(0,len(diskPatitonInfos)):
        if "分区".decode('utf-8').encode(sys.getfilesystemencoding()) in diskPatitonInfos[j]:
            adiskInfo=diskPatitonInfos[j].split("分区".decode('utf-8').encode(sys.getfilesystemencoding()))[1]
            adiskInfo=adiskInfo.split(" ".decode('utf-8').encode(sys.getfilesystemencoding()))
            for k in range(0,len(adiskInfo)):
                if len(adiskInfo[k])>0:
                    num=adiskInfo[k].strip("\n").strip(" ")
                    break 
            if "扩展的".decode('utf-8').encode(sys.getfilesystemencoding()) in diskPatitonInfos[j]:
                deleteDiskPatiton_file=open("deleteDisk"+bytes(diskTag)+"Partition"+bytes(num)+".txt","a")
                deleteDiskPatiton_file.close()  
                deleteDiskPatiton_file=open("deleteDisk"+bytes(diskTag)+"Partition"+bytes(num)+".txt","w")
                deleteDiskPatiton_file.write("select disk "+bytes(diskTag)+"\n")
                deleteDiskPatiton_file.write("select partition "+bytes(num)+"\n")
                deleteDiskPatiton_file.write("delete partition override\nexit\n")
                deleteDiskPatiton_file.flush()    
                deleteDiskPatiton_file.close() 
                deleteDiskPatiton="diskpart /s \"deleteDisk"+bytes(diskTag)+"Partition"+bytes(num)+".txt\""
                deleteDiskPatitonoutput = os.popen(deleteDiskPatiton)
                deleteDiskPatitonResault=deleteDiskPatitonoutput.read()
                os.remove("deleteDisk"+bytes(diskTag)+"Partition"+bytes(num)+".txt")
                if "成功地删除了所选分区" .decode('utf-8').encode(sys.getfilesystemencoding()) in deleteDiskPatitonResault:
                    print ">>>>>>成功地删除了" .decode('utf-8').encode(sys.getfilesystemencoding())+diskPatitonInfos[j]
                else:
                    print "====================删除失败======================="
                    print deleteDiskPatitonResault
                    print diskPatitonInfos[j]
                    deleteDiskPartitions(diskTag)
            else:
                msg= diskPatitonInfos[j]
   

def creatAndFormartDisk(diskTag):
    global  listAllDrivers
    global  drivers
    global  disks
    global  driverList
    global  lastDisks
    global  lastDriverList
    global  originalDriverList
    global  originalDiskList
    global  diskpartInfo
    global  diskPatitonInfo
    global  diskType
    print ">>>>>>正在创建U盘分区，请稍候".decode('utf-8').encode(sys.getfilesystemencoding())
    num=0
    creatDiskPatiton_file=open("creatDisk"+bytes(diskTag)+"Partition.txt","a")
    creatDiskPatiton_file.close()  
    creatDiskPatiton_file=open("creatDisk"+bytes(diskTag)+"Partition.txt","w") 
    creatDiskPatiton_file.write("select disk "+bytes(diskTag)+"\n")
    creatDiskPatiton_file.write("creat partition primary\nformat fs="+diskType+"  label=\"\" quick\n")
    creatDiskPatiton_file.flush()    
    creatDiskPatiton_file.close() 
    creatDiskPatiton="diskpart /s \"creatDisk"+bytes(diskTag)+"Partition.txt\""
    creatDiskPatitonoutput = os.popen(creatDiskPatiton)
    creatDiskPatitonResault=creatDiskPatitonoutput.read()
    os.remove("creatDisk"+bytes(diskTag)+"Partition.txt")
    if "成功地创建了指定分区" .decode('utf-8').encode(sys.getfilesystemencoding()) in creatDiskPatitonResault:
        print ">>>>>>成功地创建了指定分区并格式化" .decode('utf-8').encode(sys.getfilesystemencoding())
    else:
        print creatDiskPatitonResault
 


def cleanAll(diskTag):
    global  listAllDrivers
    global  drivers
    global  disks
    global  driverList
    global  lastDisks
    global  lastDriverList
    global  originalDriverList
    global  originalDiskList
    global  diskpartInfo
    global  diskPatitonInfo
    global  diskType
    readDiskPartitions(diskTag)
    deleteDiskPatiton_file=open("deleteDisk"+bytes(diskTag)+".txt","a")
    deleteDiskPatiton_file.close()  
    deleteDiskPatiton_file=open("deleteDisk"+bytes(diskTag)+".txt","w")
    deleteDiskPatiton_file.write("select disk "+bytes(diskTag)+"\n")
    deleteDiskPatiton_file.write("clean all\n")
    deleteDiskPatiton_file.flush()    
    deleteDiskPatiton_file.close() 
    deleteDiskPatiton="diskpart /s \"deleteDisk"+bytes(diskTag)+".txt\""
    deleteDiskPatitonoutput = os.popen(deleteDiskPatiton)
    deleteDiskPatitonResault=deleteDiskPatitonoutput.read()
    os.remove("deleteDisk"+bytes(diskTag)+".txt")
    if "成功地删除了所选分区" .decode('utf-8').encode(sys.getfilesystemencoding()) in deleteDiskPatitonResault:
        print ">>>>>>成功地删除了" .decode('utf-8').encode(sys.getfilesystemencoding())
    else:
        print deleteDiskPatitonResault


def checkDisk():
    global  listAllDrivers
    global  drivers
    global  disks
    global  driverList
    global  lastDisks
    global  lastDriverList
    global  originalDriverList
    global  originalDiskList
    global  diskpartInfo
    global  diskPatitonInfo
    global  diskType
    lastDisks=disks
    diskpart_file=open("diskpart.txt","a")
    diskpart_file.close() 
    diskpart_file=open("diskpart.txt","w")
    diskpart_file.write("list disk\n")
    diskpart_file.write("exit\n")
    diskpart_file.flush()    
    diskpart_file.close()    
    lsAllDisks="diskpart /s \"diskpart.txt\""
    lsAllDisksoutput = os.popen(lsAllDisks)
    lsAllDisksResault=lsAllDisksoutput.read()
    diskpartInfo=lsAllDisksResault
    diskpartInfos=diskpartInfo.split("-")[len(diskpartInfo.split("-"))-1]
    disksDiskInfo=diskpartInfos.split("\n".decode('utf-8').encode(sys.getfilesystemencoding()))
    os.remove("diskpart.txt")
    disks={}
    for i in range(0,len(disksDiskInfo)):
        if "磁盘".decode('utf-8').encode(sys.getfilesystemencoding()) in disksDiskInfo[i]:
            if "联机".decode('utf-8').encode(sys.getfilesystemencoding()) in disksDiskInfo[i]:
                adiskInfo=disksDiskInfo[i].split("磁盘".decode('utf-8').encode(sys.getfilesystemencoding()))[1]
                adiskInfo=adiskInfo.split("联机".decode('utf-8').encode(sys.getfilesystemencoding()))[0]
                num=adiskInfo[1].strip(" ").strip("/n")
                disks[num]=disksDiskInfo[i]
 
            if "脱机".decode('utf-8').encode(sys.getfilesystemencoding()) in disksDiskInfo[i]:
                adiskInfo=disksDiskInfo[i].split("磁盘".decode('utf-8').encode(sys.getfilesystemencoding()))[1]
                adiskInfo=adiskInfo.split("脱机".decode('utf-8').encode(sys.getfilesystemencoding()))[0]
                num=adiskInfo[1].strip(" ").strip("/n")
                disks[num]=disksDiskInfo[i]
          

def checkNewDrivers():
    global  listAllDrivers
    global  drivers
    global  disks
    global  driverList
    global  lastDisks
    global  lastDriverList
    global  originalDriverList
    global  originalDiskList
    global  diskpartInfo
    global  diskPatitonInfo
    global  diskType
    output = os.popen(listAllDrivers)
    allDrivers=output.read()
    allDriversListName=allDrivers.split(":")
    for driversname in allDriversListName:
        name=driversname.strip("\\").strip(" ").strip("\n")
        if len(name)==1:
            driverList.append(name)
            originalDriverList.append(name)
    for i in range(0,len(driverList)):
        readDriversType="fsutil fsinfo driveType "+driverList[i].strip("\\").strip(" ")+":"
        drivers[driverList[i].strip("\\").strip(" ")]=os.popen(readDriversType).read()
        pass
    while(1):
        readDrivers()
        for i in range(0,len(disks.keys)):
            if  driverList[i] in lastDriverList:
                if driverList[i] in originalDriverList  :
                    msg="原始驱动器：".decode('utf-8').encode(sys.getfilesystemencoding())+driverList[i]
                elif driverList[i] in  lastDriverList:
                    msg= "旧始驱动器：".decode('utf-8').encode(sys.getfilesystemencoding())+driverList[i]
                else:
                    print driverList[i]
                    print "err"
            else:
                print "新驱动器：".decode('utf-8').encode(sys.getfilesystemencoding())+driverList[i]
                if(isUdisk(driverList[i])):
                    formartDisk(driverList[i])
        for i in range(0,len(lastdisks)):
            if lastDriverList[i] in driverList:
                msg= "旧始驱动器：".decode('utf-8').encode(sys.getfilesystemencoding())+lastDriverList[i]
            else:
                print ">>>>>>你移除了驱动器：".decode('utf-8').encode(sys.getfilesystemencoding())+lastDriverList[i].strip("\n")
        time.sleep(1)



def checkNewDisks():
    global  listAllDrivers
    global  drivers
    global  disks
    global  driverList
    global  lastDisks
    global  lastDriverList
    global  originalDriverList
    global  originalDiskList
    global  diskpartInfo
    global  diskPatitonInfo
    global  diskType
    global  encodenum
    lastDisks=disks
    diskpart_file=open("diskpart.txt","w")
    diskpart_file.write("list disk\n")
    diskpart_file.write("exit\n")
    diskpart_file.flush()    
    diskpart_file.close()    
    lsAllDisks="diskpart /s \"diskpart.txt\""
    lsAllDisksoutput = os.popen(lsAllDisks)
    lsAllDisksResault=lsAllDisksoutput.read()
    diskpartInfo=lsAllDisksResault
    diskpartInfos=diskpartInfo.split("-")[len(diskpartInfo.split("-"))-1]
    disksDiskInfo=diskpartInfos.split("\n".decode('utf-8').encode(sys.getfilesystemencoding()))
    os.remove("diskpart.txt")
    disks={}
    for i in range(0,len(disksDiskInfo)):
        if "磁盘".decode('utf-8').encode(sys.getfilesystemencoding()) in disksDiskInfo[i]:
            if "联机".decode('utf-8').encode(sys.getfilesystemencoding()) in disksDiskInfo[i]:
                adiskInfo=disksDiskInfo[i].split("磁盘".decode('utf-8').encode(sys.getfilesystemencoding()))[1]
                adiskInfo=adiskInfo.split("联机".decode('utf-8').encode(sys.getfilesystemencoding()))[0]
                num=adiskInfo[1].strip(" ").strip("/n")
                disks[num]=disksDiskInfo[i]
                originalDiskList[num]=disksDiskInfo[i]
        
            if "脱机".decode('utf-8').encode(sys.getfilesystemencoding()) in disksDiskInfo[i]:
                adiskInfo=disksDiskInfo[i].split("磁盘".decode('utf-8').encode(sys.getfilesystemencoding()))[1]
                adiskInfo=adiskInfo.split("脱机".decode('utf-8').encode(sys.getfilesystemencoding()))[0]
                num=adiskInfo[1].strip(" ").strip("/n")
                disks[num]=disksDiskInfo[i]
                originalDiskList[num]=disksDiskInfo[i]
    print "------程序已经启动，数据无价谨慎操作！！！！等待驱动器连接>>>>>>".decode('utf-8').encode(sys.getfilesystemencoding()) 
    while(1):
        checkDisk()
        for key in disks.keys():
            if key in lastDisks.keys():
                msg=""
            else:
                value=disks[key]
                readDiskPartitions(key)
                if (bytes(key) in originalDiskList.keys() or int(key) in originalDiskList.keys()) and disks[key]==originalDiskList[key] :
                    print ">>>>>>检测到原始硬盘，等待其他驱动器连接".decode('utf-8').encode(sys.getfilesystemencoding())
                else:
                    if key==0 or key =="0":
                        pass
                        continue
                    print ">>>>>>你插入了新的驱动器：".decode('utf-8').encode(sys.getfilesystemencoding())+disks[key].strip("\n")
 
                    if int(encodenum)==1:   
                        print ">>>>>>开始删除...".decode('utf-8').encode(sys.getfilesystemencoding())
                        deleteDiskPartitions(key)
                        print ">>>>>>开始创建新分区...".decode('utf-8').encode(sys.getfilesystemencoding())
                        creatAndFormartDisk(key)
                        print "======操作完成，可以移除当前驱动器或者插入新的驱动器进行格式化操作\n\n\n".decode('utf-8').encode(sys.getfilesystemencoding())
                    elif int(encodenum)==2:
                        print ">>>>>>开始删除...".decode('utf-8').encode(sys.getfilesystemencoding())
                        deleteDiskPartitions(key)
                        print ">>>>>>开始创建新分区...".decode('utf-8').encode(sys.getfilesystemencoding())
                        creatAndFormartDisk(key)
                        print "======操作完成，可以移除当前驱动器或者插入新的驱动器进行格式化操作\n\n\n".decode('utf-8').encode(sys.getfilesystemencoding())
                    elif int(encodenum)==3:
                        print ">>>>>>开始删除...".decode('utf-8').encode(sys.getfilesystemencoding())
                        deleteDiskPartitions(key)
                        print "======操作完成，可以移除当前驱动器或者插入新的驱动器进行格式化操作\n\n\n".decode('utf-8').encode(sys.getfilesystemencoding())         
                    else:
                        pass
        for key in lastDisks.keys():
            if key in disks.keys():
                msg=""
            else:
                value=lastDisks[key]
                print ">>>>>>你移除了驱动器：".decode('utf-8').encode(sys.getfilesystemencoding())+value.strip("\n")
    
        
        time.sleep(1)
    

print ""                                                                       
print "88b           d88                                                                     ".decode('utf-8').encode(sys.getfilesystemencoding())
print "888b         d888                                                                     ".decode('utf-8').encode(sys.getfilesystemencoding())
print "88`8b       d8'88                                                                     ".decode('utf-8').encode(sys.getfilesystemencoding())
print "88 `8b     d8' 88 8b       d8 ,adPPYYba, 888888888 88       88 8b,dPPYba,  ,adPPYba,  ".decode('utf-8').encode(sys.getfilesystemencoding())
print "88  `8b   d8'  88 `8b     d8' \"\"     `Y8      a8P\" 88       88 88P'   \"Y8 a8P_____88  ".decode('utf-8').encode(sys.getfilesystemencoding())
print "88   `8b d8'   88  `8b   d8'  ,adPPPPP88   ,d8P'   88       88 88         8PP\"\"\"\"\"\"\"  ".decode('utf-8').encode(sys.getfilesystemencoding())
print "88    `888'    88   `8b,d8'   88,    ,88 ,d8\"      \"8a,   ,a88 88         \"8b,   ,aa  ".decode('utf-8').encode(sys.getfilesystemencoding())
print "88     `8'     88     Y88'    `\"8bbdP\"Y8 888888888  `\"YbbdP'Y8 88          `\"Ybbd8\"'  ".decode('utf-8').encode(sys.getfilesystemencoding())
print "                      d8'                                                             ".decode('utf-8').encode(sys.getfilesystemencoding())
print "                     d8'                                                              ".decode('utf-8').encode(sys.getfilesystemencoding())
print ""  
print "WangZhen <wangzhenjjcn@gmail.com> Myazure.org 制作出品 copyright@2018 Myazure.org".decode('utf-8').encode(sys.getfilesystemencoding())                                                                        
print ""  
print "                                    ,adPPYba,  8b,dPPYba,  ,adPPYb,d8  ".decode('utf-8').encode(sys.getfilesystemencoding())
print "                                   a8\"     \"8a 88P'   \"Y8 a8\"    `Y88  ".decode('utf-8').encode(sys.getfilesystemencoding())
print "                                   8b       d8 88         8b       88  ".decode('utf-8').encode(sys.getfilesystemencoding())
print "                            888    \"8a,   ,a8\" 88         \"8a,   ,d88  ".decode('utf-8').encode(sys.getfilesystemencoding())
print "                            888     `\"YbbdP\"'  88          `\"YbbdP\"Y8  ".decode('utf-8').encode(sys.getfilesystemencoding())
print "                                                           aa,    ,88  ".decode('utf-8').encode(sys.getfilesystemencoding())
print "                                                            \"Y8bbdP\"   ".decode('utf-8').encode(sys.getfilesystemencoding())
print ""  
print "数据无价谨慎操作！！！！！！！！此程序享有管理员权限，运行此程序数据丢失概不负责！！".decode('utf-8').encode(sys.getfilesystemencoding())
print ""  
while  int(encodenum)>4 or int(encodenum)<1 :
    print ">>>>>>请输入以下对应数字选择程序功能：".decode('utf-8').encode(sys.getfilesystemencoding()) 
    print "      删除所有分区并以NTFS格式化分区请输入【1】".decode('utf-8').encode(sys.getfilesystemencoding()) 
    print "      删除所有分区并以Fat32格式化分区请输入【2】".decode('utf-8').encode(sys.getfilesystemencoding()) 
    print "      删除所有分区不格式化请输入【3】".decode('utf-8').encode(sys.getfilesystemencoding()) 
    print "      不删除仅以FAT32格式化请输入【4】".decode('utf-8').encode(sys.getfilesystemencoding()) 
    print "      不删除仅以NTFS格式化请输入【5】".decode('utf-8').encode(sys.getfilesystemencoding()) 
    encodenum=raw_input("现在请输入对应数字或者回车，取消请直接关闭！\n".decode('utf-8').encode(sys.getfilesystemencoding()))
    pass
print "！！！！！！数据无价谨慎操作！！！！！！！！程序正在启动！！！！请等待>>>>>>".decode('utf-8').encode(sys.getfilesystemencoding())
time.sleep(1)
checkDisk()
time.sleep(1)
if int(encodenum)==1:
    diskType="NTFS"
    checkNewDisks()
elif int(encodenum)==2:
    diskType="Fat32"
    checkNewDisks()
elif int(encodenum)==3:
    diskType="Fat32"
    checkNewDisks()
elif int(encodenum)==4:
    diskType="NTFS"
    checkNewDrivers()
elif int(encodenum)==5:
    diskType="Fat32"
    checkNewDrivers()
else:
    time.sleep(1)
print "数据无价谨慎操作！！！！！！！！程序已退出！！！！".decode('utf-8').encode(sys.getfilesystemencoding())
sys.exit(0)

 
 
