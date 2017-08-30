import subprocess, os

def bashCSSfileSize (file):
	#cssBytes=`/usr/local/bin/masls -al  "$dmss_split" | awk '{print $4}'`
	command = "/usr/local/bin/masls -al " + file + " | awk '{print $4}' "
	retVal=bash (command)
	if retVal[0]==['']:
		return(0)
	else:
		return(retVal[0])
	
def bashCheckSum ( fileCheckSum, fileOutput ):
	command = "sum " + fileCheckSum + " > " + fileOutput
	result=bash (command)
	return(result)
	
def countLinesInFile ( file ):
	non_blank_count = 0

	with open(file) as infp:
		for line in infp:
		   if line.strip():
			  non_blank_count += 1
	return non_blank_count
	
def bash(cmd,cwd=None):
    '''runs a command in the bash shell'''
    #print(cmd)
    retVal = subprocess.Popen(cmd, shell=True, \
        stdout=subprocess.PIPE, cwd=cwd).stdout.read().strip('\n').split('\n')
    if retVal==['']:
        return(0)
    else:
        return(retVal)
        
def bashSplit ( Amount, pathArchive, pathSplit ):
   #split -a 3 -b $splitAmount ${tempTar}$tarFile "${tempSplit}$tarFile.part-"
   command = "split -a 3 -b " + Amount + " " + pathArchive + " " + pathSplit
   result=bash (command)
   return(result)
   
def bashTar ( pathArchive, localDir ):
   #gnutar -cvf  $tempTar$tarFile "$local_dir"
   command = "gnutar -cvf " + pathArchive + " " + localDir
   result=bash (command)
   return(result)
   
def bashMasmkdir ( cssDir, errorFile ):
   #/usr/local/bin/masmkdir -p "${dmss_dir}" 2>${baseError}stderr"
   command = "/usr/local/bin/masmkdir -p " + cssDir
   result=bash (command)
   result=bashMasDirFileexists (cssDir)
   return(result)
   
def bashMasDirFileexists ( cssDir ):
	cssDir = cssDir.rstrip("/")
	basePath = os.path.basename(cssDir) 
	dirPath = os.path.dirname(cssDir)
	command = "/usr/local/bin/masls -1 " + dirPath + " | grep " + basePath
	result=bash (command)
	if isinstance(result, list):
		if result[0] == basePath:
			return 0
		else:
			return 1
	else:
		return 1
		
def bashMasput ( file, cssPath , errorFile ):
	#/usr/local/bin/masput $tempSplit$splitTar  "$dmss_split" 2>${baseTemp}stderr
	command = "/usr/local/bin/masput " + file + " " + cssPath
	basePath = os.path.basename(file) 
	cssSplitPath = cssPath + "/" + basePath
	#print "cssSplitPath:  " + cssSplitPath
	#print "command:  " + command
	result=bash (command)
	result=bashMasDirFileexists (cssSplitPath)
	return(result)