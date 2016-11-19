var baseUrl='/';
var username;
var password;
var loginstring;

var goAdmin=function() {
    location.href="/admin/";
} 

// cookie function
function setCookie(name, value, day) {
    var expire=new Date();
    expire.setDate(expire.getDate()+day);
    cookies=name+'='+escape(value)+';path=/';
    if(typeof day!= 'undefined')
        cookies+=';expires='+expire.toGMTString()+";";
    document.cookie=cookies;
}

function getCookie(name) {
    name=name+'=';
    var cookieData=document.cookie;
    var start=cookieData.indexOf(name);
    var value='';
    if (start != -1) {
        start+=name.length;
        var end=cookieData.indexOf(';',start);
        if(end == -1)
            end=cookieData.length;
        value=cookieData.substring(start,end);
    }
    return unescape(value);
}


function button_like() {
    var item=$(document);
    var kids_id=item.find("#span_like").attr('value');
    $.ajax({
        url:"/detail/"+kids_id+"/like",
        dataType:'json',
        success:function(result){
            console.log(result)
            item.find("#span_like").text(result['like_count']);
            if(result['my_click'])
                item.find("#button_like").attr('class',"btn-like btn-display");
            else
                item.find("#button_like").attr('class',"btn-unlike btn-display");
        },
        error:function(e) {
            alert(e.responseText);
        }
    });
}
 
$(document).ready(function() {
    $(document).on("click","#button_like",button_like);
})