##################################################
#
# ACTS module
#
# Author: Paolo Andreetto, INFN
# Date: Sep 2021
#
##################################################
                                                                                                                                                            
# custom imports
from baseilc import BaseILC
from util import *

import os.path

class ACTS(BaseILC):
    """ Responsible for the ACTS installation process. """
    
    def __init__(self, name, userInput):
        BaseILC.__init__(self, userInput, name, name)

        self.download.gitrepo = name
        self.hasCMakeFindSupport = True

        # required modules
        self.reqmodules = [ "LCIO", "DD4hep" ]
        self.reqfiles = [[
            "lib64/libActsCore.so",
            "lib64/libActsPluginDD4hep.so",
            "lib64/libActsPluginJson.so",
            "lib64/libActsPluginTGeo.so"
        ]]

        self.envcmake["ACTS_BUILD_PLUGIN_DD4HEP"] = "ON"
        self.envcmake["ACTS_BUILD_PLUGIN_JSON"] = "ON"

    def compile(self):
        """ compile ACTS """
        
        os.chdir( self.installPath + "/build" )

        if( self.rebuild ):
            tryunlink( "CMakeCache.txt" )

        # build software
        if( os_system( ". ../build_env.sh ; " + self.genCMakeCmd() + " 2>&1 | tee -a " + self.logfile ) != 0 ):
            self.abort( "failed to configure!!" )

        #if( os_system( ". ../../../init_ilcsoft.sh ; make ${MAKEOPTS} 2>&1 | tee -a " + self.logfile ) != 0 ):
        if( os_system( ". ../build_env.sh ; make ${MAKEOPTS} 2>&1 | tee -a " + self.logfile ) != 0 ):
            self.abort( "failed to compile!!" )

        if( os_system( "make install" ) != 0 ):
            self.abort( "failed to install!!" )

        patch_cmd = "sed -i -e 's|Boost 1.75.0 CONFIG EXACT|Boost 1.75.0 EXACT|g' %s"
        file_to_patch = os.path.join(self.installPath, 'lib64', 'cmake', 'Acts', 'ActsConfig.cmake')
        if( os_system(patch_cmd % file_to_patch) != 0 ):
            print("Cannot patch file %s" % file_to_patch)

    def writeEnv(self, f, checked):
        if( self.name in checked ):
            return
        else:
            checked.append( self.name )

        disclaimer = 2*os.linesep + "#" + 80*'-' + os.linesep
        disclaimer +=  "#" + 5*' ' + self.name + os.linesep + "#" + 80*'-' + os.linesep
        f.write(disclaimer)

        f.write( "# --- additional " + self.name + " commands ------- " + os.linesep )
        f.write( "export LD_LIBRARY_PATH=\"" + self.installPath + "/lib64:$LD_LIBRARY_PATH\"" + os.linesep )

