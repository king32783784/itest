### sysbenchcpu

sysbenchcpu是采用sysbench benchmark工具，进行cpu性能的测试。

sysbench通过寻找最大素数的方式来测试CPU的性能。

cpu测试的参数 --cpu-max-prime=N N用来指定要寻找最大素数。

另外支持sysbench本身的参数threads，也就是进行测试线程的数量。

测试参数示例 "sysbench --test=cpu --num-threads=1 --cpu-max-prime=20000 run" 

### sysbenchmem



### stream



### iozone

iozone是一个文件系统的benchmark工具，可以测试不同的操作系统中文件系统的读写性能。

测试项目：Read, write, re-read,re-write, read backwards, read strided, fread, fwrite, random read, pread, mmap, aio_read, aio_write

测试参数示例：./iozone -r 32 -s 4g -i 0 -i 1 -i 5 -t 1

注意:

设置的测试文件的大小一定要大过你的内存（最佳为内存的两倍大小）。

itest不支持其自动模式，只支持指定具体参数的测试模式

### lmbench 

lmbench是一个内核性能测试套件。

注：

itest只选取Processor、Context switching、Local communication、File&VMsystem latencies、*Local* Communication bandwidths等５个部分的性能数据。
