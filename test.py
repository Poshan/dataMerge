import arcpy
from arcpy import env
import os
import sys
import time

#setting workspace
arcpy.env.workspace = 'F:\\projects\EDMS_merge\data'
rootPathTemp = 'F:\\projects\EDMS_merge\Temp'
rootPathOld = 'F:\\projects\EDMS_merge\old'
rootPathData = 'F:\\projects\EDMS_merge\data'
rootPathMerged = 'F:\\projects\EDMS_merge\merged'
folderList = ['canal', 'commandarea', 'conventionalgroundwaterprojects', 'conventionalsurfareprojects', 'deeptubewell', 'headworks', 'hydrologicalstation', 'meterologicalstation', 'riverbasin']


#timeNow = time.ctime()
#timeNow1 = int(time.time())
#timeNowStr = str(timeNow1)
timeNow = time.strftime("%H-%M-%S")
dateNow = time.strftime("%d-%m-%Y")
timeNowStr = timeNow + '-' + dateNow
textFileName = 'log-' + timeNowStr + '.txt'


file = open(textFileName,'w')
file.write('File Name \t')
file.write('Time \t')
file.write('\n')

#todos
#read through all the files



#merge the data
def merge (dataName):
    print (dataName)
    sys.exit('Lakuri Bhanjyang')
    print ('into the merge')
    oldDataset = os.path.join(rootPathOld, dataName)
    newDataset = dataName
    filesToMerge = [newDataset, oldDataset]
    fileTemporary = os.path.join(rootPathTemp, dataName)
    dataType = ''
    try:
        #merging datasets and storing at temp folder
        arcpy.Merge_management(filesToMerge,fileTemporary,dataType)
        print ('data merged')
    except:
        print('data unable to merge')

    #removing the dataset in old folder
    try:
        filetodelete = oldDataset
        arcpy.Delete_management(filetodelete)
        print ('removed the old dataset')
    except:
        print('data not removed')
    
    
    #copy the file in temp folder to the old folder
    outputFeatureClass = oldDataset
    arcpy.CopyFeatures_management(fileTemporary, outputFeatureClass)

    #copy the file in data folder to the Merged Folder
    #todo
    #create new folder datetime to copy the merged files inside

    mergedFileName = dataName
    mergePath = rootPathMerged + "\Merged" + timeNowStr

    
    if not os.path.exists (mergePath):
        os.makedirs(mergePath)    
    
    mergedFile = os.path.join(mergePath,mergedFileName)
    outputFeatureClass = mergedFile
    arcpy.CopyFeatures_management(newDataset, outputFeatureClass)

    #delete the file in data folder
    fileToDeleteData = newDataset
    arcpy.Delete_management(fileToDeleteData)

    #remove the temp file
    fileToDeleteTemp = fileTemporary
    arcpy.Delete_management(fileToDeleteTemp)
    
    #writing into the log file
    file.write(fileTemporary)
    file.write('\t')
    file.write(timeNow)
    file.write('\n')
    file.close()
    
   
    


#defining the coordinate system
def defineWgs(fc):
    try:
       coordinateSystem ="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"
       dessr = arcpy.Describe(fc)
       srr = dessr.spatialReference.name
       print("Your previous projection: %s" % (srr))

       arcpy.DefineProjection_management(fc, coordinateSystem)
       print("Your process finished...")
    except:
       print("Cant trasform to new projection")

def mutmToWgs(fc):
    print ('transforming')


for folder in folderList:
    url = os.path.join(rootPathData, folder)
    
        
    fcList = arcpy.ListFeatureClasses()
    for fc in fcList:
        desc = arcpy.Describe(fc)
        extend = desc.extent
        name = desc.name
        print name
        spatialReference = desc.spatialReference.name
        dataType = desc.dataType
        #datumName = desc.GCS.datumName    
        #print name
        if (spatialReference == 'Unknown') or (spatialReference == 'unknown'):
            defineWgs(name)
        elif (spatialReference == 'MUTM') or (spatialReference == 'mutm'):
            mutmToWgs(name)
        else:
            print ('data in same coordinate system')
        merge(folder)

        
    
    



    
    
