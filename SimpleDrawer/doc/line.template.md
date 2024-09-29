# 线性图的模板说明
| 参数         | 类型                            | 作用                                             |
|------------|-------------------------------|------------------------------------------------|
| title      | str                           | 图幅名字                                           |
| theme      | int                           | 图幅主题，从0~7分别对应亮色、天蓝色、暗色、棕色、NCS蓝色、高对比度、冰蓝色主题Qt主题 |
| type       | int/list[int]                 | 线型图类别，0表示折线图，1表示曲线图                            |
| polar      | bool                          | true的时候是极坐标图，反之是直角坐标系图                         |
| color      | str/list[str]                 | 图颜色                                            |
| categories | str/list[str]                 | 图类名字                                           |
| lw         | int/list[int]                 | 对应线宽                                           |
| xs         | list[float]/list[list[float]] | x坐标集合                                          |
| ys         | list[float]/list[list[float]] | y坐标集合                                          |
| xrange     | list[int] and len == 2        | x轴显示范围                                         |
| yrange     | list[int] and len == 2        | y轴显示范围                                         |
| xlabel     | str                           | x轴标签                                           |
| ylabel     | str                           | y轴标签                                           |


## 模板案例
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