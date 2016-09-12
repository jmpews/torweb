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
                $(".cpu-per").html(data['cpu_per']+"%");
                $(".ram-per").html(data['ram_per']+"%");
                $(".net-conn").html(data['net_conn']);
                $(".os-start").html(data['os_start']);
            }
        }
    });
    setTimeout(monitor_system_status, 60000);
}
function change_theme() {
    $('.color').on('click', function (e) {
        var color = $(e.target).attr('color');
        $.cookie('theme', color, {expires: 30});
        $.ajax({
            type: 'post',
            dataType: 'json',
            url: '/useropt',
            data: JSON.stringify({'opt': 'update-theme', 'data': {'theme': color}}),
            success: function(result, status) {
                if(result.errorcode == 0) {
                    $.notify('主题保存成功');
                }
                else if(result.errorcode == -3) {
                   $('#loginModal').modal('toggle');
                }
            }
        });
        $('#theme').attr('href', '/assets/css/index.'+color+'.css');
    });
}
function set_theme() {
    // function getCookie(c_name)
    // {
    //     if (document.cookie.length>0)
    //     {
    //         c_start=document.cookie.indexOf(c_name + "=")
    //         if (c_start!=-1)
    //         {
    //             c_start=c_start + c_name.length+1
    //             c_end=document.cookie.indexOf(";",c_start)
    //             if (c_end==-1) c_end=document.cookie.length
    //             return unescape(document.cookie.substring(c_start,c_end))
    //         }
    //     }
    //     return ""
    // }
    var theme = $.cookie('theme');
    if(theme) {
        $('#theme').attr('href', '/assets/css/index.'+theme+'.css');
    }
}
function change_image_preview() {
    $inputFileElm = $(this);
    var pic = document.getElementById("avatar-cropper");
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
        var pic = document.getElementById("avatar-cropper");
        pic.src=this.result;
    }
}

function show_hide_cate_nav() {
    // 解决进去时下拉菜单显示
    $(".card-header-all-bt, .card-header:after").mouseenter(function(e){
        // $(".card-header-all").css('display','block');
        $('.card-header-all').fadeIn(500);
    });
    $('.card-header-all').parent().mouseleave(function(e) {
        // $('.card-header-all').fadeOut(500);
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
        $("#emoji-list").append('<img class="emoji" src="/assets/images/emoji/basic/'+emojiArray[i]+'.png">')
    }
    add_action_emoji_img_summernote();
    $.getJSON('/assets/images/emoji/emojis.json', function(data){
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
        $("#emoji-list").append('<img class="emoji" src="/assets/images/emoji/basic/'+emojiArray[i]+'.png">')
    }
    add_action_emoji_img_medium();
    $.getJSON('/assets/images/emoji/emojis.json', function(data){
        window.emojiJSON=data;
        $("#emoji-list").append('<li class="emoji" em="heart">'+emojiJSON.heart.char+'</li>');
        add_action_emoji_char_medium();
    })
}
function load_font_avatar() {
    var colors = ['#FF5722', '#CDDC39', '#61C5FF', '#2196F3'];
   $('.avatar a span').each(function(i, item){
       var color = colors[Math.floor(Math.random() * colors.length)];
        $(item).css('background-color', color);
    });
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
//拖拽、粘贴上传
var $this;
var $ajaxUrl = '';
$.fn.pasteUploadImage = function (host) {
    $this = $(this);
    $host = host;
    $this.on('paste', function (event) {
        console.log('paste...');
        var filename, image, pasteEvent, text;
        pasteEvent = event.originalEvent;
        if (pasteEvent.clipboardData && pasteEvent.clipboardData.items) {
            image = isImage(pasteEvent);
            if (image) {
                event.preventDefault();
                filename = getFilename(pasteEvent) || "image.png";
                text = "{{" + filename + "(uploading...)}}";
                pasteText(text);
                return uploadFile(image.getAsFile(), filename);
            }
        }
    });
    $this.on('drop', function (event) {
        console.log('drop...');
        var filename, image, pasteEvent, text;
        pasteEvent = event.originalEvent;
        if (pasteEvent.dataTransfer && pasteEvent.dataTransfer.files) {
            image = isImageForDrop(pasteEvent);
            if (image) {
                event.preventDefault();
                filename = pasteEvent.dataTransfer.files[0].name || "image.png";
                text = "{{" + filename + "(uploading...)}}";
                pasteText(text);
                return uploadFile(image, filename);
            }
        }
    });
};

pasteText = function (text) {
    var afterSelection, beforeSelection, caretEnd, caretStart, textEnd;
    caretStart = $this[0].selectionStart;
    caretEnd = $this[0].selectionEnd;
    textEnd = $this.val().length;
    beforeSelection = $this.val().substring(0, caretStart);
    afterSelection = $this.val().substring(caretEnd, textEnd);
    $this.val(beforeSelection + text + afterSelection);
    $this.get(0).setSelectionRange(caretStart + text.length, caretEnd + text.length);
    return $this.trigger("input");
};
isImage = function (data) {
    var i, item;
    i = 0;
    while (i < data.clipboardData.items.length) {
        item = data.clipboardData.items[i];
        if (item.type.indexOf("image") !== -1) {
            return item;
        }
        i++;
    }
    return false;
};
isImageForDrop = function (data) {
    var i, item;
    i = 0;
    while (i < data.dataTransfer.files.length) {
        item = data.dataTransfer.files[i];
        if (item.type.indexOf("image") !== -1) {
            return item;
        }
        i++;
    }
    return false;
};
getFilename = function (e) {
    var value;
    if (window.clipboardData && window.clipboardData.getData) {
        value = window.clipboardData.getData("Text");
    } else if (e.clipboardData && e.clipboardData.getData) {
        value = e.clipboardData.getData("text/plain");
    }
    value = value.split("\r");
    return value[0];
};
getMimeType = function (file, filename) {
    var mimeType = file.type;
    var extendName = filename.substring(filename.lastIndexOf('.') + 1);
    if (mimeType != 'image/' + extendName) {
        return 'image/' + extendName;
    }
    return mimeType
};
uploadFile = function (file, filename) {
    var formData = new FormData();
    formData.append('imageFile', file);
    formData.append("mimeType", getMimeType(file, filename));

    $.ajax({
        url: $ajaxUrl,
        data: formData,
        type: 'post',
        processData: false,
        contentType: false,
        dataType: 'json',
        xhrFields: {
            withCredentials: true
        },
        success: function (data) {
            if (data.success) {
                return insertToTextArea(filename, data.message);
            }
            return replaceLoadingTest(filename);
        },
        error: function (xOptions, textStatus) {
            replaceLoadingTest(filename);
            console.log(xOptions.responseText);
        }
    });
};
insertToTextArea = function (filename, url) {
    return $this.val(function (index, val) {
        return val.replace("{{" + filename + "(uploading...)}}", "![" + filename + "](" + url + ")" + "\n");
    });
};
replaceLoadingTest = function (filename) {
    return $this.val(function (index, val) {
        return val.replace("{{" + filename + "(uploading...)}}", filename + "\n");
    });
};

// 登陆框
$('#loginModal [type="submit"]').on('click', function (event) {
    event.preventDefault();
     $.ajax({
        type: 'post',
        dataType: 'json',
        url: '/login',
        data: {
            'username': $('#loginModal #username').val(),
            'password': $('#loginModal #password').val(),
            'captcha': $('#loginModal #captcha').val()
        },
        success: function(result, status) {
            if(result.errorcode == 0) {
                var data = result['data'];
                $.notify('登陆成功');
                window.location.reload();
            }
            else if(result.errorcode == -3) {
                    $.notify(result.txt);
                    $('#captcha').val('');
                }
            else if(result.errorcode != 0) {
                $.notify(result.txt);
            }
        }
    });
    return 1;
});

$('.captcha').on('click', function (event) {
    event.preventDefault();
    var src = $(event.currentTarget).attr('src');
    var t = src.indexOf('?');
    if(t != -1)
        src = src.substring(0, t);
    src = src + '?id=' + Math.random(1).toString();
   $(event.currentTarget).attr('src', src);

});

// 获取url中的域名地址
function extractDomain(url) {
    var domain;
    //find & remove protocol (http, ftp, etc.) and get domain
    if (url.indexOf("://") > -1) {
        domain = url.split('/')[2];
    }
    else {
        domain = url.split('/')[0];
    }

    //find & remove port number
    // domain = domain.split(':')[0];

    return domain;
}

// 获取websocket_server 的url
function get_websocket_url(callback) {
    $.ajax({
        type: 'get',
        dataType: 'json',
        url: '/api/websocketurl',
        success: function (result) {
            if(result.errorcode == 0) {
                var url = result.data.url;
                if (url == '.')
                    url = extractDomain(window.location.href);
                callback(url);
                console.log('get websocket url success. and start websocket.');
            }
            else if(result.errorcode != 0) {
                console.log('get websocket url error.')
            }
        }
    })
}

// 启动系统状态参数监控的websocket服务
function start_system_monitor_websocket(url) {
     var  wsServer = 'ws://' + url + '/api/systemstatuswebsocket';
     var  websocket = new WebSocket(wsServer);
     websocket.onopen = function (evt) { onOpen(evt) };
     websocket.onclose = function (evt) { onClose(evt) };
     websocket.onmessage = function (evt) { onMessage(evt) };
     websocket.onerror = function (evt) { onError(evt) };
     function onOpen(evt) {
        console.log("Connected to WebSocket server.");
     }
     function onClose(evt) {
        console.log("Disconnected");
     }
     function onMessage(evt) {
        var data = JSON.parse(evt.data).data;
        $(".cpu-per").html(data['cpu_per']+"%");
        $(".ram-per").html(data['ram_per']+"%");
        $(".net-conn").html(data['net_conn']);
        $(".os-start").html(data['os_start']);
     }
     function onError(evt) {
        console.log('Error occured: ' + evt.data);
     }
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
    // set_theme();
    change_theme();
    load_font_avatar();
});
