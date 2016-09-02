/**
 * plugin.js
 *
 * Released under LGPL License.
 * Copyright (c) 1999-2015 Ephox Corp. All rights reserved
 *
 * License: http://www.tinymce.com/license
 * Contributing: http://www.tinymce.com/contributing
 */

/*global tinymce:true */

(function () {
    var ajaxUrl = '/custor/uploadimg';
    var loadingImage = '<img id="loadingImg" src="http://static.cnblogs.com/images/loading.gif" alt="" />';

    tinymce.create('tinymce.plugins.PasteUploadPlugin', {
        init: function (ed, url) {
            ed.on("Paste", (function (e) {
debugger;
                var image, pasteEvent, text;
                pasteEvent = e;
                if (pasteEvent.clipboardData && pasteEvent.clipboardData.items) {
                    image = isImage(pasteEvent);
                    if (image) {
                        e.preventDefault();
                        return uploadFile(image.getAsFile(), getFilename(pasteEvent));
                    }
                }
            }));
			ed.on('Drop', function (event) {
				var filename, image, pasteEvent, text;
				pasteEvent = event
				if (pasteEvent.dataTransfer && pasteEvent.dataTransfer.files) {
					image = isImageForDrop(pasteEvent);
					if (image) {
						filename = pasteEvent.dataTransfer.files[0].name || "image.png";
						event.preventDefault();
                        return uploadFile(image, filename);
					}
				}
			});
			isImageForDrop = function (data) {
				var i, item;
				i = 0;
				while (i < data.dataTransfer.files.length) {
					item = data.dataTransfer.files[i];
					if (item.type.indexOf("image") !== -1) {
						return item;
					}
					i++;
				}
				return false;
			};
            function isImage(data) {
                var i, item;
                i = 0;
                while (i < data.clipboardData.items.length) {
                    item = data.clipboardData.items[i];
                    if (item.type.indexOf("image") !== -1) {
                        return item;
                    }
                    i++;
                }
                return false;
            };
            function uploadFile(file, filename) {
                var formData = new FormData();
                formData.append('imageFile', file);
                formData.append("mimeType", file.type);

                $.ajax({
                    url: ajaxUrl,
                    data: formData,
                    type: 'post',
                    processData: false,
                    contentType: false,
                    dataType: 'json',
                    success: function (result) {
                        if (result.errorcode == 0) {
                            insertIntoTinymce(result.data.image);
                        } else {
                        }
                    },
                    error: function (xOptions, textStatus) {
                        console.log(xOptions.responseText);
                    }
                });
            };
            function insertIntoTinymce(url) {
                var content = ed.getContent();
                // content = content.replace(loadingImage, '<img src="' + url + '">');
                // ed.setContent(content);
				ed.insertContent('<img src="/static/images/' + url + '">');
                ed.selection.select(ed.getBody(), true);
                ed.selection.collapse(false);
				debugger;
            };
            function replaceLoading(filename) {
                var content = ed.getContent();
                content = content.replace(loadingImage, filename);
                ed.setContent(content);
                ed.selection.select(ed.getBody(), true);
                ed.selection.collapse(false);
            };
            function getFilename(e) {
                var value;
                if (window.clipboardData && window.clipboardData.getData) {
                    value = window.clipboardData.getData("Text");
                } else if (e.clipboardData && e.clipboardData.getData) {
                    value = e.clipboardData.getData("text/plain");
                }
                value = value.split("\r");
                return value[0];
            };
        },
    });

    // Register plugin
    tinymce.PluginManager.add("pasteUpload", tinymce.plugins.PasteUploadPlugin);
})();
