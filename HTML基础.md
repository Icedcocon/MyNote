### DOCTYPE 声明

- HTML 文件必须加上 DOCTYPE 声明，并统一使用 HTML5 的文档声明：

```html
<!DOCTYPE HTML>
```

### meta 标签

- 统一使用 “UTF-8” 编码

```html
<meta charset="utf-8">
```

- SEO 优化

```html
<!-- 页面关键词 -->
<meta name ="keywords" content =""/>
<!-- 页面描述 -->
<meta name ="description" content ="">
<!-- 网页作者 -->
<meta name ="author" content ="">
```

- 优先使用 IE 最新版本和 Chrome

```html
<meta http-equiv ="X-UA-Compatible" content ="IE = edge,chrome = 1">
```

- 为移动设备添加视口

```html
<!-- device-width 是指这个设备最理想的 viewport 宽度 -->
<!-- initial-scale=1.0 是指初始化的时候缩放大小是1，也就是不缩放 -->
<!-- user-scalable=0 是指禁止用户进行缩放 -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
```

- 禁止自动识别页面中有可能是电话格式的数字

```html
<meta name="format-detection" content="telephone=no">
```

```html

```
