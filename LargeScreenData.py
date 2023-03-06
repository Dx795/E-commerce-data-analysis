from flask import Flask,render_template,request,Response,redirect,url_for,Blueprint
from data_analysis.data_visualization_provide import *

# 创建一个蓝图的对象，蓝图就是一个小模块的抽象的概念
app_screendata = Blueprint("app_screendata", __name__)

# 国家单量分布页面
@app_screendata.route('/chart_countries_map')
def chart_countries_map():
    wj = 'static/data_table/order_cleaning_cleaning.csv'
    data=countries_sales(wj)
    return render_template('/chart/chart_countries_map.html',data=data[1])