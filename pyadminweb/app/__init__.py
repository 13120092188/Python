from flask import Flask, render_template,send_from_directory,redirect,url_for,flash,request,json
from flask_sqlalchemy import SQLAlchemy
import pymysql
from app.req import *
from app.block.next import *
import threading
import qrcode
import image
import datetime
# 创建一个flask 实例
app = Flask(__name__)
#配置数据库地址
conn = pymysql.connect(host='127.0.0.1', user='root', password='312058', db='flask', charset="utf8")
#app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:wqf0412.@127.0.0.1：3306/flask'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 引入config.py文件
# app.config.from_object('config')
#
# #创建一个 SQLAlchemy对象实例.
#db = SQLAlchemy(app)
tag=0
contact_name=1
contact_phone=1
contact_email=1
user_name = 0
#用来记录商品的id
t_id = 0
#用来记录登录的企业的id
u_id=0
bianhao=0
# #app.config["VAR_NAME"]  访问相应变量

@app.route('/signin',methods=['POST','GET'])
def do_signin():
    global user_name
    global u_id
    if request.method == 'POST':
        print("表单提交成功")
        sql = "select * from enterprise"
        cur = conn.cursor()
        cur.execute(sql)  # 执行sql语句
        conn.commit()
        results = cur.fetchall()  # 获取查询的所有记录
        print(results)
            # print( "name", "password")
            # 遍历结果
        for row in results:
                print(row)
                email = row[1]
                if(request.form.get('email') == str(email)):

                  u_id=row[6]

                  print(u_id)
                  return redirect('http://127.0.0.1:5000/')


    return render_template("signin.html")

@app.route('/signin1',methods=['POST','GET'])
def do_signin1():
    global user_name
    global u_id
    if request.method == 'POST':
        print("表单提交成功")
        sql = "select * from users"
        cur = conn.cursor()
        cur.execute(sql)  # 执行sql语句
        conn.commit()
        results = cur.fetchall()  # 获取查询的所有记录
        print(results)
            # print( "name", "password")
            # 遍历结果
        for row in results:
                print(row)
                email = row[2]
                if(request.form.get('email') == str(email)):
                  user_name=row[1]
                  u_id=row[0]
                  print(user_name)
                  print(u_id)
                  return redirect('http://127.0.0.1:5000/index1')


    return render_template("signin_1.html")

@app.route('/signup',methods=['POST','GET'])
def do_signup():
    name1 = 0
    if request.method == 'POST':
        if (request.form.get('password') ==request.form.get('password') ):
            sql = "insert into users(username, password, email) values('%s','%s','%s')" % (
                request.form.get('username'), request.form.get('password'), request.form.get('user_email'))
            cursor = conn.cursor()
            name1=2
            try:
                cursor.execute(sql)
                conn.commit()
            except:
                conn.rollback()
            cursor.close()
            return redirect('http://127.0.0.1:5000/signin')
        else:
             name1 = 1

    return render_template("signup.html",name1 = name1)

@app.route('/admission',methods=['POST','GET'])
def do_admission():
    global  tag
    global  contact_name
    global  contact_phone
    global  contact_email
    print("你进入这个界面了/。。。。。。。。。")
    if request.method == 'POST':
        if tag==0:
          print("tag0")
          contact_name=request.form.get('contact_name')
          print(contact_name)
          contact_phone=request.form.get('contact_phone')
          contact_email=request.form.get('contact_email')
          tag=tag+1
          return render_template("admission.html")
        if(tag==1):
            print("tag1")
            com_name = request.form.get('com_name')
            com_phone = request.form.get('com_phone')
            com_address = request.form.get('com_address')
            tag = tag + 1
            print(com_address)

            sql = "insert into enterprise(com_name,com_phone,com_address,contact_name,contact_phone,contact_email) " \
                  "values('%s','%s','%s','%s','%s','%s')" % (com_name, com_phone, com_address, contact_name, contact_phone, contact_email)
            print(contact_name)

            print("charru")
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()


            cursor.close()
    return render_template("admission.html")

@app.route('/find_password',methods=['POST','GET'])
def do_find_password():
    if request.method == 'POST':
        req.code(request.form.get('verify'))
        sql = "UPDATE users SET password = '%s' WHERE email= '%s'"% (request.form.get('pwd'),request.form.get('email'))
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()

    cursor.close()
    return render_template("find_password.html")

@app.route('/',methods=['POST','GET'])
@app.route('/index',methods=['POST','GET'])
def do_index():
    global bianhao
    global t_id
    global u_id
    sql = "select * from enterprise where id = %s" % u_id
    cur = conn.cursor()
    cur.execute(sql)  # 执行sql语句
    data = []
    results = cur.fetchall()  # 获取查询的所有记录
    for row in results:
        for i in row:
            data.append(i)
    print(data)

    sql1 = "select * from goods where u_id = %s" % u_id
    cur1 = conn.cursor()
    cur1.execute(sql1)  # 执行sql语句
    data1 = []
    results1 = cur1.fetchall()  # 获取查询的所有记录
    for row in results1:
        for i in row:
            data1.append(i)
    print(data1)

    if request.method == 'POST':
        bianhao = None
        bianhao=request.form.get('bianhao')
        print(bianhao)
        if(bianhao != None):
            return redirect('http://127.0.0.1:5000/search')
        else:
            t_id=request.form.get('tid')
            print(t_id)
            return redirect('http://127.0.0.1:5000/chain')

    return render_template("management.html",data = data, data1 = data1)

@app.route('/transaction',methods=['POST','GET'])
def do_transaction():
    global bianhao
    global t_id
    global u_id
    sql = "select * from enterprise where id = %s" % u_id
    cur = conn.cursor()
    cur.execute(sql)  # 执行sql语句
    data = []
    results = cur.fetchall()  # 获取查询的所有记录
    for row in results:
        for i in row:
            data.append(i)
    print(data)

    sql1 = "select * from goods where u_id = %s" % u_id
    cur1 = conn.cursor()
    cur1.execute(sql1)  # 执行sql语句
    data1 = []
    results1 = cur1.fetchall()  # 获取查询的所有记录
    for row in results1:
        for i in row:
            data1.append(i)
    print(data1)

    if request.method == 'POST':
        bianhao = None
        bianhao=request.form.get('bianhao')
        print(bianhao)
        if(bianhao != None):
            return redirect('http://127.0.0.1:5000/search')
        else:
            t_id=request.form.get('tid')
            print(t_id)
            return redirect('http://127.0.0.1:5000/chain')

    return render_template("transaction.html",data = data, data1 = data1)

@app.route('/index1',methods=['POST','GET'])
def do_index1():
    global bianhao
    global t_id
    global u_id
    sql = "select * from enterprise where id = %s" % u_id
    cur = conn.cursor()
    cur.execute(sql)  # 执行sql语句
    data = []
    results = cur.fetchall()  # 获取查询的所有记录
    for row in results:
        for i in row:
            data.append(i)
    print(data)

    sql1 = "select * from goods where u_id = %s" % u_id
    cur1 = conn.cursor()
    cur1.execute(sql1)  # 执行sql语句
    data1 = []
    results1 = cur1.fetchall()  # 获取查询的所有记录
    for row in results1:
        for i in row:
            data1.append(i)
    print(data1)

    return render_template("management_1.html",data = data, data1 = data1)



@app.route('/chain',methods=['POST','GET'])
def do_chain():
    global t_id
    sql = "select * from commodity where t_id = %s" % t_id
    cur = conn.cursor()
    cur.execute(sql)  # 执行sql语句
    data=[]
    results = cur.fetchall()  # 获取查询的所有记录
    for row in results:
        for i in row:
            data.append(i)
    print(data)
    if request.method == 'POST':
        sql = "insert into commodity(num, comm_name, processdate, specification, adress, flag, com_name, t_id) " \
              "values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (
        request.form.get('num'), request.form.get('comm_name'), request.form.get('processdate'),
        request.form.get('specification'), request.form.get('adress'), 1, request.form.get('company'), t_id)
        #加入区块
        s = request.form.get('num')
        dat=request.form.get('company')+ request.form.get('num') + request.form.get('comm_name')+\
             request.form.get('processdate')+request.form.get('specification')+request.form.get('adress')
        qcode="公司名称:"+request.form.get('company')+"编号:"+ request.form.get('num')+ "商品名称:"+request.form.get('comm_name')+"生产日期:"+\
              request.form.get('processdate')+"规格:"+request.form.get('specification')+"生产地址:"+request.form.get('adress')
        print(data)
        filer = open('app/block/record.json', 'r', encoding='utf-8')
        dic = eval(filer.read())
        i=dic[len(dic) - 1][str(len(dic) - 1)]['index']
        diff=dic[len(dic) - 1][str(len(dic) - 1)]['diff']
        if (i % 5 == 0 and i != 0):
            diff = Adjust_of_diff(diff)
        filer.close()
        previous_block = dic[len(dic) - 1][str(len(dic) - 1)]['self.hash']
        print(i)
        print(previous_block)
        print(diff)
        next_block(i,previous_block, diff, dat)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=2,
        )
        qr.add_data(qcode)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        path = 'app/static/img/' + s + '.png'
        img.save(path)

    #执行数据库操作
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()

    cursor.close()
    return render_template("information-chain.html",data=data)


#点击商品查询之后，跳转到查看区块练的界面  没有加入区块的权限，复制粘贴出一个新的html
@app.route('/search', methods=['POST', 'GET'])
def adddddd():
        global bianhao

        cur = conn.cursor()

        print(bianhao)
        sqlll = "select * from commodity where  t_id = %s " % bianhao
        cur.execute(sqlll)  # 执行sql语句
        data = []
        results = cur.fetchall()  # 获取查询的所有记录
        for row in results:
            for i in row:
                data.append(i)
        print(data)

        return render_template("search.html",data = data)



#点击商品名称的添加按钮 会跳转到这里来
@app.route('/add', methods=['POST', 'GET'])
def add():
    global u_id
    print(u_id)
    #商品的名称

    if request.method == 'POST':
        namene = request.form.get('name')
        cur = conn.cursor()
        #企业的id就是 商品的uid
        # 插入goods表 name和 tid 通过这个 tid goods和企业表对应
        sqll = "insert into goods(name,u_id,img_src) values ('%s','%s','%s')" % (namene,u_id,request.form.get('img_src'))
        cur.execute(sqll)
        conn.commit()
        print("1ccccc")
        # 从goods表中读取到 idid主键  通过这个 goods 和commodity对应
        sqlll = "select * from goods where  name=%s" % namene
        cur.execute(sqlll)  # 执行sql语句
        results = cur.fetchall()
        print(results)
        for row in results:
            tid = row[0]
        print(tid)
        sql = "insert into commodity(num, comm_name, processdate, specification, adress, flag, com_name,t_id) " \
              "values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (
                  request.form.get('num'), request.form.get('comm_name'), request.form.get('processdate'),
                  request.form.get('specification'), request.form.get('adress'), 1, request.form.get('company'), tid)
        cur.execute(sql)
        conn.commit()
        return render_template("management.html")
    return render_template("add.html")

@app.route('/user')
def do_user():
    sql = "select * from users"
    cur = conn.cursor()
    cur.execute(sql)  # 执行sql语句
    data1 = []
    results = cur.fetchall()  # 获取查询的所有记录
    for row in results:
        for i in row:
            data1.append(i)
    print(data1)

    return render_template("user.html",data1 = data1)

@app.route('/json')
def do_json():
    sql = "select * from json"
    cur = conn.cursor()
    cur.execute(sql)  # 执行sql语句
    data1 = []
    results = cur.fetchall()  # 获取查询的所有记录
    for row in results:
        for i in row:
            data1.append(i)
    print(data1)

    return render_template("json.html",data1 = data1)

@app.route('/goods')
def do_goods():
    sql = "select * from goods"
    cur = conn.cursor()
    cur.execute(sql)  # 执行sql语句
    data1 = []
    results = cur.fetchall()  # 获取查询的所有记录
    for row in results:
        for i in row:
            data1.append(i)
    print(data1)

    return render_template("goods.html",data1 = data1)

@app.route('/enterprise')
def do_enterprise():
    sql = "select * from enterprise"
    cur = conn.cursor()
    cur.execute(sql)  # 执行sql语句
    data1 = []
    results = cur.fetchall()  # 获取查询的所有记录
    for row in results:
        for i in row:
            data1.append(i)
    print(data1)

    return render_template("enterprise.html",data1 = data1)

@app.route('/commodity')
def do_commodity():
    sql = "select * from commodity"
    cur = conn.cursor()
    cur.execute(sql)  # 执行sql语句
    data1 = []
    results = cur.fetchall()  # 获取查询的所有记录
    for row in results:
        for i in row:
            data1.append(i)
    print(data1)

    return render_template("commodity.html",data1 = data1)

@app.route('/admin_base')
def do_admain_base():

    return render_template("admin-base.html")

@app.route('/admin_signin')
def do_admain_sign():

    return render_template("admin-signin.html")

@app.route('/transaction',methods=['POST','GET'])
def do_chainnnnn():
            print(1231321123)
            cursor = conn.cursor()
            sql=" select * from trun where buyid=%s " % 1
            cur=cursor.execute(sql)
            conn.commit()
            #得到了全部符合的 存到results 要转换到界面上
            results=cur.fetchall()
            print(results)

            return render_template("transaction.html")