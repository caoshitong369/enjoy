### 需求

#### 1.添加抵押币种

#### 2.编辑抵押币种

#### 技术总结：

`__getitem__` 返回键对应的值  

**example**

```
coin_list = MarketCoin().get_coin_name("code_id")
coin_list.sort(key=lambda e: e.__getitem__("coin_code"))
```

#### request.values

```
request.values.get("id", "") # 根据name为id获取参数，参数为单个的时候使用。
request.values.getlist("id", "") # 根据name为id获取参数参数为多个的时候可以使用并且是iterable。
request.values.lists() # 把前端传过来的name和value组合成元祖的形式[("a",[1, 2]),("b",[3,4])]。
request.values.to_dict()  #把前端传过来的name和value，按照字典的形式组合，如果key相同覆盖。
```

#### 前段实现 +添加 -删除

```
          <div class="row cl" id="userMetaRows">
                <label class="form-label col-xs-4 col-sm-2"><span class="c-red">*</span>借款周期：</label>
                <div class="formControls col-xs-8 col-sm-9">
                    <input type="text" value="" name="day"
                           placeholder="天" style="height: 27px">&emsp;<input type="text" value="" name="day_rate"
                                                                             placeholder="日利率‰(千分）"
                                                                             style="height: 27px">
                    <input class="btn btn-success" type="button" value="+" onclick="addMetaRow()"/>
                </div>
            </div>
```

```
            function addMetaRow() {
                        var div = document.getElementById("userMetaRows");
                        var label = document.createElement("label");
                        var br = document.createElement("br");
                        label.className = "form-label col-xs-4 col-sm-2";
                        label.innerHTML = "借款周期：";
                        var div1 = document.createElement("div");
                        div1.className = "formControls col-xs-8 col-sm-9";
                        div1.innerHTML = '<input type="text" value="" name="day" placeholder="天" style="height: 27px">&emsp;<input type="text" value="" name="day_rate" placeholder="日利率‰(千分）" style="height: 27px"> <input class="btn btn-success" type="button" value="+" onclick="addMetaRow()"/>&emsp;<input class="btn btn-danger" type="button" value="-" onclick="subMetaRow(this)"/></td>';
                        div.appendChild(br);
                        div.appendChild(label);
                        div.appendChild(div1)
            
                    }
            
                    function subMetaRow(button) {
                        var row = $(button).parent();
                        var row1 = $(row).prev();
                        var row2 = $(row1).prev();
                        $(row).remove();
                        $(row1).remove();
                        $(row2).remove()
                    }
```

#### dict

`dict()` # 空字典 {}  

`dict(a="a", b="b", t="t")` # 传入关键字 {'a': 'a', 'b': 'b', 't': 't'}  

`dict(zip(["one", "two", "three"], [1,2,3])` # 映射函数方式来构造字典{'three': 3, 'two': 2, 'one': 1}  

`dict([('one', 1),("two", 2),("three", 3)])` # 可迭代对象方式来构造字典 {"three":3, "two":2,"one":1}

