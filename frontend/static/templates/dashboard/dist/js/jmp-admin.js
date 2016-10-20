
function get_post_list() {
    $.ajax({
        type: 'post',
        dataType: 'json',
        url: '/db/post',
        data: JSON.stringify({'opt': 'get-post-list', 'data': ' '}),
        success: function (result, status) {
            if (result.errorcode == 0) {
                var data = result.data;
                for(var i = 0; i< data.length; i++) {

                }
            }
            else {
                alert(result.txt);
            }
        }
    });
}

$('.post-edit').on('click', function (e) {
    alert('post-edit-' + $(e.currentTarget).parents('[post-id]').attr('post-id'));
});

$('.post-del').on('click', function (e) {
    alert('post-del-' + $(e.currentTarget).parents('[post-id]').attr('post-id'));
});


$('.user-edit').on('click', function (e) {
    alert('user-edit-' + $(e.currentTarget).parents('[user-id]').attr('user-id'));
});

$('.user-del').on('click', function (e) {
    alert('user-del-' + $(e.currentTarget).parents('[user-id]').attr('user-id'));
});
