#!/usr/bin/python

import numpy as np
from subprocess import call

templateDirectory = "/home/bmdoekemeijer/OpenFOAM/bmdoekemeijer-2.4.0/simulationCases/NREL5MW_1turb_template"
mainDestDirectory = "/home/bmdoekemeijer/OpenFOAM/bmdoekemeijer-2.4.0/simulationCases"
		

def replaceLineInSymbFile(filePath,strToReplace,string):
	call("cp -r -L " + filePath + " " + filePath + "_tmp" , shell=True) # Create copy (non-symbolic)
	call("rm -f " + filePath , shell=True) # Remove symbolically linked file 
	call("mv " + filePath + "_tmp " + filePath , shell=True) # Rename copy to true file
	
	# Replace <string> in file
	with open(filePath) as f:
		newText=f.read().replace(strToReplace, string)
	with open(filePath, "w") as f:
		f.write(newText)
		
		
# Setup cases and submit jobs
for pitch in range(-4,5,1):
	folderName = "pitch"+str(pitch)
	jobName    = "ADMR5MW_batch_pitch"+str(pitch)
	destinationFolder = mainDestDirectory+"/"+folderName
	call("cp --preserve=links -r -s " + templateDirectory + " " + destinationFolder, shell=True)
	
	replaceLineInSymbFile(destinationFolder+'/runscript.solve.1','<templ_job_name>', jobName) # job name
	replaceLineInSymbFile(destinationFolder+'/SC_INPUT.txt','<yaw_angle>', '270.0') # yaw angle
	replaceLineInSymbFile(destinationFolder+'/SC_INPUT.txt','<pitch_angle>', str(pitch)) # pitch angle
	call("cd " + destinationFolder + " && qsub runscript.solve.1", shell=True) # submit job to queue