$(document).ready(function(){
    var nav = $('nav').children('ul').children('li');
    nav.each(function(i,e){
        let html = e.innerHTML.trim();
        if(html.match(a)){
            e.classList.add('active');
        }
    });
    let i = document.getElementById('price'),
    o = document.querySelector('output');

    o.innerHTML = i.value;

    // use 'change' instead to see the difference in response
    i.addEventListener('input', function () {
        o.innerHTML = i.value;
    }, false);
});
