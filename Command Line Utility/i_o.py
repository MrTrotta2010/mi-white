from os import path
import argparse
import sys

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', required=True, type=str, help='Input image')
	parser.add_argument('-o', required=False, type=str, help='Output file name')
	return vars(parser.parse_args())

def validate_args():
	args = parse_args()
	image_path = args['f']
	output_path = args['o']
	
	try:
		original_image = open(image_path, "r")
	except:
		print("main.py: error: couldn't find input image '" + image_path + "'")
		sys.exit(1)
	
	return image_path, output_path
