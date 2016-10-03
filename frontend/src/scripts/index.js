//小卡片mouseover
$(document).on('mouseover', '.dropdown', function () {
    $(this).find(".dropdown-menu").show()
});

//小卡片mouseout
$(document).on('mouseout', '.dropdown', function () {
    $(this).find(".dropdown-menu").hide()
});

// ajax定时轮训系统状态
function monitor_system_status() {
    $.ajax({
        type: 'get',
        dataType: 'json',
        url: '/api/systemstatus',
        success: function (data, text) {
            if (data.errorcode == 0) {
                var data = data.data;
                $(".cpu-per").html(data['cpu_per'] + "%");
                $(".ram-per").html(data['ram_per'] + "%");
                $(".net-conn").html(data['net_conn']);
                $(".os-start").html(data['os_start']);
            }
        }
    });
    setTimeout(monitor_system_status, 60000);
}

// 修改系统主题
function change_theme() {
    $('.color').on('click', function (e) {
        var color = $(e.target).attr('color');
        $.cookie('theme', color, {expires: 30});
        $.ajax({
            type: 'post',
            dataType: 'json',
            url: '/useropt',
            data: JSON.stringify({'opt': 'update-theme', 'data': {'theme': color}}),
            success: function (result, status) {
                if (result.errorcode == 0) {
                    $.notify('主题保存成功');
                }
                else if (result.errorcode == -3) {
                    $('#loginModal').modal('toggle');
                }
            }
        });
        $('#theme').attr('href', '/assets/css/index.' + color + '.css');
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
    if (theme) {
        $('#theme').attr('href', '/assets/css/index.' + theme + '.css');
    }
}

// 图片预览
function change_image_preview() {
    $inputFileElm = $(this);
    var avatar_cropper = document.getElementById("avatar-cropper");
    var avatar_file = document.getElementById("avatar-file");
    var ext = avatar_file.value.substring(avatar_file.value.lastIndexOf(".") + 1).toLowerCase();
    // gif在IE浏览器暂时无法显示
    if (ext != 'png' && ext != 'jpg' && ext != 'jpeg') {
        alert("文件必须为图片！");
        return;
    }
    if (avatar_file.size > 1024 * 3000) {
        alert("上传图片不要超过3000KB");
        return;
    }
    // IE浏览器
    if (document.all) {
        avatar_file.select();
        var reallocalpath = document.selection.createRange().text;
        var ie6 = /msie 6/i.test(navigator.userAgent);
        // IE6浏览器设置img的src为本地路径可以直接显示图片
        if (ie6) avatar_cropper.src = reallocalpath;
        else {
            // 非IE6版本的IE由于安全问题直接设置img的src无法显示本地图片，但是可以通过滤镜来实现
            avatar_cropper.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod='image',src=\"" + reallocalpath + "\")";
            // 设置img的src为base64编码的透明图片 取消显示浏览器默认图片
            avatar_cropper.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==';
        }
    }
    else {
        var f = avatar_file.files[0];
        var reader = new FileReader();
        reader.readAsDataURL(f);
        reader.onload = function (e) {
            avatar_cropper.src = e.target.result;
            // 重新载入croppper
            $(avatar_cropper).cropper('reset').cropper('replace', e.target.result);
        }
    }
    $inputFileElm.val("");
}

// html5读取文件内容
function html5Reader(file) {
    var avatar_file = file.files[0];
    var reader = new FileReader();
    reader.readAsDataURL(avatar_file);
    reader.onload = function (e) {
        var avatar_cropper = document.getElementById("avatar-cropper");
        avatar_cropper.src = this.result;
    }
}

// 上传头像
$('.upload-avatar').on('click', function (e) {
    e.preventDefault();
    var avatar64 = $('#avatar-cropper').cropper('getCroppedCanvas', {width: 200, height: 200}).toDataURL();
    $.ajax({
        type: 'post',
        dataType: 'json',
        url: '/useropt',
        data: JSON.stringify({'opt': 'update-avatar', 'data': {'avatar': avatar64.split(',')[1]}}),
        success: function (result, status) {
            if (result.errorcode == 0) {
                $.notify('头像更换成功');
                window.location.reload();
            }
            else if (result.errorcode == 1) {
                alert(result.txt);
            }
        }
    });
});

// 显示、隐藏所有分类
function show_hide_cate_nav() {
    // 解决进去时下拉菜单显示
    $(".card-header-all-bt, .card-header:after").mouseenter(function (e) {
        // $(".card-header-all").css('display','block');
        $('.card-header-all').fadeIn(500);
    });
    $('.card-header-all').parent().mouseleave(function (e) {
        // $('.card-header-all').fadeOut(500);
        $(".card-header-all").css('display', 'none');
    });
}

// 显示隐藏所有分类(post-new页面)
function post_new_show_hide_cate() {
    $(".post-new-html #topic").on('click', function (e) {
        $(".card-header-all").css('display', 'block');
    });
    $(".post-new-html .card-header-all-cate a").on('click', function (e) {
        $(".card-header-all").css('display', 'none');
        $("#topic").val($(this).html());
    });
}

//显示隐藏emoji
function show_hide_emoji_list() {
    $("#emoji-btn").on('mousedown', function (e) {
        $('#summernote').summernote('saveRange');
    }).on('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        $("#emoji-list").css('display', 'block');
    });
}

// 两种方式处理emoji
//  一种借助图片的方式，一种借助字符的方式
function show_hide_emoji_list_medium() {
    $("#emoji-btn").on('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        $("#emoji-list").css('display', 'block');
    });
}
function add_action_emoji_img_medium() {
    $('#emoji-list img.emoji').on('click', function (ei) {
        var e = $('#mediumeditor');
        e.append('<img src="' + ei.target.src + '" class="emoji">');
    });
};

function add_action_emoji_char_medium() {
    $('#emoji-list li.emoji').on('click', function (ei) {
        var e = $('#mediumeditor');
        e.append('<span class="emoji">' + window.emojiJSON[ei.target.attributes['em'].value].char + '</span>')
    });
}

function load_emoji_medium() {
    var emojiArray = ['smile', 'blush', 'grin', 'heart_eyes', 'relaxed', 'sweat_smile', 'joy', 'flushed', 'confused', 'unamused', 'sob', 'cold_sweat', 'sweat', 'scream', 'sleepy', 'mask']
    for (var i = 0; i < emojiArray.length; i++) {
        $("#emoji-list").append('<img class="emoji" src="/assets/images/emoji/basic/' + emojiArray[i] + '.png">')
    }
    add_action_emoji_img_medium();
    $.getJSON('/assets/images/emoji/emojis.json', function (data) {
        window.emojiJSON = data;
        $("#emoji-list").append('<li class="emoji" em="heart">' + emojiJSON.heart.char + '</li>');
        add_action_emoji_char_medium();
    })
}
function load_font_avatar() {
    var colors = ['#FF5722', '#CDDC39', '#61C5FF', '#2196F3'];
    $('.post-avatar a span').each(function (i, item) {
        var color = colors[Math.floor(Math.random() * colors.length)];
        $(item).css('background-color', color);
    });
}

//友好设置系统时间
function getFriendlyTime(t) {
    t = t.replace('-', '/');
    t = t.replace('-', '/');
    if (!t) return 'biu...';
    var diff = Date.now() - Date.parse(t);
    var seconds = 1000, minutes = 1000 * 60, hours = 1000 * 60 * 60, days = 1000 * 60 * 60 * 24, weeks = 1000 * 60 * 60 * 24 * 7, months = 1000 * 60 * 60 * 24 * 30, year = 1000 * 60 * 60 * 24 * 365;
    if (diff < 2 * minutes) return "A moment ago";
    if (diff < hours) return Math.floor(diff / minutes) + " mins ago";
    if (diff < days) return (Math.floor(diff / hours) == 1) ? "an hour ago" : Math.floor(diff / hours) + " hrs ago";
    if (diff < weeks) return (Math.floor(diff / days) == 1) ? "yesterday" : Math.floor(diff / days) + " days ago";
    if (diff < months) return (Math.floor(diff / weeks) == 1) ? "last week" : Math.floor(diff / weeks) + " weeks ago";
    if (diff < year) return (Math.floor(diff / months) == 1) ? "last month" : Math.floor(diff / months) + " months ago";
    return (Math.floor(diff / year) == 1) ? "an year ago" : Math.floor(diff / year) + " yrs ago";
}

// 友好替换时间
function replate_friendly_time() {
    $('.friendly-time').each(function (i, item) {
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
        success: function (result, status) {
            if (result.errorcode == 0) {
                var data = result['data'];
                $.notify('登陆成功');
                window.location.reload();
            }
            else if (result.errorcode == -3) {
                $.notify(result.txt);
                $('#captcha').val('');
            }
            else if (result.errorcode != 0) {
                $.notify(result.txt);
            }
        }
    });
    return 1;
});

// 验证码点击刷新
$('.captcha').on('click', function (event) {
    event.preventDefault();
    var src = $(event.currentTarget).attr('src');
    var t = src.indexOf('?');
    if (t != -1)
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
            if (result.errorcode == 0) {
                var url = result.data.url;
                if (url == '.')
                    url = extractDomain(window.location.href);
                callback(url);
                console.log('get websocket url success. and start websocket.');
            }
            else if (result.errorcode != 0) {
                console.log('get websocket url error.')
            }
        }
    })
}

// 启动系统状态参数监控的websocket服务
function start_system_monitor_websocket(url) {
    var wsServer = 'ws://' + url + '/api/systemstatuswebsocket';
    sys_websocket = new WebSocket(wsServer);
    sys_websocket.onopen = function (evt) {
        onOpen(evt)
    };
    sys_websocket.onclose = function (evt) {
        onClose(evt)
    };
    sys_websocket.onmessage = function (evt) {
        onMessage(evt)
    };
    sys_websocket.onerror = function (evt) {
        onError(evt)
    };

    function onOpen(evt) {
        console.log("Connected to WebSocket server.");
    }

    function onClose(evt) {
        console.log("Disconnected");
    }

    function onMessage(evt) {
        var data = JSON.parse(evt.data).data;
        $(".cpu-per").html(data['cpu_per'] + "%");
        $(".ram-per").html(data['ram_per'] + "%");
        $(".net-conn").html(data['net_conn']);
        $(".os-start").html(data['os_start']);
    }

    function onError(evt) {
        console.log('Error occured: ' + evt.data);
    }
}

// 启动聊天的websocket
function start_chat_websocket(url) {
    var wsServer = 'ws://' + url + '/user/chatwebsocket';
    chat_websocket = new WebSocket(wsServer);
    chat_websocket.onopen = function (evt) {
        onOpen(evt)
    };
    chat_websocket.onclose = function (evt) {
        onClose(evt)
    };
    chat_websocket.onmessage = function (evt) {
        onMessage(evt)
    };
    chat_websocket.onerror = function (evt) {
        onError(evt)
    };

    function onOpen(evt) {
        console.log("Connected to WebSocket server.");
        // 请求更新 最近用户列表
        send_socket_message('update_recent_user_list', '')
    }

    function onClose(evt) {
        console.log("Disconnected");
    }

    function onMessage(evt) {
        var result = JSON.parse(evt.data);
        console.log(result);
        if (result.errorcode == 0) {
            handle_receive_message(result.data);
        }
    }

    function onError(evt) {
        console.log('Error occured: ' + evt.data);
    }
}

// 发送操作码和数据
function send_socket_message(opt, data) {
    if (data == '')
        data = 'x';
    var message = JSON.stringify({
        'opt': opt,
        'data': data
    });
    chat_websocket.send(message);
}

// 设置当前聊天用户
function set_current_user(user_id) {
    window.sessionStorage.setItem('current_user_id', user_id);

}

// 判断是否为当前用户
function is_current_user(user_id) {
    var curent_user_id = window.sessionStorage.getItem('current_user_id');
    if (curent_user_id) {
        if (curent_user_id == user_id) {
            return true
        }
    }
    return false;
}

// 判断 最近用户列表是否存在
function is_current_user_list(user_id) {
    var recent_user_list = window.sessionStorage.getItem('recent_user_list');
    if (recent_user_list) {
        recent_user_list = JSON.parse(recent_user_list);
    }
    else
        return false;
    var user_id_list = recent_user_list.user_id_list;
    if(user_id_list) {
        if(user_id_list.indexOf(user_id)!= -1)
            return true;
    }
    return false;
}

// 把消息添加到消息列表的html中
function append_message_to_chat_content(message) {
    if (message[0] == "<")
        var s = "<li class='chat-other cl'><img class='avatar' src='/assets/images/avatar/" + $('.chat .chat-header').attr('other_avatar') + "'><div class='chat-text'>" + message[1] + "</div></li>";
    else
        var s = "<li class='chat-self cl'><img class='avatar' src='/assets/images/avatar/" + $('.chat .chat-header').attr('me_avatar') + "'><div class='chat-text'>" + message[1] + "</div></li>";

    $('.chat .chat-content ul').append(s);
}
function append_tmp_user_to_user_list(other_id, other_name, other_avatar) {
    $('.chat-user-all').append("<div class='chat-user' other='" + other_id + "'><img class='chat-user-avatar' src='/assets/images/avatar/"+ other_avatar +"'><span class='chat-user-name'>" + other_name + "</span></div>")
    // 点击用户头像, 初始化,与该用户的聊天记录窗口
    $('.chat-user').on('click', function (e) {
        var other_id = $(e.currentTarget).attr('other');
        set_current_user(other_id);
        send_socket_message('recent_chat_message', {'user_id': other_id})
    });
}
// 打开聊天页面
$('.real-time-chat').on('click', function () {
    $('.no-recent-user-list').show();
    send_socket_message('update_recent_user_list_and_open', '');
});

// 更新用户列表
function generate_chat_user_list() {
    var recent_user_list = window.sessionStorage.getItem('recent_user_list');
    if (recent_user_list) {
        recent_user_list = JSON.parse(recent_user_list);
    }
    else {
        send_socket_message('update_recent_user_list', '');
        return;
    }
    $('.chat-user-all').html('');
    for (var i = 0; i < recent_user_list.user_id_list.length; i++) {
        var user_id = recent_user_list.user_id_list[i];
        var other_id = recent_user_list[user_id].other_id;
        var other_avatar = recent_user_list[user_id].other_avatar;
        var other_name = recent_user_list[user_id].other_name;
        $('.chat-user-all').append("<div class='chat-user' other='" + other_id + "'><img class='chat-user-avatar' src='/assets/images/avatar/"+ other_avatar +"'><span class='chat-user-name'>" + other_name + "</span></div>")
    }
    // 点击用户头像, 初始化,与该用户的聊天记录窗口
    $('.chat-user').on('click', function (e) {
        var other_id = $(e.currentTarget).attr('other');
        set_current_user(other_id);
        send_socket_message('recent_chat_message', {'user_id': other_id})
    });
}

// 更新聊天记录窗口
function generate_chat_content_html(data) {
    $('.chat .chat-title').html('chat 2 ' + data['other_name']);
    $('.chat .chat-header').attr('other_avatar', data['other_avatar']);
    $('.chat .chat-header').attr('me_avatar', data['me_avatar']);
    $('.chat .chat-header').attr('other_id', data['other_id']);
    var recent_message = data['msg'];
    $('.chat .chat-content ul').html('');
    for (var i = 0; i < recent_message.length; i++) {
        if (recent_message[i][0] == "<")
            var s = "<li class='chat-other cl'><img class='avatar' src='/assets/images/avatar/" + data['other_avatar'] + "'><div class='chat-text'>" + recent_message[i][1] + "</div></li>";
        else
            var s = "<li class='chat-self cl'><img class='avatar' src='/assets/images/avatar/" + data['me_avatar'] + "'><div class='chat-text'>" + recent_message[i][1] + "</div></li>";
        $('.chat .chat-content ul').append(s);
    }
    $('.chat-container').show()
}

// 根据操作码,处理接收到的消息数据
function handle_receive_message(data) {
    // 更细最近用户列表
    if (data.code == 'update_recent_user_list') {
        window.sessionStorage.setItem('recent_user_list', JSON.stringify(data));
        generate_chat_user_list();
    }
    else if (data.code == 'update_recent_user_list_and_open') {
        window.sessionStorage.setItem('recent_user_list', JSON.stringify(data));
        generate_chat_user_list();
        $('.chat-container').show()
    }
    // 处理消息数据
    else if (data.code == 'receive_message') {
        // 判断是否为当前用户
        if (!is_current_user(data.other_id)) {
            // 如果不是当前用户更新 用户最近列表的未读消息数
            send_socket_message('update_recent_user_list', '');
        }
        else {
            // 如果是当前用户 append到当前聊天内容中
            append_message_to_chat_content(data.msg);
            generate_chat_user_list();
        }
    }
    else if (data.code == 'recent_chat_message') {
        generate_chat_content_html(data);
        if(!is_current_user_list(data.other_id)) {
            append_tmp_user_to_user_list(data.other_id, data.other_name, data.other_avatar);
        }
    }
}


function get_message_cache_from_server(user_id, callback) {
    $.ajax({
        type: 'post',
        dataType: 'json',
        url: '/useropt',
        data: JSON.stringify({
            'opt': 'realtime-chat',
            'data': {'other': user_id}
        }),
        success: function (result, status) {
            if (result.errorcode == 0) {
                var message_cache = result.data;
                window.sessionStorage.setItem(user_id, JSON.stringify(message_cache));
                callback(message_cache);
            }
            else if (result.errorcode == -3) {
                $.notify(result.txt);
                return false;
            }
            else if (result.errorcode != 0) {
                $.notify(result.txt);
                return false;
            }
        }
    });
}


$(document).click(function (e) {

    if ($('.chat-container').is(":hidden")) {
        return;
    }
    else {
        // $(".chat-container").hide();
    }

    if ($("#emoji-list").is(":hidden")) {
        return;
    }
    else {
        $("#emoji-list").hide();
    }
});

$(document).ready(function () {
    $(".chat-close").on("click", function (e) {
        $(".chat-container").hide();
    });
    //replate_friendly_time();
    // set_theme();
    change_theme();
    load_font_avatar();
});
