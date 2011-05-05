from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse

from gallery.models import Gallery

def view_galleries(request, gallery=None):
    if gallery:
        gallery = get_object_or_404(Gallery, slug=gallery)
    else:
        galleries = Gallery.objects.exclude(pictures=None)
    

    
    if request.is_ajax():
        import json
        if gallery:
            json_obj = gallery.pictures.all()
        else:
            json_obj = galleries
        # Prepare object for JSON
        json_list = []
        for obj in json_obj:
            json_dict = {}
            for item, value in obj.__dict__.items():
                # Exclude special attributes (begins with '_')
                if item[0] != '_':
                    json_dict[item] = unicode(value)
            json_list.append(json_dict)
        return HttpResponse(json.dumps(json_list), content_type='text/json')
    
    return render_to_response('gallery.html', locals(), RequestContext(request))