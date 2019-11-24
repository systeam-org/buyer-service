import mysql.connector
import os
from stompest.config import StompConfig
from stompest.sync import Stomp
from stompest.protocol import StompSpec
import socket

cnx = None

def get_connection():
    global cnx

    if not cnx:
        cnx = mysql.connector.connect(user = 'root', password='Admin@123', host='localhost', database = 'systeam_ecommerce',
                              auth_plugin='mysql_native_password')
        cnx.autocommit = True
    return cnx

def get_categories():
    cursor = get_connection().cursor()
    cursor.execute("SELECT category_name FROM category")
    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append(row[0])
    return result


def get_products(category):
    cursor = get_connection().cursor()

    if category:
        cursor.execute("SELECT * FROM products where category_name = '" + category + "'")
    else:
        cursor.execute("SELECT * FROM products")

    rows = cursor.fetchall()

    result = []
    for row in rows:
        product = {}
        product['product_id'] = row[0]
        product['category_name'] = row[1]
        product['product_name'] = row[3]
        product['description'] = row[4]
        product['price'] = row[5]
        product['image'] = row[7]
        result.append(product)
    return result



def place_order(body):
    conn= get_connection()
    cursor = conn.cursor()

    sql = "Insert into orders (total_amount, created_on, status, email)  values (%s, %s,%s,%s )"
    values = (body['total_amount'], body['created_on'], 'Ordered', body['email'])
    rows = cursor.execute(sql, values)

    order_id = cursor.lastrowid

    for row in body['products']:
        sql = "Insert into order_details (product_id, order_id, product_name, quantity, unit_cost)  values (%s, %s, %s, %s, %s)"
        values = (row['product_id'], order_id, row['product_name'], row['quantity'], row['unit_cost'])
        rows = cursor.execute(sql, values)

    conn.commit()

    queue = '/queue/ordered'
    amq_conf = None
    if isOpen('activemq.default', 61612):
        amq_conf = StompConfig('tcp://activemq.default:61612')
    else:
        amq_conf = StompConfig('tcp://localhost:30012')
    try:
        client = Stomp(amq_conf)
        client.connect()
        client.send(queue, str(order_id).encode())
        client.disconnect()
    except:
        print("something went wrong")

    return {'order_id': order_id}


def isOpen(dns,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((dns, int(port)))
      s.shutdown(2)
      return True
   except:
      return False

def get_orders(email):

    cursor = get_connection().cursor()

    cursor.execute("SELECT * FROM orders join order_details on orders.order_id = order_details.order_id where orders.email = '" + email + "'")

    rows = cursor.fetchall()

    processed_orders =[]
    result = []
    for row in rows:
        order_id = row[0]
        if order_id not in processed_orders:
            order = {'order_id': order_id}
            order['total_amount'] = row[1]
            order['created_on'] = str(row[2])
            order['status'] = row[3]
            order['products'] = []
            result.append(order)
            processed_orders.append(order_id)

    for row in rows:
        order_id = row[0]
        product = {}
        product['product_name'] = row[8]
        product['product_id'] = row[6]
        product['quantity'] = row[9]
        product['unit_cost'] = row[10]

        for i in range(len(result)):
            if result[i]['order_id'] == order_id:
                result[i]['products'].append(product)
    return result


def get_user(email):
    cursor = get_connection().cursor()
    cursor.execute("SELECT role FROM users where email = '"+email+"'")
    rows = cursor.fetchall()

    if len(rows) < 1:
        return None
    else:
        return {'role': rows[0][0]}

def add_or_update_user(body):

    current_role = get_user(body['email'])

    if current_role:
        current_role = current_role['role']
    conn= get_connection()
    cursor = conn.cursor()

    if not current_role:
        sql = "Insert into users (first_name, last_name, email, token, role)  values (%s, %s,%s, %s,%s)"
        values = (body['first_name'], body['last_name'],  body['email'], body['token'], 'Buyer')
        rows = cursor.execute(sql, values)
    elif current_role == 'Seller':
        sql = "Update users SET role = 'Buyer-Seller' , token = '" + body['token'] +"' where email = '" +body['email']+ "'"
        rows = cursor.execute(sql)
    elif current_role == 'Buyer' or current_role == 'Buyer-Seller':
        sql = "Update users SET token = '" + body['token'] +"' where email = '" +body['email']+ "'"
        rows = cursor.execute(sql)

    conn.commit()

    return True