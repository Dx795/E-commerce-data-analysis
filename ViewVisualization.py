from flask import Flask,render_template,request,Response,redirect,url_for,Blueprint
import os, sys
from data_analysis.data_visualization_provide import *
from data_processing.dataCrawl import *
from data_processing.dataCleaning import *

# 创建一个蓝图的对象，蓝图就是一个小模块的抽象的概念
app_Visualization = Blueprint("app_Visualization", __name__)


# 可视化图表 单量分布情况
@app_Visualization.route('/chart_danliang_distribution')
def chart_danliang_provide():
    wj = 'static/data_table/order_cleaning_cleaning.csv'
    # 第一个图
    data = Account_sales(wj)
    data = list(data)
    data_list = {}
    data_list["账户"] = data[0]
    data_list["单量"] = data[1]

    # 第二个图
    data2=State_sales(wj)
    data_list2={}
    data_list2["状态"] = data2[0]
    data_list2["单量"] = data2[1]

    # 第三个图
    data3=Store_sales(wj)
    data_list3 = {}
    var=''
    for i in range(0,len(data3[0])):
        if( i==len(data3[0])-1):
            var += data3[0][i]
        else:
            var+= data3[0][i]+","
    data_list3["店铺名"]=var
    data_list3["单量"] = data3[1]

    print(data_list)
    print(data_list2)
    print(data_list3)
    return render_template('/chart/chart_danliang_distribution.html',data_list=data_list,data_list2=data_list2,data_list3=data_list3)

# 可视化图表 单量分布情况
@app_Visualization.route('/chart_shouru_distribution')
def chart_shouru_distribution():
    wj = 'static/data_table/order_cleaning_cleaning.csv'
    data=Account_shouru(wj)
    beifenbi=[] #百分比
    for i in range(len(data)):
        beifenbi.append(round(data[i]/sum(data),2)*100)
    print(beifenbi)
    return render_template('/chart/chart_shouru_distribution.html',data=data,beifenbi=beifenbi)



# 最佳商品
@app_Visualization.route('/chart_goods_best')
def chart_goods_best():
    wj = 'static/data_table/order_cleaning_cleaning.csv'
    product_wj = 'static/data_table/product.csv'
    data = goods_sales(wj, product_wj)

    data_list = {}
    var=''
    for i in range(0,len(data[0])):
        if( i==len(data[0])-1):
            var += data[0][i]
        else:
            var+= data[0][i]+","
    data_list["sku"]=var
    data_list["数量"] = data[1]
    data_list["类别"] = data[2]
    img_list=[]
    for i in range(3):
        img_item = {}
        img_item["img"] = data[3][i]
        img_list.append(img_item)
    print(img_list)

    return render_template('/chart/chart_goods_best.html',data=data_list,img_list=img_list)

@app_Visualization.route('/chart_time_danliang')
def chart_time_danliang():
    wj = 'static/data_table/order_cleaning_cleaning.csv'
    data = time_dangliang_sales(wj, 10, 2022, '12')
    data_list = {}
    var = ''
    for i in range(0, len(data[0])):
        if (i == len(data[0]) - 1):
            var += data[0][i]
        else:
            var += data[0][i] + ","
    data_list["日"]=var
    data_list["单量"]=data[1]
    print(data_list)
    return render_template('/chart/chart_time_danliang.html',data_list=data_list,account=10,month=12)


@app_Visualization.route('/chart_time_danliang_form', methods=["POST"])
def chart_time_danliang_form():
    account = int(request.form.get("account"))
    year = int(request.form.get("year"))
    month = request.form.get("month")
    wj = 'static/data_table/order_cleaning_cleaning.csv'
    data = time_dangliang_sales(wj, account, year, month)
    data_list = {}
    var = ''
    for i in range(0, len(data[0])):
        if (i == len(data[0]) - 1):
            var += data[0][i]
        else:
            var += data[0][i] + ","
    data_list["日"]=var
    data_list["单量"]=data[1]
    print(data_list)
    return render_template('/chart/chart_time_danliang.html',data_list=data_list,account=account,month=month)

@app_Visualization.route('/chart_time_shouru')
def chart_time_shouru():
    wj = 'static/data_table/order_cleaning_cleaning.csv'
    data = time_shouru_sales(wj, 10, 2022, '12')
    data_list = {}
    var = ''
    for i in range(0, len(data[0])):
        if (i == len(data[0]) - 1):
            var += data[0][i]
        else:
            var += data[0][i] + ","
    data_list["日"] = var
    data_list["收入"] = data[1]
    print(data_list)
    return render_template('/chart/chart_time_shouru.html', data_list=data_list, account=10, month=12)

@app_Visualization.route('/chart_time_shouru_form', methods=["POST"])
def chart_time_shouru_form():
    account = int(request.form.get("account"))
    year = int(request.form.get("year"))
    month = request.form.get("month")
    wj = 'static/data_table/order_cleaning_cleaning.csv'
    data = time_shouru_sales(wj, account, year, month)
    data_list = {}
    var = ''
    for i in range(0, len(data[0])):
        if (i == len(data[0]) - 1):
            var += data[0][i]
        else:
            var += data[0][i] + ","
    data_list["日"] = var
    data_list["收入"] = data[1]
    print(data_list)
    return render_template('/chart/chart_time_shouru.html',data_list=data_list,account=account,month=month)

# 热力图页面
@app_Visualization.route('/chart_ciyun')
def chart_ciyun():
    wj = 'static/data_table/order_cleaning_cleaning.csv'
    data_02 = ci_show(wj, 2)
    data_06 = ci_show(wj, 6)
    data_09 = ci_show(wj, 9)
    data_10 = ci_show(wj, 10)
    data_11 = ci_show(wj, 11)
    data_17 = ci_show(wj, 17)

    data2=get_reli_data(data_02,0)
    print(data2)
    data6=get_reli_data(data_06,1)
    data9=get_reli_data(data_09,2)
    data10=get_reli_data(data_10,3)
    data11=get_reli_data(data_11,4)
    data17=get_reli_data(data_17,5)
    data2.extend(data6)
    data2.extend(data9)
    data2.extend(data10)
    data2.extend(data11)
    data2.extend(data17)

    return render_template('/chart/chart_ciyun.html',data=data2)

def get_reli_data(data,row):
    data2 = []
    for i in range(len(data[0])):
        data_02_item = []
        data_02_item.append(row)
        data_02_item.append(int(data[0][i])-1)
        data_02_item.append(data[1][i])
        data2.append(data_02_item)
    for i in range(12-len(data2)-1,-1,-1):
        data2.insert(0,[row,i,0])
    return data2
