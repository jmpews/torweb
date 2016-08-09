//小卡片mouseover
$(document).on('mouseover', '.dropdown', function ()
{
    $(this).find(".dropdown-menu").show()
});

//小卡片mouseout
$(document).on('mouseout', '.dropdown', function ()
{
    $(this).find(".dropdown-menu").hide()
});

function monitor_system_status() {
    $.ajax({
        type: 'get',
        dataType: 'json',
        url: '/api/systemstatus',
        success: function(data, text) {
            if(data.errorcode == 0) {
                var data = data.data;
                console.log(data);
                $(".cpu-per").html(data['cpu_per']+"%");
                $(".ram-per").html(data['ram_per']+"%");
                $(".net-conn").html(data['net_conn']);
                $(".os-start").html(data['os_start']);
            }
        }
    })
    setTimeout(monitor_system_status, 5000);
}

function change_image_preview() {
    var pic = document.getElementById("avatar-preview");
    var file = document.getElementById("avatar");
    console.log(pic);
    console.log(file);
    var ext=file.value.substring(file.value.lastIndexOf(".")+1).toLowerCase();
    // gif在IE浏览器暂时无法显示
    if(ext!='png'&&ext!='jpg'&&ext!='jpeg'){
        alert("文件必须为图片！"); return;
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
    }else{
        html5Reader(file);
    }
}

function html5Reader(file){ 
    var file = file.files[0]; 
    var reader = new FileReader(); 
    reader.readAsDataURL(file); 
    reader.onload = function(e){ 
        var pic = document.getElementById("avatar-preview");
        pic.src=this.result;
    } 
}

function show_hide_nav() {
    var t = 0;
    $(".card-header-all-bt").mouseenter(function(e){
        $(".card-header-all").css('display','block');
    })
    $(".card-header").mouseleave(function(e) {
        $(".card-header-all").css('display','none');
        //$(".card-header-all").css('display','none');
    });
    $(".card-header-all").mouseenter(function(e){
        $(".card-header-all").css('display','block');
    }).mouseleave(function(e) {
        $(".card-header-all").css('display','none');
    });
}

