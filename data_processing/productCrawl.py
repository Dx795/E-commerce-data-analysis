from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.request import  HTTPCookieProcessor,build_opener
from requests.auth import HTTPBasicAuth
import requests,csv,time


# 爬取商品数据

# 1、获取每一页的url
def Get_Url(pagcount,pagSize):
    all_url=[]
    for i in range(1,pagcount+1):
        all_url.append("https://linkeoo.com/api/warehouse/product/?current="+str(i)+"&pageSize="+str(pagSize)+"&status=NORMAL")
    return all_url

# 2、获取每个url的详细信息
def Get_order_url(all_url,headers):
    num=1
    for i in all_url:
        r=requests.get(url=i,headers=headers)
        Analysis_Json(r.json()["results"])
        time.sleep(5)
        print("第%s页爬完了" %num)
        num+=1

# 3、解析json格式数据
def Analysis_Json(data):
    print("这一页一共有%d条数据" %(len(data)))
    # 订单列表（汇总）
    pro_list = []
    # 截取数据
    for i in range(0, len(data)):
        pro_item=[]
        pro_item.append(data[i]['base_info']["main_sku"]) #商品sku
        pro_item.append(data[i]['base_info']["title_zh"]) #商品标题
        pro_item.append(data[i]['base_info']["category_info"]
                        ["category_tree"]["tree_name"][0]+">"+data[i]
        ['base_info']["category_info"]["category_tree"]["tree_name"][1]) #商品类别
        pro_item.append(data[i]['base_info']["images"][0]["url"]) #商品标题
        pro_item.append(data[i]["developer"]["username"]) #开发员
        # 准备规格
        sku_list=[] #商品规格列表
        # print(len(data[i]['base_info']["skus"]))
        for j in range(0,len(data[i]['base_info']["skus"])):
            sku_item=[]
            sku_item.append(data[i]['base_info']["skus"][j]["sku"]) #规格sku
            sku_item.append(data[i]['base_info']["skus"][j]["img_url"]) #规格图片
            sku_item.append(data[i]['base_info']["skus"][j]["price"]) #仓库价格
            sku_list.append(sku_item)

        pro_item.append(sku_list)
        pro_list.append(pro_item)
    Save_data(pro_list)

# 4、保存为文件
def Save_data(pro_list):
    with open(r'../static/data_table/product.csv', 'a', encoding='utf-8', newline='')as f:
        wt=csv.writer(f)
        num=1 #提示作用
        for i in range(0, len(pro_list)):
            for j in range(0,len(pro_list[i][5])):
                if(j==0):
                    wt.writerow([pro_list[i][0],pro_list[i][1],pro_list[i][2],pro_list[i][3],pro_list[i][4],pro_list[i][5][j][0],pro_list[i][5][j][1],pro_list[i][5][j][2]])
                else:
                    wt.writerow(["","","","","",pro_list[i][5][j][0],pro_list[i][5][j][1],pro_list[i][5][j][2]])
            print("%d 条写入" %num)
            num+=1
        print('已写入')
        f.close()

if __name__ == '__main__':
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46',
        'authorization': 'token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMiwidXNlcm5hbWUiOiIwMDEwIiwiZXhwIjoxNjcxMzMzNzIwLCJlbWFpbCI6IiJ9.4b3pp2mgQe6mRzfgbicIuoriP3L5JuyhyXhD6CPXo8E'}

    # 爬取数据 数据爬取页数和 一页的条数
    all_url=Get_Url(pagcount=18,pagSize=100)
    with open(r'../static/data_table/product.csv', 'a', encoding='utf-8', newline='') as f:
        table_lable = ['产品Sku', '中文标题', '类别', '商品主图','开发员','规格Sku', '规格图片', '规格价格']
        wt = csv.writer(f)
        wt.writerow(table_lable)
    Get_order_url(all_url,header)







