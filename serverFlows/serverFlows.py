from flask import Flask
from endpoints.save_request import save_request
from endpoints.delete_request import delete_request
from endpoints.return_request import return_request
from waitress import serve

app = Flask(__name__)

# Registrar los endpoints importados
app.add_url_rule('/save-request', view_func=save_request, methods=['POST'])
app.add_url_rule('/delete-request', view_func=delete_request, methods=['POST'])
app.add_url_rule('/return-request', view_func=return_request, methods=['POST'])

if __name__ == '__main__':
    serve(app, host='10.5.15.76', port=8080)