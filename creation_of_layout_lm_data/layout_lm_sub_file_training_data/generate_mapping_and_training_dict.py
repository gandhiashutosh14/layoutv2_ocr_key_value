

def combine_elements_to_string(lst):
    return ''.join(map(str, lst))

def find_min_max_coordinates(coord_list):
    if len(coord_list) != 4:
        raise ValueError("Input should be a list of four coordinates [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]")

    x_values, y_values = zip(*coord_list)

    x_min = min(x_values)
    y_min = min(y_values)
    x_max = max(x_values)
    y_max = max(y_values)

    return [x_min, y_min, x_max, y_max]




def generate_dict_and_mapping_dict_from_main_list(main_list):
    # concatenate_numbers = lambda nums: int(''.join(map(str, nums)))

    training_data = {}
    training_data["form"] = []
    mapping_dict ={}
    count = 0
    for i in main_list:
        # print(i)
        # break
        cor = find_min_max_coordinates(i['Coordinate'])
        mapping_dict[str(combine_elements_to_string(cor))] = i['Coordinate']
        wor = i['word']
        dict_box = {}
        dict_box["box"] =cor 
        dict_box["text"] = wor
        dict_box["label"] = "other"
        json_dict = {}
        json_dict['box']= cor 
        json_dict["text"] = wor 
        dict_box['words'] = []
        dict_box['words'].append(json_dict)
        dict_box['linking'] = []
        dict_box['id'] = count
        training_data["form"].append(dict_box)
        count +=1
    return mapping_dict,training_data

