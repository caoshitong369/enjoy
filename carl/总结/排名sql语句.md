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