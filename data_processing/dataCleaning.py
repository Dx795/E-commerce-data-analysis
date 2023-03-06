import pandas as pd
import json
import ast

# 1、从order.csv中获得数据
def get_data(wj,table_name):
    raw_data = pd.read_csv(wj, encoding='utf-8')
    print(raw_data)
    wj=wj.split(table_name)[0]+table_name+'_cleaning.csv'
    print(wj)
    clean_data(raw_data,wj,table_name)

def clean_data(data, wj,table_name):
    data=data.drop(columns=['订单id','税费','其他费用'],axis=1)# 去除无用的数据列
    data.drop_duplicates(inplace=True) #删除重复值
    data.replace('已申请跟踪单号', '线上支付', inplace=True)  #将订单状态为已申请跟踪单号的订单修改为线上支付
    data.replace('已打印面单','线上支付', inplace=True)  #将订单状态为已打印面单的订单修改为线上支付
    data.replace('有留言', '线上支付', inplace=True)  #将订单状态为已申请跟踪单号的订单修改为线上支付

    # 填充空值
    print(data.isnull().sum())
    data.loc[data.买家留言.isnull(), '买家留言'] = "无留言"

    #实际运费的计算（为0则为预估运费）
    data.loc[data.实际运费 == 0, '总费用'] = data['总费用']+data['预估运费']
    data.loc[data.实际运费==0,'订单实际收入（订单总收入-订单总费用）']= data['总收入']-data['总费用']
    data.loc[data.实际运费==0, '实际运费'] = data['预估运费']
    #增加预估收入列 计算为：收入*汇率
    data.insert(23,'预估收入（人民币）',data['订单实际收入（订单总收入-订单总费用）']*data['出单汇率'],allow_duplicates = False)
    #国家列名内容的修改
    data.loc[data.下单国家 =="BR", '下单国家'] ='巴西'
    data.loc[data.下单国家 =="VN", '下单国家'] ='越南'
    data.loc[data.下单国家 =="SG", '下单国家'] ='新加坡'
    data.loc[data.下单国家 =="PH", '下单国家'] ='菲律宾'
    data.loc[data.下单国家 =="ID", '下单国家'] ='印度尼西亚'
    data.loc[data.下单国家 =="TW", '下单国家'] ='台湾'
    data.loc[data.下单国家 =="TH", '下单国家'] ='泰国'
    data.loc[data.下单国家 =="MY", '下单国家'] ='马来西亚'
    data.loc[data.下单国家 =="MX", '下单国家'] ='墨西哥'
    data.loc[data.下单国家 =="CO", '下单国家'] ='哥伦比亚'
    data.loc[data.下单国家 =="CL", '下单国家'] ='智利'
    data.loc[data.下单国家 =="PL", '下单国家'] ='波兰'

    #将购买的商品的内容 列表出现有空的删除（无法提供成本价格）
    data=delete_no_goods(data)
    data.to_csv(wj,encoding='utf-8',index=None)

    raw_data = pd.read_csv(wj, encoding='utf-8')
    data=delete_no_goods(raw_data)

    wj = wj.split(table_name)[0] + table_name + '_cleaning_cleaning.csv'
    data.to_csv(wj,encoding='utf-8',index=None)



def delete_no_goods(data):
    index_list=[]
    for index, row in data.iterrows():
        sp_list=ast.literal_eval(data['购买的商品'][index])
        if (len(sp_list[0][0])==0):
            index_list.append(index)

    print(len(index_list))
    index_list.reverse() #倒序遍历
    for i in range(0,len(index_list)):
        # print(index_list[i])
        data.drop(data.index[index_list[i]], inplace=True)


    return data



if __name__ == '__main__':
    get_data()

