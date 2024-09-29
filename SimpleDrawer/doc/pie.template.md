# 饼状图的模板说明
| 参数                    | 类型            | 作用                                             |
|-----------------------|---------------|------------------------------------------------|
| title                 | str           | 图幅名字                                           |
| theme                 | int           | 图幅主题，从0~7分别对应亮色、天蓝色、暗色、棕色、NCS蓝色、高对比度、冰蓝色主题Qt主题 |
| default-color         | bool          | 是否采用默认颜色，true的话，color设置失效                      |
| color                 | str/list[str] | 图颜色                                            |
| categories            | str/list[str] | 图类名字                                           |
| hole                  | float         | 饼洞大小，取值0~1，0表示无洞                               |
| format                | int           | 在显示百分比情况下，百分比精确位数，非负整数                         |
| datas                 | list[float]   | 数据集合                                           |
| label-visible         | bool          | 名字是否可见                                         |
| datas-visible         | bool          | 是否显示数据                                         |
| use-percentage        | bool          | 数据可见前提下，是否采用占比模式显示                             |

## 模板案例
```json
{
  "title" : "饼状图名字",
  "theme" : 0,
  "default-color" : false,
  "color" : ["red", "blue", "yellow", "tan", "darkcyan"],
  "categories" : ["Python", "C", "Dart", "Golang", "C++"],
  "hole" : 0,
  "format" : 2,
  "datas" : [43.6, 22.5, 16.23, 7.8, 33.9],
  "label-visible" : true,
  "datas-visible" : true,
  "use-percentage" : true
}
```