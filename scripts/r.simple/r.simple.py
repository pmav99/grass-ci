#!/usr/bin/env python

#%module
#% description: Selects values from raster above value of mean plus standard deviation
#% keyword: raster
#% keyword: select
#% keyword: standard deviation
#%end
#%option G_OPT_R_INPUT
#%end
#%option G_OPT_R_OUTPUT
#%end


import sys

import grass.script as gscript
# from grass.exceptions import CalledModuleError


def main():
    options, flags = gscript.parser()
    return 0


if __name__ == "__main__":
    sys.exit(main())
