$(document).ready(function(){
    var nav = $('nav').children('ul').children('li');
    nav.each(function(i,e){
        let html = e.innerHTML.trim();
        if(html.match(a)){
            e.classList.add('active');
        }
    });
    let i = document.getElementById('price-range'),
    o = document.querySelector('output');
    // use 'change' instead to see the difference in response
    if(i){
        o.innerHTML = i.value;
    }
    if(i){
        i.oninput = function () {
            o.innerHTML = i.value;
        };
    }
    var con = {
      'brands':brands,
      'categories':categories
    }
    $('.categories').on('click', function() {
        if ($(this).is(':checked')) {
            // Show an alert when the checkbox is checked
            if(categories.indexOf($(this).attr('name')) !=-1){
                categories.push($(this).attr('name'));
            }
        }
        else{
            var index = categories.indexOf($(this).attr('name'));
            if (index > -1) {
                categories.splice(index, 1);
            }
        }
      });
    $('.brands').on('click', function() {
        if ($(this).is(':checked')) {
            // Show an alert when the checkbox is checked
            if(brands.indexOf($(this).attr('name')) !=-1){
                brands.push($(this).attr('name'));
            }
        }
        else{
            var index = brands.indexOf($(this).attr('name'));
            if (index > -1) {
                brands.splice(index, 1);
            }
        }
      });
      $('#i').on('click', function(e){
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'price': i.value,
                'brands': brands,
                'categories':categories,
                'csrfmiddlewaretoken': csrftoken,
            },
            success: function (response) {
                con = {
                    'brands':brands,
                    'categories':categories
                }
                var insert = `<div class="items">`;
                for(const key in response){
                    let output = `
                    <div style="background-image:linear-gradient(rgb(0,0,0,0.5),rgb(0,0,0,0.5)),url('${media_link}${response[key].featured_image}');">
                        <a href="/single-product/${response[key].slug}"><h3 id="name">${response[key].name}</h3></a>
                        <p class="price">price: ${response[key].price} INR </p>
                        <p class="rating"><i class="fa fa-star" style="font-size: 18px;"></i> ${response[key].rating} out of 5</p>
                        <p><span class="category">${response[key].category}</span>, <span class="brand">${response[key].brand}</span></p>
                    `;
                    if(login == '1'){
                        if(response[key].cart == 1){
                            output += `
                            <center id="{{j.id}}"><a href="${cart}"><button class="view-cart">View Cart &rarr;</button></a></center>
                            `;
                        }
                        else{
                            output += `
                            <center id="{{j.id}}"><button type="button" class="add-to-cart" id="{{j.id}}">Add to Cart</button></center>
                            `;
                        }
                    }
                    output += '</div>';
                    insert += output;
                }
                insert +=  '</div>';
                document.getElementById('container').innerHTML = insert;
            },
            error:function(response){
                console.log(response);
            }
        });
      });
      if(i){
        i.onchange = function() {
            var a = $(this).val();
            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'price': a,
                    'brands': con.brands,
                    'categories':con.categories,
                    'csrfmiddlewaretoken': csrftoken,
                },
                success: function (response) {
                    var insert = `<div class="items">`;
                    for(const key in response){
                        let output = `
                        <div style="background-image:linear-gradient(rgb(0,0,0,0.5),rgb(0,0,0,0.5)),url('${media_link}${response[key].featured_image}');">
                            <a href="/single-product/${response[key].slug}"><h3 id="name">${response[key].name}</h3></a>
                            <p class="price">price: ${response[key].price} INR </p>
                            <p class="rating"><i class="fa fa-star" style="font-size: 18px;"></i> ${response[key].rating} out of 5</p>
                            <p><span class="category">${response[key].category}</span>, <span class="brand">${response[key].brand}</span></p>
                        `;
                        if(login == '1'){
                            if(response[key].cart == 1){
                                output += `
                                <center id="{{j.id}}"><a href="${cart}"><button class="view-cart">View Cart &rarr;</button></a></center>
                                `;
                            }
                            else{
                                output += `
                                <center id="{{j.id}}"><button type="button" class="add-to-cart" id="{{j.id}}">Add to Cart</button></center>
                                `;
                            }
                        }
                        output += '</div>';
                        insert += output;
                    }
                    insert +=  '</div>';
                    document.getElementById('container').innerHTML = insert;
                },
                error: function(response){
                    console.log(response);
                }
            });
        }
      }
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
                $('center#'.concat(id)).html(`<a href="${cart}"><button class="view-cart">View Cart &rarr;</button></a>`);
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
    $('#order').on('click', function(e){
        e.preventDefault();
        let err = $('#error');
        err.css('display', 'block');
        var e = '';
        let username = $('input[name=username]').val();
        if(username == null || username == ''){
            e += "Invalid Username<br>";
        }
        let firstname = $('input[name=firstname]').val();
        if(firstname == null || firstname == ''){
            e += "Invalid Firstname<br>";
        }
        let lastname = $('input[name=lastname]').val();
        if(lastname == null || lastname == ''){
            e += "Invalid Lastname<br>";
        }
        let email = $('input[name=email]').val();
        if(email == null || email == ''){
            e += "Invalid Email<br>";
        }
        let address = $('input[name=address]').val();
        if(address == null || address == ''){
            e += "Invalid Address<br>";
        }
        let payment = $('input[name=payment]:checked').val();
        if(payment == null){
            e += "Choose a Payment Method<br>";
        }
        err.html(e);
        var order_dict = {
            'csrfmiddlewaretoken': csrftoken,
            'username': username,
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'address': address,
            'payment': payment,
        }
        if((username != null || username != '') && (firstname != null || firstname != '') && (lastname  != null || lastname  != '') && (email  != null || email  != '') && (address  != null || address  != '') && payment  != null){
            $.ajax({
                type: "POST",
                url: order,
                data:order_dict,
                success: function(response){
                    window.location = order
                },
                error: function(response){
                    console.log(response);
                }
            })
        }
    })
});
