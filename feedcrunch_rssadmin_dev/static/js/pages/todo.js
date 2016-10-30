$( document ).ready(function() {
    var todo = function() { 
        $('.todo-list .todo-item label').click(function() {
        if($(this).parent().children('input').is(':checked')) {
            $(this).parent().toggleClass('complete');
        } else {
            $(this).parent().toggleClass('complete');
        }
    });
    
    $('.todo-nav .all-task').click(function() {
        $('.todo-list').removeClass('only-active');
        $('.todo-list').removeClass('only-complete');
        $('.todo-nav li.active').removeClass('active');
        $(this).addClass('active');
    });
    
    $('.todo-nav .active-task').click(function() {
        $('.todo-list').removeClass('only-complete');
        $('.todo-list').addClass('only-active');
        $('.todo-nav li.active').removeClass('active');
        $(this).addClass('active');
    });
    
    $('.todo-nav .completed-task').click(function() {
        $('.todo-list').removeClass('only-active');
        $('.todo-list').addClass('only-complete');
        $('.todo-nav li.active').removeClass('active');
        $(this).addClass('active');
    });
    
    $('.all-check label').click(function() {
        if($(this).parent().children('input').is(':checked')) {
            $('.todo-list .todo-item input:checked + label').click();
        } else {
            $('.todo-list .todo-item input:not(:checked) + label').click();
        }
    });
    
    $('.remove-todo-item').click(function() {
        $(this).parent().remove();
    });
    };
    
    todo();
    
    $(".add-task").keypress(function (e) {
        var checkboxId = $('.todo-item').length + 1;
        if ((e.which == 13)&&(!$(this).val().length == 0)) {
            $('<div class="todo-item added"><input type="checkbox" id="todo' + checkboxId + '" /> <label for="todo' + checkboxId + '">' + $(this).val() + '</label><a href="javascript:void(0);" class="pull-right remove-todo-item"><i class="material-icons">delete</i></a></div>').insertAfter('.todo-list .todo-item:last-child');
            $(this).val('');
        } else if(e.which == 13) {
            alert('Please enter new task');
        }
        $('.todo-list .todo-item.added label').click(function() {
            if($(this).parent().children('input').is(':checked')) {
                $(this).parent().toggleClass('complete');
            } else {
                $(this).parent().toggleClass('complete');
            }
        });
        $('.todo-list .todo-item.added .remove-todo-item').click(function() {
            $(this).parent().remove();
        });
    });
});