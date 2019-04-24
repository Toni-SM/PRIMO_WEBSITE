
function validateData(){
    if(!$("#field-name").val().length){
        return false;
    }
    if(!$("#field-surname").val().length){
        return false;
    }
    // if(!$("#field-institute").val().length){
        // return false;
    // }
    if(!$("#field-category").val().length){
        return false;
    }
    if(!$("#field-email").val().length){
        return false;
    }
    if(!$("#field-password").val().length){
        return false;
    }
    if(!$("#field-repeat-password").val().length){
        return false;
    }
    return true;
}

function register(){
    // validate
    if(!validateData())
        return;
    
    // check password
    if($("#field-password").val()!=$("#field-repeat-password").val()){
        showMessage("warning", "The passwords didn't match. Try again", 2500);
        return;
    }
    
    if($("#field-password").val().length<8){
        showMessage("warning", "Please choose a stronger password. Try a mix of letters, numbers, and symbols.", 2500);
        return;
    }
    
    var data={
        "name": $("#field-name").val(),
        "surname": $("#field-surname").val(),
        "institute": $("#field-institute").val(),
        "category": $("#field-category").val(),
        "email": $("#field-email").val(),
        "password": $("#field-password").val()
    };
    
    $.post('/register', {"data": JSON.stringify(data)}, function(response){
        console.log(response);
        if(response.status){
            window.open("/login", "_self");
        }
        else{
            showMessage("warning", response.message, 2500);
        }
    });
}

$('#button-register').click(function(){
    register();
});
