#
# framework.py - Handle the modules for weeman
#
# Copyright (c) 2015 by Hypsurus <hypsurus@mail.ru>
#
# See 'LICENSE'  for copying
#

# Python3 print
from __future__ import print_function

import glob
import os
import sys
import importlib
from core.misc import printt
from core.complete import complete
from core.config import __framework_version__

array = ["list", "run", "back", "help", "info"]

class framework(object):
    """ Handle framework modules """
    def __init__(self):
        self.modules = []
        self.modules_folder = "./modules"
        self.o_modules = []
        self.c_modules = 0
    def help(self):
        sys.stdout.write("\033[01;31m")
        print("\trun    - load module.")
        print("\tlist   - list modules.")
        print("\tinfo   - get info for about module.")
        print("\tback   - return to weeman shell.")
        print("\thelp   - we all know (:.\033[00m")

    def print_startup(self, modules_count):
        """
            Print the startup banner for framework
        """
        print("\033[H\033[J") # Clear the screen
        print("\033[01;31m")
        sys.stdout.write(open("core/logo.txt", "r").read()[:-1])
        print("\033[00m") 
        print("\033[01;37m\t   The weeman framework %s | modules: \033[01;31m%d\033[00m" % (__framework_version__, 
            modules_count))
    def shell(self):
        args = None
        # Get all modules
        self.modules_get_list()
        self.print_startup(len(self.o_modules))
        complete(array+self.o_modules)
        
        while True:
            args = raw_input("framework >>> ") or "help"
            args = args.split()
            if args[0] == "list":
                print("\t-----------\n"
                      "\t| modules |\n"
                      "\t-----------\n"
                      "\t-----------------------------------\n"
                      "\t| ID  | Name | Version | Information |")
                for mod in self.o_modules:
                    try:
                        self.c_modules += 1
                        m = importlib.import_module("modules.%s" %(mod))
                    except ImportError:
                        print("\t>> %s - [ERROR ON LOAD]" %(mod))
                    else:
                        print("\t", end="")
                        line = "\t| %d]. %s (%s) - %s\t|" %(self.c_modules, 
                            mod, m.MODULE_VERSION, m.MODULE_DE)
                        _ = len(line)
                        print("-" * _)
                        print(line)
                print("\t", end="")
                print("-" * _)
            elif args[0] == "run":
                try:
                    _ = args[1]
                except IndexError:
                    print("Usage: run [module] [args] ...")
                else:
                    self.module_execute(args)
            elif args[0] == "back" or args[0] == "quit":
                break
            elif args[0] == "info":
                try:
                    _ = args[1]
                except IndexError:
                    print("Usage: info [module]")
                else:
                    self.module_read(_)
            elif args[0] == "help":
                self.help()
            else:
                printt(2, "%s - unknown command" % (args[0]))

    def modules_get_list(self):
        """ Get the modules list from modules/ """
        home = os.getcwd()
        os.chdir(self.modules_folder)
        self.modules = glob.glob("*.py")
        if not self.modules:
            printt(2, "No modules found.")
        else:
            os.chdir(home)
            for module in self.modules:
                module = module.split(".")[0]
                if module == "__init__":
                    continue
                self.o_modules.append(module)

    def module_read(self, module):
        """ Read module information """
        try:
            m = importlib.import_module("modules.%s" % (module)) 
        except ImportError:
            print("Error: cannot load \'%s\' to the framework ..." % (module))
        else:
            try:
                print("name:   : %s" % module)
                print("info    : %s" % m.MODULE_DE)
                print("date    : %s" % m.MODULE_DATE)
                print("version : %s" % m.MODULE_VERSION)
                print("author  : %s" % m.MODULE_AUTHOR)
                print("license : %s" % m.MODULE_LICENSE)
            except IndexError:
                printt(2, "Error: please set all MODULE_* variables for this module.")


    def module_execute(self, args):
        """ Runs the module """
        module = args[1]
        # Wee dont need to check ImportError, we do it in modules_list()
        try:
            m = importlib.import_module("modules.%s" % (module))
            m.main(args)
        except ImportError:
            printt(2, "Cannot load \'%s\' to the framework." % module)
