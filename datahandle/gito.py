import sys
import subprocess

# print(sys.argv)
cmdlist = [
    "git add *",
    "git commit -m \"22\" ",
    "git push"
    ]
for i in range(len(cmdlist)):
    exe = cmdlist[i]
    child = subprocess.Popen(exe, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
#    None 好像也是成功
    if(child.returncode != 0 and child.returncode != None):  
        print(child.communicate()[0])
        exit()
#         

# print("$$$$$$$$$$$$$$$ " + str(child.communicate()[0]))
# print("$$$$$$$$$$$$$$$ " + str(child.returncode))


ress = subprocess.check_output("git add *",stderr=subprocess.STDOUT,shell=True)
print(ress)
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
    
