from flask import Flask,render_template,request,Response,redirect,url_for,Blueprint
import os, sys
from data_analysis.data_visualization_provide import *
from data_processing.dataCrawl import *
from data_processing.dataCleaning import *

# 创建一个蓝图的对象，蓝图就是一个小模块的抽象的概念 
app_index = Blueprint("app_index", __name__)

# 登录页面
@app_index.route('/')
def login():
    return render_template('login.html')

@app_index.route('/index')
def index():
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
        'authorization': 'token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMiwidXNlcm5hbWUiOiIwMDEwIiwiZXhwIjoxNjc4Njg3NTIxLCJlbWFpbCI6IiJ9.eHyhZ-N8ODn4p7ThnutbihGApaOpOkzVLLJsRD8tj3A'}

    try:os.remove('static/data_table/day_order.csv')
    except:print("已经删除文件了")
    table_name='day_order'
    wj=r'static/data_table/'+table_name+'.csv'

    # 1、爬取数据 数据爬取页数和 一页的条数
    all_url = Get_Url(pagcount=1, pagSize=30)
    with open(wj, 'a', encoding='utf-8', newline='') as f:
        table_lable = ['订单id', '订单编号', '下单国家', '店铺名', '订单拥有账户', '买家昵称',
                       '创建时间', '买家留言', '订单状态', '出单汇率', '平台佣金', '交易费用',
                       '服务费', '优惠券', '预估运费', '实际运费', '税费', '退款', '其他费用', '总费用',
                       '商品收入', '运费收入', '平台补贴', '其他收入', '总收入', '订单实际收入（订单总收入-订单总费用）',
                       '购买的商品']
        wt = csv.writer(f)
        wt.writerow(table_lable)
    Get_order_url(all_url, header,wj)
    # 2、数据清洗
    get_data(wj,table_name)
    # 3、根据清洗的数据 进行数据统计分析
    wj = wj.split(table_name)[0] + table_name + '_cleaning_cleaning.csv'

    data=Index_sales(wj)
    data_list = {}
    var=''
    for i in range(0,len(data[0])):
        if( i==len(data[0])-1):
            var += data[0][i]
        else:
            var+= data[0][i]+","
    data_list["时间"] = var
    data_list["单量"] = data[1]
    # 求出最大值 让y轴的长度＋1
    max_px=sorted(data_list["单量"],reverse=True)
    max = max_px[0]+1

    # 主页右边的4个值
    data_list["用户"] = data[2]
    data_list["出单"] =data[3]
    data_list["销冠"] = data[4]
    data_list["收入"] = round(data[5], 2)
    print(data_list)
    print(max)

    return render_template('index.html',data_list=data_list,max=max)

