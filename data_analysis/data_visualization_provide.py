import datetime
import time
from time import strftime
from pandas import DataFrame
import ast

from matplotlib import pyplot as plt
import pandas as pd

# 单量分布页面
# 根据账户分组 计算各账户单量
def Account_sales(wj):
    data = pd.read_csv(wj, encoding='utf-8')
    data=data.groupby("订单拥有账户").agg({"订单编号": "count"}).reset_index()
    zh = pd.to_numeric(data["订单拥有账户"])  # object类型转为int类型
    count = pd.to_numeric(data["订单编号"])  # object类型转为int类型
    return(zh.tolist(),count.to_list())


# 根据订单状态 计算各状态单量分布
def  State_sales(wj):
    data = pd.read_csv(wj, encoding='utf-8')
    data = data.groupby("订单状态").agg({"订单编号": "count"}).reset_index()
    data=pd.concat([data[29:30],data[37:38],data[40:41]],ignore_index=True)
    zt = data["订单状态"]
    count = pd.to_numeric(data["订单编号"])  # object类型转为int类型
    return (zt.tolist(), count.to_list())

# 根据店铺名分组 计算各单量分布
def Store_sales(wj):
    data = pd.read_csv(wj, encoding='utf-8')
    data = data.groupby("店铺名").agg({"订单编号": "count"}).reset_index()
    dp = data["店铺名"]
    count = pd.to_numeric(data["订单编号"])  # object类型转为int类型
    return (dp.tolist(), count.to_list())


# 用于主页的显示
def Index_sales(wj):
    data=pd.read_csv(wj, encoding='utf-8')
    for i in reversed(range(0,len(data))):
        # print(i)
        if((int(data['创建时间'][i][8:10]))!=datetime.datetime.now().day):
            data.drop(data.index[i], inplace=True)
    for i in reversed(range(0, len(data))):
        data['创建时间'][i]=data['创建时间'][i][11:13]+":00"
    data = data.dropna(axis=0)
    # 去除已作废
    for i in reversed(range(0, len(data))):
        if (data['订单状态'][i]=="已作废"):
            data.drop(data.index[i], inplace=True)
    data2 = data.groupby("创建时间").agg({"订单编号": "count"}).reset_index()
    time = data2["创建时间"]
    count = pd.to_numeric(data2["订单编号"])  # object类型转为int类型
    # 主页右边的4个值提供
    # 1、够买人数
    data3=data.groupby("买家昵称").agg({"订单编号": "count"}).reset_index()
    buy_sum=len(data3["买家昵称"])
    # 2、出单数
    chudan_sum=data2['订单编号'].sum()
    # 3、销冠店铺
    data4=data.groupby("店铺名").agg({"订单编号": "count"}).reset_index()
    dp_name=data4["店铺名"][data4['订单编号'].argmax()]
    # 4、总收入
    shouru_sum = data[data.columns[23]].sum()
    return (time.tolist(), count.to_list(),buy_sum,chudan_sum,dp_name,shouru_sum)


# 收入分布页面
def Account_shouru(wj):
    data = pd.read_csv(wj, encoding='utf-8')
    data = data.groupby("订单拥有账户").agg({data.columns[23]: "sum"}).reset_index()
    print(data)
    zh = pd.to_numeric(data["订单拥有账户"])  # object类型转为int类型
    sum = pd.to_numeric(data[data.columns[1]])  # object类型转为int类型
    sum=sum.to_list()
    for i in range(len((sum))):
        sum[i]=round(sum[i],2)
    return (sum)


# 世界单量分布页面
def countries_sales(wj):
    data = pd.read_csv(wj, encoding='utf-8')
    data=data.groupby("下单国家").agg({"订单编号": "count"}).reset_index()
    gj = data["下单国家"]
    count = pd.to_numeric(data["订单编号"])  # object类型转为int类型
    return (gj.tolist(), count.to_list())

# 商品分析页面
def goods_sales(wj,product_data_wj):
    # 1、打开文件 商品列是列表的形式存储的
    data = pd.read_csv(wj, encoding='utf-8')
    # 2、把商品列表都取出来转为DataFrame格式 加到dfs列表
    dfs=[]
    for i in range(len(data)):
        sp_list=ast.literal_eval(data['购买的商品'][i])
        dfs.append(DataFrame(sp_list))
    # 3、把整个dfs列表合并成一个DataFrame
    data = pd.concat(dfs)
    # 4、给data加列名 先按照sku规格分组
    data.columns = ["产品Sku", "图链接", "数量"]
    data=data.groupby('产品Sku').agg({"数量": "sum"}).reset_index()
    # 5、进行列名的取值 取前6个元素（商品主sku）
    for index, row in data.iterrows():  #获得商品sku
        data['产品Sku'][index]=data['产品Sku'][index][0:6]
    # 6、对产品Sku进行分组 计算数量
    data2=data.groupby('产品Sku').agg({"数量": "sum"}).reset_index()
    # 7、去除第一行空行（不得劲）
    data2=data2.drop([0])
    # 8、按照数量排序
    data2 = data2.sort_values("数量", ascending=False)
    # 9、取前10条数据
    data2=data2[0:10]
    # 10、读取另一个文件 进行合并 取得商品主图链接
    product_data=pd.read_csv(product_data_wj, encoding='utf-8')
    # 11、开始合并
    merge_data=pd.merge(data2, product_data)
    #12、取值
    sku=merge_data['产品Sku']
    count=merge_data['数量']
    category=merge_data['类别']
    img=merge_data['商品主图']
    return (sku.tolist(), count.to_list(),category.tolist(), img.to_list())


# 时间单量页面
def time_dangliang_sales(wj,zh_name,year,month):
    # 1、打开文件
    data = pd.read_csv(wj, encoding='utf-8')
    # 2、找出不是 想要的账户的下标 删掉这些行
    indexs = data[data['订单拥有账户'] != zh_name].index
    data.drop(indexs, inplace=True)
    # 3、多出两列  一列 月份，一列天数，对这两列根据创建时间来赋值
    data.loc[:, '月份'] = 0
    data.loc[:, '日'] = 0
    for index, row in data.iterrows():
        data['月份'][index]=data['创建时间'][index][5:7]
        data['日'][index]=data['创建时间'][index][8:10]

    # 4、根据传过来的月份 把其他月份删掉
    indexs = data[data['月份']!= month].index
    data.drop(indexs, inplace=True)
    # 5、进行单数统计
    data=data.groupby(['日']).agg({"订单编号": "count"}).reset_index()
    # 6、传值
    day = data['日']
    count = data['订单编号']
    return (day.tolist(), count.to_list())

# 时间收入页面
def time_shouru_sales(wj,zh_name,year,month):
    # 1、打开文件
    data = pd.read_csv(wj, encoding='utf-8')
    # 2、找出不是 想要的账户的下标 删掉这些行
    indexs = data[data['订单拥有账户'] != zh_name].index
    data.drop(indexs, inplace=True)
    # 3、多出两列  一列 月份，一列天数，对这两列根据创建时间来赋值
    data.loc[:, '月份'] = 0
    data.loc[:, '日'] = 0
    for index, row in data.iterrows():
        data['月份'][index] = data['创建时间'][index][5:7]
        data['日'][index] = data['创建时间'][index][8:10]

    # 4、根据传过来的月份 把其他月份删掉
    indexs = data[data['月份'] != month].index
    data.drop(indexs, inplace=True)
    # 5、进行单数统计
    data = data.groupby(['日']).agg({data.columns[23]: "sum"}).reset_index()
    # 6、传值
    day = data['日']
    shouru=data[data.columns[1]]
    for i in range(len(shouru.tolist())):
        shouru[i]=round(shouru[i],2)
    return (day.tolist(),shouru.tolist())

# 数据预览页面
def data_show(wj):
    data=pd.read_csv(wj, encoding='utf-8')
    return data

# 热力图页面
def ci_show(wj,zh_name):
    data=pd.read_csv(wj, encoding='utf-8')
    indexs = data[data['订单拥有账户'] != zh_name].index
    data.drop(indexs, inplace=True)
    # 多出1列  一列月份
    data.loc[:, '月份'] = 0
    for index, row in data.iterrows():
        data['月份'][index] = data['创建时间'][index][5:7]

    data = data.groupby(['月份']).agg({'订单编号': "count"}).reset_index()
    yf=data['月份']
    count=data['订单编号']

    return (yf.tolist(),count.to_list())



if __name__ == '__main__':
    data=ci_show('../order_cleaning_cleaning.csv',10)
    print(data)
