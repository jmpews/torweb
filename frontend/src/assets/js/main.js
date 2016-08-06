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
