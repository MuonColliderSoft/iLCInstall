##################################################
#
# Digitizer module
#
# Author: P. Andreetto, INFN
# Date: Apr, 2023
#
##################################################

from .baseilc import BaseILC
from .marlinpkg import MarlinPKG

class Digitizer(MarlinPKG):
    """ Responsible for the Digitizer installation process. """

    def __init__(self, userInput):
        MarlinPKG.__init__(self, "Digitizer", userInput )

        self.hasCMakeFindSupport = True

        # required modules
        self.reqmodules = [ "Marlin", "MarlinUtil", "GSL", "DD4hep", "RAIDA" ]

    def postCheckDeps(self):
        BaseILC.postCheckDeps(self)

        # fill MARLIN_DLL
        self.parent.module('Marlin').envpath["MARLIN_DLL"].append(self.installPath + "lib/libMuonCVXDDigitiser.so")
        self.parent.module('Marlin').envpath["MARLIN_DLL"].append(self.installPath + "lib/libMuonCVXDRealDigitiser.so")

