
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


var pdf_document=null;

function changePage(p){
    if(!pdf_document)
        return;
    pdf_document.getPage(p).then(function(page){
        // you can now use *page* here
        var viewport = page.getViewport({scale: 2});

        var canvas = document.getElementById('pdf-canvas');
        var context = canvas.getContext('2d');
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        var renderContext = {canvasContext: context, viewport: viewport};
        page.render(renderContext);
    });  
}

var loadingTask = pdfjsLib.getDocument(PDF_FILE);
loadingTask.promise.then(function(pdf){
    pdf_document=pdf;
    console.log("pages", pdf_document.numPages);
    changePage(1);
});
