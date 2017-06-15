# -*- coding:utf-8 -*-
# renthub restful api

from flask import Flask
from flask import request
from flask import jsonify
from flask import send_file
import sqlite3
import sys
import time

'''
==========  ===============================================  =============================
HTTP 方法   URL                                              动作
==========  ===============================================  ==============================
GET         http://[hostname]/todo/api/v1.0/tasks            检索任务列表
GET         http://[hostname]/todo/api/v1.0/tasks/[task_id]  检索某个任务
POST        http://[hostname]/todo/api/v1.0/tasks            创建新任务
PUT         http://[hostname]/todo/api/v1.0/tasks/[task_id]  更新任务
DELETE      http://[hostname]/todo/api/v1.0/tasks/[task_id]  删除任务
==========  ================================================ =============================
'''

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/')
def hello_world():
    return 'RentHub Restful API V1.0.'


@app.route('/9437DC9F2456E68DFB3DE48A17FFACE0.txt/')
def ssl_verify():
    return send_file('9437DC9F2456E68DFB3DE48A17FFACE0.txt')


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/api/sys/', methods=['GET'])
def get_sys():
    info = {}
    try:
        conn = sqlite3.connect('../rent-hub-py/results/db_hub.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM db_hub ORDER BY id DESC LIMIT 1')
        value = cursor.fetchone()
        info = {
            'update_time': value[1],
            'total_count': value[2],
            'update_count': value[3]
        }
    except Exception, e:
        print 'database error', e
    finally:
        cursor.close()

    return jsonify({'info': info})


@app.route('/api/recommended/', methods=['GET'])
def rmd_list():
    limit = request.args.get('limit')
    rmd_list = []
    try:
        conn = sqlite3.connect('../rent-hub-py/results/result_renthub.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, user, headimage, title, updatetime, coverimage, note FROM rent WHERE coverimage IS NOT NULL ORDER BY note DESC, updatetime DESC LIMIT ?',
                       [limit])
        values = cursor.fetchall()
        for row in values:
            d = {'id': row[0],
                 'user': row[1],
                 'headimage': row[2],
                 'title': row[3],
                 'updatetime': row[4],
                 'coverimage': row[5]
                 }
            rmd_list.append(d)
    except Exception, e:
        print 'database error', e
    finally:
        cursor.close()

    return jsonify({'rmd_list': rmd_list})


@app.route('/api/search/all/', methods=['GET'])
def search_all():
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    sort_arg = request.args.get('sort')
    keyword = request.args.get('keyword').strip()

    topic_list = []
    total_count = 0

    if sort_arg == '1':
        sort = 'posttime'
    elif sort_arg == '2':
        sort = 'note'
    else:
        sort = 'updatetime'

    try:
        conn = sqlite3.connect('../rent-hub-py/results/result_renthub.sqlite')
        cursor = conn.cursor()
        sql = "SELECT id, user, headimage, title, updatetime, coverimage FROM rent WHERE title LIKE '%" + keyword \
              + "%' ORDER BY " + sort +" DESC LIMIT ?,?"
        print sql
        cursor.execute(sql, [offset, limit])
        values = cursor.fetchall()
        cursor.close()
        for row in values:
            d = {'id': row[0],
                 'user': row[1],
                 'headimage': row[2],
                 'title': row[3],
                 'updatetime': row[4],
                 'coverimage': row[5]
                 }
            topic_list.append(d)
        cursor = conn.cursor()
        sql = "SELECT * FROM rent WHERE title LIKE '%" + keyword + "%'"
        cursor.execute(sql)
        values = cursor.fetchall()
        total_count = len(values)
    except Exception, e:
        print 'database error', e
    finally:
        cursor.close()

    return jsonify({'topic_list': topic_list, 'total_count': total_count})


@app.route('/api/search/', methods=['GET'])
def search():
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    city = request.args.get('city')
    sort_arg = request.args.get('sort')
    keyword = request.args.get('keyword')

    topic_list = []
    total_count = 0

    if sort_arg == '1':
        sort = 'posttime'
    elif sort_arg == '2':
        sort = 'note'
    else:
        sort = 'updatetime'

    try:
        conn = sqlite3.connect('../rent-hub-py/results/result_renthub.sqlite')
        cursor = conn.cursor()
        sql = "SELECT id, user, headimage, title, updatetime, coverimage FROM rent WHERE city=? and title LIKE '%" \
              + keyword + "%' ORDER BY " + sort + " DESC LIMIT ?,?"
        cursor.execute(sql, [city, offset, limit])
        values = cursor.fetchall()
        cursor.close()
        for row in values:
            d = {'id': row[0],
                 'user': row[1],
                 'headimage': row[2],
                 'title': row[3],
                 'updatetime': row[4],
                 'coverimage': row[5]
                 }
            topic_list.append(d)
        cursor = conn.cursor()
        sql = "SELECT * FROM rent WHERE city=? and title LIKE '%" + keyword + "%'"
        cursor.execute(sql, [city])
        values = cursor.fetchall()
        total_count = len(values)
    except Exception, e:
        print 'database error', e
    finally:
        cursor.close()

    return jsonify({'topic_list': topic_list, 'total_count': total_count})


@app.route('/api/lists/all/', methods=['GET'])
def list_all():
    topic_list = []
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    sort_arg = request.args.get('sort')
    if sort_arg == '1':
        sort = 'posttime'
    elif sort_arg == '2':
        sort = 'note'
    else:
        sort = 'updatetime'
    try:
        conn = sqlite3.connect('../rent-hub-py/results/result_renthub.sqlite')
        cursor = conn.cursor()
        sql = 'SELECT id, user, headimage, title, updatetime, coverimage FROM rent ORDER BY ' + sort +' DESC LIMIT ?,?'
        cursor.execute(sql, [offset, limit])
        values = cursor.fetchall()
        for row in values:
            d = {'id': row[0],
                 'user': row[1],
                 'headimage': row[2],
                 'title': row[3],
                 'updatetime': row[4],
                 'coverimage': row[5]
                 }
            topic_list.append(d)
    except Exception, e:
        print 'database error', e
    finally:
        cursor.close()

    return jsonify({'topic_list': topic_list})



@app.route('/api/lists/', methods=['GET'])
def list():
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    city = request.args.get('city')
    sort_arg = request.args.get('sort')
    topic_list = []

    if sort_arg == '1':
        sort = 'posttime'
    elif sort_arg == '2':
        sort = 'note'
    else:
        sort = 'updatetime'

    try:
        conn = sqlite3.connect('../rent-hub-py/results/result_renthub.sqlite')
        cursor = conn.cursor()
        sql = "SELECT id, user, headimage, title, updatetime, coverimage FROM rent WHERE city= ? ORDER BY " + sort + " DESC LIMIT ?, ?"
        cursor.execute(sql, [city, offset, limit])
        values = cursor.fetchall()
        for row in values:
            d = {'id': row[0],
                 'user': row[1],
                 'headimage': row[2],
                 'title': row[3],
                 'updatetime': row[4],
                 'coverimage': row[5]
                 }
            topic_list.append(d)
    except Exception, e:
        print 'database error', e
    finally:
        cursor.close()

    return jsonify({'topic_list': topic_list})


@app.route('/api/detail/<topic_id>/', methods=['GET'])
def detail(topic_id):
    detail = {}
    try:
        conn = sqlite3.connect('../rent-hub-py/results/result_renthub.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM rent WHERE id=?', [topic_id])
        value = cursor.fetchone()
        str_value = value[4].encode('utf-8', errors='strict')
        detail = {'id': value[0],
                  'user': value[1],
                  'headimage': value[2],
                  'title': value[3],
                  'content': str_value,
                  'posttime': value[6],
                  'updatetime': value[7],
                  'source': value[9],
                  'note': value[10] if value[10] != None else 0
                  }
    except Exception, e:
        print 'database error', e
        return
    finally:
        cursor.close()

    return jsonify({'detail': detail})


if __name__ == '__main__':
    app.run(debug=True)
