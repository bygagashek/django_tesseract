from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings
import django.urls
from wsgiref.util import FileWrapper
import os
import mimetypes
from django.http import StreamingHttpResponse
from myapp.models import Document
from myapp.forms import DocumentForm
from django.urls import reverse
from PIL import Image
import pytesseract
import os


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('text'))
    else:
        form = DocumentForm() # A empty, unbound form
    # Render list page with the form
    return render(request, 'list.html', {'form': form})

def rasp(request):
    path_images = os.path.join(settings.BASE_DIR, 'media/documents')
    path_to_save = os.path.join(settings.BASE_DIR, 'media/text/')
    arr = os.listdir(path_images)
    documents = Document.objects.filter().order_by('-id')[:1]
    for documents in arr:
        f = open(path_to_save + 'text.txt','w')
        text = pytesseract.image_to_string(Image.open(path_images + "/" + documents),
                                           lang='rus')
        f.write(text)
        f.close()
    Document.objects.filter().order_by('-id')[:1].delete
    path_to_remove = path_images + "/" + documents
    os.remove(path_to_remove)

    return HttpResponseRedirect(reverse('download'))

def download(request):
    path_to_save = os.path.join(settings.BASE_DIR, 'media/text/')
    f = open(path_to_save + "text.txt")
    fd = f.readlines()
    return render(request, 'text.html', {'value': fd})

def download_file(request):
    path_to_save = os.path.join(settings.BASE_DIR, 'media/text/')
    the_file = path_to_save + '/text.txt'
    filename = os.path.basename(the_file)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunk_size),
                                     content_type=mimetypes.guess_type(the_file)[0])
    response['Content-Length'] = os.path.getsize(the_file)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
