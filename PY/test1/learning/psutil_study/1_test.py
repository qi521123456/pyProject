import psutil
import time

time.sleep(0.5)  # 等一下回得出cpu_percent,否则为0.0
# cpu
print(psutil.cpu_times(),psutil.cpu_count(logical=False), psutil.cpu_times_percent(), psutil.cpu_percent())

# 物理内存
print(str(psutil.virtual_memory()))

# 交换区内存、swap内存/虚拟内存/
print(psutil.swap_memory())

# 磁盘
print(psutil.disk_usage('D:/').free / (1024*1024*1024))

