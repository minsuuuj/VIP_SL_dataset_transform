import os
import json
import re

meta_value = {"url" : "-",\
            "name" : " ",\
            "duration" : " ",\
            "exportedOn" : " "}

def trans_timestamp(time_text):
    time_list = time_text.split(':')
    return float(time_list[-1])

def preprocessing_ass(text):
    # Dialogue에서 Start, End, Text 추출
    dialogue_pattern = r"Dialogue: (\d+),(\d+:\d+:\d+\.\d+),(\d+:\d+:\d+\.\d+),(.+),,(.+)"
    matches = re.findall(dialogue_pattern, text)
    dialogue_info = []
    for match in matches:
        start_time = trans_timestamp(match[1])
        end_time = trans_timestamp(match[2])
        text = match[-1]
        dialogue_info.append({"start": start_time, "end": end_time, "attributes": [{"name" : text}]})
    return dialogue_info


data_directory = './data/'

for file_name in os.listdir(data_directory):
    with open(data_directory + file_name, "r", encoding="utf-8") as file:
        ass_content = file.read()
        data_value = preprocessing_ass(ass_content)

    json_data = {"metaData" : meta_value, "data" : data_value}

    json_file_path = "./json_data/" + file_name.split('.')[0] +'.json'
    with open(json_file_path, 'w', encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)