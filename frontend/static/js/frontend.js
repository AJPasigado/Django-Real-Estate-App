function modifyURL(name, value) {
    var href = window.location.href;
    var regex = new RegExp("[&\\?]" + name + "=.+");

    if (regex.test(href)) {
        window.location.href = href.replace(regex, "&" + name + "=" + value);
    }
    else {
        if(href.indexOf("?") > -1)
            window.location.href = href + "&" + name + "=" + value;
        else
            window.location.href = href + "?&" + name + "=" + value;
    }
}

function submitform(){
    document.getElementById("querybox").value = document.getElementById("navsearchbox").value;
    document.getElementById("optionsbox").value = document.getElementById("navsearchtick").checked ?  "sale" : "rent";
}

function hidefilter(){
    document.getElementById("searchfilters").addClass("invisible");
}

$('.search-filterbadge').on("click", function() {
    $('.search-filtercont').slideToggle( 500, function() {
        if ( $('.search-filterbadge').text() == "HIDE FILTERS ⯅"){
            $('.search-filterbadge').text("SHOW FILTERS ⯆");
            $('.search-filtersapplied').fadeIn(200);
        } else {
            $('.search-filterbadge').text("HIDE FILTERS ⯅");
            $('.search-filtersapplied').fadeOut(200);
        }
    });
});

$('.prod-desccontread').on("click", function() {
        if ( $('.prod-desccontread').text() == "Read More"){
            $('.prod-desccontread').text("Read Less");
            
            $('.prod-desccont').addClass("prod-desccontmax");
        } else {
            $('.prod-desccontread').text("Read More");
            
            $('.prod-desccont').removeClass("prod-desccontmax");
        }
});