### python对时间的操作

#### datetime的操作

```
import datetime
# 当前日期时间
print(datetime.datetime.now())
# 2019-08-10 09:42:10.951399

# 格式化时间
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

# 多加一天
print(datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

# fromtimestamp(t):使用时间戳构造对象
datetime.date.fromtimestamp(1231312421)
# 2009-01-07

# today():使用今天的日期构造对象
datetime.date.today()
# 2019-08-10

# fromordinal(n):使用日期叙述构造对象
datetime.date.fromordinal(1231)
# 0004-05-15 传入参数为一个整数序数，代表从公元1年1月1日开始的序数，序数每增加1代表增加1天，返回最终计算出的日期。
```