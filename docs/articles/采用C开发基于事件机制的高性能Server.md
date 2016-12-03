Title: C实现的事件循环的Server
Date: 2016-2-27 03:43
Author: jmpews
Category: Pattern
Tags: epoll,select
Slug: minihttpd

本来是在研究网络协议搞出来的一个小玩意, 能快速提供web服务, 采select等事件模型. https://github.com/jmpews/minihttpd

## 几个遇到的问题:
#### 1.正确关闭socket
不要使用 `close()`, 服务端会产生大量 `TIME_WAIT`, 客户端接受不到发送缓冲区数据.

close是直接关闭读和写, 摧毁socket, 不能再使用该socket, 服务端收不到ack等数据.

正确的处理方法应该是, 先采用 `shutdown(client_fd,FD_WR)`, 将缓冲区数据发送完毕, 接受ACK, 发送FIN, 告诉客户端, 不再写入数据, 等待客户端关闭连接, 服务端读取到0字节数据, 进而关闭socket连接.

#### 2.处理epoll的ET模式

ET模式, 在于减少事件的频繁响应, 只有当socket的状态change的时候, 才会发出响应, 所以 `listen_fd `接受到accept请求, 并不知道具体有几个并发socket请求, 所以需要 `while(accept())` 直到 `EAGAIN` 的errno(读取也是类似).

##  几个代码实现细节:
#### 1. 如何实现通用类型链表
```
typedef struct node
{
    ElemType *data;
    struct node * next;
}ListNode;


typedef int (*FindElemFunc)(ElemType *,ElemType *key);

int list_append(ListNode *,ElemType *);  //追加元素节点
ElemType *list_get_by_func(ListNode *,FindElemFunc,ElemType *);  //查找元素
ListNode *new_list_node();    //新建元素节点

/* 新节点加在head之后 */
int list_append(ListNode *head,ElemType *elem)
{
    ListNode *node;
    node=new_list_node();
    node->data=elem;
    node->next=head->next;
    head->next=node;
    return 0;
}

/* 通过自定义函数查找节点 */
ElemType *list_get_by_func(ListNode *head,FindElemFunc func,void *key)
{
    ListNode *tmp=head->next;
    if(tmp==NULL)
        return NULL;
    do{
        if(func(tmp->data,key))
        {
            return tmp->data;
        }
    }while(tmp=tmp->next);
    return NULL;
}

/* 新建链表节点 */
ListNode *new_list_node(){
    ListNode *tmp;
    tmp=(ListNode *)malloc(sizeof(ListNode));
    tmp->data=NULL;
    tmp->next=NULL;
    return tmp;
}
```


#### 2. socket节点的实现

建立一个链表, 对于到来的请求, 分配一个结构体.

```
/* 请求结构体 */
typedef struct {
    char *read_cache;       //缓存读取内容
    int read_cache_len;     //缓存的内容长度
    char *header_dump;      //缓存请求头
    int header_dump_len;    //请求头的长度
    char method;            //请求方法
    char *request_path;     //请求路径
    long body_len;          //请求的body长度
}Req;

/* 响应结构体 */
typedef struct {
    long response_cache_len;    //响应内容长度
    char *response_path;        //响应文件路径
}Resp;

/* socket连接节点 */
typedef struct sn{
    int client_fd;          //socket连接描述符
    char IO_STATUS;         //socket状态
    Req request;            //socket对应的请求
    Resp response;          //socket对应的响应
    struct sn *next;
}SocketNode;

/* new socket节点 */
SocketNode *new_socket_node() {
    SocketNode *tmp = (SocketNode *) malloc(sizeof(SocketNode));
    memset(tmp, 0, sizeof(SocketNode));
    tmp->request.read_cache=NULL;
    tmp->request.header_dump=NULL;
    return tmp;
}

/* 查找socket描述符节点 */
SocketNode *find_socket_node(SocketNode *head,INT_32 client_fd) {
    SocketNode *tmp = head;
    if (head == NULL) {
        PRINT_ERROR("Socket-Head-Node is None");
        exit(1);
    }
    do{
        if (tmp->client_fd == client_fd)
            return tmp;
    }while(tmp=tmp->next);
    return NULL;

}

/* 添加节点到Header-Node与其他Node之间 */
void add_socket_node(SocketNode *head,SocketNode *client) {
    client->next = head->next;
    head->next = client;
}

/* 根据socket描述符释放节点 */
void free_socket_node(SocketNode *head,INT_32 client_fd) {
    SocketNode *tmp = head;
    SocketNode *k=NULL;
    //空链表
    if (tmp->next == NULL) {
        printf("! free_socket_node ERROR\n");
        exit(1);
    }
    if (head->client_fd==client_fd) {
        head=head->next;
        free_buf(k->request.read_cache);
        free_buf(k->request.header_dump);
        free_buf(k->request.request_path);
        free_buf(k->response.response_path);
        free_buf(k);
        close(client_fd);
        return;
    }
    while((tmp->next)!=NULL){
        if (tmp->next->client_fd == client_fd)
            break;
        tmp=tmp->next;
    }

    k = tmp->next;
    //没找到node
    if (k == NULL) {
        PRINT_ERROR("socket-node not found for client_fd");
        close(client_fd);
        exit(1);
    }

    tmp->next = k->next;
    printf("FREE:ID-%d,PATH-%s\n",client_fd,k->request.request_path);
    free_buf(k->request.read_cache);
    free_buf(k->request.header_dump);
    free_buf(k->request.request_path);
    free_buf(k->response.response_path);
    free_buf(k);

    close(client_fd);
    TIP printf("> SOCKET[%d] ready close.\n", client_fd);
}
```

#### 3.`read_line` 读一行实现
函数设计尽量模块独立, 最好不要在`read_line`中引用其他结构体、函数等.

```
INT_32 read_line(INT_32 sock, char *buf,int BUF_SIZE,int *len) {
    char c='\0' ;
    INT_32 r=0,t=0;
    *len=0;
    //buf[BUF_SIZE-1] must be '\0'
    while ((t < BUF_SIZE - 1) && (c != '\n')) {
        r = recv(sock, &c, 1, 0);
        if (r > 0) {
            // 判断下一个符号是否是\r, 如果是则表明为\r\n结束符
            if (c == '\r') {
                // MSG_PEEK:从缓冲区copy数据, 并不删除数据, 如果符合再次读取数据
                r = recv(sock, &c, 1, MSG_PEEK);
                if (r > 0 && c == '\n')
                    recv(sock, &c, 1, 0);
                else
                    c = '\n';
            }
            buf[t] = c;
            t++;
        }
        else
            break;
    }

    buf[t++]='\0';
    *len=t;

    if (r < 0) {
        // 缓冲区为空,读取失败
        if (errno == EAGAIN) {
            return IO_EAGAIN;
        }
        else {
            PRINT_ERROR("get_line");
            return IO_ERROR;
        }
    }
    else if(r>0)
            return IO_LINE_DONE;
    return IO_ERROR;
}
```
#### 4. `read_line_more` 读取一行无论多少数据
返回malloc的返回的地址, 注意释放

```
//读取一行无论数据有多长
int read_line_more(int client_fd, char **malloc_buffer, int *len) {
    int r;
    int n = 0;
    int t;
    char *malloc_buf=NULL;
    int BUF_SIZE=1024;
    char buf[BUF_SIZE];

    memset(buf, 0, BUF_SIZE);
    *len=0;

    r = read_line(client_fd, buf, BUF_SIZE, &t);

    /*
     * 读取流程:
     * 读取一行(buf_size=1024)
     * 拷贝到buf
     * >进行状态判断
     * 1. 最后字符!='\n',且读取状态为IO_LINE_DONE
     *      重新读取
     * 2. 读取错误IO_EAGAIN || IO_ERROR
     *      返回buf+状态码
     * 3. 最后字符为'\n'
     *      读取完毕, 返回返回buf+状态码
     */
   while(1){
        if(!malloc_buf)
            malloc_buf = (char *) malloc(sizeof(char) * t);
        else
            malloc_buf = (char *) realloc(malloc_buf, (n + t) * sizeof(char));
        memcpy(malloc_buf + n, buf, t);
        n += t;
        if(buf[t-1-1]!='\n' && r == IO_LINE_DONE ) {
           r=read_line(client_fd, buf, BUF_SIZE, &t);
        }
        else if(buf[t-1-1]=='\n' && r == IO_LINE_DONE)
        {
            *len=n;
            *malloc_buffer=malloc_buf;
            return r;
        }
        else if(r == IO_ERROR || r== IO_EAGAIN)
        {
            *len=n;
            *malloc_buffer=malloc_buf;
            return r;
        }

   }
}
```
#### 5. 请求处理流程
每次设置不同的状态码, 根据不同的状态码, 进入不同函数处理.

发现设计模式真的重要, 之前一直在纠结整个处理流程应该怎么处理, 然后琢磨出应该用状态码来表明步骤. 过了一段时间, 再一想, 这特么不就是状态机么？！

在处理流程的过程中,case并没有接continue;(PS:如果while+switch+continue会不会更好)

```
int handle_request(int client_fd){
    int r;
    SocketNode *client_sock;
    client_sock=find_socket_node(SocketHead,client_fd);
    switch (client_sock->IO_STATUS) {
        case R_HEADER_INIT:
            printf("\0");
        case R_HEADER_START:
        {
            r=request_header_start(client_fd);
            if (r==IO_EAGAIN) {
                if (client_sock->request.method==M_ERROR)
                    return IO_ERROR;
                return IO_EAGAIN;
            }
            else if(r==IO_ERROR)
                return IO_ERROR;
        }
        case R_HEADER_BODY:
        {
            r=request_header_body(client_fd);
            if (r==IO_EAGAIN) {
                if (client_sock->request.method==M_ERROR)
                    return IO_ERROR;
                return IO_EAGAIN;
            }
            else if(r==IO_ERROR)
                return IO_ERROR;
        }
        case R_BODY:
        {
            r=request_body(client_fd);
            if (r==IO_EAGAIN||(client_sock->request.method==M_ERROR)) {
                return IO_EAGAIN;
            }
            else if(r==IO_ERROR)
                return IO_ERROR;
        }
        default:
            break;
    }
    return IO_DONE;
}
```
### 5. 路由实现

```
typedef struct urlroute{
    char route[64];
    char *(*func)(SocketNode *);
} URL_ROUTE;
ListNode *head_route;

// 返回一个函数指针,该函数返回接受SocketNode * 参数,返回char *
typedef char *(*RouteFunc)(SocketNode *);

// 路由处理函数
char *route_func1(SocketNode *tmp){
    char *str;
    char *s="route.1:hello world\n\0";
    str=(char *)malloc(1024*sizeof(char));
    strcpy(str,s);
    str[strlen(s)]='\0';
    return str;
}

char *route_func2(SocketNode *tmp){
    char *str;
    char *s="route.2:hello world\n\0";
    str=(char *)malloc(1024*sizeof(char));
    strcpy(str,s);
    str[strlen(s)]='\0';
    return str;
}
char *route_func3(SocketNode *tmp){
    return tmp->request.header_dump;
}

//配合任意类型的链表, 返回ElemType *, 然后对返回, 进行强制类型转换.
int find_route(ElemType *data,void *key){
    if(!strcasecmp((char *)key, ((URL_ROUTE *)data)->route)){
        printf("匹配到route:%s",(char *)key);
        return 1;
    }
    return 0;
}

//new
URL_ROUTE *new_route_node(char *route_str,RouteFunc func){
    URL_ROUTE *tmp=(URL_ROUTE *)malloc(sizeof(URL_ROUTE));
    strcpy(tmp->route,route_str);
    tmp->func=func;
    return tmp;
}

//注册路由
void init_route(){
    head_route=NewElemNode();
    ListAppend(head_route, new_route_node("/route1", route_func1));
    ListAppend(head_route, new_route_node("/route2", route_func2));
    ListAppend(head_route, new_route_node("/echo", route_func3));
}

//对于传入的route_key(请求路径)匹配路由表, 调用处理函数, 返回`char *`
char *handle_route(SocketNode *client_sock,char *route_key){
    char *resp;
    ElemType *data;
    data=GetElem(head_route, find_route, route_key);
    if(data)
    {
        resp=((URL_ROUTE *)data)->func(client_sock);
        return resp;
    }
    else{
        return NULL;
    }
}

```
### 6. 处理响应文件(发送缓冲区EAGAIN处理)
返回已发送的长度

```
INT_32 send_file(INT_32 client_fd,char *file_path,long *len) {
    int buffer_size=1024;
    FILE *fd;
    long file_length = 0;
    char buf[buffer_size];
    int t=0,r = 0;

    fd = fopen(file_path, "r");
    if (fd == NULL) {
        perror("! send_file/fopen error\n");
        exit(1);
    }

    //内容长度, 暂时不用, 协议自动计算
    fseek(fd, 0, SEEK_END);
    file_length = ftell(fd);
    rewind(fd);

    //设置文件当前指针,为上次没有读完的
    if (*len)
        fseek(fd, *len, SEEK_SET);
    else
        send_headers(client_fd);
    while (1) {
        memset(buf, 0, buffer_size);
        t = fread(buf, sizeof(char), buffer_size, fd);
        r = send(client_fd, buf, t, 0);
        if (r < 0) {
            if (errno == EAGAIN) {
                fclose(fd);
                return IO_EAGAIN;
            }
            else {
                printf("! Send Error:");
                fclose(fd);
                return IO_ERROR;
            }
        }
        *len+=r;
        if ((*len+2)>=file_length||t<=(buffer_size-2)){
            fclose(fd);
            return IO_DONE;
        }

    }
}

```

Epoll的参考资料:

1. http://vizee.org/blog/epoll-et-note/
2. http://www.ccvita.com/515.html
3. http://blog.lucode.net/linux/epoll-tutorial.html

typedef  void ElemType;
