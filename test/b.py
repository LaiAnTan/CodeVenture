import subprocess
import sys

print(sys.executable)
proc = subprocess.Popen([sys.executable, "/home/notchuasai/shit/test/a.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print (proc.communicate()[0].decode())