import json
import glob
import os
import tqdm

files_to_flip = glob.glob("../DATA/Mediapipe_Data_July_2020/10-02-20_p8-left_4K+Depth/*/*/*.data")

for fileName in tqdm.tqdm(files_to_flip):

	with open(fileName) as f:
	  data = json.load(f)

	flipped_json = {}

	for i in data:
		flipped_json[i] = {}
		flipped_json[i]["boxes"] = data[i]["boxes"]
		flipped_json[i]["faces"] = data[i]["faces"]
		flipped_json[i]["landmarks"] = data[i]["landmarks"]

		if flipped_json[i]["boxes"] is not None and len(flipped_json[i]["boxes"]) >= 2:
			flipped_json[i]["boxes"]["0"], flipped_json[i]["boxes"]["1"] = flipped_json[i]["boxes"]["1"], flipped_json[i]["boxes"]["0"]

		if flipped_json[i]["landmarks"] is not None and len(flipped_json[i]["landmarks"]) >= 2:
			flipped_json[i]["landmarks"]["0"], flipped_json[i]["landmarks"]["1"] = flipped_json[i]["landmarks"]["1"], flipped_json[i]["landmarks"]["0"]

	flipped_fileName = fileName.replace("p8-left", "p8-left-flipped")
	os.makedirs("/".join(flipped_fileName.split("/")[:-1]), exist_ok=True)
	with open(flipped_fileName, 'w') as json_file:
  		json.dump(flipped_json, json_file, indent=4)







