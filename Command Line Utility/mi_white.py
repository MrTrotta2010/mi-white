import util
import crop
import i_o
import cv2

if __name__ == "__main__":
	image_path, output_path = i_o.validate_args()
	original_image = cv2.imread(image_path)
	
	resized_image = util.fit_to_screen_size(original_image, 600)
	result, cropped_image = crop.crop_image(original_image)
	
	if output_path:
		try:
			cv2.imwrite(output_path, cropped_image)
		except:
			print("main.py: error: couldn't save cropped image to path '" + output_path +"'")

	else:
		print("Showing cropped image. Press any key...")
		cv2.imshow("Cropped Image (press any key)", cropped_image)
		cv2.waitKey(0)
