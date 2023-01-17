##################################################
#
# Marlin module
#
# Author: Jan Engels, DESY
# Date: Jan, 2007
#
##################################################

# custom imports
from .baseilc import BaseILC
from .util import *


class Marlin(BaseILC):
    """ Responsible for the Marlin software installation process. """
    
    def __init__(self, userInput):
        BaseILC.__init__(self, userInput, "Marlin", "Marlin")

        self.download.supportedTypes = [ "GitHub" ] 
        self.download.gituser = 'iLCSoft'
        self.download.gitrepo = 'Marlin'

        self.reqfiles = [ ["lib/libMarlin.a", "lib/libMarlin.so", "lib/libMarlin.dylib"], ["bin/Marlin"] ]

        # LCIO is required for building Marlin
        self.reqmodules = [ "LCIO", "GEAR" ]

        # optional modules
        self.optmodules = [ "CLHEP", "LCCD" , "AIDA" ]

        self.envcmake['MARLIN_GUI']='OFF'
    
    def compile(self):
        """ compile Marlin """
        
        os.chdir( self.installPath )

        os.chdir( "build" )

        if( self.rebuild ):
            tryunlink( "CMakeCache.txt" )

        # build software
        if( os_system( self.genCMakeCmd() + " 2>&1 | tee -a " + self.logfile ) != 0 ):
            self.abort( "failed to configure!!" )
        
        if( os_system( ". ../build_env.sh ; make ${MAKEOPTS} 2>&1 | tee -a " + self.logfile ) != 0 ):
            self.abort( "failed to compile!!" )

        if( os_system( ". ../build_env.sh ; make install 2>&1 | tee -a " + self.logfile ) != 0 ):
            self.abort( "failed to install!!" )

        # execute ctests
        if( self.makeTests ):

            if( os_system( "unset MARLIN_DLL && make test" ) != 0 ):
                self.abort( "failed to execute Marlin tests" )


    def preCheckDeps(self):
        BaseILC.preCheckDeps(self)
        if( self.mode == "install" ):
            if self.cmakeBoolOptionIsSet( "MARLIN_GUI" ):
                if( sys.platform != "mac" and sys.platform != "darwin" ):
                    self.addExternalDependency( ["QT"] )
                self.reqfiles.append(["bin/MarlinGUI"])
    
    def postCheckDeps(self):
        BaseILC.postCheckDeps(self)

        self.env["MARLIN"] = self.installPath
        self.envpath["PATH"].append( '$MARLIN/bin' )

        if( self.mode == "install" ):
            # check for QT 4
            if( "QT" in self.reqmodules_external ):
                qt = self.parent.module("QT")
                if( qt != None and Version( qt.version ) < '4.0' ):
                    self.abort( "you need QT 4!! QT version " + qt.version + " found..." )

    def writeEnv(self, f, checked):
        """ helper function used for writing the environment to a file """
        
        # resolve circular dependencies
        if( self.name in checked ):
            return
        else:
            checked.append( self.name )

        if self.env or sum(map(len, self.envpath.values()), 0):
            f.write( 2*os.linesep + "#" + 80*'-' + os.linesep + "#" + 5*' ' \
                    + self.name + os.linesep + "#" + 80*'-' + os.linesep )
        
        # first write the priority values
        for k in self.envorder:
            f.write( "export " + str(k) + "=\"" + str(self.env[k]) + "\"" + os.linesep )
        # then write the rest
        for k, v in self.env.iteritems():
            if k not in self.envorder:
                f.write( "export " + str(k) + "=\"" + str(self.env[k]) + "\"" + os.linesep )
    
        f.write( "# --- additional " + self.name + " commands ------- " + os.linesep ) 
        for c in self.envcmds:
            f.write( c + os.linesep ) 

        # list of "trivial" paths we do not want to add again to PATH and co
        ignorepaths = ['/usr/bin','/usr/lib','/sbin','/usr/sbin']
        # path environment variables
        for k, v in self.envpath.iteritems():
            if( len(v) != 0 ):
                # expand every variable we introduced previously
                exp = str().join(v)
                for e, ev in self.env.iteritems():
                    p = re.compile(r"\$"+str(e)) # compile regular expression to match shell variable
                    exp = p.sub(str(ev), exp)  # replace with expanded variable for absolute path
                # check for match
                if exp in ignorepaths:
                    continue
                path = str.join(':', v)
                if k == "MARLIN_DLL":
                    f.write( "export " + k + "=\"" + path + "\"" + os.linesep )
                else:
                    f.write( "export " + k + "=\"" + path + ":$" + k + "\"" + os.linesep )

        if( len(checked) > 1 ):
            mods = self.optmodules + self.reqmodules
        else:
            # buildonly modules are only written for the package were they are needed
            mods = self.optmodules + self.reqmodules + self.reqmodules_buildonly + self.reqmodules_external
        
        for modname in mods:
            self.parent.module(modname).writeEnv(f, checked)

