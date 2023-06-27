## Context

`Context` 是 `gin` 最重要的部分之一。它允许我们在中间件之间传递变量，管理流程，验证请求的 JSON 并返回 JSON 响应等。

```go
type Context struct {
    Request *http.Request
    Writer  ResponseWriter

    Params Params

    // Keys is a key/value pair exclusively for the context of each request.
    Keys map[string]any

    // Errors is a list of errors attached to all the handlers/middlewares who used this context.
    Errors errorMsgs

    // Accepted defines a list of manually accepted formats for content negotiation.
    Accepted []string
    // contains filtered or unexported fields
}
```

### 函数和方法

## CreateTestContextOnly

`func CreateTestContextOnly(w http.ResponseWriter, r *Engine) (c *Context)`

- 版本: v1.8.2
- 功能说明: 为了测试目的基于引擎返回新的上下文
- 参数说明:
  - w (http.ResponseWriter): HTTP响应处理
  - r (*Engine): Gin框架引擎
- 返回值说明: 返回一个新的上下文对象

## Abort

`func (c *Context) Abort()`

- 功能说明: 阻止调用挂起的处理程序, 但当前处理程序不会停止。例如，如果您有一个验证中间件来验证当前请求是否已授权, 如果授权失败 (例如，密码不匹配), 则调用 Abort 以确保不调用此请求的其余处理程序。

## AbortWithError

`func (c *Context) AbortWithError(code int, err error) *Error`

- 功能说明: AbortWithError 调用 `AbortWithStatus()` 和 `Error()`方法。此方法将停止链式调用, 回写状态码并将指定的错误推送到 Error 中。
- 参数说明:
  - code (int): HTTP状态码
  - err (error): 错误信息
- 返回值说明: 返回一个错误类型对象

## AbortWithStatus

`func (c *Context) AbortWithStatus(code int)`

- 功能说明: `AbortWithStatus` 调用 `Abort()` 并写入带有指定状态码的头。例如，未能验证请求的尝试失败可能会使用：`context.AbortWithStatus(401)`。

## AbortWithStatusJSON

`func (c *Context) AbortWithStatusJSON(code int, jsonObj any)`

- 版本: v1.3.0
- 功能说明: AbortWithStatusJSON 调用 `Abort()` ，并在内部调用 *JSON* 方法, 此方法将停止链式调用, 写入状态码并返回一个 JSON 主体。它还将 Content-Type 设置为" application/json"。
- 参数说明:
  - code (int): HTTP状态码
  - jsonObj (any): JSON数据对象

## AddParam

`func (c *Context) AddParam(key, value string)`

- 版本: v1.8.0
- 功能说明: 在上下文中添加参数，并用给定值替换路径参数键以进行端到端测试。 例如路由：'/user/:id'，调用：`AddParam("id"，1)`，结果为：'/user/1'。

## AsciiJSON

`func (c *Context) AsciiJSON(code int, obj any)`

- 版本: v1.3.0
- 功能说明: 将给定结构序列化为 JSON，并将其写入响应主体中。并且集内容类型"application/json"

### func (*Context) Bind

```go
func (c *Context) Bind(obj any) error 
```

方法将根据请求的方法和Content-Type来自动选择绑定引擎，具体采用哪种绑定将根据头字段"Content-Type"来决定，例如：

- "application/json" --> JSON绑定
- "application/xml" --> XML绑定

若Content-Type 为"application/json" 则会将请求主体解析为JSON，如果JSON输入不合法用JSON或XML解析将会出错，此时将会向响应写入400错误并设置"Content-Type"头为"text/plain"。

### func (*Context) BindHeader

```go
func (c *Context) BindHeader(obj any) error 
```

方法是 c.MustBindWith(obj, binding.Header) 的快捷方式。

### func (*Context) BindJSON

```go
func (c *Context) BindJSON(obj any) error 
```

方法是 c.MustBindWith(obj, binding.JSON) 的快捷方式。

### func (*Context) BindQuery

```go
func (c *Context) BindQuery(obj any) error 
```

方法是 c.MustBindWith(obj, binding.Query) 的快捷方式 。

### func (*Context) BindTOML

```go
func (c *Context) BindTOML(obj interface{}) error 
```

方法是 c.MustBindWith(obj, binding.TOML) 的快捷方式。

### func (*Context) BindUri

```go
func (c *Context) BindUri(obj any) error 
```

方法将根据 binding.Uri 将传递的结构指针绑定，如果发生任何错误，它将使用HTTP 400中止请求。

### func (*Context) BindWith

```go
func (c *Context) BindWith(obj any, b binding.Binding) error 
```

方法将使用指定的绑定引擎将传递的结构指针绑定。详见绑定包。

### func (*Context) BindXML

版本:v1.4.0

`func (c *Context) BindXML(obj any) error`

BindXML是`c.MustBindWith(obj, binding.BindXML)`的快捷方式。

### func (*Context) BindYAML

版本:v1.4.0

`func (c *Context) BindYAML(obj any) error`

BindYAML是`c.MustBindWith(obj, binding.YAML)`的快捷方式。

### func (*Context) ClientIP

`func (c *Context) ClientIP() string`

ClientIP实现了一种尽力而为的算法来返回真实的客户端IP。它调用`c.RemoteIP()`方法来检查远程IP是否是受信任的代理。如果是，则会尝试解析Engine.RemoteIPHeaders中定义的头文件（默认为[X-Forwarded-For，X-Real-Ip]）。如果头文件在语法上无效或者远程IP与受信任的代理不对应，则返回请求中的远程IP（来自Request.RemoteAddr）。

### func (*Context) ContentType

`func (c *Context) ContentType() string`

ContentType返回请求的Content-Type头信息。

### func (*Context) Cookie

`func (c *Context) Cookie(name string) (string, error)`

Cookie返回请求中提供的指定cookie的值，如果没有找到则返回ErrNoCookie。并返回未转义的命名cookie。如果多个cookie与给定名称匹配，则只返回一个cookie。

### func (*Context) Copy

`func (c *Context) Copy() *Context`

Copy返回当前上下文的副本，可以安全地在请求范围之外使用。当上下文必须传递给goroutine时，必须使用此方法。

### func (*Context) Data

`func (c *Context) Data(code int, contentType string, data []byte)`

Data将一些数据写入响应体流并更新HTTP状态码。

### func (*Context) DataFromReader

版本:v1.3.0

`func (c *Context) DataFromReader(code int, contentLength int64, contentType string, reader io.Reader, extraHeaders map[string]string)`

DataFromReader将指定的reader写入响应体流并更新HTTP状态码。

### func (*Context) Deadline

`func (c *Context) Deadline() (deadline time.Time, ok bool)`

Deadline返回当c.Request没有上下文时，没有截止日期（ok==false）。

### func (*Context) DefaultPostForm

`func (c *Context) DefaultPostForm(key, defaultValue string) string`

DefaultPostForm从POST urlencoded表单或多部分表单中获取指定的键名key的值，如果存在，则返回该值，否则返回指定的defaultValue字符串。有关详细信息，请参见：PostForm()和GetPostForm()。

### func (*Context) DefaultQuery

`func (c *Context) DefaultQuery(key, defaultValue string) string`

DefaultQuery返回指定键名的url查询值，如果存在，则返回该值，否则返回指定的defaultValue字符串。有关详细信息，请参见：Query()和GetQuery()。

例如：
GET /?name=Manu&lastname=
c.DefaultQuery("name", "unknown") == "Manu"
c.DefaultQuery("id", "none") == "none"
c.DefaultQuery("lastname", "none") == ""

### func (*Context) Done

`func (c *Context) Done() <-chan struct{}`

Done在c.Request没有上下文时返回nil（将永远等待的通道）。

### func (*Context) Err

`func (c *Context) Err() error`

Err在c.Request没有上下文时返回nil。

## Gin框架Context结构体的方法

### func (*Context) Error

`func (c *Context) Error(err error) *Error`

Error将错误附加到当前上下文。该错误被推送到错误列表中。最好对解析请求期间发生的每个错误调用Error。可以使用中间件来收集所有错误并将它们一起推送到数据库中、打印日志或将其附加在HTTP响应中。如果err为nil，则会引发panic。

### func (*Context) File

`func (c *Context) File(filepath string)`

File以高效的方式将指定的文件写入响应体流中。

### func (*Context) FileAttachment

版本:v1.4.0

`func (c *Context) FileAttachment(filepath, filename string)`

FileAttachment以高效的方式将指定的文件写入响应体流中。在客户端，该文件通常会带有给定的文件名进行下载。

### func (*Context) FileFromFS

版本:v1.6.0

`func (c *Context) FileFromFS(filepath string, fs http.FileSystem)`

FileFromFS以高效的方式将http.FileSystem中指定的文件写入响应体流中。

### func (*Context) FormFile

版本:v1.3.0

`func (c *Context) FormFile(name string) (*multipart.FileHeader, error)`

FormFile返回提供的表单键名的第一个文件。

### func (*Context) FullPath

版本:v1.5.0

`func (c *Context) FullPath() string`

FullPath返回匹配的路由完整路径。对于找不到的路由，返回空字符串。

例如：
router.GET("/user/:id", func(c *gin.Context) {
c.FullPath() == "/user/:id" // true
})

### func (*Context) Get

`func (c *Context) Get(key string) (value any, exists bool)`

Get返回给定键的值，即(value, true)。如果该值不存在，则返回(nil, false)。

### func (*Context) GetBool

版本:v1.3.0

`func (c *Context) GetBool(key string) (b bool)`

GetBool将与键关联的值作为布尔值返回。

### func (*Context) GetDuration

版本:v1.3.0

`func (c *Context) GetDuration(key string) (d time.Duration)`

GetDuration将与键关联的值作为持续时间返回。

### func (*Context) GetFloat64

版本:v1.3.0

`func (c *Context) GetFloat64(key string) (f64 float64)`

GetFloat64将与键关联的值作为float64返回。

### func (*Context) GetHeader

版本:v1.3.0

`func (c *Context) GetHeader(key string) string`

GetHeader从请求头中返回值。

### func (*Context) GetInt

版本:v1.3.0

`func (c *Context) GetInt(key string) (i int)`

GetInt将与键关联的值作为整数返回。

### func (*Context) GetInt64

版本:v1.3.0

`func (c *Context) GetInt64(key string) (i64 int64)`

GetInt64将与键关联的值作为整数返回。

### func (*Context) GetPostForm

`func (c *Context) GetPostForm(key string) (string, bool)`

GetPostForm类似于PostForm(key)。当POST urlencoded表单或多部分表单中存在该键时，它会返回指定的键名key的值`(value, true)`（即使该值为空字符串），否则返回("", false)。例如，在更新用户电子邮件的PATCH请求期间：

```
email=mail@example.com  -->  ("mail@example.com", true) := GetPostForm("email") // 将email设置为"mail@example.com"
   email=                  -->  ("", true) := GetPostForm("email") // 将email设置为空字符串""
                        -->  ("", false) := GetPostForm("email") // 不对email进行任何操作
```

### func (*Context) GetPostFormArray

`func (c *Context) GetPostFormArray(key string) (values []string, ok bool)`

GetPostFormArray返回给定表单键名的字符串切片，以及一个布尔值，用于指示是否至少存在一个给定键的值

### func (*Context) GetPostFormMap

版本:v1.3.0

`func (c *Context) GetPostFormMap(key string) (map[string]string, bool)`

GetPostFormMap返回给定表单键名的映射，以及一个布尔值，用于指示是否至少存在一个给定键的值。

### func (*Context) GetQuery

`func (c *Context) GetQuery(key string) (string, bool)`

GetQuery类似于Query()，如果它存在，则返回带有键名的url查询值`(value, true)`（即使该值为空字符串），否则返回`("", false)`。它是`c.Request.URL.Query().Get(key)`的快捷方式。

例如：
GET /?name=Manu&lastname=
("Manu", true) == c.GetQuery("name")
("", false) == c.GetQuery("id")
("", true) == c.GetQuery("lastname")

### func (*Context) GetQueryArray

`func (c *Context) GetQueryArray(key string) (values []string, ok bool)`

GetQueryArray返回给定查询键名的字符串切片，以及一个布尔值，用于指示是否至少存在一个给定键的值。

### func (*Context) GetQueryMap

版本:v1.3.0

`func (c *Context) GetQueryMap(key string) (map[string]string, bool)`

GetQueryMap返回给定查询键名的映射，以及一个布尔值，用于指示是否至少存在一个给定键的值。

### func (*Context) GetRawData

版本:v1.3.0

`func (c *Context) GetRawData() ([]byte, error)`

GetRawData返回流数据。

### func (*Context) GetString

版本:v1.3.0

`func (c *Context) GetString(key string) (s string)`

GetString将与键关联的值作为字符串返回。

## Context.GetStringMap

函数签名：`func (c *Context) GetStringMap(key string) (sm map[string]interface{})`

从键中返回与之关联的值作为接口映射。

## Context.GetStringMapString

函数签名：`func (c *Context) GetStringMapString(key string) (sms map[string]string)`

从键中返回与之关联的值作为字符串映射。

## Context.GetStringMapStringSlice

函数签名：`func (c *Context) GetStringMapStringSlice(key string) (smss map[string][]string)`

从键中返回与之关联的值作为字符串切片的映射。

## Context.GetStringSlice

函数签名：`func (c *Context) GetStringSlice(key string) (ss []string)`

从键中返回与之关联的值作为字符串切片。

## Context.GetTime

函数签名：`func (c *Context) GetTime(key string) (t time.Time)`

从键中返回与之关联的值作为时间。

## Context.GetUint

函数签名：`func (c *Context) GetUint(key string) (ui uint)`

从键中返回与之关联的值作为无符号整数。

## Context.GetUint64

函数签名：`func (c *Context) GetUint64(key string) (ui64 uint64)`

从键中返回与之关联的值作为无符号整数。

## Context.HTML

函数签名：`func (c *Context) HTML(code int, name string, obj interface{})`

HTML 根据模板文件名渲染 HTTP 模板。它还更新 HTTP 代码并将 Content-Type 设置为“text/html”。参见 http://golang.org/doc/articles/wiki/

## Context.Handler

函数签名：`func (c *Context) Handler() HandlerFunc`

Handler 返回主处理程序。

## Context.HandlerName

函数签名：`func (c *Context) HandlerName() string`

HandlerName 返回主处理程序的名称。例如，如果处理程序是“handleGetUsers()”，则此函数将返回“main.handleGetUsers”。

## Context.HandlerNames

函数签名：`func (c *Context) HandlerNames() []string`

HandlerNames 按降序返回此上下文中所有已注册处理程序的列表，遵循 HandlerName() 的语义。

## Context.Header

函数签名：`func (c *Context) Header(key, value string)`

Header 是 c.Writer.Header().Set(key, value) 的智能快捷方式。它在响应中写入标头。如果 value == ""，则此方法删除标头 c.Writer.Header().Del(key)。

## Context.IndentedJSON

函数签名：`func (c *Context) IndentedJSON(code int, obj interface{})`

IndentedJSON 将给定的结构体序列化为漂亮的 JSON（带缩进和换行符）并写入响应正文。它还将 Content-Type 设置为“application/json”。警告：我们建议仅出于开发目的使用此选项，因为打印漂亮的 JSON 更加耗费 CPU 和带宽。请改用 Context.JSON()。

## Context.IsAborted

函数签名：`func (c *Context) IsAborted() bool`

IsAborted 如果当前上下文已中止，则返回 true。

## Context.IsWebsocket

函数签名：`func (c *Context) IsWebsocket() bool`

如果请求标头指示客户端正在启动 websocket 握手，则 IsWebsocket 返回 true。

## Context.JSON

函数签名：`func (c *Context) JSON(code int, obj interface{})`

JSON 将给定结构体序列化为 JSON 并写入响应正文。它还将 Content-Type 设置为“application/json”。

## Context.JSONP

函数签名：`func (c *Context) JSONP(code int, obj interface{})`

JSONP 将给定的结构体序列化为 JSON 并写入响应正文。它向响应正文添加填充，以从与客户端不同域的服务器请求数据。它还将 Content-Type 设置为“application/javascript”。

## Context.MultipartForm

函数签名：`func (c *Context) MultipartForm() (*multipart.Form, error)`

MultipartForm 是解析后的多部分表单，包括文件上传。

## Context.MustBindWith

函数签名：`func (c *Context) MustBindWith(obj interface{}, b binding.Binding) error`

MustBindWith 使用指定的绑定引擎绑定传递的结构体指针。如果发生任何错误，它将使用 HTTP 400 中止请求。参见绑定包。

## Context.MustGet

函数签名：`func (c *Context) MustGet(key string) interface{}`

如果给定键的值存在，则 MustGet 返回该值，否则它会 panic。

## Context.Negotiate

函数签名：`func (c *Context) Negotiate(code int, config Negotiate)`

根据可接受的 Accept 格式调用不同的 Render。

## Context.NegotiateFormat

函数签名：`func (c *Context) NegotiateFormat(offered ...string) string`

NegotiateFormat 返回一个可接受的 Accept 格式。

## Context.Next

函数签名：`func (c *Context) Next()`

Next 应仅在中间件内部使用。它在调用处理程序内部执行链中的待处理程序。请参见 GitHub 中的示例。

## Context.Param

函数签名：`func (c *Context) Param(key string) string`

Param 返回 URL 参数的值。它是 c.Params.ByName(key) 的快捷方式。

router.GET("/user/:id", func(c *gin.Context) {
// 对 /user/john 的 GET 请求
id := c.Param("id") // id == "/john"
// 对 /user/john/ 的 GET 请求
id := c.Param("id") // id == "/john/"
})

## Context.PostForm

函数签名：`func (c *Context) PostForm(key string) string`

如果存在，则从 POST urlencoded 表单或多部分表单中返回指定键的值，否则返回空字符串("")。

## Context.PostFormArray

函数签名：`func (c *Context) PostFormArray(key string) []string`

对于给定的表单键，PostFormArray 返回一个字符串切片。切片的长度取决于具有给定键的参数数量。

## Context.PostFormMap

函数签名：`func (c *Context) PostFormMap(key string) map[string]string`

PostFormMap 返回给定表单键的映射。

## Context.ProtoBuf

函数签名：`func (c *Context) ProtoBuf(code int, obj interface{})`

ProtoBuf 将给定结构体序列化为 ProtoBuf 并写入响应正文。

## Context.PureJSON

函数签名：`func (c *Context) PureJSON(code int, obj interface{})`

PureJSON 将给定的结构体序列化为 JSON 并写入响应正文。与 JSON 不同，PureJSON 不会将特殊的 html 字符替换为它们的 Unicode 实体。

## Context.Query

函数签名：`func (c *Context) Query(key string) string`

如果存在，则返回键控 URL 查询值，否则返回空字符串("")。它是 c.Request.URL.Query().Get(key) 的快捷方式。

```
GET /path?id=1234&name=Manu&value=
   c.Query("id") == "1234"
   c.Query("name") == "Manu"
   c.Query("value") == ""
   c.Query("wtf") == ""
```

## Context.QueryArray

函数签名：`func (c *Context) QueryArray(key string) []string`

QueryArray 返回给定查询键的字符串切片。切片的长度取决于具有给定键的参数数量。

## Context.QueryMap

函数签名：`func (c *Context) QueryMap(key string) map[string]string`

QueryMap 返回给定查询键的映射。

## Context.Redirect

函数签名：`func (c *Context) Redirect(code int, location string)`

Redirect 返回到特定位置的 HTTP 重定向。

## Context.RemoteIP

函数签名：`func (c *Context) RemoteIP() string`

RemoteIP 从 Request.RemoteAddr 解析 IP，规范化并返回 IP（不带端口）。

## Context.Render

函数签名：`func (c *Context) Render(code int, r render.Render)`

Render 写入响应头并调用 render.Render 渲染数据。

## Context.SSEvent

函数签名：`func (c *Context) SSEvent(name string, message interface{})`

SSEvent 将 Server-Sent Event 写入正文流中。

## Context.SaveUploadedFile

函数签名：`func (c *Context) SaveUploadedFile(file *multipart.FileHeader, dst string) error`

SaveUploadedFile 将表单文件上传到指定的目标位置。

## Context.SecureJSON

函数签名：`func (c *Context) SecureJSON(code int, obj interface{})`

SecureJSON 将给定结构体序列化为 Secure JSON 并写入响应正文。默认情况下，如果给定结构体是数组值，则在响应正文前面添加“while(1),”。它还将 Content-Type 设置为“application/json”。

## func (*Context) Set

goCopy code

`func (c *Context) Set(key string, value any)`

- 功能：为该上下文存储一个新的键/值对。如果c.Keys未被使用过，则也会惰性地初始化它。
- 参数：key-键名，value-键值
- 返回值：无

## func (*Context) SetAccepted

goCopy code

`func (c *Context) SetAccepted(formats ...string)`

- 功能：设置Accept头数据。
- 参数：formats-格式列表
- 返回值：无

## func (*Context) SetCookie

goCopy code

`func (c *Context) SetCookie(name, value string, maxAge int, path, domain string, secure, httpOnly bool)`

- 功能：将一个Set-Cookie头添加到ResponseWriter的头部。提供的cookie必须有一个有效的名称。无效的cookie可能会被默默丢弃。
- 参数：
  - name-cookie的名称
  - value-cookie的值
  - maxAge-cookie的最大有效时间
  - path-限制cookie的路径
  - domain-cookie所属域
  - secure-指定是否通过HTTPS传输cookie
  - httpOnly-指定cookie是否只能由HTTP访问
- 返回值：无

## func (*Context) SetSameSite

goCopy code

`func (c *Context) SetSameSite(samesite http.SameSite)`

- 功能：设置cookie的SameSite属性。
- 参数：samesite-SameSite属性值
- 返回值：无

## func (*Context) ShouldBind

goCopy code

`func (c *Context) ShouldBind(obj any) error`

- 功能：根据Method和Content-Type选择一个绑定引擎来自动绑定。根据"Content-Type"头不同，会使用不同的绑定方式，例如：
  - "application/json" --> JSON绑定
  - "application/xml" --> XML绑定
- 参数：obj-目标结构体指针
- 返回值：error类型，绑定成功返回nil，否则返回错误信息。与c.Bind()不同，该方法不会在输入无效时设置响应状态代码为400或中止。

## func (*Context) ShouldBindBodyWith

goCopy code

`func (c *Context) ShouldBindBodyWith(obj any, bb binding.BindingBody) (err error)`

- 功能：类似于ShouldBindWith，但将请求体存储到上下文中，并在下一次调用时重用。
- 参数：
  - obj-目标结构体指针
  - bb-绑定引擎
- 返回值：error类型，绑定成功返回nil，否则返回错误信息。该方法在绑定之前读取请求体，因此如果只需调用一次，则应使用ShouldBindWith以获得更好的性能。

## func (*Context) ShouldBindHeader

goCopy code

`func (c *Context) ShouldBindHeader(obj any) error`

- 功能：c.ShouldBindWith(obj, binding.Header)的快捷方式。

### func (*Context) Set

`Set(key string, value any)` 方法用于为此上下文存储一个新的键值对。如果此前没有使用过c.Keys，则也会惰性地初始化它。

### func (*Context) SetAccepted

`SetAccepted(formats ...string)` 方法用于设置“Accept”头数据。

### func (*Context) SetCookie

`SetCookie(name, value string, maxAge int, path, domain string, secure, httpOnly bool)` 方法会向ResponseWriter的头信息中添加一个Set-Cookie头。提供的cookie必须有一个有效的Name。无效的cookie可能会被静默丢弃。

### func (*Context) SetSameSite

`SetSameSite(samesite http.SameSite)` 方法用于设置cookie的SameSite属性。

### func (*Context) ShouldBind

`ShouldBind(obj any) error` 方法会检查Method和Content-Type以自动选择绑定引擎，根据“Content-Type”标头使用不同的绑定方法，例如：

- `application/json` --> JSON绑定
- `application/xml` --> XML绑定

如果Content-Type == `application/json`，则它会将请求体解析为JSON，使用JSON或XML作为JSON输入。它将json有效载荷解码为指定为指针的结构体。类似于c.Bind()，但此方法不会在输入无效时设置响应状态代码为400或中止。

### func (*Context) ShouldBindBodyWith

`ShouldBindBodyWith(obj any, bb binding.BindingBody) (err error)` 方法类似于`ShouldBindWith`，但它会将请求体存储到上下文中，并在再次调用时重用。

注意：此方法在绑定之前读取请求体。因此，如果只需要调用一次，请使用ShouldBindWith以获得更好的性能。

### func (*Context) ShouldBindHeader

`ShouldBindHeader(obj any) error` 方法是`c.ShouldBindWith(obj, binding.Header)`的一种快捷方式。

### func (*Context) ShouldBindJSON

`ShouldBindJSON(obj any) error` 方法是`c.ShouldBindWith(obj, binding.JSON)`的一种快捷方式。

### func (*Context) ShouldBindQuery

`ShouldBindQuery(obj any) error` 方法是`c.ShouldBindWith(obj, binding.Query)`的一种快捷方式。

### func (*Context) ShouldBindTOML

`ShouldBindTOML(obj interface{}) error` 方法是`c.ShouldBindWith(obj, binding.TOML)`的一种快捷方式。

### func (*Context) ShouldBindUri

`ShouldBindUri(obj any) error` 方法使用指定的绑定引擎绑定传递的结构体指针。

### func (*Context) ShouldBindWith

`ShouldBindWith(obj any, b binding.Binding) error` 方法使用指定的绑定引擎绑定传递的结构体指针。有关绑定包的详细信息，请参见binding package。

## 设置操作

- `func (c *Context) Set(key string, value any)`：为该上下文存储一个新的键值对，如果之前没有使用过c.Keys，则会懒惰初始化。
- `func (c *Context) SetAccepted(formats ...string)`：设置Accept头数据。
- `func (c *Context) SetCookie(name, value string, maxAge int, path, domain string, secure, httpOnly bool)`：为ResponseWriter的头部添加一个Set-Cookie头。提供的cookie必须有一个有效的Name，否则可能会被静默丢弃。
- `func (c *Context) SetSameSite(samesite http.SameSite)`：用于cookie。

## 绑定操作

- `func (c *Context) ShouldBind(obj any) error`：检查Method和Content-Type，自动选择绑定引擎。它根据“Content-Type”头使用不同的绑定引擎进行绑定，例如：
  
  - "application/json" --> JSON绑定
  - "application/xml" --> XML绑定
  
  如果Content-Type == "application/json"，则将请求正文解析为JSON，使用JSON或XML作为JSON输入。它将json有效载荷解码为指定为指针的结构。与`c.Bind()`相似，但是如果输入无效，则此方法不会将响应状态代码设置为400或中止。

- `func (c *Context) ShouldBindBodyWith(obj any, bb binding.BindingBody) (err error)`：类似于ShouldBindWith，但它会将请求体存储在上下文中，并在再次调用时重用。
  
  **注意**：此方法在绑定之前读取body。因此，如果您只需要调用一次，应使用ShouldBindWith获得更好的性能。

- `func (c *Context) ShouldBindHeader(obj any) error`：是`c.ShouldBindWith(obj, binding.Header)`的快捷方式。

- `func (c *Context) ShouldBindJSON(obj any) error`：是`c.ShouldBindWith(obj, binding.JSON)`的快捷方式。

- `func (c *Context) ShouldBindQuery(obj any) error`：是`c.ShouldBindWith(obj, binding.Query)`的快捷方式。

- `func (c *Context) ShouldBindTOML(obj interface{}) error`：是`c.ShouldBindWith(obj, binding.TOML)`的快捷方式。

- `func (c *Context) ShouldBindUri(obj any) error`：使用指定的绑定引擎绑定传递的结构体指针。

- `func (c *Context) ShouldBindWith(obj any, b binding.Binding) error`：使用指定的绑定引擎绑定传递的结构体指针。请参阅binding包。

## 其他操作

- `func (c *Context) Status(code int)`：设置HTTP响应代码。
- `func (c *Context) Stream(step func(w io.Writer) bool) bool

### func (*Context) Value

goCopy code

`func (c *Context) Value(key any) any`

Value 返回与此上下文关联的 key 的值，如果没有与 key 关联的值，则返回 nil。对于相同的 key，连续的 Value 调用返回相同的结果。

### func (*Context) XML

goCopy code

`func (c *Context) XML(code int, obj any)`

XML 将给定的结构体序列化为 XML，并将其写入响应体。它还将 Content-Type 设置为 "application/xml"。

### func (*Context) YAML

goCopy code

`func (c *Context) YAML(code int, obj any)`

YAML 将给定的结构体序列化为 YAML，并将其写入响应体。

## 新增

### func (*Context) ShouldBindXML

goCopy code

`func (c *Context) ShouldBindXML(obj any) error`

ShouldBindXML 是 c.ShouldBindWith(obj, binding.XML) 的快捷方式。

### func (*Context) ShouldBindYAML

goCopy code

`func (c *Context) ShouldBindYAML(obj any) error`

ShouldBindYAML 是 c.ShouldBindWith(obj, binding.YAML) 的快捷方式。

### func (*Context) String

goCopy code

`func (c *Context) String(code int, format string, values ...any)`

String 将给定的字符串写入响应体。

### func (*Context) TOML

goCopy code

`func (c *Context) TOML(code int, obj interface{})`

TOML 将给定的结构体序列化为 TOML，并将其写入响应体。  

---

## Params类型

### type Params

`type Params []Param`

Params是Param-slice，由路由器返回。该切片是有序的，第一个URL参数也是第一个切片值。因此，可以通过索引安全地读取值。

### func (Params) ByName

`func (ps Params) ByName(name string) (va string)`

ByName返回与给定名称匹配的第一个Param的值。如果找不到匹配的Param，则返回空字符串。

### func (Params) Get

`func (ps Params) Get(name string) (string, bool)`

Get返回与给定名称匹配的第一个Param的值和一个布尔值true。如果找不到匹配的Param，则返回空字符串和一个布尔值false。

### type RecoveryFunc

版本:v1.7.0

`type RecoveryFunc func(c *Context, err any)`

RecoveryFunc定义可传递给CustomRecovery的函数。

--- 

## Param类型

### type Param

go複製代碼

`type Param struct {     Key   string     Value string }`

Param是一个单一的URL参数，由键和值组成
