def linked_123(list_of_word ,label,training_data):
    list_word = []
    
    for i in training_data['form']:
        list_word.append(i['text'])
    if len(list_of_word)==2:
        word1 = list_of_word[0]
        word2 = list_of_word[1]
        if word1 and word2 in list_word:
            
            index_of_word1 = list_word.index(word1)
            # print(index_of_word1)
            # print(training_data['form'][index_of_word1])
            # print(i)
            id_of_word1 = training_data['form'][index_of_word1]["id"]
            print(id_of_word1)
        # if word2 in list_word:
            index_of_word2 = list_word.index(word2)
            
            id_of_word2 = training_data['form'][index_of_word2]["id"]
            print(id_of_word2)
            print(type(training_data['form'][id_of_word1]["linking"]))
            training_data['form'][id_of_word1-1]["linking"].append([id_of_word1,id_of_word2])
            training_data['form'][id_of_word1-1]["label"] = label
            training_data['form'][id_of_word2-1]["linking"].append([id_of_word1,id_of_word2])
            training_data['form'][id_of_word2-1]["label"] = label
        else:
            print("word not found")
    if len(list_of_word)<2:
        word1 = list_of_word[0]
        
        if word1 in list_word:
            index_of_word1 = list_word.index(word1)
            id_of_word1 = training_data['form'][index_of_word1]["id"]
            print(id_of_word1)
            training_data['form'][id_of_word1-1]["label"] = label
        else:
            print("word not found")
    return training_data

# training = linked_123("Batch No.","BT95BM105C","Batch",training)
# print(training)