# _*_ coding:utf-8 _*_
from app import create_app


app=create_app()

if __name__=="__main__":
    # 生产环境 nginx + uwsgi
    app.run(debug=app.config['DEBUG'],host='0.0.0.0',port=4000)
