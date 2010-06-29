# python looks in sys.path when importing modules
# sys.path[0] is the directory containing the script that was used to invoke the Python interpreter (where ilcsoft-install lives)
import sys
sys.path.append( sys.path[0] + '/ilcsoft' )
#sys.path.append( sys.path[0] + '/ilcsoft/simtools' )
#print 'DEBUG: sys.path: ' + str(sys.path)

from ilcsoft import ILCSoft

# core software
from lcio import LCIO
from lccd import LCCD
from gear import GEAR
from raida import RAIDA
from ced import CED

# marlin & friends
from marlinpkg import MarlinPKG
from marlinpkg import ConfigPKG
from marlin import Marlin
from marlinutil import MarlinUtil
from marlinreco import MarlinReco
from cedviewer import CEDViewer
from pandora import PandoraPFA
from pandoranew import PandoraPFANew
from marlinpandora import MarlinPandora
from silicondigi import SiliconDigi
from lcfivertex import LCFIVertex
from eutelescope import Eutelescope
from overlay import Overlay
from marlintpc import MarlinTPC
from ckfit import CKFit

# simtools
#from simtoolsmaker import SimToolsMaker
from simtools import *  # modules defined in simtools/__init__.py

# cmake
from cmake import CMake
from cmakemods import CMakeModules

# external (with install support)
from druid import Druid
from mokka import Mokka
from conddbmysql import CondDBMySQL
from cernlib import CERNLIB
from clhep import CLHEP
from heppdt import HepPDT
from gsl import GSL
from qt import QT
from aidajni import AIDAJNI
from jaida import JAIDA
from dcap import dcap

# external (without install support)
from root import ROOT
from geant4 import Geant4
from java import Java
from mysql import MySQL
