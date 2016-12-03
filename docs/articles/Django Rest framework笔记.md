Title: Django Rest framework笔记
Date: 2015-11-27 03:43
Author: jmpews
Category: Django
Tags: python,restful,django
Slug: django-restful

## 最简洁使用

```
# 配置路由
url(r'^api/v1/test_rest/',test_rest.views.test_poc_list_view.as_view()),

class test_PocSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    vul__name=serializers.CharField(read_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

# 配置视图的两种方法
#1.函数方法
@api_view(['POST','GET'])
def test_poc_list(request):
    if request.method=='GET':
        test_pocs=Poc.objects.values('id','vul__name').all()
        serializer=test_PocSerializer(test_pocs,many=True)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        pass

#2.类视图
class Test_Poc_List(APIView):
    # get方法
    def get(self,request):
        if request.method=='GET':
            test_pocs=Poc.objects.values('id','vul__name').all()
            serializer=test_PocSerializer(test_pocs,many=True)
            return JSONResponse(serializer.data)
        elif request.method == 'POST':
            pass
#3.更加封装的view
class Test_Poc_List_(generics.ListAPIView):
   queryset=Poc.objects.values('id','vul__name').all()
   serializer_class = test_PocSerializer
```

##  技巧点

```
# 调用一个特殊的方法去返回该field
required = serializers.SerializerMethodField('get_required')
def get_required(self, obj):
  # obj是正在序列化的instance
  pass
```
