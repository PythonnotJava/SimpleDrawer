# 拖拽式显示模板

只需要在模板中声明class属性，class属性有以下取值：bar、line、scatter、pie之一，就能自动转换

### 例子——线型图拖拽

```json
{
  "title" : "折线图名字",
  "theme" : 2,
  "polar" : true,
  "type" : [0, 1],
  "color" : ["red", "blue"],
  "categories" : ["A Type", "B Type"],
  "lw" : [10, 5],
  "xs" : [
    [1, 2, 3, 4.5],
    [0.5, 1.5, 2.5, 3.5, 4.5]
  ],
  "ys" : [
    [3, 4, 5, 10],
    [1, 3, 7, 3, 0, 6]
  ],
  "xrange" : [-5, 10],
  "yrange" : [-2, 10],
  "xlabel" : "标签1",
  "ylabel" : "标签2"
}
```

### 修改后

```json
{
  "class" : "line",
  "title" : "折线图名字",
  "theme" : 2,
  "polar" : true,
  "type" : [0, 1],
  "color" : ["red", "blue"],
  "categories" : ["A Type", "B Type"],
  "lw" : [10, 5],
  "xs" : [
    [1, 2, 3, 4.5],
    [0.5, 1.5, 2.5, 3.5, 4.5]
  ],
  "ys" : [
    [3, 4, 5, 10],
    [1, 3, 7, 3, 0, 6]
  ],
  "xrange" : [-5, 10],
  "yrange" : [-2, 10],
  "xlabel" : "标签1",
  "ylabel" : "标签2"
}
```
