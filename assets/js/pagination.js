$(function(container){
    var url = $(this).attr('data-url');
    var div = container;
        $.ajax({
            url: url,
            type: 'get',
            dataType: 'json',
            success: function(data){
                $(container).html(data.html_list);
            }
        })
});