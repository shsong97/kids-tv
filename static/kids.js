
var addYoutube=function() {
    var msg=$("#writearea").val();
    $.ajax({
        type:"POST",
        url:baseUrl+"api/timeline/create/",
        data:{ message : msg },
        beforeSend:function(req) {
            req.setRequestHeader('Authorization',loginstring);
        },
        success:function(){
            alert("OK");
            doReload();
        },
        error:function(){
            alert("Fail to write data!");
        },
    });
}