# 饼状图的模板说明
| 参数            | 类型                            | 作用                                             |
|---------------|-------------------------------|------------------------------------------------|
| title         | str                           | 图幅名字                                           |
| theme         | int                           | 图幅主题，从0~7分别对应亮色、天蓝色、暗色、棕色、NCS蓝色、高对比度、冰蓝色主题Qt主题 |
| type          | int                           | 图类型，0~5分别表示竖向排列柱状图、竖向堆叠柱状图、竖向百分比柱状图、横向的对应三种    |
| value-visible | bool                          | 是否显示数据                                         |
| default-color | bool                          | 是否采用默认颜色，true的话，color设置失效                      |
| color         | str/list[str]                 | 图颜色                                            |
| categories    | str/list[str]                 | 图类名字                                           |
| bw            | float                         | 柱的宽度，取值范围0~1，建议0.5                             |
| format        | int                           | 在显示百分比情况下，百分比精确位数，非负整数                         |
| datas         | list[float]/list[list[float]] | 数据集合                                           |
| rorate        | int                           | 柱标签展示角度                                        |
| labels        | list[str]                     | 柱标签                                            |
| xlabel        | str                           | x轴标签                                           |
| ylabel        | str                           | y轴标签                                           |

## 模板案例
```json
{
  "title" : "柱状图名字",
  "theme" : 2,
  "type" : 0,
  "value-visible" : true,
  "default-color" : false,
  "color" : ["tan", "blue", "skyblue"],
  "categories" : ["A Type", "B Type", "C Type"],
  "bw" : 0.5,
  "datas" : [
    [5, 6, 4, 2, 1],
    [0, 2, 9, 6, 3],
    [3.5, 2.6, 4, 5, 2]
  ],
  "rorate" : 0,
  "labels" : ["January", "February", "March", "April", "May"],
  "xlabel" : "标签1",
  "ylabel" : "标签2"
}
```