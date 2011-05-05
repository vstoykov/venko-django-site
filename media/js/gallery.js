var galleries_obj;
var gallery_json = '/static/js/gallery.json'

function galleryShow(gallery) {
  gallery = galleries_obj[gallery]
  pictures = gallery.pictures;
  $('#gallery_list').html('');
  for (item in pictures) {
    picture = pictures[item];
    $('#gallery_list').append('<li><div class="thumb-holder"><a href="'+picture.src+'"><img src="'+picture.thumb.src+'" width="'+picture.thumb.width+'" height="'+picture.thumb.height+'" alt="" class="shadow" /></a></div><!--p>'+picture.title+'</p--></li>');
    //$('#gallery_list').append('<li><a href="'+picture.src+'">'+picture.thumb.outerHTML+'</a><p>'+picture.title+'</p></li>');
  }
  $('#gallery_list a').lightBox();
  $('#galleries_list').hide()
  $('#gallery_list').fadeIn('slow', function(){$('.backToGalleries').css('visibility', 'visible');});
}

function listGalleries(galleries) {
  if (galleries == undefined) galleries = galleries_obj;
  $('.backToGalleries').css('visibility', 'hidden');
  $('#galleries_list').html('');
  for (gallery in galleries) {
    gallery_obj = galleries[gallery];
    $('#galleries_list').append('<li><a href="javascript:void(0)" id="gallery_'+gallery+'" name="'+gallery+'"><img src="/static/img/gallery-folder.png" class="shadow" /><p>'+gallery_obj.title+'</p></a></li>');
    $('#gallery_'+gallery).click(function(){
      gallery = $(this).attr('name');
      galleryShow(gallery);
    });
  }
  $('#gallery_list').hide()
  $('#galleries_list').fadeIn('slow');
}

function loadGalleryData() {
  $.getJSON(gallery_json, function(data) {
    //console.log(data);
    for(var gallery in data) {
        gallery_obj = data[gallery];
        pictures = gallery_obj.pictures
        gallery_obj.pictures_obj = {}
        for(var item in pictures) {
            picture = pictures[item];
            g_location = '/static/gallery/'+gallery+'/';
            pic_location = g_location + picture;
            thumb_pic = new Image();
            thumb_pic.src = g_location + 'thumbs/' + picture;;
            gallery_obj.pictures_obj[item] = {'src':pic_location, 'thumb':thumb_pic, 'title': picture.replace(/_/g, ' ')}
        };
        gallery_obj.pictures = gallery_obj.pictures_obj
        delete gallery_obj.pictures_obj
    }

    galleries_obj = data;

    listGalleries(data)
  });
}

$(document).ready(function(){
  if (galleries_obj == undefined) loadGalleryData();
});
