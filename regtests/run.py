import os, glob
import subprocess
import filecmp
import argparse
import shutil

def CleanBuildDir(path):
    subprocess.call(['make','-C',path,'clean'])

def BuildExec(path):
    print "Build path = %s"%(path)

    CleanBuildDir(path)
    subprocess.call(['make','-C',path,'-j','12'])

def BuildExecs(rootPath):

    PrintHeader('building geninit')
    BuildExec(os.path.join(rootPath,'init'))

    PrintHeader('building rxmd')
    BuildExec(os.path.join(rootPath,'src'))

def PrintHeader(header):
    print "================================="
    print header
    print "================================="

def Clean(cwdPath,rootPath,regTests):

    srcPath=os.path.join(rootPath,'src')
    initPath=os.path.join(rootPath,'init')
    CleanBuildDir(srcPath)
    CleanBuildDir(initPath)

    for t in regTests:

        PrintHeader(t)

        unitTestPath = os.path.join(cwdPath,t)
        runDir = os.path.join(unitTestPath,'run')
        CleanBuildDir(runDir)

def RunTest(testName):

    logFileName = testName+'.log'
    print "  Running test"
    with open (logFileName, 'w') as output:
        subprocess.call(['make','run'], stdout=output, stderr=output)

def CompareRef(ref,currentRefPath, refPath):

    if(not filecmp.cmp(currentRefPath, refPath)):
        print "    ---------------------------------"
        print "    %s is different: "%(ref)
        print "    ---------------------------------"

        logFilePath = ref +'.log'

        with open(logFilePath,'w') as output:
            subprocess.call(['diff',currentRefPath,refPath],stdout=output)

        if(logFilePath):
            with open(logFilePath,'r') as output:
                print output.read()
    else:
        print "    %s Pass"%(ref)

def UpdateRef(ref,currentRefPath, refPath):
    print "  Copying %s to %s"%(currentRefPath, refPath)
    shutil.copyfile(currentRefPath, refPath)

def RunRegTests(cwdPath,regTests,runTestFunc,runRefFunc):

    for t in regTests:

        PrintHeader(t)

        unitTestPath = os.path.join(cwdPath,t)
        runDir = os.path.join(unitTestPath,'run')
        print "  Entering %s"%(runDir)
        os.chdir(runDir)

        if(runTestFunc):
            runTestFunc(t)
    
        refDir = os.path.join(unitTestPath,'refs')
        refFiles = glob.glob(refDir+'/*')
        print "  refDir = %s "%(refDir)
    
        for refPath in refFiles:
            refName = os.path.basename(refPath) 
            currentRefPath = os.path.join(runDir,'DAT',refName)

            if(runRefFunc):
                runRefFunc(refName,currentRefPath,refPath)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument('-r','--run', help="run all tests.", action="store_true", default=False)
    parser.add_argument('-c','--clean',help="clean up test directories.", action="store_true", default=False)
    parser.add_argument('-u','--update',help="update references.", action="store_true", default=False)
    parser.add_argument('-b','--build',help="build geninit and rxmd that are used in each test.", action="store_true", default=False)

    cwdPath=os.getcwd()
    rootPath=os.path.dirname(os.path.join('..',cwdPath))

    regTests = filter(os.path.isdir, os.listdir(cwdPath))

    args = parser.parse_args()

    if args.clean:
        Clean(cwdPath,rootPath,regTests)

    if args.build:
        BuildExecs(rootPath)

    if args.run:
        RunRegTests(cwdPath,regTests,RunTest,CompareRef)

    if args.update:
        RunRegTests(cwdPath,regTests,False,UpdateRef)
