# _*_ coding:utf-8 _*_
# 导入相关模块


# 连接数据库 localhost是你的IP address
import json
import datetime
import threading
import requests
from pymongo import MongoClient, InsertOne
from bson import ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        return json.JSONEncoder.default(self, o)

def my_job():
    lists= []
    listss= []
    jiefangList = []
    sichuanList = []
    client = MongoClient('localhost', 27017)
    print(client)  # 成功则说明连接成功
    # 用户验证 连接mydb数据库,账号密码认证
    db = client.article  # 连接对应的数据库名称，系统默认数据库admin

    #db.authenticate('root', '你的密码password')

    # 连接所用集合，也就是我们通常所说的表
    collection = db.article_list_kuaizixun
    collectionList = db.article_list
    collectionjiefang = db.article_list_jiefang
    collectionsichuan = db.article_list_sichuan
    import json
    # 读取数据
    try:
        datas =(list(collection.find({"push_state":0},{"push_state":0,"only_id":0})))
        datasList = (list(collectionList.find({"push_state": 0}, {"push_state": 0, "only_id": 0})))
        datasjiefang = (list(collectionjiefang.find({"push_state": 0}, {"push_state": 0, "only_id": 0})))
        datassichuan = (list(collectionsichuan.find({"push_state": 0}, {"push_state": 0, "only_id": 0})))
        # data = pd.DataFrame(list(collection.find({"push_state":1},{"push_state":0,"only_id":0})))
        for line in datas:
            lists.append(line)
        for line in datasList:
            listss.append(line)
        for line in datasjiefang:
            jiefangList.append(line)
        for line in datassichuan:
            sichuanList.append(line)

        url = 'http://218.94.77.147:18080/api/kafka'

        data={
            "topic":"topic-wemedia",
            "list":lists,
        }
        dataList = {
            "topic": "topic-wemedia",
            "list": listss,
        }
        jiefangdata = {
            "topic": "topic-wemedia",
            "list": jiefangList,
        }
        sichuandata = {
            "topic": "topic-wemedia",
            "list": sichuanList,
        }
        requests.post(url, data = json.dumps(data,cls=JSONEncoder),stream=True)
        requests.post(url, data=json.dumps(dataList, cls=JSONEncoder), stream=True)
        requests.post(url, data=json.dumps(jiefangdata, cls=JSONEncoder), stream=True)
        requests.post(url, data=json.dumps(sichuandata, cls=JSONEncoder), stream=True)
        id = []
        idList = []
        jiefangId = []
        sichuanId = []
        for key in datas:
            id.append(key['_id'])

        for keys in datasList:
            idList.append(keys['_id'])

        for keyss in datasjiefang:
            jiefangId.append(keyss['_id'])

        for sichuaKey in datassichuan:
            sichuanId.append(sichuaKey['_id'])







        for i in id:
            db.article_list_kuaizixun.update_one({"_id":ObjectId(i)}, {'$set':{"push_state":1}})

        for i in idList:
            db.article_list.update_one({"_id": ObjectId(i)}, {'$set': {"push_state": 1}})

        for i in jiefangId:
            db.article_list_jiefang.update_one({"_id": ObjectId(i)}, {'$set': {"push_state": 1}})

        for i in sichuanId:
            db.article_list_sichuan.update_one({"_id": ObjectId(i)}, {'$set': {"push_state": 1}})


            #db.colleciton.update_many({查询条件},{$修改器:{修改值}})
            # print(results.text)
            # print(results.status_code)
            #关闭连接
        client.close()

    except Exception as err:
        import traceback
        traceback.print_exc()
        pass


def func():
  # 每2s执行一次
  my_job()
  threading.Timer(2, func).start()


if __name__ == "__main__":
  a = {'x': 1}
  func()