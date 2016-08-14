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

function index_show_hide_cate_nav() {
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

function post_new_show_hide_cate() {
    $(".post-new-html #topic").on('click', function(e){
        $(".card-header-all").css('display','block');
    });
    $(".post-new-html .card-header-all-cate a").on('click', function(e){
        $(".card-header-all").css('display','none');
        $("#topic").val($(this).html());
    });
}

function show_hide_emoji_list() {
    $("#emoji-btn").on('mousedown', function(e){
        $('#summernote').summernote('saveRange');
         }).on('click',function(e){
            e.preventDefault();
            e.stopPropagation();
            $("#emoji-list").css('display', 'block');
    });
}
function add_action_emoji_img() {
    $('#emoji-list img.emoji').on('click', function(ei){
        console.log('test');
        var e = $('#summernote');
        e.summernote('restoreRange');
        e.summernote('insertImage', ei.target.src, function($image){
            $image.addClass('emoji');
            $image.css('width', '20px');
        });
    });
};

function add_action_emoji_char() {
    $('#emoji-list li.emoji').on('click', function(ei){
        var e = $('#summernote');
        e.summernote('restoreRange');
        debugger;
         var t = $('<span class="emoji">'+window.emojiJSON[ei.target.attributes['em'].value].char+'</span>');
         e.summernote('insertNode', t[0]);
    });
};
// 两种方式处理emoji
//  一种借助图片的方式，一种借助字符的方式
function load_emoji() {
    var emojiArray=['smile', 'blush', 'grin', 'heart_eyes', 'relaxed', 'sweat_smile', 'joy', 'flushed', 'confused', 'unamused', 'sob', 'cold_sweat', 'sweat', 'scream', 'sleepy', 'mask']
    for (var i=0; i<emojiArray.length; i++) {
        $("#emoji-list").append('<img class="emoji" src="/static/images/emoji/basic/'+emojiArray[i]+'.png">')
    }
    add_action_emoji_img();
    $.getJSON('/static/images/emoji/emojis.json', function(data){
        window.emojiJSON=data;
        $("#emoji-list").append('<li class="emoji" em="heart">'+emojiJSON.heart.char+'</li>');
        add_action_emoji_char();
    })
}

$(document).click(function() {
    if ($("#emoji-list").is(":hidden")) {
        return;
    }
    else {
        $("#emoji-list").hide();
    }
});
