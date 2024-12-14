from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pymysql.constants.ER import HOSTNAME
from sqlalchemy import text

app = Flask(__name__)

HOSTNAME = '127.0.0.1'
PORT = 3306
USERNAME = 'root'
PASSWORD = '5739'
DATABASE = 'customer'
app.config['SQLALCHEMY_DATABASE_URI']=f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}/{DATABASE}?charset=utf8mb4'

db = SQLAlchemy(app)

# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute(text("select 1"))
#         print(rs.fetchone())

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username= db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

# customer=Customer(username='张三', password='123456', email='123456@gmail.com')
with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/customer/add')
def add_customer():
    customer = Customer(username='张三', password='123456', email='123456@gmail.com')
    db.session.add(customer)
    db.session.commit()
    return '创建成功'

@app.route('/customer/query')
def query_customer():
    #1.get:根据主键查找
    # customer = Customer.query.get(1)
    # print(f'id={customer.id},username={customer.username},email={customer.email}')
    #2.filter_by查找
    #QuerySet 类列表对象
    #Query： 类数组
    customers = Customer.query.filter_by(username='张三')
    for customer in customers:
        print(customer.username)

    return '数据查找成功'

@app.route('/customer/update')
def update_customer():
    customer = Customer.query.filter_by(username='张三').first()
    customer.password = '654321'
    db.session.commit()
    print(f'id={customer.id},username={customer.username},password={customer.password},email={customer.email}')
    return '修改密码成功'

@app.route('/customer/delete')
def delete_customer():
    customer = Customer.query.filter_by(username='张三').first()
    db.session.delete(customer)
    db.session.commit()
    return '删除成功'





if __name__ == '__main__':
    app.run()
