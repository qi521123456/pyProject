import subprocess

###
# p = subprocess.Popen('dir *.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# #print(p.stdout.readlines())
# for line in p.stdout.readlines():
#     print(line.decode('gb2312')+'---\n')


child = subprocess.Popen('ping -n 5 blog.linuxeye.com ',shell=True)#,stdout=subprocess.PIPE  --控制台信息赋值给child.stdout
#child.kill()
print(child.pid,child.poll() is None)
#child.terminate()
child.wait()

print('parent process')
print(child.pid,child.poll() is None)
print(child.stdin,child.stdout,child.stderr)


# child1 = subprocess.Popen('dir *.py', shell=True,stdout=subprocess.PIPE)
# print(child1.stdout.read())
# #或者child1.communicate()