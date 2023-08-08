$(document).ready(function(){
    $('.add-to-cart').on('click', function(){
        var id = $(this).attr('id');
        $.ajax({
            type: "POST",
            url: cart,
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'id': id,
            },
            success: function(response) {
                let co = document.querySelector('#center-'.concat(id));
                co.innerHTML = `<a href="${cart}"><button class="view-cart">View Cart &rarr;</button></a>`;
            },
            error: function(response){
                console.log(response);
            }
        });
    });
    $('#update').on('click', function(e){
        e.preventDefault();
        var cont = $('.cart tbody').children();
        var dict = {}
        cont.each(function(i, e){
            let id = $(this).attr('id');
            if(id){
                let c = '.cart tbody tr td input#quantity-'.concat(id);
                dict[id] = $(c).val();
            }
        });
        $.ajax({
            type: "POST",
            url: cart,
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'dict': JSON.stringify(dict),
            },
            success: function(response) {
                var tot = 0;
                for(const key in dict){
                    let f = '.bill div span#quantity-'.concat(key);
                    $(f).text(dict[key]);
                    let g = '.cart tbody tr td#price-'.concat(key);
                    let cost = dict[key] * parseInt($(g).text());
                    tot += cost;
                    let inp = '.bill div p span#price-'.concat(key);
                    $(inp).text(cost);
                }
                let total = '.bill div p span#price-total';
                $(total).text(tot);
            },
            error: function(response){
                console.log(response);
            }
        });
    });
    $('.fa-trash').on('click', function(){
        var id = $(this).attr('id');
        $.ajax({
            type: "POST",
            url: cart,
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'delete': id,
            },
            success: function(response) {
                $('tr#'.concat(id)).remove();
                let price = parseInt($('.bill div#'.concat(id,' p span#price-',id)).html());
                let tot = parseInt($('.bill div p span#price-total').text()) - price;
                $('.bill div#'.concat(id)).remove();
                $('.bill div p span#price-total').text(tot);
                if( $('.cart tbody').children().length == 1){
                    $('<div class="empty"><p>0 items Added</p></div>').insertAfter('.cart');
                    $('#update').remove();
                    $('.bill').remove();
                }
            },
            error: function(response){
                console.log(response);
            }
        });
    });
})