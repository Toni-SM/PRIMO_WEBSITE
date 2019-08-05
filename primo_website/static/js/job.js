
function validation(validation_status){
    
    var data={
        "status": validation_status,
        "job": JOB_ID
    };
    
    $.post('/job-validation', {"data": JSON.stringify(data)}, function(response){
        console.log(response);
        window.open("/job/"+JOB_ID+"?tab=1", "_self"); 
        // if(response.status){
            // window.open("/accounts", "_self");
        // }
        // else{
            // showMessage("danger", response.message, 2500);
        // }
    });
}

$('#button-validate-job').click(function(){
    validation("validate");
});

$('#button-invalidate-job').click(function(){
    validation("invalidate");
});

$('#button-remove-validation').click(function(){
    validation("remove");
});
