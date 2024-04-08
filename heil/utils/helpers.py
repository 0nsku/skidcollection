import os
import sys

def restart():
    os.execvp(sys.executable, ['python'] + sys.argv)