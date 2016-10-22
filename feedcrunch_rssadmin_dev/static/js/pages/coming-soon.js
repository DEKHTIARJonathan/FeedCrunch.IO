$( document ).ready(function() {
     var twoDaysFromNow = new Date().valueOf() + 2 * 24 * 60 * 60 * 1000;
  $('#countdown').countdown(twoDaysFromNow, function(event) {
    var totalHours = event.offset.totalDays * 24 + event.offset.hours;
    $(this).html(event.strftime(totalHours + ':%M:%S'));
  });
});