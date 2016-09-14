-- MySQL dump 10.13  Distrib 5.7.14, for osx10.11 (x86_64)
--
-- Host: localhost    Database: torweb
-- ------------------------------------------------------
-- Server version	5.7.14

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `collectpost`
--

DROP TABLE IF EXISTS `collectpost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `collectpost` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `post_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `collect_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `collectpost_post_id` (`post_id`),
  KEY `collectpost_user_id` (`user_id`),
  CONSTRAINT `collectpost_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`),
  CONSTRAINT `collectpost_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `collectpost`
--

LOCK TABLES `collectpost` WRITE;
/*!40000 ALTER TABLE `collectpost` DISABLE KEYS */;
INSERT INTO `collectpost` VALUES (1,1,3,'2016-09-04 19:52:59'),(2,2,1,'2016-09-10 03:00:03');
/*!40000 ALTER TABLE `collectpost` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `follower`
--

DROP TABLE IF EXISTS `follower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `follower` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `follower_id` int(11) NOT NULL,
  `follow_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `follower_user_id` (`user_id`),
  KEY `follower_follower_id` (`follower_id`),
  CONSTRAINT `follower_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `follower_ibfk_2` FOREIGN KEY (`follower_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `follower`
--

LOCK TABLES `follower` WRITE;
/*!40000 ALTER TABLE `follower` DISABLE KEYS */;
INSERT INTO `follower` VALUES (1,1,2,'2016-09-04 19:31:47'),(2,2,3,'2016-09-04 19:53:23');
/*!40000 ALTER TABLE `follower` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `opt` int(11) NOT NULL,
  `msg` varchar(71) NOT NULL,
  `extra_user_id` int(11) DEFAULT NULL,
  `extra_post_id` int(11) DEFAULT NULL,
  `extra_post_reply_id` int(11) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notification_user_id` (`user_id`),
  KEY `notification_extra_user_id` (`extra_user_id`),
  KEY `notification_extra_post_id` (`extra_post_id`),
  KEY `notification_extra_post_reply_id` (`extra_post_reply_id`),
  CONSTRAINT `notification_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `notification_ibfk_2` FOREIGN KEY (`extra_user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `notification_ibfk_3` FOREIGN KEY (`extra_post_id`) REFERENCES `post` (`id`),
  CONSTRAINT `notification_ibfk_4` FOREIGN KEY (`extra_post_reply_id`) REFERENCES `postreply` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification`
--

LOCK TABLES `notification` WRITE;
/*!40000 ALTER TABLE `notification` DISABLE KEYS */;
INSERT INTO `notification` VALUES (1,2,1,'发表新文章',1,1,NULL,'2016-09-04 19:31:47',0),(2,2,2,'发表新评论',1,4,4,'2016-09-09 20:11:54',0),(3,2,1,'发表新文章',1,6,NULL,'2016-09-11 03:39:35',0),(4,2,2,'发表新评论',1,2,5,'2016-09-12 02:37:29',0);
/*!40000 ALTER TABLE `notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post`
--

DROP TABLE IF EXISTS `post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  `create_time` datetime NOT NULL,
  `latest_reply_user_id` int(11) DEFAULT NULL,
  `latest_reply_time` datetime DEFAULT NULL,
  `visit_count` int(11) NOT NULL,
  `reply_count` int(11) NOT NULL,
  `collect_count` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `post_topic_id` (`topic_id`),
  KEY `post_user_id` (`user_id`),
  KEY `post_latest_reply_user_id` (`latest_reply_user_id`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`topic_id`) REFERENCES `posttopic` (`id`),
  CONSTRAINT `post_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `post_ibfk_3` FOREIGN KEY (`latest_reply_user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
INSERT INTO `post` VALUES (1,1,'SICP换零钱(递归转尾递归)','\n<pre><code>\n\n/*\n * =====================================================================================\n *\n *  Filename:  p26.c\n *\n *  Description: change money\n *\n *  Version:  1.0\n *  Created:  2016/08/02 14时58分22秒\n *  Revision:  none\n *  Compiler:  gcc\n *\n *  Author:  jmpews (jmpews.github.io), jmpews@gmail.com\n *\n * =====================================================================================\n */\n\n\n#include &lt;stdlib.h&gt;\n#include &lt;stdio.h&gt;\n#include &lt;string.h&gt;\nint count_change(int amount);\nint cc(int amount, int kinds_of_coins);\nvoid count_iter(int *tmp, int t, int amount);\nint get_coin(int index_of_coin);\nint get_index_tmp(int index_of_coin);\nint *get_tmp_array(int kinds_of_coins);\nint get_recycle_value(int index_of_coin, int current_amount, int *tmp_array);\nvoid update_recycle_value(int index_of_coin, int *tmp_array, int value);\n\nint main ( int argc, char *argv[] )\n{\n    int t;\n    t = count_change(100);\n    printf(&quot;%d&quot;, t);\n    return EXIT_SUCCESS;\n}               /* ----------  end of function main  ---------- */\n\nint count_change(int amount) {\n    cc(amount, 5);\n    return 0;\n}\n\nint cc(int amount, int kinds_of_coins) {\n    int *tmp = get_tmp_array(kinds_of_coins);\n    int t = 0;\n    tmp[0] = 0;\n    count_iter(tmp, t, amount);\n    return 0;\n}\n\n// 这里这里也是关键点，这个尾递归的结束由t(当前需要兑换的金钱)和amount(需要兑换的目标金钱)控制，为线性，也就是说时间复杂度为O(n)\nvoid count_iter(int *tmp, int t, int amount) {\n    int r;\n    r = get_recycle_value(1, t, tmp);\n    update_recycle_value(1, tmp, r);\n\n    //C2(t) = C2(t-get_coin(2)) + C1(t)\n    r = get_recycle_value(2, t, tmp) + r;\n    update_recycle_value(2, tmp, r);\n\n    //C3(t) = C3(t-get_coin(3)) + C2(t)\n    r = get_recycle_value(3, t, tmp) + r;\n    update_recycle_value(3, tmp, r);\n\n    //C4(t) = C4(t-get_coin(4)) + C3(t)\n    r= get_recycle_value(4, t, tmp) + r;\n    update_recycle_value(4, tmp, r);\n\n    //C5(t) = C5(t-get_coin(5)) + C4(t)\n    r = get_recycle_value(5, t, tmp) + r;\n    if(t == amount) {\n        printf(&quot;final-value: %d\n&quot;, r);\n        exit(1);\n    }\n    update_recycle_value(5, tmp, r);\n\n    count_iter(tmp, t+1, amount);\n}\n\nint get_coin(int index_of_coin) {\n    switch(index_of_coin) {\n        case 1: return 1;\n        case 2: return 5;\n        case 3: return 10;\n        case 4: return 25;\n        case 5: return 50;\n        default: exit(1);\n    }\n}\n\n// 对于C1、C2、C3、C4、C5缓存队列开始的位置\nint get_index_tmp(int index_of_coin) {\n    switch(index_of_coin) {\n        case 1: return 0;\n        case 2: return 1;\n        case 3: return 6;\n        case 4: return 16;\n        case 5: return 41;\n        default: exit(1);\n    }\n}\n\n// 分配固定的缓存, 无论需要兑换多少金钱，只要金币种类不变，缓存的大小就是固定的。 空间复杂度为常量。\n// &quot;因为它的状态能由其中的三个状态变量完全刻画，解释器在执行 这一计算过程时，只需要保存这三个变量的轨迹就足够了&quot; 这句话在这里就有体现了\nint *get_tmp_array(int kinds_of_coins) {\n    int *tmp;\n    int i;\n    int sum = 0;\n    for(i=1 ; i&lt;kinds_of_coins ; i++) {\n        sum += get_coin(i);\n    }\n    tmp = (int *)malloc(sizeof(int) * sum);\n    memset(tmp, 0 ,sizeof(int) * sum);\n    return tmp;\n}\n\n// 获取重复利用值, 每次缓存队列头的位置\n// 比如: 此时缓存队列为[C2(0), C2(1), C2(2), C2(3), C2(4)]\n// C2(5) = C1(5) + C2(0) 此时我们需要取缓存队列头的值C2(0)\n// 计算完得到C2(5)，需要执行update_recycle_value将得到C2(5)进队列，除去旧的C2(0)，此时队列头尾C2(1)，即为计算C2(6)需要的缓存值\nint get_recycle_value(int index_of_coin, int current_amount, int *tmp_array) {\n    int t = get_index_tmp(index_of_coin);\n    if(current_amount &lt; get_coin(index_of_coin)){\n        return 0;\n    }\n    else if(current_amount == get_coin(index_of_coin)){\n        return 1;\n    }\n    else {\n        return tmp_array[t];\n    }\n}\n\n// 更新重复利用值(队列的概念), 计算出最新的值，需要替换旧的利用值\n// 比如: C2(5) = C1(5) + C2(0)\n// 现在C2缓存队列中有[C2(0), C2(1), C2(2), C2(3), C2(4)]，我们需要将C2(5)进队列，[C2(1), C2(2), C2(3), C2(4), C2(5)]\nvoid update_recycle_value(int index_of_coin, int *tmp_array, int value) {\n    int i;\n    int t = get_index_tmp(index_of_coin);\n    for(i = 0; i&lt; (get_coin(index_of_coin)-1); i++) {\n        tmp_array[t+i] = tmp_array[t+i+1];\n    }\n    tmp_array[t+get_coin(index_of_coin)-1] = value;\n}\n\n</code></pre>\n',1,'2016-09-04 19:31:47',3,'2016-09-04 19:52:39',15,2,0),(2,1,'Tornado非阻塞机制中Future、IOLoop、Coroutine配合使用','<p>首先需要明确的，tornado中异步是建立在事件循环机制之上，也就是IoLoop。</p>\n\n<p>先举一个正常的例子</p>\n\n<pre><code>from tornado.httpclient import AsyncHTTPClient\nfrom tornado import gen\nimport tornado.ioloop\n\n@gen.coroutine\ndef fetch_coroutine(url):\n    http_client = AsyncHTTPClient()\n    response = yield http_client.fetch(url)\n    print(response)\nfetch_coroutine(&#39;http://jmpews.com&#39;)\ntornado.ioloop.IOLoop.instance().start()\n</code></pre>\n\n<p>伪代码例子</p>\n\n<pre><code>def work():\n  future = Future()\n  ioloop.add_result_callback(future.set_result(&#39;result)) // 触发ioloop响应结果时，设置future状态为完成\n  return future\n\ndef coroutine():\n  def wrap_func(func):\n    d = func()\n    result = next(d) //future\n    future.add_done_callback(d.send(result)) // 设置当future状态为完成时，触发send来恢复协程，继续执行func。\n    \n@coroutine\ndef func():\n  print(&#39;step in&#39;)\n  result = yield work()\n  print(&#39;step out&#39;)\n</code></pre>\n\n<h2 id=\"toc_0\">yield : 异步协程同步写法，配合@tornado.gen.coroutine</h2>\n\n<hr/>\n\n<p>yield，有两个作用，一个是用于挂起当前函数(yield)，第二个可以相当于封装后的callback(yield send)，只不过它的callback是<code>generator.send(&#39;result&#39;)</code>，用于恢复挂起函数继续执行。这里需要注意的是，我们需要在挂起当前函数时注册事件循环机制的响应callback为<code>generator.send(&#39;result&#39;)</code>。</p>\n\n<p>所以，使用yield的第一个问题就是，在哪里设置的<code>generator.send(&#39;result&#39;)</code>。这里以<code>AsyncHTTPClient</code>为例。</p>\n\n<h2 id=\"toc_1\">Future : 连接ioloop和yield</h2>\n\n<p>提供<code>set_result</code>和<code>set_done</code>方法，来触发Future上的callback，其中的callback包含<code>Runner.run()</code> ，实质为 <code>generator.send(&#39;result&#39;)</code>，也就是在yield中必须要明确的在哪里设置<code>generator.send(&#39;result&#39;)</code>。</p>\n\n<h2 id=\"toc_2\">IOLoop : 调度center</h2>\n\n<p>注册响应事件的callback为Future的<code>set_restult()</code>，等待事件触发</p>\n\n<h2 id=\"toc_3\">这里以<code>AsyncHTTPClient</code>为例分析整个流程</h2>\n\n<pre><code># 文件信息: tornado.httpclient\n# 涉及到类名: AsyncHTTPClient\n# 涉及到函数名: fetch\n\ncode ignore...\n\n从这段代码得到函数执行流程: \nfetch\nfetch_impl(request, handle_response)\nhandle_response(response)\nfuture.set_result(response)\n\n\n额外执行流程为:\n\nfuture.add_done_callback(handle_future)\n</code></pre>\n\n<hr/>\n\n<pre><code># 文件信息: tornado.concurrent\n# 涉及到类名: Future \n# 涉及到函数名: add_done_callback, set_result, _set_done\n\ncode ignore...\n\n从这段代码得到函数执行流程: \n\nset_result(self, result)\n|\n_set_done(self)\n|\nfor cb in self._callbacks: cb(self)\n\n额外信息执行流程为:\n\nadd_done_callback(self, fn)\n|\nself._callbacks.append(fn)\n</code></pre>\n\n<hr/>\n\n<pre><code># 文件信息: tornado.gen\n# 涉及到函数名: coroutine, _make_coroutine_wrapper\n\ncode ignore...\n\n#从这段代码可以得到函数执行流程: \n\n_make_coroutine_wrapper(func, replace_callback=True)\n|\nresult = func(*args, **kwargs)\n|\nyielded = next(result)\n|\nRunner(result, future, yielded)\n</code></pre>\n\n<hr/>\n\n<pre><code># 文件信息: tornado.gen\n# 涉及到类名: Runner\n# 涉及到函数名: __init__, handle_yield, run\n\ncode ignore...\n\n从这段代码可以得到函数执行流程: \n\n__init__(self, gen, result_future, first_yielded)\n|\nself.handle_yield(first_yielded)\n|\nself.io_loop.add_future(self.future, lambda f: self.run())\n</code></pre>\n\n',3,'2016-09-04 19:55:23',1,'2016-09-12 02:37:29',41,1,0),(3,3,'DES_CFB_64加解密算法的C语言实现','<p>看过一个搞二进制的哥们把99宿舍的搞定了加密解密方式。用的是<code>des_cfb64</code>加密的方式，但是用了几个python加密库都不对，就尝试自己给python写了一个模块，用的是openssl的lib</p>\n\n<h3 id=\"toc_0\">核心的加密解密模块</h3>\n\n<pre><code>#pycet.c\n#include &quot;Python.h&quot;\n#include &lt;stdio.h&gt;\n#include &lt;string.h&gt;\n#include &lt;stdlib.h&gt;\n#include &lt;openssl/des.h&gt;\n\nchar * Encrypt( char *Key, char *Msg, int size);\nchar * Decrypt( char *Key, char *Msg, int size);\nstatic PyObject *SpamError;\n\nstatic PyObject *\ncet_des_cfb64(PyObject *self,PyObject *args)\n{\n    unsigned char * txt;\n    unsigned int length;\n    unsigned char * key;\n    unsigned int C;\n    char * r;\n    int i=0;\n    PyObject *result;\n\n    //接受python参数\n    if(!PyArg_ParseTuple(args,&quot;s#sI&quot;,&amp;txt,&amp;length,&amp;key,&amp;C))\n    {\n        return NULL;\n    }\n\n    //分配result_buffer\n    r = malloc(length);\n\n    //加密和解密\n    if(C)\n        memcpy(r, Encrypt(key, txt, length), length);\n    else\n        memcpy(r, Decrypt(key, txt, length), length);\n\n\n    //保存成python结果\n    result = PyBytes_FromStringAndSize(r,length);\n\n    //释放malloc\n    free(r);\n    return result;\n}\n\n// 安装约定部分\n//\nstatic PyMethodDef SpamMethods[]={\n    {&quot;cetdes&quot;,cet_des_cfb64,METH_VARARGS,&quot;cet_des_cfb64&quot;},\n    {NULL,NULL,0,NULL}\n};\n\nstatic struct PyModuleDef spammodule = {\n    PyModuleDef_HEAD_INIT,\n    &quot;cetdes&quot;,\n    NULL,\n    -1,\n    SpamMethods\n};\nPyMODINIT_FUNC\nPyInit_cetdes(void)\n{\n    PyObject *m;\n    m = PyModule_Create(&amp;spammodule);\n    if(m==NULL)\n        return NULL;\n    SpamError = PyErr_NewException(&quot;cetdes.error&quot;,NULL,NULL);\n    Py_INCREF(SpamError);\n    PyModule_AddObject(m,&quot;error&quot;,SpamError);\n    return m;\n}\n\n//des_cfb64_encrypt\nchar *\nEncrypt( char *Key, char *Msg, int size)\n{\n\n    static char*    Res;\n    int             n=0;\n    DES_cblock      Key2;\n    DES_key_schedule schedule;\n\n    Res = ( char * ) malloc( size );\n\n    /* Prepare the key for use with DES_cfb64_encrypt */\n    memcpy( Key2, Key,8);\n    DES_set_odd_parity( &amp;Key2 );\n    DES_set_key_checked( &amp;Key2, &amp;schedule );\n\n    /* Encryption occurs here */\n    DES_cfb64_encrypt( ( unsigned char * ) Msg, ( unsigned char * ) Res,\n               size, &amp;schedule, &amp;Key2, &amp;n, DES_ENCRYPT );\n\n     return (Res);\n}\n\n//des_cfb64_decrypt\nchar *\nDecrypt( char *Key, char *Msg, int size)\n{\n\n    static char*    Res;\n    int             n=0;\n\n    DES_cblock      Key2;\n    DES_key_schedule schedule;\n\n    Res = ( char * ) malloc( size );\n\n    /* Prepare the key for use with DES_cfb64_encrypt */\n    memcpy( Key2, Key,8);\n    DES_set_odd_parity( &amp;Key2 );\n    DES_set_key_checked( &amp;Key2, &amp;schedule );\n\n    /* Decryption occurs here */\n    DES_cfb64_encrypt( ( unsigned char * ) Msg, ( unsigned char * ) Res,\n               size, &amp;schedule, &amp;Key2, &amp;n, DES_DECRYPT );\n\n    return (Res);\n\n}\n</code></pre>\n\n<h3 id=\"toc_1\">安装模块</h3>\n\n<pre><code>#setup.py\nfrom distutils.core import setup,Extension\nmoduleone=Extension(&#39;cetdes&#39;,\n        sources=[&#39;pycet.c&#39;],\n        include_dirs=[&#39;/usr/local/opt/openssl/include&#39;],\n        library_dirs=[&#39;/usr/local/opt/openssl/lib&#39;],\n        libraries = [&#39;crypto&#39;]\n        )\nsetup(name=&#39;cetdes&#39;,\n    version=&#39;1.0&#39;,\n    description=&#39;This is cetdes&#39;,\n    ext_modules=[moduleone]\n)\n</code></pre>\n\n<p>链接<code>-lcrypto</code>库,LIB: <code>-L/usr/local/opt/openssl/lib</code>,INCLUDE: <code>-I/usr/local/opt/openssl/include</code></p>\n\n<h3 id=\"toc_2\">参考链接</h3>\n\n<p>[Extending Python with C or C++(官方)] <a href=\"https://docs.python.org/3.5/extending/extending.html\">https://docs.python.org/3.5/extending/extending.html</a></p>',3,'2016-09-04 20:07:51',3,'2016-09-04 20:09:12',12,1,0),(4,3,'SICP零钱置换','<p>递归和迭代的转化，关键需要明确哪些是递归的冗余数据，也就说哪些是迭代可以重复利用数据。下面具体分析。</p>\n\n<p>给不同的coin分配索引</p>\n\n<pre><code>(define (first-denomination kinds-of-coins)\n    (cond ((= kinds-of-coins 1) 1)\n        ((= kinds-of-coins 2) 5)\n        ((= kinds-of-coins 3) 10)\n        ((= kinds-of-coins 4) 25)\n        ((= kinds-of-coins 5) 50)))\n\n</code></pre>\n\n<h3 id=\"toc_0\">递归的思路</h3>\n\n<p>将总数为a的现金换成n种硬币的不同方式的数目等于</p>\n\n<ol>\n<li>将现金a换成除第一种硬币以外的其他硬币的不同方式，加上2</li>\n<li>将现金a－d换成所有种类硬币的不同方式。其中d为第一种硬币的面值。</li>\n</ol>\n\n<p>可以写递归公式</p>\n\n<p><code>Ct(N) = Ct(N-first-denomination(t)) + Ct-1(N)</code></p>\n\n<p>t(下标)为几种硬币，N为现金数。例如：t为5，N为100美分，所以总数目=(将100美分换成1,5,10,25这四种硬币组成方法数)+(将100-50美分换成1,5,10,25,50这五种硬币组成的方法数)</p>\n\n<p>通过公式进行初步运算，渐渐会发现冗余数据(重复利用的数据)</p>\n\n<pre><code>C5(100)=C4(100)+C5(50)\n    C4(100)==C3(100)+C4(75)\n        C3(100)=C2(100)+C3(90)\n            C2(100)=C1(100)+C2(95)\n                C2(95)=C1(95)+C2(90)\n                    C2(90)=C1(90)+C2(85)\n                        C2(85)=C1(85)+C2(80)\n                            C2(80)=C1(80)+C2(75)\n                                C2(75)=C1(75)+C2(70)\n                                    ...\n            # C2(90) 重复\n            C3(90)=C2(90)+C3(80)\n                # C2(80) 重复\n                C3(80)=C2(80)+C3(70)\n                    # C2(70) 重复\n                    C3(70)=C2(70)+C3(60)\n                        ...\n        C4(75)=C3(75)+C4(50)\n            C3(75)=C2(75)+C3(65)\n                ...\n            C4(50)=C3(50)+C4(25)\n                ...\n    C5(50)=C4(50)+C5(0)\n        C5(50)=C4(50)+C5(0)\n            ...\n</code></pre>\n\n<p>上面可能不太直观</p>\n\n<pre><code>C2(4) = C1(4) + C2(-1)\nC2(5) = C1(5) + C2(0)\nC2(6) = C1(6) + C2(1)\nC2(7) = C1(7) + C2(2)\nC2(8) = C1(8) + C2(3)\nC2(9) = C1(9) + C2(4) //出现重复利用值C2(4) 间隔为5\nC2(10) = C1(10) + C2(5) //出现重复利用值C2(5) 间隔为5\nC2(11) = C1(11) + C2(6)\nC2(12) = C1(12) + C2(7)\nC2(13) = C1(13) + C2(8)\nC2(14) = C1(14) + C2(9)\nC2(15) = C1(15) + C2(10)\nC2(16) = C1(16) + C2(11)\n\n\nC3(4) = C2(4) + C3(-6)\nC3(5) = C2(5) + C3(-5)\nC3(6) = C2(6) + C3(-4)\nC3(7) = C2(7) + C3(-3)\nC3(8) = C2(8) + C3(-2)\nC3(9) = C2(9) + C3(-1)\nC3(10) = C2(10) + C3(0)\nC3(11) = C2(11) + C3(1)\nC3(12) = C2(12) + C3(2)\nC3(13) = C2(13) + C3(3)\nC3(14) = C2(14) + C3(4) //出现重复利用值C3(4) 间隔为10\nC3(15) = C2(15) + C3(5) //出现重复利用值C3(5) 间隔为10\nC3(16) = C2(16) + C3(6)\n</code></pre>\n\n<p><strong>所以对于C2来说，始终需要缓存5个可以重复利用值(长度为5的缓存队列);对于C3，始终需要缓存10个可以重复利用值(长度为10的缓存队列);对于C4，使用需要缓存25个(...);对于C5来说，使用需要缓存50个可以重复利用值(...)</strong></p>\n\n<h3 id=\"toc_1\">迭代思路</h3>\n\n<ol>\n<li>迭代是线性O(n)时间+常量空间消耗(不会随n改变)</li>\n<li>迭代需要<strong>重复利用</strong>递归产生的冗余数据.</li>\n<li>迭代的状态能由这些变量完全刻画</li>\n</ol>\n\n<p>假设有5种硬币，现金100美分</p>\n\n<p>C 源码</p>\n\n<pre><code>/*\n * =====================================================================================\n *\n *  Filename:  p26.c\n *\n *  Description: change money\n *\n *  Version:  1.0\n *  Created:  2016/08/02 14时58分22秒\n *  Revision:  none\n *  Compiler:  gcc\n *\n *  Author:  jmpews (jmpews.github.io), jmpews@gmail.com\n *\n * =====================================================================================\n */\n\n\n#include &lt;stdlib.h&gt;\n#include &lt;stdio.h&gt;\n#include &lt;string.h&gt;\nint count_change(int amount);\nint cc(int amount, int kinds_of_coins);\nvoid count_iter(int *tmp, int t, int amount);\nint get_coin(int index_of_coin);\nint get_index_tmp(int index_of_coin);\nint *get_tmp_array(int kinds_of_coins);\nint get_recycle_value(int index_of_coin, int current_amount, int *tmp_array);\nvoid update_recycle_value(int index_of_coin, int *tmp_array, int value);\n\nint main ( int argc, char *argv[] )\n{\n    int t;\n    t = count_change(100);\n    printf(&quot;%d&quot;, t);\n    return EXIT_SUCCESS;\n}               /* ----------  end of function main  ---------- */\n\nint count_change(int amount) {\n    cc(amount, 5);\n    return 0;\n}\n\nint cc(int amount, int kinds_of_coins) {\n    int *tmp = get_tmp_array(kinds_of_coins);\n    int t = 0;\n    tmp[0] = 0;\n    count_iter(tmp, t, amount);\n    return 0;\n}\n\n// 这里这里也是关键点，这个尾递归的结束由t(当前需要兑换的金钱)和amount(需要兑换的目标金钱)控制，为线性，也就是说时间复杂度为O(n)\nvoid count_iter(int *tmp, int t, int amount) {\n    int r;\n    r = get_recycle_value(1, t, tmp);\n    update_recycle_value(1, tmp, r);\n\n    //C2(t) = C2(t-get_coin(2)) + C1(t)\n    r = get_recycle_value(2, t, tmp) + r;\n    update_recycle_value(2, tmp, r);\n\n    //C3(t) = C3(t-get_coin(3)) + C2(t)\n    r = get_recycle_value(3, t, tmp) + r;\n    update_recycle_value(3, tmp, r);\n\n    //C4(t) = C4(t-get_coin(4)) + C3(t)\n    r= get_recycle_value(4, t, tmp) + r;\n    update_recycle_value(4, tmp, r);\n\n    //C5(t) = C5(t-get_coin(5)) + C4(t)\n    r = get_recycle_value(5, t, tmp) + r;\n    if(t == amount) {\n        printf(&quot;final-value: %d\\n&quot;, r);\n        exit(1);\n    }\n    update_recycle_value(5, tmp, r);\n\n    count_iter(tmp, t+1, amount);\n}\n\nint get_coin(int index_of_coin) {\n    switch(index_of_coin) {\n        case 1: return 1;\n        case 2: return 5;\n        case 3: return 10;\n        case 4: return 25;\n        case 5: return 50;\n        default: exit(1);\n    }\n}\n\n// 对于C1、C2、C3、C4、C5缓存队列开始的位置\nint get_index_tmp(int index_of_coin) {\n    switch(index_of_coin) {\n        case 1: return 0;\n        case 2: return 1;\n        case 3: return 6;\n        case 4: return 16;\n        case 5: return 41;\n        default: exit(1);\n    }\n}\n\n// 分配固定的缓存, 无论需要兑换多少金钱，只要金币种类不变，缓存的大小就是固定的。 空间复杂度为常量。\n// &quot;因为它的状态能由其中的三个状态变量完全刻画，解释器在执行 这一计算过程时，只需要保存这三个变量的轨迹就足够了&quot; 这句话在这里就有体现了\nint *get_tmp_array(int kinds_of_coins) {\n    int *tmp;\n    int i;\n    int sum = 0;\n    for(i=1 ; i&lt;kinds_of_coins ; i++) {\n        sum += get_coin(i);\n    }\n    tmp = (int *)malloc(sizeof(int) * sum);\n    memset(tmp, 0 ,sizeof(int) * sum);\n    return tmp;\n}\n\n// 获取重复利用值, 每次缓存队列头的位置\n// 比如: 此时缓存队列为[C2(0), C2(1), C2(2), C2(3), C2(4)]\n// C2(5) = C1(5) + C2(0) 此时我们需要取缓存队列头的值C2(0)\n// 计算完得到C2(5)，需要执行update_recycle_value将得到C2(5)进队列，除去旧的C2(0)，此时队列头尾C2(1)，即为计算C2(6)需要的缓存值\nint get_recycle_value(int index_of_coin, int current_amount, int *tmp_array) {\n    int t = get_index_tmp(index_of_coin);\n    if(current_amount &lt; get_coin(index_of_coin)){\n        return 0;\n    }\n    else if(current_amount == get_coin(index_of_coin)){\n        return 1;\n    }\n    else {\n        return tmp_array[t];\n    }\n}\n\n// 更新重复利用值(队列的概念), 计算出最新的值，需要替换旧的利用值\n// 比如: C2(5) = C1(5) + C2(0)\n// 现在C2缓存队列中有[C2(0), C2(1), C2(2), C2(3), C2(4)]，我们需要将C2(5)进队列，[C2(1), C2(2), C2(3), C2(4), C2(5)]\nvoid update_recycle_value(int index_of_coin, int *tmp_array, int value) {\n    int i;\n    int t = get_index_tmp(index_of_coin);\n    for(i = 0; i&lt; (get_coin(index_of_coin)-1); i++) {\n        tmp_array[t+i] = tmp_array[t+i+1];\n    }\n    tmp_array[t+get_coin(index_of_coin)-1] = value;\n}\n</code></pre>\n\n<h3 id=\"toc_2\">参考</h3>\n\n<p><a href=\"http://stackoverflow.com/questions/1485022/sicp-making-change/\">http://stackoverflow.com/questions/1485022/sicp-making-change/</a></p>',3,'2016-09-04 20:07:51',1,'2016-09-09 20:11:54',13,2,0),(6,4,'test','<p>test</p>',1,'2016-09-11 03:39:35',NULL,NULL,3,0,0);
/*!40000 ALTER TABLE `post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `postcategory`
--

DROP TABLE IF EXISTS `postcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `postcategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `str` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `postcategory_str` (`str`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `postcategory`
--

LOCK TABLES `postcategory` WRITE;
/*!40000 ALTER TABLE `postcategory` DISABLE KEYS */;
INSERT INTO `postcategory` VALUES (1,'学习','study'),(2,'专业','major'),(3,'生活','live'),(4,'爱好','hobby');
/*!40000 ALTER TABLE `postcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `postreply`
--

DROP TABLE IF EXISTS `postreply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `postreply` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `post_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `content` longtext NOT NULL,
  `create_time` datetime NOT NULL,
  `like_count` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `postreply_post_id` (`post_id`),
  KEY `postreply_user_id` (`user_id`),
  CONSTRAINT `postreply_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`),
  CONSTRAINT `postreply_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `postreply`
--

LOCK TABLES `postreply` WRITE;
/*!40000 ALTER TABLE `postreply` DISABLE KEYS */;
INSERT INTO `postreply` VALUES (1,1,2,'迭代需要重复利用递归产生的冗余数据','2016-09-04 19:31:47',0),(2,1,3,'<p>Please Write Here.</p><p>cool!&nbsp;<img src=\"http://127.0.0.1:9000/assets/images/emoji/basic/relaxed.png\" class=\"emoji\"></p>','2016-09-04 19:52:39',0),(3,3,3,'<h2>我</h2><p>草</p><h2>可<br>以</h2><p>的</p><p>。</p><h2>牛</h2><p>逼</p><p><br></p><p><br></p><img src=\"http://127.0.0.1:9000/assets/images/emoji/basic/cold_sweat.png\" class=\"emoji\"><p><br></p>','2016-09-04 20:09:12',0),(4,4,1,'Please Write Here.<img src=\"http://127.0.0.1:9000/assets/images/emoji/basic/grin.png\" class=\"emoji\">','2016-09-09 20:11:54',0),(5,2,1,'<blockquote>Please Write Here.</blockquote>','2016-09-12 02:37:29',0);
/*!40000 ALTER TABLE `postreply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `posttopic`
--

DROP TABLE IF EXISTS `posttopic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `posttopic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `str` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `posttopic_str` (`str`),
  KEY `posttopic_category_id` (`category_id`),
  CONSTRAINT `posttopic_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `postcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `posttopic`
--

LOCK TABLES `posttopic` WRITE;
/*!40000 ALTER TABLE `posttopic` DISABLE KEYS */;
INSERT INTO `posttopic` VALUES (1,1,'学习资料','study-material'),(2,1,'考研资料','study-advance-material'),(3,1,'竞赛','study-competition'),(4,1,'请教','study-advice'),(5,2,'计算机','major-computer'),(6,3,'电影资源','live-movie'),(7,3,'共享账号','live-account'),(8,3,'电脑故障','live-computer-repair'),(9,4,'摄影','hobby-photography'),(10,4,'健身','hobby-fitness'),(11,NULL,'通知','notice'),(12,NULL,'讨论','discussion');
/*!40000 ALTER TABLE `posttopic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile`
--

DROP TABLE IF EXISTS `profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `nickname` varchar(16) NOT NULL,
  `weibo` varchar(64) NOT NULL,
  `website` varchar(64) NOT NULL,
  `reg_time` datetime NOT NULL,
  `last_login_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `profile_user_id` (`user_id`),
  CONSTRAINT `profile_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile`
--

LOCK TABLES `profile` WRITE;
/*!40000 ALTER TABLE `profile` DISABLE KEYS */;
INSERT INTO `profile` VALUES (1,1,'','','','2016-09-04 19:31:47','2016-09-04 19:31:47'),(2,2,'','','','2016-09-04 19:31:47','2016-09-04 19:31:47'),(3,3,'asdfasdf','xxxx','','2016-09-04 19:31:53','2016-09-04 19:31:53'),(4,4,'','','','2016-09-09 20:04:13','2016-09-09 20:04:13');
/*!40000 ALTER TABLE `profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(16) NOT NULL,
  `nickname` varchar(16) DEFAULT NULL,
  `email` varchar(32) NOT NULL,
  `avatar` varchar(20) DEFAULT NULL,
  `theme` varchar(16) DEFAULT NULL,
  `role` int(11) NOT NULL,
  `password` varchar(32) NOT NULL,
  `salt` varchar(64) NOT NULL,
  `key` varchar(64) NOT NULL,
  `level` int(11) NOT NULL,
  `reg_time` datetime NOT NULL,
  `key_time` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_username` (`username`),
  KEY `user_key` (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','','admin@jmp.com','admin.png','color3',1,'b27dc61aa843fca2660b8186ae559dce','zjePZcUNBtP03PXI5EoNnkAJ4z1eIl8fmcZrLpzJuykeL3DQHoVcr6FBwNZrjD','ubybGYznaHX3cCSgTVAfQYyKvQLFodO4E3iuWYkVQ2rp8ZweR9nRWv5HF13Kew',10,'2016-09-04 19:31:47',1472988707),(2,'test','','test@jmp.com','default_doubi.png',NULL,1,'31723dae49ef41a1d926255b21d249bd','nHaHovT1v8JgNDLOzw5bE0ZMyJEH3H86IBQNHHKJBv303enTgVaPnNyqHPNWqS','A3qBHqqDg07G8vbN2Shcc3AgPpEZNedBNKZvNfJ6DgZC7VzYbNdn7966UPwpvB',10,'2016-09-04 19:31:47',1472988707),(3,'jmpews','','jmpews@jmp.cn','default_doubi.png',NULL,1,'ea7b1b78fa0ff84ac3dc0d0b1ed8a806','VLBXDYPv42YTLkBqV5Dr18i2FjlxrPhibHxmwnDuGLSe1TLkiu9EnT3YSVVTTI','JHtm0mwWNMXiMWz5k6zyQAnbBUQD2NKjoiIYI806cSxUVCPsnThtVf4zRO8AMJ',10,'2016-09-04 19:31:53',1472988713),(4,'test123','','test@test.com','default_doubi.png',NULL,1,'66a82afa993ebd7f48f9208ede378ef5','pPMnthyuWTwWOkIfNittaWXcCvVov5AFepNmQGWyGNX7ileiy48RI4pLy6T8Py','gkblbJ1cUkTxQRTkdVb822UGFM8NM14EqL4IDn7HoZQBLdNtzwO1ALo51S6nJE',10,'2016-09-09 20:04:13',1473422653);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-09-14 22:26:47
