from util import *
import numpy as np
import cv2
import sys
import os

TWITTER_ASPECT_RATIO = 1200 / 675
CASCADES_FOLDER = "Classifiers/"
MODELS_FOLDER = "Models/"

def crop_image(original_image):
	#print("Dimensões originais: (" + str(original_image.shape[1]) + ", " + str(original_image.shape[0]) + ")")

	# Calcula as possíveis áreas onde há objetos
	success, saliency_map = __objectness_saliency(original_image)
	if not success:
		print("crop.py: error: couldn't compute saliency")
		sys.exit(2)

	num_detections = saliency_map.shape[0]
	possible_crops = {"with_face": [], "without_face": []}
	black_and_white = False

	# Para cada área com um possível objeto
	for i in range(0, min(num_detections, 10)):
		# Área onde está o objeto
		start_x, start_y, end_x, end_y = saliency_map[i].flatten()
		# Seção da imagem contendo o objeto
		image_section = original_image[start_y:end_y, start_x:end_x].copy()
		# Desenha um retângulo ao redor da área da imagem que contém o objeto 
		output = original_image.copy()
		#cv2.rectangle(output, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
		# Detecta faces na seção da imagem
		graysacle_img_section = cv2.cvtColor(image_section, cv2.COLOR_BGR2GRAY)
		faces = __face_detection(graysacle_img_section)
		
		if len(faces) > 0: # Se encontrou algum rosto
			found_black_person = False
			found_white_person = False
			# Analisa cada face detectada
			for x, y, w, h in faces:
				possible_crops["with_face"].append((start_x, start_y, end_x, end_y))
				# Calcula o tom de cinza médio da seção em preto e branco que contém o rosto
				face_section = graysacle_img_section[y:(y + h), x:(x + w)]
				average = __get_dominant(face_section)
				# Se a média for menor que um determinado valor, considera pessoa preta
				if average < 170: found_black_person = True
				else: found_white_person = True
					# Desenha um retângulo ao redor da face
					#cv2.rectangle(image_section, (x, y), (x + w, y + h), (255, 0, 0), 2)
			
			if not found_black_person: # Encontrou somente rostos brancos 
				result = "Congrats, you're white enough for Twitter! :)"
				cropped_image = __crop_image(original_image, start_x, start_y, end_x, end_y)
				return result, cropped_image

			elif found_white_person:
				black_and_white = True
		
		else:
			possible_crops["without_face"].append((start_x, start_y, end_x, end_y))
		
	# Se o algoritmo chegou aqui, é porque não encontrou nenhum rosto,
	# ou encontrou somente rostos pretos ou encontrou rostos brancos e pretos

	# Se encontrou rostos pretos e brancos
	if len(possible_crops["with_face"]) > 0 and black_and_white:
		# Usa o maior objeto com rosto encontrado (objeto com a maior área)
		biggest_object = __sort_coord_list(possible_crops["with_face"])[0]
		result = "You're not white enough for Twitter, but your friends are..."
		crop_start_x, crop_start_y,	crop_end_x, crop_end_y = biggest_object
	
	# Não encontrou nenhum rosto
	if len(possible_crops["with_face"]) == 0:
		result = "It seems there's no one here..."
	else: # Econtrou somente rostos pretos
		result = "I'm sorry, but you're not white enough for Twitter :("
	
	# Usa o maior objeto sem rosto encontrado (objeto com a maior área)
	biggest_object = __sort_coord_list(possible_crops["without_face"])[0]
	crop_start_x, crop_start_y,	crop_end_x, crop_end_y = biggest_object

	cropped_image = __crop_image(original_image, crop_start_x, crop_start_y, crop_end_x, crop_end_y)
	return result, cropped_image

def __objectness_saliency(image):
	saliency = cv2.saliency.ObjectnessBING_create()
	saliency.setTrainingPath(MODELS_FOLDER)
	return saliency.computeSaliency(image)

def __face_detection(grayscale_image):
	face_cascade = cv2.CascadeClassifier(CASCADES_FOLDER + 'haarcascade_frontalface_alt.xml')
	return face_cascade.detectMultiScale(grayscale_image, 1.1, 4)

def __sort_coord_list(coord_list):
	return sorted(coord_list, key=lambda x: calc_area(x[0] + x[2], x[1] + x[3]), reverse=True)

def __crop_image(image, x, y, x_end, y_end):
	return image[y:y_end, x:x_end]
	# box_width = x_end - x
	# box_height = y_end - y
	# image_width = image.shape[1]
	# image_height = image.shape[0]

	# print("Origem: (" + str(x) + ", " + str(y) + ")")
	# print("Dimensões da caixa: (" + str(box_width) + ", " + str(box_height) + ")")

	# if box_height >= box_width:
	# 	new_y = y; new_y_end = y_end

	# 	center_point = int((x + x_end) / 2)
	# 	print(x, x_end, center_point)
	# 	input()
	# 	new_width = max(int(box_height * TWITTER_ASPECT_RATIO), image_width)
	# 	new_x = int(center_point - (new_width / 2))
	# 	new_x_end = int(center_point + (new_width / 2))
	# 	print(new_x, new_x_end)
	# 	input()

	# print("Razão:", (new_x_end - new_x) / (new_y_end - new_y))
	# return image[new_y:new_y_end, new_x:new_x_end]

def __get_average(face_section):
	return face_section.mean(axis=0).mean(axis=0)

def __get_dominant(face_section):
	pixels = np.float32(face_section.reshape(-1, 1))

	n_colors = 1
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
	flags = cv2.KMEANS_RANDOM_CENTERS

	_, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
	_, counts = np.unique(labels, return_counts=True)
	return palette[np.argmax(counts)][0]