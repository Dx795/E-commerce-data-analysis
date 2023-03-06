import numpy as np
from flask import Flask,render_template,request,Response,redirect,url_for,Blueprint
from data_analysis.data_visualization_provide import *
from data_model.model import get_model

# 创建一个蓝图的对象，蓝图就是一个小模块的抽象的概念
app_statistical = Blueprint("app_statistical", __name__)

@app_statistical.route('/dataPreview')
def dataPreview():
    wj = 'static/data_table/order_cleaning_cleaning.csv'
    data=data_show(wj)[0:10]
    data_array = np.array(data)
    sj=data_array.tolist()
    print(sj)
    # print(type(bh))
    return  render_template('dataPreview.html',sj=sj,count=0)

@app_statistical.route('/dataPreview_up/<count>')
def dataPreview_up(count):
    wj = 'static/data_table/order_cleaning_cleaning.csv'
    count=int(count)
    count-=10
    data=data_show(wj)[count:count+10]
    data_array = np.array(data)
    sj=data_array.tolist()
    print(sj)
    # print(type(bh))
    return  render_template('dataPreview.html',sj=sj,count=count)

@app_statistical.route('/dataPreview_down/<count>')
def dataPreview_down(count):
    count=int(count)
    wj = 'static/data_table/order_cleaning_cleaning.csv'
    count+=10
    data=data_show(wj)[count:count+10]
    data_array = np.array(data)
    sj=data_array.tolist()
    print(sj)
    # print(type(bh))
    return  render_template('dataPreview.html',sj=sj,count=count)



@app_statistical.route('/datamodeling')
def datamodeling():
    wj = 'static/data_table/order_cleaning_cleaning.csv'
    data=get_model(wj)
    datalist={}
    var = ''
    for i in range(0, len(data['买家昵称'].tolist())):
        if (i == len(data['买家昵称'].tolist()) - 1):
            var += (data['买家昵称'].tolist())[i]
        else:
            var += (data['买家昵称'].tolist())[i] + ","
    datalist['买家昵称']=var
    datalist['Frequency']=data['Frequency'].tolist()
    datalist['Monetary']=data['Monetary'].tolist()
    datalist['Recency']=data['Recency'].tolist()

    print(datalist)
    return render_template('datamodeling.html',datalist=datalist)
