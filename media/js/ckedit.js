window.onload = function() {
    CKEDITOR.config.toolbar_Custom =
    [
    	['Source','Maximize'],
    	['Cut','Copy','Paste','PasteText','PasteFromWord'],
    	['Undo','Redo','-','-','SelectAll','RemoveFormat'],
    	['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
    	['NumberedList','BulletedList','-','Outdent','Indent','Blockquote','CreateDiv'],
    	['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
    	['Link','Unlink','Anchor'],
    	['Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak'],
    	['Format'],
    ];
    
    CKEDITOR.replace('id_content',{
      skin: "v2",
      toolbar: 'Custom',
      height: '400px',
      width: '818px',
    });    
}
