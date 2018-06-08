import os
import ast
from flask_uploads import UploadSet, configure_uploads, DATA
from flask import Flask, render_template, jsonify, request, url_for

from functions import *

app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def home():
    panels_script = ""
    join_modal_script = ""
    attending_modal_script = ""
    list_of_dicts = load_cache('planner_cache')
    if request.method == 'POST':
        request_form = request.form.to_dict()
        print("\nORIGINAL FORM: ", request_form, "\n")
        if request_form['post_type'] == 'create':
            panel_dictionary = process_create_event_dictionary(request_form, list_of_dicts)
            list_of_dicts.append(panel_dictionary)
            pickle_cache(list_of_dicts, 'planner_cache')
            print("\nPICKLED CACHE: ", list_of_dicts, "\n")
            list_of_dicts = load_cache('planner_cache')
            print("\nLOADED CACHE: ", list_of_dicts, "\n")
        if request_form['post_type'] == 'join':
            list_index = find_panel_dictionary_for_join(request_form, list_of_dicts)
            person_dictionary = process_join_dictionary(request_form, list_of_dicts[list_index])
            list_of_dicts = add_person_dictionary_to_attending(person_dictionary, list_index, list_of_dicts)
            pickle_cache(list_of_dicts, 'planner_cache')
            list_of_dicts = load_cache('planner_cache')
        if request_form['post_type'] == 'admin':
            string_list_of_dicts = request_form['message']
            list_of_dicts = ast.literal_eval(string_list_of_dicts)
            pickle_cache(list_of_dicts, 'planner_cache')
            list_of_dicts = load_cache('planner_cache')


    list_of_dicts = sort_list_of_dicts_by_time(list_of_dicts)
    for panel_dictionary in list_of_dicts:
        join_modal = create_join_form(panel_dictionary)
        join_modal_script = join_modal_script + join_modal

        attending_modal = create_attending_modal(panel_dictionary)

        attending_modal_script = attending_modal_script + attending_modal

        panel = create_panel(panel_dictionary)
        panels_script = panels_script + panel

    return render_template('Blog Template.html', join_modals = join_modal_script, panels = panels_script, attending_modals = attending_modal_script)

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        request_form = request.form.to_dict()
        if request_form['password'] == '5511':
            list_of_dicts = load_cache('planner_cache')
            return render_template('Admin.html', list_of_dicts = str(list_of_dicts))
if __name__ == "__main__":
    # the main function just runs the app
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host=HOST, port=PORT, debug = True)
