$(document).ready(function(){
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
    });
});