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

function html5Reader(file) {
    var file = file.files[0];
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function(e) {
        var pic = document.getElementById("avatar-preview");
        pic.src=this.result;
    }
}

function show_hide_cate_nav() {
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
function add_action_emoji_img_summernote() {
    $('#emoji-list img.emoji').on('click', function(ei){
        var e = $('#summernote');
        e.summernote('restoreRange');
        e.summernote('insertImage', ei.target.src, function($image){
            $image.addClass('emoji');
            $image.css('width', '20px');
        });
    });
};

function add_action_emoji_char_summernote() {
    $('#emoji-list li.emoji').on('click', function(ei){
        var e = $('#summernote');
        e.summernote('restoreRange');
         var t = $('<span class="emoji">'+window.emojiJSON[ei.target.attributes['em'].value].char+'</span>');
         e.summernote('insertNode', t[0]);
    });
};
// 两种方式处理emoji
//  一种借助图片的方式，一种借助字符的方式
function load_emoji_summernote() {
    var emojiArray=['smile', 'blush', 'grin', 'heart_eyes', 'relaxed', 'sweat_smile', 'joy', 'flushed', 'confused', 'unamused', 'sob', 'cold_sweat', 'sweat', 'scream', 'sleepy', 'mask']
    for (var i=0; i<emojiArray.length; i++) {
        $("#emoji-list").append('<img class="emoji" src="/static/images/emoji/basic/'+emojiArray[i]+'.png">')
    }
    add_action_emoji_img_summernote();
    $.getJSON('/static/images/emoji/emojis.json', function(data){
        window.emojiJSON=data;
        $("#emoji-list").append('<li class="emoji" em="heart">'+emojiJSON.heart.char+'</li>');
        add_action_emoji_char_summernote();
    })
}
function show_hide_emoji_list_medium() {
    $("#emoji-btn").on('click',function(e){
            e.preventDefault();
            e.stopPropagation();
            $("#emoji-list").css('display', 'block');
    });
}
function add_action_emoji_img_medium() {
    $('#emoji-list img.emoji').on('click', function(ei){
        var e = $('#mediumeditor');
        e.append('<img src="'+ei.target.src+'" class="emoji">');
    });
};

function add_action_emoji_char_medium() {
    $('#emoji-list li.emoji').on('click', function(ei){
        var e = $('#mediumeditor');
        e.append('<span class="emoji">'+window.emojiJSON[ei.target.attributes['em'].value].char+'</span>')
    });
};
function load_emoji_medium() {
    var emojiArray=['smile', 'blush', 'grin', 'heart_eyes', 'relaxed', 'sweat_smile', 'joy', 'flushed', 'confused', 'unamused', 'sob', 'cold_sweat', 'sweat', 'scream', 'sleepy', 'mask']
    for (var i=0; i<emojiArray.length; i++) {
        $("#emoji-list").append('<img class="emoji" src="/static/images/emoji/basic/'+emojiArray[i]+'.png">')
    }
    add_action_emoji_img_medium();
    $.getJSON('/static/images/emoji/emojis.json', function(data){
        window.emojiJSON=data;
        $("#emoji-list").append('<li class="emoji" em="heart">'+emojiJSON.heart.char+'</li>');
        add_action_emoji_char_medium();
    })
}

function getFriendlyTime(t)
{
    t = t.replace('-', '/')
    t = t.replace('-', '/')
    console.log(t);
    if(!t) return 'biu...';
    var diff = Date.now() - Date.parse(t); 
    var seconds = 1000, minutes = 1000 * 60, hours = 1000 * 60 * 60, days = 1000 * 60 * 60 * 24, weeks = 1000 * 60 * 60 * 24 * 7, months = 1000 * 60 * 60 * 24 * 30, year = 1000 * 60 * 60 * 24 * 365; 
    if(diff < 2 * minutes) return "A moment ago";
    if(diff < hours) return Math.floor(diff/minutes) + " mins ago";
    if(diff < days) return (Math.floor(diff/hours)==1)?"an hour ago":Math.floor(diff/hours) + " hrs ago";
    if(diff < weeks) return (Math.floor(diff/days)==1)?"yesterday":Math.floor(diff/days) + " days ago";
    if(diff < months) return (Math.floor(diff/weeks)==1)?"last week":Math.floor(diff/weeks) + " weeks ago";
    if(diff < year) return (Math.floor(diff/months)==1)?"last month":Math.floor(diff/months) + " months ago";
    return (Math.floor(diff/year)==1)?"an year ago":Math.floor(diff/year) + " yrs ago";
}

// 友好替换时间
function replate_friendly_time() {
    $('.friendly-time').each(function(i, item){
        $(item).html(getFriendlyTime($(item).html()));
    });
}
$(document).click(function() {
    if ($("#emoji-list").is(":hidden")) {
        return;
    }
    else {
        $("#emoji-list").hide();
    }
});
$(document).ready(function () {
    //replate_friendly_time();
});
