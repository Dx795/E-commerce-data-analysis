from flask import Flask,render_template,request,Response,redirect,url_for

app = Flask(__name__)

# **********************************   登 录 和 主 页 ********************************
from LoginAndIndex import app_index
app.register_blueprint(app_index)

# **********************************   数 据 统 计 ********************************
from DataStatistical import app_statistical
app.register_blueprint(app_statistical)

# **********************************   可 视 化 图 表 ********************************
from ViewVisualization import app_Visualization
app.register_blueprint(app_Visualization)

# **********************************   大 屏 数 据 图 ********************************
from LargeScreenData import app_screendata
app.register_blueprint(app_screendata)

if __name__ == '__main__':
    app.run()
