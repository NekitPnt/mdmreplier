from flask import Flask, request
import json
import main
import traceback

app = Flask(__name__)


@app.route('/', methods=['POST'])
def processing():
    try:
        data = json.loads(request.data)
        if 'type' not in data.keys():
            return 'not vk'
        else:
            return main.response_handler_for_vk(data)
    except json.decoder.JSONDecodeError:
        return 'ok'


@app.errorhandler(500)
def error_handler(e):
    # уведомляете админа об ошибке
    main.error_notificator(traceback.format_exc())
    # возвращаете ВК ok
    return 'ok'
