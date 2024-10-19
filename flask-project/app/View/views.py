from flask import render_template

class EVView:
    @staticmethod
    def render_EVCharger_bar_chart():
        return render_template('EVCharger_barChart.html')
    
    @staticmethod
    def render_EVCharger_table():
        return render_template('EVCharger_lists.html')
    
    @staticmethod
    def render_EVCharger_map():
        return render_template('EVCharger_map.html')
    
    @staticmethod
    def render_home():
        return render_template('index.html')
    
    staticmethod
    def render_error_404():
        return render_template('404.html')