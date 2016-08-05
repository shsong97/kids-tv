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
