# -*- coding:utf-8 -*-
# renthub restful api

from flask import Flask, jsonify
from flask import request
import sqlite3

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
    return 'Hello World!'


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/api/lists/', methods=['GET'])
def get_list():
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    topic_list = []
    try:
        conn = sqlite3.connect('database/result_20170521_204824.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT id, user, headimage, title, posttime FROM rent ORDER BY id ASC limit ?, ?',
                       [offset, limit])
        values = cursor.fetchall()
        for row in values:
            d = {'id': row[0],
                 'user': row[1],
                 'headimage': row[2],
                 'title': row[3],
                 'posttime': row[4]
                 }
            topic_list.append(d)
    except Exception, e:
        print 'database error', e
        return
    finally:
        cursor.close()
    return jsonify({'topic_list': topic_list})


@app.route('/api/detail/<topic_id>/', methods=['GET'])
def get_detail(topic_id):
    detail = {}
    try:
        conn = sqlite3.connect('database/result_20170521_204824.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM rent WHERE id=?', topic_id)
        value = cursor.fetchone()
        detail = {'id': value[0],
                  'user': value[1],
                  'headimage': value[2],
                  'title': value[3],
                  'content': value[4],
                  'posttime': value[6]
                  }

    except Exception, e:
        print 'database error', e
        return
    finally:
        cursor.close()

    return jsonify({'detail': detail})


if __name__ == '__main__':
    app.run(debug=True)
