
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


var currentPdfDocument=null;
var currentNumberOfPages=null;
var currentPage=0;

function shiftPage(s){
    changePage(currentPage+s);
}

function changePage(p){
    if((!currentPdfDocument || !p) || p>currentNumberOfPages)
        return;
    currentPage=p;
    currentPdfDocument.getPage(p).then(function(page){
        // you can now use *page* here
        var viewport = page.getViewport({scale: 2});

        var canvas = document.getElementById('pdf-canvas');
        var context = canvas.getContext('2d');
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        var renderContext = {canvasContext: context, viewport: viewport};
        page.render(renderContext);

        // pagination
        $("#li-pagination-current").html("&nbsp;"+String(currentPage)+" of "+String(currentNumberOfPages)+"&nbsp;");
        
        if(currentNumberOfPages<=1){
            $("#li-pagination-previous").toggleClass("disabled", true);
            $("#li-pagination-next").toggleClass("disabled", true);
        }
        else{
            $("#li-pagination-previous").toggleClass("disabled", currentPage==1);
            $("#li-pagination-next").toggleClass("disabled", currentPage==currentNumberOfPages);
        }
    });      
}

var loadingTask = pdfjsLib.getDocument(PDF_FILE);
loadingTask.promise.then(function(pdf){
    currentPdfDocument=pdf;
    
    // create pagination
    currentNumberOfPages=currentPdfDocument.numPages;
    
    // change page
    changePage(1);
});
