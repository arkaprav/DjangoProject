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

    o.innerHTML = i.value;

    // use 'change' instead to see the difference in response
    i.oninput = function () {
        o.innerHTML = i.value;
    };
    $('.categories').on('click', function() {
        if ($(this).is(':checked')) {
            // Show an alert when the checkbox is checked
            if(categories.indexOf($(this).attr('name'))==-1){
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
            if(brands.indexOf($(this).attr('name'))==-1){
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
      var con = {
        'brands':brands,
        'categories':categories
      }
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
                        <h3 id="name">${response[key].name}</h3>
                        <p class="price">price: ${response[key].price} INR </p>
                        <p class="rating"><i class="fa fa-star" style="font-size: 18px;"></i> ${response[key].rating} out of 5</p>
                        <p><span class="category">${response[key].category}</span>, <span class="brand">${response[key].brand}</span></p>
                    </div>
                    `;
                    insert += output;
                }
                insert +=  '</div>';
                document.getElementById('container').innerHTML = insert;
            }
        });
      });
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
                        <h3 id="name">${response[key].name}</h3>
                        <p class="price">price: ${response[key].price} INR </p>
                        <p class="rating"><i class="fa fa-star" style="font-size: 18px;"></i> ${response[key].rating} out of 5</p>
                        <p><span class="category">${response[key].category}</span>, <span class="brand">${response[key].brand}</span></p>
                    </div>
                    `;
                    insert += output;
                }
                insert +=  '</div>';
                document.getElementById('container').innerHTML = insert;
            }
        });
    }
});
