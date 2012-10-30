(function($) {
    $(document).ajaxSend(function(event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        function sameOrigin(url) {
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                !(/^(\/\/|http:|https:).*/.test(url));
        }
        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });
    $(document).ready(function() {
        var submit_form = function(form_object) {
            form_object.find('.success').hide();
            form_object.find('.error').hide();
            var values = {};
            form_object.find(':input').each(function() {
                values[this.name] = $(this).val();
            });
            $.ajax({
                type: "POST",
                url: form_object.attr('action'),
                data: values,
                success: function(data) {
                    form_object.find('.success').show();
                    form_object.trigger('vote_submit', [data]);
                },
                error: function() {
                    form_object.find('.error').show();
                }
            });
        };
        $('form.ratings').each(function() {
            var form_object = $(this);
            form_object.submit(function() {
                submit_form(form_object);
                return false;
            });
            form_object.bind('star_change', function(event, value) {
                submit_form(form_object);
            });
            form_object.bind('star_delete', function(event) {
                submit_form(form_object);
            });
            form_object.bind('slider_delete', function(event) {
                submit_form(form_object);
            });
        });
    });
})(jQuery);
