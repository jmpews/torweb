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
    $('.all-cate-card .card-block').mouseenter(function (e) {
        $(".card-header-all").css('display', 'none');
    })
}

// 显示隐藏所有分类(post-new页面)
function post_new_show_hide_cate() {
    // $(".post-new-html #topic").on('click', function (e) {
    //     $(".card-header-all").css('display', 'block');
    // });
    // $(".post-new-html .card-header-all-cate a").on('click', function (e) {
    //     $(".card-header-all").css('display', 'none');
    //     $("#topic").val($(this).html());
    // });
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
$("#loginModal [type='submit']").on('click', function (event) {
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
            $('.loading').hide();
            $('#loginModal .captcha').click();
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
    if(src == "") {
        src = "/utils/captcha";
    }
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
    //replate_friendly_time();
    // set_theme();
    change_theme();
    load_font_avatar();
});

/**
 * Created by jmpews on 2016/10/31.
 */

$('.dropdown-menu').on('click', function (e) {
    console.log('dropdown-menu.click');
    if ($(e.currentTarget).is(":hidden")) {
        return
    }
    $(e.currentTarget).hide();
});


function init_tiny_nav() {
    var current_url = location.href;
    var current_filter = url('?filter', current_url);
    $('.tiny-nav .nav-item').each(function (e) {
        var f = url('?filter', $(this).attr('href'))
        if ((!current_filter) && f == 'all') {
            $(this).addClass('transition active');
            return
        }
        if (f == current_filter) {
            $(this).addClass('transition active');
            return
        }
    });
}

window.url = (function() {

    function _t() {
        return new RegExp(/(.*?)\.?([^\.]*?)\.?(com|net|org|biz|ws|in|me|co\.uk|co|org\.uk|ltd\.uk|plc\.uk|me\.uk|edu|mil|br\.com|cn\.com|eu\.com|hu\.com|no\.com|qc\.com|sa\.com|se\.com|se\.net|us\.com|uy\.com|ac|co\.ac|gv\.ac|or\.ac|ac\.ac|af|am|as|at|ac\.at|co\.at|gv\.at|or\.at|asn\.au|com\.au|edu\.au|org\.au|net\.au|id\.au|be|ac\.be|adm\.br|adv\.br|am\.br|arq\.br|art\.br|bio\.br|cng\.br|cnt\.br|com\.br|ecn\.br|eng\.br|esp\.br|etc\.br|eti\.br|fm\.br|fot\.br|fst\.br|g12\.br|gov\.br|ind\.br|inf\.br|jor\.br|lel\.br|med\.br|mil\.br|net\.br|nom\.br|ntr\.br|odo\.br|org\.br|ppg\.br|pro\.br|psc\.br|psi\.br|rec\.br|slg\.br|tmp\.br|tur\.br|tv\.br|vet\.br|zlg\.br|br|ab\.ca|bc\.ca|mb\.ca|nb\.ca|nf\.ca|ns\.ca|nt\.ca|on\.ca|pe\.ca|qc\.ca|sk\.ca|yk\.ca|ca|cc|ac\.cn|com\.cn|edu\.cn|gov\.cn|org\.cn|bj\.cn|sh\.cn|tj\.cn|cq\.cn|he\.cn|nm\.cn|ln\.cn|jl\.cn|hl\.cn|js\.cn|zj\.cn|ah\.cn|gd\.cn|gx\.cn|hi\.cn|sc\.cn|gz\.cn|yn\.cn|xz\.cn|sn\.cn|gs\.cn|qh\.cn|nx\.cn|xj\.cn|tw\.cn|hk\.cn|mo\.cn|cn|cx|cz|de|dk|fo|com\.ec|tm\.fr|com\.fr|asso\.fr|presse\.fr|fr|gf|gs|co\.il|net\.il|ac\.il|k12\.il|gov\.il|muni\.il|ac\.in|co\.in|org\.in|ernet\.in|gov\.in|net\.in|res\.in|is|it|ac\.jp|co\.jp|go\.jp|or\.jp|ne\.jp|ac\.kr|co\.kr|go\.kr|ne\.kr|nm\.kr|or\.kr|li|lt|lu|asso\.mc|tm\.mc|com\.mm|org\.mm|net\.mm|edu\.mm|gov\.mm|ms|nl|no|nu|pl|ro|org\.ro|store\.ro|tm\.ro|firm\.ro|www\.ro|arts\.ro|rec\.ro|info\.ro|nom\.ro|nt\.ro|se|si|com\.sg|org\.sg|net\.sg|gov\.sg|sk|st|tf|ac\.th|co\.th|go\.th|mi\.th|net\.th|or\.th|tm|to|com\.tr|edu\.tr|gov\.tr|k12\.tr|net\.tr|org\.tr|com\.tw|org\.tw|net\.tw|ac\.uk|uk\.com|uk\.net|gb\.com|gb\.net|vg|sh|kz|ch|info|ua|gov|name|pro|ie|hk|com\.hk|org\.hk|net\.hk|edu\.hk|us|tk|cd|by|ad|lv|eu\.lv|bz|es|jp|cl|ag|mobi|eu|co\.nz|org\.nz|net\.nz|maori\.nz|iwi\.nz|io|la|md|sc|sg|vc|tw|travel|my|se|tv|pt|com\.pt|edu\.pt|asia|fi|com\.ve|net\.ve|fi|org\.ve|web\.ve|info\.ve|co\.ve|tel|im|gr|ru|net\.ru|org\.ru|hr|com\.hr|ly|xyz)$/);
    }

    function _d(s) {
      return decodeURIComponent(s.replace(/\+/g, ' '));
    }

    function _i(arg, str) {
        var sptr = arg.charAt(0),
            split = str.split(sptr);

        if (sptr === arg) { return split; }

        arg = parseInt(arg.substring(1), 10);

        return split[arg < 0 ? split.length + arg : arg - 1];
    }

    function _f(arg, str) {
        var sptr = arg.charAt(0),
            split = str.split('&'),
            field = [],
            params = {},
            tmp = [],
            arg2 = arg.substring(1);

        for (var i = 0, ii = split.length; i < ii; i++) {
            field = split[i].match(/(.*?)=(.*)/);

            // TODO: regex should be able to handle this.
            if ( ! field) {
                field = [split[i], split[i], ''];
            }

            if (field[1].replace(/\s/g, '') !== '') {
                field[2] = _d(field[2] || '');

                // If we have a match just return it right away.
                if (arg2 === field[1]) { return field[2]; }

                // Check for array pattern.
                tmp = field[1].match(/(.*)\[([0-9]+)\]/);

                if (tmp) {
                    params[tmp[1]] = params[tmp[1]] || [];
                
                    params[tmp[1]][tmp[2]] = field[2];
                }
                else {
                    params[field[1]] = field[2];
                }
            }
        }

        if (sptr === arg) { return params; }

        return params[arg2];
    }

    return function(arg, url) {
        var _l = {}, tmp, tmp2;

        if (arg === 'tld?') { return _t(); }

        url = url || window.location.toString();

        if ( ! arg) { return url; }

        arg = arg.toString();

        if (tmp = url.match(/^mailto:([^\/].+)/)) {
            _l.protocol = 'mailto';
            _l.email = tmp[1];
        }
        else {

            // Ignore Hashbangs.
            if (tmp = url.match(/(.*?)\/#\!(.*)/)) {
                url = tmp[1] + tmp[2];
            }

            // Hash.
            if (tmp = url.match(/(.*?)#(.*)/)) {
                _l.hash = tmp[2];
                url = tmp[1];
            }

            // Return hash parts.
            if (_l.hash && arg.match(/^#/)) { return _f(arg, _l.hash); }

            // Query
            if (tmp = url.match(/(.*?)\?(.*)/)) {
                _l.query = tmp[2];
                url = tmp[1];
            }

            // Return query parts.
            if (_l.query && arg.match(/^\?/)) { return _f(arg, _l.query); }

            // Protocol.
            if (tmp = url.match(/(.*?)\:?\/\/(.*)/)) {
                _l.protocol = tmp[1].toLowerCase();
                url = tmp[2];
            }

            // Path.
            if (tmp = url.match(/(.*?)(\/.*)/)) {
                _l.path = tmp[2];
                url = tmp[1];
            }

            // Clean up path.
            _l.path = (_l.path || '').replace(/^([^\/])/, '/$1').replace(/\/$/, '');

            // Return path parts.
            if (arg.match(/^[\-0-9]+$/)) { arg = arg.replace(/^([^\/])/, '/$1'); }
            if (arg.match(/^\//)) { return _i(arg, _l.path.substring(1)); }

            // File.
            tmp = _i('/-1', _l.path.substring(1));
            
            if (tmp && (tmp = tmp.match(/(.*?)\.(.*)/))) {
                _l.file = tmp[0];
                _l.filename = tmp[1];
                _l.fileext = tmp[2];
            }

            // Port.
            if (tmp = url.match(/(.*)\:([0-9]+)$/)) {
                _l.port = tmp[2];
                url = tmp[1];
            }

            // Auth.
            if (tmp = url.match(/(.*?)@(.*)/)) {
                _l.auth = tmp[1];
                url = tmp[2];
            }

            // User and pass.
            if (_l.auth) {
                tmp = _l.auth.match(/(.*)\:(.*)/);

                _l.user = tmp ? tmp[1] : _l.auth;
                _l.pass = tmp ? tmp[2] : undefined;
            }

            // Hostname.
            _l.hostname = url.toLowerCase();

            // Return hostname parts.
            if (arg.charAt(0) === '.') { return _i(arg, _l.hostname); }

            // Domain, tld and sub domain.
            if (_t()) {
                tmp = _l.hostname.match(_t());

                if (tmp) {
                    _l.tld = tmp[3];
                    _l.domain = tmp[2] ? tmp[2] + '.' + tmp[3] : undefined;
                    _l.sub = tmp[1] || undefined;
                }
            }

            // Set port and protocol defaults if not set.
            _l.port = _l.port || (_l.protocol === 'https' ? '443' : '80');
            _l.protocol = _l.protocol || (_l.port === '443' ? 'https' : 'http');
        }

        // Return arg.
        if (arg in _l) { return _l[arg]; }

        // Return everything.
        if (arg === '{}') { return _l; }

        // Default to undefined for no match.
        return undefined;
    };
})();

if(typeof jQuery !== 'undefined') {
    jQuery.extend({
        url: function(arg, url) { return window.url(arg, url); }
    });
}