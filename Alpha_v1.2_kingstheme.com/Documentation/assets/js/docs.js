$( document ).ready(function() {
       $('#search').bind('keyup change', function(ev) {
        // pull in the new value
        var searchTerm = $(this).val();

        // remove any old highlighted terms
        $('body').removeHighlight();

        // disable highlighting if empty
        if ( searchTerm ) {
            // highlight the new term
            $('.mn-inner').highlight( searchTerm );
        }
    });
    
    $('a[href^="#"]').on('click',function (e) {
        e.preventDefault();

        var target = this.hash;
        var $target = $(target);
        var scrollTo = $target.offset().top - 70

        $('html, body').stop().animate({
            'scrollTop': scrollTo
        }, 1000, 'easeInOutExpo');
    });
    $('pre').addClass('prettyprint');
    prettyPrint();
});
