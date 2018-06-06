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

def process_create_event_dictionary(dictionary):
    new_dictionary = {}
    new_dictionary['title'] = dictionary['title'].upper()
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

    new_dictionary['attending'] = {}

    return new_dictionary



def create_join_form(dictionary):
    joinmodal_string = """
    <div id="joinmodal" class="modal">
      <span onclick="document.getElementById('joinmodal').style.display='none'" class="close" title="Cancel">&times;</span>
      <form class="modal-content" action="{{ url_for('home') }}" method=POST>
        <div class="container">
          <h1>Join Event</h1>
          <hr>
          <label for="Name"><b>Name</b></label>
          <input type="text" placeholder="Enter Name" name="name" required>"""
    if dictionary['transportation'] == True:
        joinmodal_string = joinmodal_string + """

          <label for="Name"><b><i class="fa fa-car" aria-hidden="true"></i> </b></label>
          <select id = 'soflow' name="car">
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
    if dictionary['comments'] == True:
          <label for="comment"><b>Comment</b></label>
          <input type="text" placeholder="Max 50 characters" name="description" maxlength="50">

          <hr>
          <label>
            <input type="checkbox" name="need-ride" style="margin-bottom:15px"> I need a ride.

          <hr>
      <input type="hidden" name="post_title" value="This work????">
          <div class="clearfix">
            <button type="button" onclick="document.getElementById('joinmodal').style.display='none'" class="cancelbtn">Cancel</button>
            <button type="submit" class="signupbtn">Join</button>
          </div>
        </div>
      </form>
    </div>
    """

def create_panel(title, time, date, description, transportation):
