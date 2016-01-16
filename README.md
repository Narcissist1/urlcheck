# urlcheck

### 检测一个域名下所有URL的可用性

用法: python check_url.py

#### 各个函数作用
* get_logger()  设置log，文件名格式为LOGfor-domain_in_year-month-day
* urlvalidator() 检查URL合法性
* stop_flag() 边界判定函数，本站的URL有可能外链到其他网址，需要去除
* bfs_path() 主扫描函数，相当于将参数URL作为父节点，该URL下包含的所有合法URL作为子节点，扫描处理过父节点后将所有合法子节点入队列，每次取队列首URL作为参数传入，相当于一个广度优先搜索
* class myThread(threading.Thread) 线程类，采用多线程运行扫描，重写__init__() 和 run() 方法，由于python 队列实现了锁原语，run函数里面的锁主要针对VISITED集合，VISITED集合表示已经处理过的URL，防止重复检查
* main() 主函数，用于设置log，队列等初始化操作，以及建立线程
