### sysbenchcpu

sysbenchcpu是采用sysbench benchmark工具，进行cpu性能的测试。

sysbench通过寻找最大素数的方式来测试CPU的性能。

cpu测试的参数 --cpu-max-prime=N N用来指定要寻找最大素数。

另外支持sysbench本身的参数threads，也就是进行测试线程的数量。

测试参数示例 "sysbench --test=cpu --num-threads=1 --cpu-max-prime=20000 run" 
