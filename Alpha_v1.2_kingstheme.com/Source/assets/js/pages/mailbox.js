$( document ).ready(function() {
    jQuery.fn.extend({
    toggleText: function (a, b){
        var that = this;
        if (that.text() != a && that.text() != b){
            that.text(a);
        }
        else
            if (that.text() == a){
                that.text(b);
            }
        else
            if (that.text() == b){
                that.text(a);
            }
        return this;
    }
});
    $('.details-toggle').click(function() { 
        $('.details-list').toggle();
        $(".details-toggle").toggleText('Hide Details', 'Show Details');
    });
    
    var editor = new Simditor({
        textarea: $('#editor'),
        toolbar: [
  'bold',
  'italic',
  'underline',
  'strikethrough',
  'ol',
  'ul',
  'blockquote',
  'code'
]
    });
});