$(document).ready(function(){
    dict = {}
    $('.left-arrow').on('click', function(e){
        e.preventDefault();
        let id = $(this).attr('id');
        if(dict.hasOwnProperty(id) == false){
            dict[id] = {
                'total': $('.items#'.concat(id)).children().length-3,
                'reached': 0,
            }
        }
        if(dict[id]['total'] != dict[id]['reached']){
            let margin = $('.items#'.concat(id,' div:first-child')).css('margin-left');
            let spec_margin = String(parseInt(margin) - 460).concat('px');
            $('.items#'.concat(id,' div:first-child')).css('margin-left', spec_margin);
            dict[id]['reached'] += 1;
        }
    });
    $('.right-arrow').on('click', function(e){
        e.preventDefault();
        let id = $(this).attr('id');
        if(dict.hasOwnProperty(id) == false){
            dict[id] = {
                'total': $('.items#'.concat(id)).children().length-3,
                'reached': 0,
            }
        }
        if(dict[id]['reached'] != 0){
            let margin = $('.items#'.concat(id,' div:first-child')).css('margin-left');
            let spec_margin = String(parseInt(margin) + 460).concat('px');
            $('.items#'.concat(id,' div:first-child')).css('margin-left', spec_margin);
            dict[id]['reached'] += 1;
        }
    });
})