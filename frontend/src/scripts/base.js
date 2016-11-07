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
