$(function(){

    $(".js-add-litigant").click(function(){
        var btn = $(this);
       $.ajax({
           url: btn.attr('data-url'),
           type: 'get',
           dataType: 'json',
           success: function(data) {
               $("#modal-litigant .modal-content").html(data.html_form);
               // Only show modal AFTER the json form data has been received; this prevents a previously populated form
               // entry from showing up and being instantly overridden when the new data is received, thus confusing the user.
               $("#modal-litigant").modal("show");
           }
       });

    });

    $(".js-edit-litigant").click(function(){
        var btn = $(this);
       $.ajax({
           url: btn.attr('data-url'),
           type: 'get',
           dataType: 'json',
           success: function(data) {
               $("#modal-litigant .modal-content").html(data.html_form);
               $("#modal-litigant").modal("show");
           }
       });
    });

    $("#modal-litigant").on("submit", ".js-add-litigant-form", function(){
        var form = $(this);
        console.log('clicked some shit');
       // return false is used because we are capturing the submit event and this will stop the browser from performing
        // a full HTTP POST to the server
       return false;
    });

});