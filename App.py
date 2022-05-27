from flask import Flask,jsonify,request,make_response,url_for,redirect


app = Flask(__name__)

@app.route("/")
def inicio():
    return "Hola flask"

hola = "hola"

@app.route("/inicio", methods=['POST'])
def json_example():
    # request_data = get_objects("language")

    # language = request_data['language']
    # framework = request_data['framework']

    # # two keys are needed because of the nested object
    # python_version = request_data['version_info']['python']

    # # an index is needed because of the array
    # example = request_data['examples'][0]
    # get("prueba")
    # boolean_test = request_data['boolean_test']

    return request.json
    # return render_template("index.html", hola = hola)