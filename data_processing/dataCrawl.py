import requests,csv,time
import pandas as pd
from lxml import etree

# 1、获取每一页的url
def Get_Url(pagcount,pagSize):
    all_url=[]
    for i in range(1,pagcount+1):
        all_url.append("https://linkeoo.com/api/order/list/?current="+str(i)+"&pageSize="+str(pagSize)+"&status=all")
    return all_url

# 2、获取每个url的详细信息
def Get_order_url(all_url,headers,wj):
    num=1
    for i in all_url:
        print(i)
        r=requests.get(url=i,headers=headers)
        try:
            Analysis_Json(r.json()["results"],wj)
        except Exception as e:
            print("数据已经爬取完毕,没有更多数据可以获得")
            break
        time.sleep(5)
        print("第%s页爬完了" %num)
        num+=1

# 3、解析json格式数据
def Analysis_Json(data,wj):
    print("这一页一共有%d条数据" %(len(data)))
    # 截取有用信息
    # 订单列表（汇总）
    ord_list = []

    for i in range(0, len(data)):
        # 每一个订单（列表） ord_item_list
        ord_item_list = []

        # 商品列表
        ord_item_list.append(data[i]['id'])  # 本地订单id
        ord_item_list.append(data[i]['order_sn'])  # 订单编号
        ord_item_list.append(data[i]['region'])  # 订单位置
        ord_item_list.append(data[i]['shop_info']["name"])  # 下单店铺名
        ord_item_list.append(data[i]['shop_info']["username"])  # 订单拥有账户
        ord_item_list.append(data[i]['buyer_username'])  # 订单买家昵称
        ord_item_list.append(data[i]['create_time'])  # 订单创建时间
        ord_item_list.append(data[i]['message_from_buyer'])  # 买家留言
        #订单状态
        if (len(data[i]['tags']) > 0):
            ord_item_list.append(data[i]['tags'][0]['label'])
        else:
            ord_item_list.append("线上支付")

        ord_item_list.append(data[i]['bill']['current_exchange_rate'])  # 订单出单汇率

        #出单收费
        ord_item_list.append(data[i]['bill']['fee']['commission_fee'])  # 订单平台佣金
        ord_item_list.append(data[i]['bill']['fee']['transaction_fee'])  # 订单交易费用
        ord_item_list.append(data[i]['bill']['fee']['service_fee'])  # 订单服务费
        ord_item_list.append(data[i]['bill']['fee']['voucher_fee'])  # 订单优惠券
        ord_item_list.append(data[i]['bill']['fee']['estimated_shipping_fee'])  # 订单预估运费
        ord_item_list.append(data[i]['bill']['fee']['actual_shipping_fee'])  # 订单实际运费
        ord_item_list.append(data[i]['bill']['fee']['tax'])  # 订单税费
        ord_item_list.append(data[i]['bill']['fee']['refund_fee'])  # 订单退款
        ord_item_list.append(data[i]['bill']['fee']['other_fee'])  # 订单其他费用
        ord_item_list.append(data[i]['bill']['fee']['total_fee'])  # 订单总费用


        ord_item_list.append(data[i]['bill']['income']['product_amount'])  # 订单商品收入
        ord_item_list.append(data[i]['bill']['income']['shipping_amount'])  # 订单运费收入
        ord_item_list.append(data[i]['bill']['income']['platform_rebate'])  # 订单平台补贴
        ord_item_list.append(data[i]['bill']['income']['other_income'])  # 订单其他收入
        ord_item_list.append(data[i]['bill']['income']['total_amount'])  # 订单总收入

        ord_item_list.append(data[i]['bill']['escrow_amount'])  # 订单实际收入（订单总收入-订单总费用）

        # 每一个订单里面的 购买商品详情
        ord_item=[]
        for j in range(0,len(data[i]['items'])):
            ord_item_xp=[]
            ord_item_xp.append(data[i]['items'][j]['variation_sku'])  # 购买的商品规格
            ord_item_xp.append(data[i]['items'][j]['item_url'])  # 购买的商品图片
            ord_item_xp.append(data[i]['items'][j]['purchase_quantity'])  # 购买的商品数量
            ord_item.append(ord_item_xp)

        ord_item_list.append(ord_item)
        ord_list.append(ord_item_list)

    # for i in range(0,len(data)):
    #     print(ord_list[i])
    Save_data(ord_list,wj)

# 4、保存为文件
def Save_data(ord_list,wj):
    with open(wj, 'a', encoding='utf-8', newline='')as f:
        wt=csv.writer(f)
        num=0
        for i in range(0, len(ord_list)):
            num+=1
            wt.writerow(ord_list[i])
        print('%d 条数据已写入' %num)
        f.close()

if __name__ == '__main__':
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46',
        'authorization': 'token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMiwidXNlcm5hbWUiOiIwMDEwIiwiZXhwIjoxNjcxOTA0MzM4LCJlbWFpbCI6IiJ9.NcFzRinGlesd9GIESZB9K1x9E3VpOd_keEZq4Apb6Os'}

    # 爬取数据 数据爬取页数和 一页的条数
    all_url=Get_Url(pagcount=1,pagSize=10)
    with open(r'../static/data_table/order_test_10.csv', 'a', encoding='utf-8', newline='') as f:
        table_lable = ['订单id', '订单编号', '下单国家', '店铺名','订单拥有账户', '买家昵称',
                       '创建时间', '买家留言', '订单状态', '出单汇率', '平台佣金','交易费用',
                       '服务费','优惠券','预估运费', '实际运费','税费', '退款', '其他费用','总费用',
                       '商品收入', '运费收入', '平台补贴','其他收入', '总收入', '订单实际收入（订单总收入-订单总费用）',
                       '购买的商品']
        wt = csv.writer(f)
        wt.writerow(table_lable)
    Get_order_url(all_url,header)