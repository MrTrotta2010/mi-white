from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

from miwhite.settings import MEDIA_ROOT, CROPPED_ROOT
from .modules.crop import crop_image

import cv2

# Create your views here.
def home(request):
	context = {}
	try:
		if request.method == 'POST':
			if request.FILES['picture']:
				picture = request.FILES['picture']
					
				fs = FileSystemStorage()
				filename = fs.save(picture.name, picture)

				in_path = MEDIA_ROOT + "/" + filename
				out_path = CROPPED_ROOT + "/" + filename
				print("<<<", in_path)
				print(">>>", out_path)

				#image = util.fit_to_screen_size(image, 600)
				result = crop_image(in_path, out_path)
				fs.delete(filename)

				context['img'] = filename
				context['msg'] = result
				return render(request, 'cropper/visualize.html', context)

		return render(request, 'cropper/upload.html', context)

	except MultiValueDictKeyError:
		return render(request, 'cropper/upload.html', context)

def crop(request):
	return HttpResponse('Chegou no crop hein!')