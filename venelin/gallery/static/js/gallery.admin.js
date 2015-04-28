/*global window, document, location, django*/

(function ($) {
    "use strict";
    $.fn.fileUploadDropZone = function DropZone(options) {
        var $this = this,
            dropZoneTimeOut = null;

        options = $.extend({
            dropEffect: 'copy',
            dropZoneClass: 'drop-zone',
            dragoverClass: 'in',
            overlyClass: 'drop-zone-overly',
            delay: 200
        }, options);

        $this.addClass(options.dropZoneClass).append(
            $('<div>', {'class': options.overlyClass})
        );

        $([document, window]).bind('dragover', function (e) {
            e.preventDefault();
            var dataTransfer = e.originalEvent.dataTransfer,
                types = dataTransfer.types;

            if (dropZoneTimeOut) {
                clearTimeout(dropZoneTimeOut);
            }
            if (types && types.contains('Files')) {
                e.stopPropagation();
                $this.addClass(options.dragoverClass);
                dataTransfer.dropEffect = options.dropEffect;
            }

        }).bind('drop', function (e) {
            e.preventDefault();
            if (dropZoneTimeOut) {
                clearTimeout(dropZoneTimeOut);
            }
            $this.removeClass(options.dragoverClass);

        }).bind('dragleave', function (e) {
            if (dropZoneTimeOut) {
                clearTimeout(dropZoneTimeOut);
            }
            dropZoneTimeOut = setTimeout(function () {
                dropZoneTimeOut = null;
                $this.removeClass(options.dragoverClass);
            }, options.delay);
        });

        return $this;
    };

    $(document).on('ready', function () {
        var $form = $('#gallery_form'),
            $fieldset = $form.find('fieldset.module:first'),
            $picturesGroup = $('#pictures-group'),
            $field = $('<input>', {type: 'file', multiple: 'multiple', 'class': 'fileupload'}),
            $loading = $('<span>', {'class': 'loading hidden'}),
            $row = $('<div>', {'class': 'form-row'}).append(
                $('<div>').append([
                    $('<label>').get(0),
                    $field.get(0),
                    $loading.get(0)
                ])
            ),
            progress = 0;

        $fieldset.append($row);

        $field.fileupload({
            dataType: 'json',
            url: 'upload/',
            paramName: 'image',
            dropZone: $fieldset.fileUploadDropZone(),
            done: function (e, data) {
                if (progress === 100) {
                    setTimeout(function () {
                        location.reload();
                    }, 100);
                }
            },
            progressall: function (e, data) {
                progress = parseInt(data.loaded / data.total * 100, 10);
                $loading.removeClass('hidden');
            }
        });

        // Replace link for adding new images with new one that will open file dialog
        setTimeout(function () {
            var $addRow = $picturesGroup.find('.add-row a');
            $addRow.replaceWith(
                $('<a>', {href: 'javascript:;'}).text($addRow.text()).on('click', function (e) {
                    e.stopPropagation();
                    e.preventDefault();
                    $field.trigger('click');
                })
            );
        });
    });
}(django.jQuery));
