# 目录

[toc]

# 技术总结

## flask操作原生数据库  

### 用到的包

`from sqlalchemy.ext.declarative import declarative_base`  

`from sqlalchemy import (MetaData, create_engine)`  

`from sqlalchemy.orm import sessionmaker`  

`from contextlib import contextmanager`  

### 详细介绍

#### 利用contextlib创建一个上下文管理器  

```python
from contextlib import contextmanager

@contextmanager
def file_open(path):
    try:
        f_obj = open(path, "w")
        yield f_obj
    except OSError:
        print("We had an error!")
    finally:
        print("Closing file")
        f_obj.close()

if __name__ == "__main__":
    with file_open("test/test.txt") as fobj:
        fobj.write("Testing context managers")
```

在这里，我们从contextlib模块中引入contextmanager，然后装饰我们所定义的file_open函数。这就允许我们使用Python的with语句来调用file_open函数。在函数中，我们打开文件，然后通过yield，将其传递出去，最终主调函数可以使用它。

一旦with语句结束，控制就会返回给file_open函数，它继续执行yield语句后面的代码。这个最终会执行finally语句--关闭文件。如果我们在打开文件时遇到了OSError错误，它就会被捕获，最终finally语句依然会关闭文件句柄。  

#### 原生sql语句组合

根据幸运值进行排名
```
        select uid,score,arrive_time,(select count(uid) from super_lotto_dk_bet_with_rank_num as lotto where lotto.uid=T.uid group by uid) as num,rank from (select uid,score,status,arrive_time,create_time,RANK() OVER(order by score desc) as rank from super_lotto_dk_bet_with_rank_num) as T
```

原生sql语句组合（sql语句+where语句+order by语句+limit语句)

```
        select_sql = 'select uid,score,arrive_time,(select count(uid) from super_lotto_dk_bet_with_rank_num as lotto where lotto.uid=T.uid group by uid) as num,rank from (select uid,score,status,arrive_time,create_time,RANK() OVER(order by score desc) as rank from super_lotto_dk_bet_with_rank_num) as T'
        where = []
        where_sql = ''
        if uid:
            where.append("uid={}".format(uid))
        if start_time:
            where.append("create_time > {}".format(start_time_stamp))
        if end_time:
            where.append("arrive_time < {}".format(end_time_stamp))
        if where:
            where_sql = "WHERE " + ' AND '.join(where)
        query_sql = ''.join([select_sql, where_sql, limit_sql])
```  

#### 连接数据库及发送sql语句

```
db_engine_activity = create_engine('postgresql://wumingshun:qhvce0813@127.0.0.1:5432/activity',encoding='utf-8',convert_unicode=True,pool_recycle=60 * 5,pool_size=5,echo=False)
ActivityBase = declarative_base(bind=db_engine_activity)
ActivityMetaData = MetaData(bind=db_engine_activity)
activity_session = sessionmaker(bind=db_engine_activity,expire_on_commit=False)
```

```
@contextmanager
def create_activity_session(): # 使用上下文管理器的方式，解决出现异常及关闭问题
ps = activity_session()
try:
    yield ps
except Exception as e:
    logging.error('数据库错误,回退:{}'.format(e))
    ps.rollback() # 出现异常
    raise e 
finally:
    ps.close()
    
@contextmanager
def create_activity_conn():
    conn = db_engine_activity.connect()
    try:
        yield conn
    except Exception as e:
        logging.error('数据库错误: {}'.format(e))
        raise e
    finally:
        conn.close()
        
def query_dk_lotto(query_sql):
    with_activity_conn() as conn:
        rt = conn.excute(query_sql)
        res = rt.fetchall()
        return res
```

### flask 利用ORM操作数据库

```
db_engine = create_engine('postgresql://wumingshun:qhvce0813@127.0.0.1:5432/activity',encoding='utf-8',convert_unicode=True,pool_recycle=60 * 5,pool_size=5,echo=False)
QHealthBase = declarative_base(bind=db_engine)
session = sessionmaker(bind=db_engine,expire_on_commit=False)
metadata = MetaData(bind=db_engine)

class CoinDayCount(QHealthBase):
    # 如果是数据库已经把表创建好了利用autoload=True可以转化为orm语句
    __table__ = Table("coin_day_count",metadata,autoload=True)
    
    # 如果数据库没有创建表可以利用orm进行创建
    user_table = Table('user',metadata,
    Column('id', Interger, primary_key=True)

metadata.create_all()
    
```