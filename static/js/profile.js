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
});