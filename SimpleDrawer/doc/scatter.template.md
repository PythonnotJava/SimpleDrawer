# 散点图的模板说明
| 参数 | 类型        | 作用                     
|----|-----------|------------------------|
|   title | str       | 图幅名字                   |
|   theme | int       | 图幅主题，具体支持见theme说明      |
|   polar | bool      | true的时候是极坐标图，反之是直角坐标系图 |
|   shape | list[str] | 散点形状                   |
|  size  |           |                        |
|  color  |           |                        |
|   categories |           |                        |
|   xs |           |                        |
|    ys|           |                        |
|  xrange  |           |                        |
|  yrange  |           |                        |
|  xlabel |           |                        |
|   ylabel |           |                        |


## 模板案例
```json
{
  "title" : "散点图名字",
  "theme" : 2,
  "polar" : false,
  "shape" : ["c", "r", "r"],
  "size" : [20, 20, 30],
  "color" : ["red", "blue", "grey"],
  "categories" : ["A Type", "B Type", "C Type"],
  "xs" : [
    [1, 2, 3, 4],
    [0.5, 0.7, 1.2, 4],
    [0.5, 0.7, 1.2, 4]
  ],
  "ys" : [
    [3, 4, 5, 6],
    [1, 3, 7, 3],
    [0, 3, 2, 6]
  ],
  "xrange" : [-5, 10],
  "yrange" : [-2, 10],
  "xlabel" : "标签1",
  "ylabel" : "标签2"
}```