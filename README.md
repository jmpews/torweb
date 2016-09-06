# jmp

## Features(even Tricks?)

### utils
#### how to get args?
1. `get_cleaned_post_data_http_error` `get_cleaned_query_data_http_error` 获取参数，如果获取不到返回`HTTPError(400)`
2. `get_cleaned_query_data` `get_cleaned_post_data` 获取参数，返回自定义异常

### cache with trick

在`/app/cache.py` 缓存一些需要**面向所有用户使用**的缓存，比如缓存文章分类、热门文章分类、系统状态

### deal with exception 

decorator

def foo():
    print(hello')

pass

### fast with coroutine

pass
