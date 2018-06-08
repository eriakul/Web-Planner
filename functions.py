from pickle import dump, load
from random import randint

def load_cache(file):
    cache = load( open( file, "rb" ) )
    return cache

def pickle_cache(variable, file_name):
    dump(variable, open(file_name, 'wb'))

def add_panel_dictionary_to_cache(panel_dictionary, file_name):
    list_of_dicts = load_cache(file_name)
    list_of_dicts.append(panel_dictionary)
    pickle_cache(list_of_dicts, file_name)

def convert_date(string):
    months_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'October','September',
                   'November', 'December']
    list_form = string.split('-')
    month_index = int(list_form[1])-1
    month = months_list[month_index]
    converted_date = month+" "+list_form[2]+", "+ list_form[0]
    return converted_date

def process_create_event_dictionary(dictionary, list_of_dicts):
    new_dictionary = {}
    list_of_current_ids = [int(i['post_id']) for i in list_of_dicts]
    rand_id = randint(0,7000)
    while rand_id in list_of_current_ids:
         rand_id = randint(0,7000)
    new_dictionary['post_id'] = str(rand_id)
    new_dictionary['join_modal_id'] = new_dictionary['post_id'] + "_join_modal"
    new_dictionary['attending_modal_id'] = new_dictionary['post_id'] + "_attending_modal"
    new_dictionary['title'] = dictionary['title'].upper()
    new_dictionary['description'] = dictionary['description']
    new_dictionary['time'] = dictionary['time']
    new_dictionary['unprocessed_date'] = dictionary['date']
    new_dictionary['date'] = convert_date(dictionary['date'])
    keys = list(dictionary.keys())
    checkboxes = ['transportation','comments', 'groupme']
    for i in checkboxes:
        if i in keys:
            new_dictionary[i] = True
        else:
            new_dictionary[i] = False

    new_dictionary['attending'] = []

    return new_dictionary



def create_join_form(panel_dictionary):
    joinmodal_string = """
    <div id="%s" class="modal">
      <span onclick="document.getElementById('%s').style.display='none'" class="close" title="Cancel">&times;</span>
      <form class="modal-content" action ="/" method=POST>
        <div class="container">
          <h1>Join Event</h1>
          <hr>
          <label for="Name"><b>Name</b></label>
          <input type="text" placeholder="Enter Name" name="name" required>"""
    joinmodal_string = joinmodal_string % (panel_dictionary['join_modal_id'], panel_dictionary['join_modal_id'])
    if panel_dictionary['transportation'] == True:
        joinmodal_string = joinmodal_string + """

          <label for="Name"><b><i class="fa fa-car" aria-hidden="true"></i> </b></label>
          <select name="car">
            <option value="True">I have a car.</option>
            <option value="False">I don't have a car.</option>
          </select>
          <label for="extra_seats"><b> Seats Open</b></label>
          <select name="extra_seats">
            <option value="0">0</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
            <option value="6">6</option>
            <option value="7">7</option>
          </select>
          <br><br>"""
    if panel_dictionary['comments'] == True:
        joinmodal_string = joinmodal_string + """
          <label for="comment"><b>Comment</b></label>
          <input type="text" placeholder="Optional. Max 50 characters" name="comment" maxlength="50">
          <hr>"""
    if panel_dictionary['transportation'] == True:
        joinmodal_string = joinmodal_string + """
          <label>
            <input type="checkbox" name="need_ride" style="margin-bottom:15px"> I need a ride.
            <hr>"""
    joinmodal_string = joinmodal_string + """
      <input type="hidden" name="post_id" value="%s">
      <input type="hidden" name="post_type" value="join">
          <div class="clearfix">
            <button type="button" onclick="document.getElementById('%s').style.display='none'" class="cancelbtn">Cancel</button>
            <button type="submit" class="signupbtn">Join</button>
          </div>
        </div>
      </form>
    </div>
    """
    joinmodal_string = joinmodal_string % (panel_dictionary['post_id'], panel_dictionary['join_modal_id'])
    return joinmodal_string

def find_panel_dictionary_for_join(dictionary, list_of_dicts):
    for i in range(len(list_of_dicts)):
        if list_of_dicts[i]['post_id'] == dictionary['post_id']:
            return i



def process_join_dictionary(dictionary, panel_dictionary):
    list_of_attending_dicts = panel_dictionary['attending']
    list_of_current_ids = [int(i['person_id']) for i in list_of_attending_dicts]
    rand_id = randint(0,7000)
    new_dictionary = {}
    while rand_id in list_of_current_ids:
        rand_id = randint(0,7000)
    new_dictionary['person_id'] = str(rand_id)
    new_dictionary['post_id'] = panel_dictionary['post_id']
    new_dictionary['name'] = dictionary['name']
    if panel_dictionary['comments'] == True:
        new_dictionary['comment'] = dictionary['comment']
    if panel_dictionary['transportation'] == True:
        new_dictionary['extra_seats'] = int(dictionary['extra_seats'])
        if dictionary['car'] == 'True':
            new_dictionary['car'] = True
        elif dictionary['car'] == 'False':
            new_dictionary['car'] = False
            new_dictionary['extra_seats'] = 0
        keys = list(dictionary.keys())
        if 'need_ride' in keys:
            new_dictionary['need_ride'] = True
        else:
            new_dictionary['need_ride'] = False
    return new_dictionary

def add_person_dictionary_to_attending(person_dictionary, list_index, list_of_dicts):
    list_of_dicts[list_index]['attending'].append(person_dictionary)
    return list_of_dicts

def create_attending_modal(panel_dictionary):
    attending_list = panel_dictionary['attending']
    if panel_dictionary['comments'] == True and panel_dictionary['transportation'] == False:
        header = """
            <table>
              <tr>
                <th>Name</th>
                <th>Comment</th>
              </tr>
            """

        body = ""
        for person in attending_list:
            temp_body = """
            <tr>
                <td>{}</td>
                <td>{}</td>
            <tr>
            """.format(person['name'], person['comment'])
            body = body+temp_body
        end = "</table>"
        table = header+body+end

    if panel_dictionary['transportation']==True and panel_dictionary['comments'] == False:
        header = """
            <table>
              <tr>
                <th><div class="tooltip">NR
                <span class="tooltiptext">Need Ride</span></div></th>
                <th>Name</th>
                <th>Car</th>
                <th>Extra Seats</th>
              </tr>
            """

        body = ""
        for person in attending_list:
            temp_body = """
            <tr>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
            </tr>
            """
            if person['need_ride'] == True and person['car'] == False:
                temp_body = temp_body.format('<i class="fa fa-exclamation-circle" id = id_red >', person['name'], '', str(person['extra_seats']))
            if person['need_ride'] == False and person['car'] == True:
                temp_body = temp_body.format('', person['name'], '<i class="fa fa-car" aria-hidden="true"></i>', str(person['extra_seats']))
            if person['need_ride'] == True and person['car'] == True:
                temp_body = temp_body.format('<i class="fa fa-exclamation-circle" id = id_red >', person['name'], '<i class="fa fa-car" aria-hidden="true"></i>', str(person['extra_seats']))
            if person['need_ride'] == False and person['car'] == False:
                temp_body = temp_body.format('', person['name'], '', str(person['extra_seats']))
            body = body+temp_body
        end = "</table>"
        table = header+body+end


    if panel_dictionary['transportation']==True and panel_dictionary['comments'] == True:
        header = """
            <table>
              <tr>
                <th><div class="tooltip">NR
                    <span class="tooltiptext">Need Ride</span></div></th>
                <th>Name</th>
                <th>Car</th>
                <th>Extra Seats</th>
                <th>Comment</th>
              </tr>
            """
        body = ""
        for person in attending_list:
            temp_body = """
            <tr>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
            </tr>
            """
            if person['need_ride'] == True and person['car'] == False:
                temp_body = temp_body.format('<i class="fa fa-exclamation-circle" id = id_red >', person['name'], '', str(person['extra_seats']), person['comment'])
            if person['need_ride'] == False and person['car'] == True:
                temp_body = temp_body.format('', person['name'], '<i class="fa fa-car" aria-hidden="true"></i>', str(person['extra_seats']), person['comment'])
            if person['need_ride'] == True and person['car'] == True:
                temp_body = temp_body.format('<i class="fa fa-exclamation-circle" id = id_red >', person['name'], '<i class="fa fa-car" aria-hidden="true"></i>', str(person['extra_seats']), person['comment'])
            if person['need_ride'] == False and person['car'] == False:
                temp_body = temp_body.format('', person['name'], '', str(person['extra_seats']), person['comment'])
            body = body+temp_body
        end = "</table>"
        table = header+body+end

    if panel_dictionary['transportation']==False and panel_dictionary['comments'] == False:
        header = """
            <table>
              <tr>
                <th>Name</th>
              </tr>
            """

        body = ""
        for person in attending_list:
            temp_body = """
            <tr>
                <td>{}</td>
            </tr>
            """
            temp_body = temp_body.format(person['name'])
            body = body+temp_body
        end = "</table>"
        table = header+body+end

    attending_modal_script ="""   <div id="{}" class="modal">
      <span onclick="document.getElementById('{}').style.display='none'" class="close" title="Cancel">&times;</span>
      <form class="modal-content" action="{{ url_for('home') }}" method=POST>
        <div class="container">
          <h1>Attending</h1>
          <hr>""".format(panel_dictionary['attending_modal_id'], panel_dictionary['attending_modal_id']) +table+ """<hr>
                <div class="clearfix">
                  <button type="button" onclick="document.getElementById('{}').style.display='none'" class="cancelbtn">Cancel</button>
                </div>
              </div>
            </form>
          </div>""".format(panel_dictionary['attending_modal_id'])
    # attending_modal_script = attending_modal_script % (panel_dictionary['attending_modal_id'], panel_dictionary['attending_modal_id'])
    return attending_modal_script

def calculate_seats(attending_list):
    list_of_need = [1 for i in attending_list if i['need_ride']]
    number_of_need = len(list_of_need)
    list_of_seats = [int(i['extra_seats']) for i in attending_list]
    number_of_seats = sum(list_of_seats)
    seats_open = number_of_seats - number_of_need
    return seats_open


def create_panel(panel_dictionary):
    header = """
    <div class="w3-card-4 w3-margin w3-white">
    <div class="w3-container">
      <br>
      <h3><b>%s</b></h3>
      <h5>%s, <span class="w3-opacity">%s</span></h5>
    </div>
    <div class="w3-container">
      <p>%s</p>
      <br>
      <div class="w3-row">
        <div class="w3-col m8 s12">
          <button class="w3-button w3-padding-large w3-white w3-border attendingbtn" onclick= "document.getElementById('%s').style.display='block'" ><b>View Attending</b></button>
          <button class="w3-button w3-padding-large w3-white w3-border joinbtn" onclick= "document.getElementById('%s').style.display='block'"><h3><b>JOIN »</b></h3></button>
        </div>
    """
    header = header % (panel_dictionary['title'], panel_dictionary['time'], panel_dictionary['date'], panel_dictionary['description'],
    panel_dictionary['attending_modal_id'], panel_dictionary['join_modal_id'])

    if panel_dictionary['transportation'] == True:
        seats_open = calculate_seats(panel_dictionary['attending'])

        if seats_open > 0:
            text = """<p><h4>%s car seats open</h4></p>"""
            text = text % (str(seats_open))
            header = header + text
        elif seats_open < 0:
            text = """<p><h6>%s people need rides</h6></p>"""
            text = text % (str(abs(seats_open)))
            header = header + text
        else:
            header = header + "<p><h4><hr></h4></p>"
    else:
        header = header + "<p><h4><hr></h4></p>"


    end = """

              </div>
            </div>
          </div>"""
    panels_script = header+end
    return panels_script

def sort_list_of_dicts_by_time(list_of_dicts):
    new_list = sorted(list_of_dicts, key=lambda dictionary : dictionary['unprocessed_date'])
    return new_list
