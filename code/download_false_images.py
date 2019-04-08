import pandas as pd
import os

holding_dir = "/imgs_false"
dir_path = os.path.dirname(os.path.abspath(__file__))
export_dir = dir_path + holding_dir

if not os.path.exists(holding_dir): 
	os.makedirs(holding_dir)

false_image_df = pd.read_csv("vision_labels_false.csv")
false_image_locations = false_image_df["gcs_uri"]

file_count = 0
for index, image in false_image_locations.iteritems():
	if file_count > 10000:
		break
	#Hacky way to just get folder and image name from full gs location string
	image_id = image[-18:].strip('frames/').replace("/","_")
	export_file = export_dir + "/{}".format(image_id)
	print(export_file)
	gsutil_command = "gsutil cp {} {}".format(image,export_file)

	os.system(gsutil_command)
	file_count +=1


