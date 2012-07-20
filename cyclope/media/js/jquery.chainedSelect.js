/**
 * jQuery ChainedSelect
 *
 * Chain multiple select lists to each other, so changing an option in one
 * (the parent) modifies the options in the others (the targets).
 *
 * Based on Remy Sharp's "selectChain" plugin, available at:
 * http://remysharp.com/2007/09/18/auto-populate-multiple-select-boxes/
 *
 * @author Stanislaus Madueke (stan DOT madueke AT gmail DOT com)
 * @requires jQuery 1.2.6 or later
 *
 * Licensed under the New BSD License
 * See: http://www.opensource.org/licenses/bsd-license.php
 */
(function($) {
    $.fn.chainedSelect = function(options) {
        var settings = $.extend({}, $.fn.chainedSelect.defaults, options);
        var cache = settings.cacheClass(settings);

        return this.each(function() {
            var $$ = $(this);
            // Load metadata for this Select element, if available:
            var opts = $.metadata ? $.extend({}, settings, $$.metadata()) : settings;
            // Add a preloader GIF beside this element, if "preloadUrl" is present:
            var showPreloader, hidePreloader;
            if (opts.preloadUrl) {
                opts.preloader = $('<img />').css({
                    position: 'absolute',
                    border: 'none',
                    display: 'none'
                }).attr('src', opts.preloadUrl);
                $$.after(opts.preloader);

                showPreloader = function() {
                    opts.preloader.css({
                        left: $$.position().left + $$.outerWidth() + 5,
                        top: $$.position().top + ($$.outerHeight()/2) - 8
                    }).show();
                }
                hidePreloader = function() {
                    opts.preloader.hide();
                }
            } else {
                showPreloader = hidePreloader = function(){};
            }

            if (!(opts.parent instanceof $)) opts.parent = $(opts.parent);

            opts.parent.change(function() {
                var param = $(this).val();
                var key = $(this).attr('id') + '::' + param;

                $$.attr('disabled', 'disabled');

                var data = cache.getItem(key);
                if (data) {
                    addOptions($$, opts, data);
                } else {
                    showPreloader();
                    $.ajax({
                        url: opts.url,
                        data: {'q': param},
                        type: (opts.type || 'get'),
                        dataType: 'json',
                        global: false,
                        success: function(data) {
                            addOptions($$, opts, data);
                            hidePreloader();
                            cache.setItem(key, data);
                        },
                        error: function(xhr, msg, e) {
                            if (opts.error) opts.error(xhr, msg, e);
                        }
                    });
                }
            });

            if (opts.parent.val()) {
                // If the parent list has a selected value, trigger
                // its "change" event so chained lists can update
                // their options:
                opts.parent.trigger('change');
            }
        });
    }

    function addOptions(target, opts, data) {
        var curValue = target.val();
        target.empty();

        for (i=0; i<data.length; i++) {
            var value, label;
            if (typeof data[i] == 'object') {
                value = data[i][opts.value];
                label = data[i][opts.label];
            } else {
                value = label = data[i];
            }
            target.get(0).options[i] = new Option(label, value);
        }

        // Restore the previous selection. If nothing was selected
        // before, select the first option:
        if (curValue) {
            target.val(curValue);
        } else {
            target.find('option:first').attr('selected', 'selected');
        }
        // Trigger the change event, so other lists chained to this
        // one get updated too:
        target.attr('disabled', '').trigger('change');
    }

    /*
     * A Quick-n-dirty LRU cache.
     *
     * This probably isn't the best implementation, but it works fine
     * for me...KISS, and all that :)
     *
     * If you'd like something more fancy, check out: http://monsur.com/projects/jscache/
     * You can supply a different cache class by either overriding the default, or
     * passing it as an option, in the call to "chainedSelect".
     *
     * Your custom cache class must implement the following methods:
     *
     *     getItem(key):        Get the item with the specified "key" from the cache.
     *
     *     setItem(key, value): Add "value" to the cache under the supplied "key".
     *
     *     clear():             Clear all items from the cache (not currently used).
     *
     * In addition, its constructor should take a single argument; it'll be passed a hash
     * of options used to initialize the plugin.
     */
    var cache = {}, keys = [];
    $.fn.chainedSelect.Cache = function(opts) {
        return {
            getItem: function(key) {
                key = this.replace(key);
                if (key in cache) return cache[key];
                else return null;
            },
            setItem: function(key, value) {
                if (value) {
                    key = this.replace(key);
                    cache[key] = value;
                    var length = keys.push(key);
                    if (length > opts.cacheLength) {
                        delete cache[keys.shift()];
                    }
                }
            },
            replace: function(key){
                // This way region view ajax calls are cached
                return key.replace(/id_regionview_set-\d-/, "");
            },
            clear: function() {
                cache = {};
                keys = [];
            }
        }
    };

    /* Plugin defaults */
    $.fn.chainedSelect.defaults = {
        value: 'pk',                            // The name of the field containing the option's value
        label: 'name',                          // The name of the field containing text for the option's label
        preloadUrl: '',                         // The URL to a GIF image to be used as a preloader
        cacheClass: $.fn.chainedSelect.Cache,   // The cache used to store the results of AJAX calls
        cacheLength: 10,                        // The maximum number of entries that should be cached
        error: null                             // Function called if an AJAX call returns an error
    }
})(jQuery);
