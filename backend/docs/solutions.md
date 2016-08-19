## 解决头像上传和缩小

#### 上传头像

HTML如下

```
<img id="avatar-preview"src="/avatar/{{current_user.avatar}}">
<!-- custom upload button --->
<button class="btn btn-outline-primary btn-sm select-avatar">
	<input type="file" class="file-input" id="avatar" name="avatar" onchange="change_image_preview()">选择
</button>
<button type="submit" class="btn btn-outline-primary btn-sm upload-avatar">保存</button>
```

JS如下

```
function change_image_preview() {
    $inputFileElm = $(this);
    var pic = document.getElementById("avatar-preview");
    var file = document.getElementById("avatar");
    console.log(pic);
    console.log(file);
    var ext=file.value.substring(file.value.lastIndexOf(".")+1).toLowerCase();
    // gif在IE浏览器暂时无法显示
    if(ext!='png'&&ext!='jpg'&&ext!='jpeg'){
        alert("文件必须为图片！"); return;
    }
    if(file.size > 1024*3000){
        alert("上传图片不要超过3000KB");
        return;
    }
    // IE浏览器
    if (document.all) {

        file.select();
        var reallocalpath = document.selection.createRange().text;
        var ie6 = /msie 6/i.test(navigator.userAgent);
        // IE6浏览器设置img的src为本地路径可以直接显示图片
        if (ie6) pic.src = reallocalpath; 
        else { 
            // 非IE6版本的IE由于安全问题直接设置img的src无法显示本地图片，但是可以通过滤镜来实现
            pic.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod='image',src=\"" + reallocalpath + "\")";
            // 设置img的src为base64编码的透明图片 取消显示浏览器默认图片
            pic.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==';
        }
    }
    else {
        var f = file.files[0];
        var reader = new FileReader();
        reader.readAsDataURL(f);
        reader.onload = function(e) {
            pic.src=this.result;
            $(pic).cropper('reset').cropper('replace', this.result);
        }
    }
    $inputFileElm.val("");
}

$('#avatar-preview').cropper({
    viewMode: 2,
    aspectRatio: 1 / 1,
    checkImageOrigin: true,
});

$('.upload-avatar').on('click', function(e){
    e.preventDefault();
    var avatar64 = $('#avatar-preview').cropper('getCroppedCanvas', {width: 100, height: 100}).toDataURL()
    $.ajax({
       type: 'post',
       dataType: 'json',
       url: '/useropt',
       data: JSON.stringify({'opt': 'update-avatar', 'data': {'avatar': avatar64.split(',')[1]}}),
       success: function(result, status) {
           if(result.errorcode == 0) {
               $.notify('头像更换成功');
           }
           else if(result.errorcode == 1) {
               alert(result.txt);
           }
       }
    });
});


```
使用copper
