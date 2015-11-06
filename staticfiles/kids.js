var baseUrl='/';
var username;
var password;
var loginstring;

var doJoin=function() {
    var name=$("#name").val();
    username=$("#username").val();
    password=$("#password").val();
    $.ajax({
        type:'post',
        url:baseUrl+'api/user/create/',
        data:{
            username:username,
            name:name,
            password:password
        },
        success:function() {
            alert("OK");
            location.href=baseUrl+"login.html";
        },
        error:function(msg) {
            alert("Error!");
        },
    });
}

var goAdmin=function() {
    location.href="/admin/";
}
 
var doWriteTimeline=function() {
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

var doGetTimeline=function() {
    $.ajax({
        type:'GET',
        url:baseUrl+'api/timeline/',
        beforeSend:function(req) {
            req.setRequestHeader('Authorization',loginstring);
        },
        success:function(data){
            for(var i in data.messages) {
                doAppend(data.messages[i]);
            }
            $("#total").html(data.total_count);
            $("#mine").html($('[name=deleteMsg]').length-1);
            $("#username").html(username);
            $("#writearea").val("");
        },
        error:function(){
            alert("Fail to get data!");
        },
    });
}

var doAppend=function(data) {
    node=$("#msgTemplate").clone();
    $(".name",node).append(data.username);
    $(".content",node).append(data.message);
    $(".date",node).append(data.created);
    $(".like",node).append(data.liked+" ");
    $("#like",node).attr("value",data.id);
    $("#dislike",node).attr("value",data.id);
    if(username==data.username)
        $("[name=deleteMsg]",node).attr("value",data.id);
    else
        $("[name=deleteMsg]",node).remove();
    
    node.show();
    $("#timelinearea").append(node);
}

var doReload=function(){
    doClear();
    doGetTimeline();
}

var doClear=function() {
    $("#timelinearea").html("");
}

var doDeleteTimeline=function() {
    var id=$(this).val()+"/delete/";
    $.ajax({
        type:'post',
        url:baseUrl+'api/timeline/'+id,
        beforeSend:function(req) {
            req.setRequestHeader('Authorization',loginstring);
        },
        success:function(data){
            doReload();
        },
        error:function(msg) {
            alert("Fail to delete data!");
        },
    });
}

var doSearchTimeline=function() {
    $.ajax({
        type:'get',
        url:baseUrl+'api/timeline/find/',
        data:{query:$("#search").val()},
        beforeSend:function(req) {
            req.setRequestHeader('Authorization',loginstring);
        },
        success:function(data){
            doClear();
            for(var i in data) {
                doAppend(data[i]);
            }
            $("#total").html(data.length);
            $("#mime").html($('[name=deleteMsg]').length-1);
            $("#search").val("");
        },
        error:function(msg) {
            alert("Fail to get data!");
        },
    });
}


var doLike=function() {
    var id=$(this).val();
    $.ajax({
        type:'post',
        url:baseUrl+'api/timeline/'+id+'/like/',
        beforeSend:function(req) {
            req.setRequestHeader('Authorization',loginstring);
        },
        success:function(data){
            doReload();
        },
        error:function(msg) {
            alert("Fail to set data!");
        },
    });
}

var doGetUserInfo=function() {
    var username=$("div",this).html();
    $.ajax({
        type:'get',
        url:baseUrl+'api/profile/'+username,
        beforeSend:function(req) {
            req.setRequestHeader('Authorization',loginstring);
        },
        success:function(data){
            $("#modalid").html(data.username);
            $("#modalnickname").html(data.nickname);
            $("#modalcountry").html(data.country);
            $("#modalcomment").html(data.comment);
            $("#modalurl").html(data.url);
            $("#myModal").modal("show");
        },
        error:function(msg) {
            alert("Fail to get data!");
        },
    });
}

var doGetProfile=function() {
    $.ajax({
        type:'get',
        url:baseUrl+'api/profile/',
        beforeSend:function(req) {
            req.setRequestHeader('Authorization',loginstring);
        },
        success:function(data){
            fillProfile(data);
        },
        error:function(msg){
            alert("Fail to get data!");
        },
    });
}

var fillProfile=function(data) {
    $("#bigid").html(data.username);
    $("#bignickname").html("a.k.a "+data.nickname);
    $("#bigcomment").html(data.comment);

    $("#comment").val(data.comment);
    $("#nickname").val(data.nickname);
    $("#country").val(data.country);
    
    $("#web").val(data.url);
    $("#labelnick").html("Nickname : "+data.nickname);
    $("#labelcountry").html("Country : "+data.country);
    $("#labelurl").html("URL : "+data.url);
}

var doSetProfile=function() {
    var nickname=$("#nickname").val();
    var comment=$("#comment").val();
    var country=$("#country").val();
    var url=$("#web").val();

    $.ajax({
        type:'post',
        url:baseUrl+'api/profile/',
        data:{nickname:nickname,comment:comment,country:country,url:url},
        beforeSend:function(req) {
            req.setRequestHeader('Authorization',loginstring);
        },
        success:function(data){
            alert("OK");
            location.reload();
        },
        error:function(msg){
            alert("Error!");
        },
    })
}

var doCancel=function() {
    location.reload();
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
