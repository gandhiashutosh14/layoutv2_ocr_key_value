def index_reset(training_data):
    count = 1 
    for i in training_data['form']:
        i['id'] =count
        count +=1
    return training_data