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
