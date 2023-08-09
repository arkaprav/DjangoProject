$(document).ready(function(){
    $('.menu').on('click', function(e){
        e.preventDefault();
        if($('.menu').hasClass('active') == true){
            $('.menu').removeClass('active')
        }
        $(this).addClass('active');
        id = $(this).attr('id');
        if(id == 'dashboard'){
            $('#content').html(personal);
        }
        if(id == 'orders'){
            $('#content').html(orders);
        }
        if(id == 'favourites'){
            $('#content').html(favourites);
        }
    })
    $('#update-details.update').on('click', function(e){
        e.preventDefault();
        dict = {}
        dict['csrfmiddlewaretoken'] = csrf_token;
        dict['username'] = $('#username').val();
        dict['firstname'] = $('#firstname').val();
        dict['lastname'] = $('#lastname').val();
        dict['email'] = $('#email').val();
        $.ajax({
            type: 'POST',
            url: profile,
            data: dict,
            success: function(response){
                console.log(response);
            },
            error: function(response){
                console.log(response);
            } 
        });
    });
});