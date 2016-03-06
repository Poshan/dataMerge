import arcpy
from arcpy import env
import os
import sys
import time

#settings
arcpy.env.workspace = 'F:\\projects\EDMS_merge\data'
rootPathTemp = 'F:\\projects\EDMS_merge\Temp'
rootPathOld = 'F:\\projects\EDMS_merge\old'
rootPathData = 'F:\\projects\EDMS_merge\data'
rootPathMerged = 'F:\\projects\EDMS_merge\merged'
folderList = ['canal', 'commandarea', 'conventionalgroundwaterprojects', 'conventionalsurfareprojects', 'deeptubewell', 'headworks', 'hydrologicalstation', 'meterologicalstation', 'riverbasin']


#timeNow = time.ctime()
#timeNow1 = int(time.time())
#timeNowStr = str(timeNow1)
timeNow = time.strftime("%H_%M_%S")
dateNow = time.strftime("%d_%m_%Y")
timeNowStr = timeNow + '-' + dateNow
textFileName = 'log-' + timeNowStr + '.txt'


file = open(textFileName,'w')
file.write('File Name \t')
file.write('Time \t')
file.write('\n')


#merge the data
def merge (folderName1, data):
    timeNowStr = timeNow + '_' + dateNow
    print ('into the merge')
    dataName = os.path.join(folderName1, data)
    folderNameShp = folderName1 + '.shp'
    newDataName = os.path.join(folderName1, folderNameShp)
    oldDataset = os.path.join(rootPathOld, newDataName)
    newDataset = os.path.join(rootPathData, dataName)
    filesToMerge = [newDataset, oldDataset]
    fileTemporary = os.path.join(rootPathTemp, newDataName)
    
    #print('newDataName' + newDataName)
    #print('oldDataset' + oldDataset)
    #print('newDataset' + newDataset)
    #print('Temporary ' + fileTemporary)
    
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

    mergedFileName = dataName
    mergePath = rootPathMerged + "\Merged" + timeNowStr

        
    mergedFolder = os.path.join(mergePath,folderName1)
    mergedFile = os.path.join(mergePath,mergedFileName)
    
    print mergedFolder
    print mergedFile

    if not os.path.exists (mergedFolder):
        os.makedirs(mergedFolder)

    tempFileName = timeNowStr + data
    
    outputFeatureClass = mergedFolder +'\Merged_' + tempFileName
    print outputFeatureClass
    

    arcpy.CopyFeatures_management(newDataset, outputFeatureClass)

    #delete the file in data folder
    fileToDeleteData = newDataset
    arcpy.Delete_management(fileToDeleteData)

    #remove the temp file
    fileToDeleteTemp = fileTemporary
    arcpy.Delete_management(fileToDeleteTemp)
    
    #writing into the log file
    file.write(newDataset)
    file.write('\t')
    file.write(timeNow)
    file.write('\n')
    
   
    


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

def mutmToWgs(name):
    #todo
    print ('transforming')
    projected_name = name + '_projected'
    name_project = os.path.join(rootPathData, projected_name)
    arcpy.Project_management(name, name_Project, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", "mutmToWgs", "PROJCS['Everest_Adj_1937_Transverse_Mercator',GEOGCS['GCS_Everest_Adj_1937',DATUM['D_Everest_Adj_1937',SPHEROID['Everest_Adjustment_1937',6377276.345,300.8017]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',84.0],PARAMETER['Scale_Factor',0.9999],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", "NO_PRESERVE_SHAPE", "")
    print ('transformation completed')
    


for folder in folderList:
    url = os.path.join(rootPathData, folder)
    arcpy.env.workspace = url
    fcList = arcpy.ListFeatureClasses()
    for fc in fcList:
        desc = arcpy.Describe(fc)
        extend = desc.extent
        name = desc.name
        print name
        spatialReference = desc.spatialReference.name
        dataType = desc.dataType

        if (spatialReference == 'Unknown') or (spatialReference == 'unknown'):
            defineWgs(name)
            merge(folder,name)
        elif (spatialReference == 'MUTM') or (spatialReference == 'mutm'):
            mutmToWgs(name)
            projected_name = name + '_projected'
            merge(folder, projected_name)
            
        else:
            print ('data in same coordinate system')
            merge(folder,name)
        print ('after merge')
file.close()

        
    
    



    
    
