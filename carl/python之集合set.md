### 集合set
集合是一个无序不重复元素的集。  
#### 创建空集合
```
s=set()  
s1=set([]) #列表
s2=set(()) #元祖
s3=set({}) #字典
```
#### 创建非空集合
```
s1=set([1, 2, 3, 4])
s3=set({"a":2, "b":3,"c":4})
```
**注**：字典转set集合，需要注意的是，只取了字典的key。  
### 集合的操作
#### 集合添加
集合的添加有两种方式，分别是**add**和**update**。但是他们在添加元素时是有区别的:  
* add()方法  
  把要传入的元素作为一个整体添加到集合中,如：  
```
s=set()
s.add("carl")
set(["carl"])
```
* update()方法  
  把要传入的元素拆分成单个字符，存于集合中，并去掉重复的字符。  
```
s=set()
s.update("carl")
set(["c", "a", "r", "l"])
```
#### 集合删除
**remove**:如果存在则删除，不存在则报错
```
s=set("one")
s.remove("e")
```
**discard**:如果存在则删除，不存在则什么都不做
```
s = set("one")
s.discard("e")
```
**pop**:随机删除一个元素，如果是空集合会引发`KeyError`错误  
**clear**:清空集合中所有元素
### 集合的其他方法
| 函数 | 说明 |
| :----: | :----: |
| len(s) | set的长度 |
| x in s | 测试x是否是s的成员 |
| x not in s | 测试x是否不是s的成员 |
| s.issubset(t) | 测试是否s中的每一个元素都在t中 |
| s.issuperset(t) | 测试是否t中的每一个元素都在s中 |
| s.union(t) | 返回一个新的set包含s和t中的每一个元素 |
| s.intersection(t) | 返回一个新的set包含s和t中的公共元素 |
| s.difference(t) | 返回一个新的set包含s中有但是t中没有的元素 |
| s.symmetric_difference(t) | 返回一个新的set包含s和t中不重复的元素 |
| s.copy() | 返回一个set"s"的一个浅复制 |
