import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import datetime

matplotlib.rcParams['font.family'] = 'Helvetica Neue, Helvetica, Arial'
def get_model(wj):
    online_retail=pd.read_csv(wj, encoding='utf-8')
    online_retail.insert(1, '总收入（人民币）', online_retail['总收入'] * online_retail['出单汇率'], allow_duplicates=False)

    rfm_data=online_retail.groupby(['买家昵称']).agg({
        '创建时间': 'max',  #客户的消费的时间
        '订单编号': pd.Series.nunique,
        '总收入（人民币）': 'sum'   #客户消费消费的金额
    }).reset_index()

    compare_date =pd.to_datetime(online_retail['创建时间'].max())+ datetime.timedelta(days = 1)  #以这个数据中最大日期为分析时间
    rfm_data['Recency'] =  compare_date - pd.to_datetime(rfm_data['创建时间'])   #以分析时间减去客户最后一次消费时间，时间差算出R频率
    rfm_data['Recency'] =  rfm_data['Recency'].map(lambda x:x.days)  #不加x.days，得到的是'326 days 02:49:00' 这个格式

    #整理汇总数据
    rfm_data.drop('创建时间', axis = 1, inplace = True)  #删除不必要的列
    rfm_data.rename(columns = {
        '总收入（人民币）': 'Monetary',
        '订单编号': 'Frequency'
    }, inplace = True)   #命名另外两列的字段名，因为已经是要做分析的数据，不再用像时间那样处理

    return rfm_data


if __name__ == '__main__':
    main()