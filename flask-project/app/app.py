from flask import Flask
from Controller.evController import EVController
from View.views import EVView

app = Flask(__name__)

# EV 관련 컨트롤러 초기화
ev_controller = EVController()

@app.route('/api/get_EVinfo/all')
def get_EVInfo_All():
    return ev_controller.get_ev_info_all()

@app.route('/api/get_EVinfo/CType')
def get_EVInfo_ChargerType():
    return ev_controller.get_ev_info_charger_type()

@app.route('/api/get_EVinfo/location')
def get_EVInfo_Location():
    return ev_controller.get_location_and_draw_map()


@app.route('/EVcharge/barChart')
def EVcharge_barChart():
    return EVView.render_EVCharger_bar_chart()

@app.route('/EVcharge/lists')
def EVcharge_table():
    return EVView.render_EVCharger_table()

@app.route('/EVcharge/map')
def EVcharge_map():
    return EVView.render_EVCharger_map()

@app.route('/404')
def error_404():
    return EVView.render_error_404()

@app.route('/')
def home():
    return EVView.render_home()

@app.route('/index')
def index():
    return EVView.render_home()

if __name__ == '__main__':
    app.run(debug=True)