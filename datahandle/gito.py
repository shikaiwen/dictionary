import sys
import subprocess
from sys import stdin
# https://stackoverflow.com/questions/14457303/python-subprocess-and-user-interaction
# print(sys.argv)
cmdlist = [
    "git add *",
    "git commit -m \"22\" ",
    "git push origin master"
    ]

for i in range(len(cmdlist)):
    exe = cmdlist[i]
    child = subprocess.Popen(exe, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
#    None 好像也是成功
    if(child.returncode != 0 and child.returncode != None):  
        retuple = child.communicate() 
#         print(retuple[0])
#         exit()
#         

# print("$$$$$$$$$$$$$$$ " + str(child.communicate()[0]))
# print("$$$$$$$$$$$$$$$ " + str(child.returncode))

# ress = subprocess.check_output("git add *",stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE,shell=True)
# print(ress)
exit()

if(len(sys.argv) == 1):
    cmdlist = [
        "git add *",
        "git commit -m 'simple commit'",
        "git push"
        ]
    
#     cmd = "git add * \n git commit -m 'simple commit' "
#     cmd = "git status \n"
#     cmd = "ls"
    
    subprocess.call("\n&&".join(cmdlist), shell=False)
    
