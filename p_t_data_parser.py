import csv
import json

qa_pairs = {
    "HUMOR": "ISTHECARDACARTOON",
    "ANIMALS": "WHATKINDOFANIMAL",
    "HOLIDAYS": "WHICHHOLIDAY",
    "NATURE": "WHATKINDOFNATURESCENE",
    "RELIGION": "WHATKINDOFRELIGIOUSSCENE",
    "PEOPLE": "WHATCANYOUIDENTIFYABOUTTHESEPEOPLE",
    "POLITICSANDGOVERNMENT": "WHATKINDOFPOLITICALIMAGE",
    "SPORTS": "WHICHSPORT",
    "TRANSPORTATION": "WHATKINDOFTRANSPORTATION",
    "BUILDINGS": "WHATKINDOFBUILDING",
    "STREETVIEWS": "WHATKINDOFSTREETVIEW",
}

def save_dict_to_json(data_dict, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)

def find_task_values(csv_file_path):
    # We will parse each row and push the results into this list
    output = [] 
    justJson = []
    with open(csv_file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            try:
                # Parse the 12th column as JSON
                data_dict = json.loads(row[11]) # Assuming 0-based indexing, so 11 is the 12th column
                if isinstance(data_dict, list):
                    justJson.append(data_dict)
                    # this is the row's output, which will be pushed into the final list
                    outpObj = {}
                    for i in data_dict:
                        if i['task'] == 'T0':
                            for j in i["value"]:
                                if j['task'] == 'T1':
                                    outpObj["T1"] = j["value"]
                                elif j['task'] == 'T2':
                                    outpObj["T2"] = []
                                    for lang in j["value"]:
                                        outpObj["T2"].append(lang["label"])
                                elif j['task'] == 'T3' and len(j["value"]) > 0:
                                    outpObj["T3"] = j["value"]
                        if i['task'] == 'T5':
                            for j in i["value"]:
                                if j['task'] == 'T6':
                                    outpObj[ "T6" ] = []
                                    for q in j["value"]:
                                        outpObj[ "T6" ].append(q["choice"])
                                        try: 
                                            question = qa_pairs[q["choice"]]
                                            if len(q["answers"][question]) > 0:
                                                for a in q["answers"][question]:
                                                    print(a)
                                                    outpObj[ "T6" ].append(a)
                                        # if this choice doesnt have a question / isn't in our QA dict, move on
                                        except KeyError: 
                                            pass
                        if i['task'] == 'T8':
                            for j in i["value"]:
                                if j['task'] == 'T9' and len( j["value"] ) > 0:
                                    outpObj["T9"] = j["value"]
                                elif j['task'] == 'T11' and len( j["value"] ) > 0:
                                    outpObj["T11"] = j["value"]
                                elif j['task'] == 'T20' and len( j["value"] ) > 0:
                                    outpObj["T20"] = j["value"]
                    output.append(outpObj)
            except json.JSONDecodeError:
                print('json parse FAIL')
                # Move on if JSON parsing fails
                pass
    
    return output, justJson

csv_file_path = 'data.csv'  # Replace with your CSV file path
outputList, justJson = find_task_values(csv_file_path)
# print(outputList)

json_file_path = 'result.json'  # Replace with the desired output JSON file path
save_dict_to_json(outputList, json_file_path)

jjson_file_path = 'json.json'  # Replace with the desired output JSON file path
save_dict_to_json(justJson, jjson_file_path)

print(f"Dictionary has been saved as {json_file_path}.")


