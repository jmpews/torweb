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