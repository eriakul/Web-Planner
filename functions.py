from pickle import dump, load

def load_cache(file):
    cache = load( open( file, "rb" ) )
    return cache

def pickle_cache(variable, file_name):
    dump(variable, open(file_name, 'wb'))

def add_panel_dictionary_to_cache(dictionary, file_name):
    list_of_dicts = load_cache(file_name)
    list_of_dicts.append(dictionary)
    pickle_cache(list_of_dicts, file_name)

def convert_date(string):
    months_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'October','September',
                   'November', 'December']
    list_form = string.split('-')
    month_index = int(list_form[1])-1
    month = months_list[month_index]
    converted_date = month+" "+list_form[2]+", "+ list_form[0]
    return converted_date

def process_dictionary(dictionary):
    new_dictionary = {}
    new_dictionary['title'] = dictionary['title'].upper()
    new_dictionary['time'] = dictionary['time']
    new_dictionary['date'] = converted_date(dictionary['date'])
    keys = list(dictionary.keys())
    checkboxes = ['transportation','comments', 'groupme']
    for i in checkboxes:
        if i in keys:
            new_dictionary[i] = True
        else:
            new_dictionary[i] = False

    new_dictionary['attending'] = {}

    return new_dictionary



def create_join_form(transportation, comment):

def create_panel(title, time, date, description, transportation):
