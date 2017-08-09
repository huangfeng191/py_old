#!/usr/bin/env python
import logging
import sys
import os.path
import platform
import site

for p in sys.path:

    arch = ''
    system = ''

    if os.path.exists( "%s/PlatLib" % p ):

        arch,_ = platform.architecture()

        if arch == '32bit':
            arch = "x86"
        elif arch == '64bit':
            arch = 'x86_64'

        system = platform.system()

        lib = "%s/PlatLib/%s/%s" % (p,system,arch)

        if os.path.exists(lib):
            site.addsitedir(lib)
        else:
            logging.warn("%s does not exists!",lib)
        break

