$(function(){
    var loadForm = function(){
        var url = $(this).attr('data-url');
        $.ajax({
            url: url,
            type: 'get',
            dataType: 'json',
            success: function(data){
                $('#modal-litigant .modal-content').html(data.html_form);
            },
            complete: function(){
                $('#modal-litigant').modal('show');
            }
        })
    };

    var saveForm = function(){
        console.log('bing!');
        var form = $(this);
        $.ajax({
            url: form.attr('action'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',
            success: function(data){
                if(data.form_is_valid){
                   $('#ajax_litigant_list ul').html(data.html_litigant_list);
                   $('#modal-litigant').modal('hide');
                } else {
                    $('#modal-litigant .modal-content').html(data.html_form);
                }
            }
        })
    return false
    };

    var loadDeleteForm = function(){
        var url = $(this).attr('data-url');
        $.ajax({
            url: url,
            type: 'get',
            dataType: 'json',
            success: function(data){
                $('#modal-delete-litigant .modal-content').html(data.html_form);
            },
            complete: function(){
                $('#modal-delete-litigant').modal('show');
            }
        })
    };

    var saveDeleteForm = function(){
        console.log('bing!');
        var form = $(this);
        $.ajax({
            url: form.attr('action'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',
            success: function(data){
                if(data.form_is_valid){
                   $('#ajax_litigant_list ul').html(data.html_litigant_list);
                   $('#modal-delete-litigant').modal('hide');
                } else {
                    $('#modal-delete-litigant .modal-content').html(data.html_form);
                }
            }
        })
    return false
    };


$('#add_litigant').click(loadForm);
$('#modal-litigant').on('submit', '.add-litigant-form', saveForm);

$('#ajax_litigant_list').on('click', '.edit_litigant', loadForm);
$('#modal-litigant').on('submit', '.edit_litigant_form', saveForm);

$('#ajax_litigant_list').on('click', '.delete_litigant', loadDeleteForm);
$('#modal-delete-litigant').on('submit', '.delete_litigant_form', saveDeleteForm);

});
