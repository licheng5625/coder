function removeReblogs () {
    var page = document.getElementById("left_column");
    var posts = page.getElementsByTagName("ol");
    var postlist = posts[0].getElementsByTagName("li");
    var classdata;
    var is_reblog;
    var elements;
    var alltags;
    for (i = postlist.length - 1; i > 0; i--) {
        classdata = postlist[i].className;
        is_reblog = (classdata.search(/is_reblog/) != -1);
        if (is_reblog) {
            postlist[i].innerHTML = classdata;
            postlist[i].parentNode.removeChild(postlist[i]);
        }
    }
    setTimeout(function(){removeReblogs()}, 200);
}

removeReblogs();
