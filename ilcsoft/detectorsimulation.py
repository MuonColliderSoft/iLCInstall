##################################################
#
# DetectorSimulation module
#
# Author: A. Gianelle, INFN
# Date: Jan, 2023
#
##################################################
               

# custom imports
from .baseilc import BaseILC
from util import *

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

try:
    import simplejson as json
except:
    import json


class DetectorSimulation(BaseILC):
    """ Responsible for the DetectorSimulation installation process. """

    def __init__(self, userInput):
        BaseILC.__init__(self, userInput, "DetectorSimulation", "detector-simulation")
        self.reqfiles = []
        self.hasCMakeBuildSupport = False
        self.hasCMakeFindSupport = False
        self.skipCompile = True
        self.reqmodules = []
        self.download.gitrepo = "detector-simulation"

    def setMode(self, mode):
        BaseILC.setMode(self, mode)
        self.downloadOnly = True
        self.installPath = self.parent.installPath + "/" + self.alias + "/"


    def downloadSources(self):
        """ download sources """
        
        # create install base directory
        trymakedir( os.path.dirname( self.installPath ))
    
        os.chdir( os.path.dirname(self.installPath) )

        if ( self.download.type[:6] == "GitHub" ):
            if self.version =="HEAD" or self.version =="dev" or self.version =="devel" or self.version =="master" or self.download.branch:
                #clone the whole repo into the directory
                branch = 'master' if self.download.branch is None else self.download.branch
                cmd="git clone -b %s https://github.com/%s/%s.git %s" % (branch, self.download.gituser, self.download.gitrepo, self.version)
                print("Executing command:",cmd)
                if os_system( cmd ) != 0:
                    self.abort( "Problems occurred during execution of " + cmd + " [!!ERROR!!]")

                print("Cloning of repository %s/%s into directory %s sucessfully finished" % (self.download.gituser, self.download.gitrepo, self.installPath))

            elif 'message' not in list(json.loads(urlopen('https://api.github.com/repos/%s/%s/git/refs/tags/%s' % (self.download.gituser, self.download.gitrepo, self.version)).read()).keys()):
                cmd = "curl -L -k https://api.github.com/repos/%s/%s/tarball/refs/tags/%s | tar xz --strip-components=1 -C %s" % (self.download.gituser, self.download.gitrepo, self.version, self.installPath)
                if os_system( cmd ) != 0:
                    self.abort( "Could not download and extract tag " + self.version + " [!!ERROR!!]")
                print("Downloading of the tag %s of repository %s/%s into directory %s sucessfully finished" % (self.version, self.download.gituser, self.download.gitrepo, self.installPath))

            else:
                self.abort( "The specified tag " + self.branch + " does not exist [!!ERROR!!]")
 
