```go
type Request struct {
    // 方法指定HTTP方法（GET、POST、PUT等）.
    // 对于客户端请求，空字符串意味着GET。
    // Go的HTTP客户端不支持用CONNECT方法发送请求。
    Method string

    // URL指的是被请求的URI（对于服务器请求）或要访问的URL（用于客户端请求）。
    // 对于服务器请求，URL是由Request-Line上提供的存储在RequestURI中的URI
    // 解析而来。 对于大多数请求，除Path和RawQuery以外的字段将是空的
    // （见RFC 7230，第5.3节）
    // 对于客户端请求，URL的Host指定了要连接的服务器，
    // 而Request的Host字段可以选择指定HTTP请求中要发送的Host头值。
    // 而Request的Host字段可以选择//指定在HTTP请求中发送的Host头值。
    URL *url.URL

    // The protocol version for incoming server requests.
    //
    // For client requests, these fields are ignored. The HTTP
    // client code always uses either HTTP/1.1 or HTTP/2.
    // See the docs on Transport for details.
    Proto      string // "HTTP/1.0"
    ProtoMajor int    // 1
    ProtoMinor int    // 0

    // Header包含服务器接收到的请求头字段或客户端将要发送的请求头字段。
    // 如果服务器收到了以下请求头行：
    // Host: example.com
    // accept-encoding: gzip, deflate
    // Accept-Language: en-us
    // fOO: Bar
    // foo: two
    // 那么
    // Header = map[string][]string{
    // "Accept-Encoding": {"gzip, deflate"},
    // "Accept-Language": {"en-us"},
    // "Foo": {"Bar", "two"},
    // }
    // 对于传入的请求，Host头将升级为Request.Host字段并从Header映射中删除。
    // HTTP定义了标头名称不区分大小写。请求解析器通过使用CanonicalHeaderKey实现这一点，
    // 将连字符后的第一个字符及其后面的所有字符转换为大写字母，其余转换为小写字母。
    // 对于客户端请求，某些标头（如Content-Length和Connection）在需要时将自动写入，
    // 并且Header中的值可能会被忽略。
    Header Header

    // Body是请求的正文。
    // 对于客户端请求，nil正文表示该请求没有正文，例如GET请求。
    // HTTP客户端的传输负责调用Close方法。
    // 对于服务器请求，请求正文始终为非nil，但在没有正文时会立即返回EOF。
    // 服务器将关闭请求正文，而ServeHTTP处理程序不需要关闭。
    // Body必须允许同时调用Read和Close。特别是，调用Close应该取消等待输入的Read的阻塞。
    Body io.ReadCloser

    // GetBody defines an optional func to return a new copy of
    // Body. It is used for client requests when a redirect requires
    // reading the body more than once. Use of GetBody still
    // requires setting Body.
    //
    // For server requests, it is unused.
    GetBody func() (io.ReadCloser, error)

    // ContentLength records the length of the associated content.
    // The value -1 indicates that the length is unknown.
    // Values >= 0 indicate that the given number of bytes may
    // be read from Body.
    //
    // For client requests, a value of 0 with a non-nil Body is
    // also treated as unknown.
    ContentLength int64

    // TransferEncoding lists the transfer encodings from outermost to
    // innermost. An empty list denotes the "identity" encoding.
    // TransferEncoding can usually be ignored; chunked encoding is
    // automatically added and removed as necessary when sending and
    // receiving requests.
    TransferEncoding []string

    // Close indicates whether to close the connection after
    // replying to this request (for servers) or after sending this
    // request and reading its response (for clients).
    //
    // For server requests, the HTTP server handles this automatically
    // and this field is not needed by Handlers.
    //
    // For client requests, setting this field prevents re-use of
    // TCP connections between requests to the same hosts, as if
    // Transport.DisableKeepAlives were set.
    Close bool

    // For server requests, Host specifies the host on which the
    // URL is sought. For HTTP/1 (per RFC 7230, section 5.4), this
    // is either the value of the "Host" header or the host name
    // given in the URL itself. For HTTP/2, it is the value of the
    // ":authority" pseudo-header field.
    // It may be of the form "host:port". For international domain
    // names, Host may be in Punycode or Unicode form. Use
    // golang.org/x/net/idna to convert it to either format if
    // needed.
    // To prevent DNS rebinding attacks, server Handlers should
    // validate that the Host header has a value for which the
    // Handler considers itself authoritative. The included
    // ServeMux supports patterns registered to particular host
    // names and thus protects its registered Handlers.
    //
    // For client requests, Host optionally overrides the Host
    // header to send. If empty, the Request.Write method uses
    // the value of URL.Host. Host may contain an international
    // domain name.
    Host string

    // Form contains the parsed form data, including both the URL
    // field's query parameters and the PATCH, POST, or PUT form data.
    // This field is only available after ParseForm is called.
    // The HTTP client ignores Form and uses Body instead.
    Form url.Values

    // PostForm contains the parsed form data from PATCH, POST
    // or PUT body parameters.
    //
    // This field is only available after ParseForm is called.
    // The HTTP client ignores PostForm and uses Body instead.
    PostForm url.Values

    // MultipartForm is the parsed multipart form, including file uploads.
    // This field is only available after ParseMultipartForm is called.
    // The HTTP client ignores MultipartForm and uses Body instead.
    MultipartForm *multipart.Form

    // Trailer specifies additional headers that are sent after the request
    // body.
    //
    // For server requests, the Trailer map initially contains only the
    // trailer keys, with nil values. (The client declares which trailers it
    // will later send.)  While the handler is reading from Body, it must
    // not reference Trailer. After reading from Body returns EOF, Trailer
    // can be read again and will contain non-nil values, if they were sent
    // by the client.
    //
    // For client requests, Trailer must be initialized to a map containing
    // the trailer keys to later send. The values may be nil or their final
    // values. The ContentLength must be 0 or -1, to send a chunked request.
    // After the HTTP request is sent the map values can be updated while
    // the request body is read. Once the body returns EOF, the caller must
    // not mutate Trailer.
    //
    // Few HTTP clients, servers, or proxies support HTTP trailers.
    Trailer Header

    // RemoteAddr allows HTTP servers and other software to record
    // the network address that sent the request, usually for
    // logging. This field is not filled in by ReadRequest and
    // has no defined format. The HTTP server in this package
    // sets RemoteAddr to an "IP:port" address before invoking a
    // handler.
    // This field is ignored by the HTTP client.
    RemoteAddr string

    // RequestURI is the unmodified request-target of the
    // Request-Line (RFC 7230, Section 3.1.1) as sent by the client
    // to a server. Usually the URL field should be used instead.
    // It is an error to set this field in an HTTP client request.
    RequestURI string

    // TLS allows HTTP servers and other software to record
    // information about the TLS connection on which the request
    // was received. This field is not filled in by ReadRequest.
    // The HTTP server in this package sets the field for
    // TLS-enabled connections before invoking a handler;
    // otherwise it leaves the field nil.
    // This field is ignored by the HTTP client.
    TLS *tls.ConnectionState

    // Cancel is an optional channel whose closure indicates that the client
    // request should be regarded as canceled. Not all implementations of
    // RoundTripper may support Cancel.
    //
    // For server requests, this field is not applicable.
    //
    // Deprecated: Set the Request's context with NewRequestWithContext
    // instead. If a Request's Cancel field and context are both
    // set, it is undefined whether Cancel is respected.
    Cancel <-chan struct{}

    // Response is the redirect response which caused this request
    // to be created. This field is only populated during client
    // redirects.
    Response *Response
    // contains filtered or unexported fields
}
```

## httputil

##### type ReverseProxy

```go
type ReverseProxy struct {
    // Rewrite 是用于修改请求并通过 Transport 发送新请求的函数
    // 得到的响应被完整复制并反回给原客户端，服务器返回后不能再对 ProxyRequest 做额外处理
    // 请求头中的 Forwarded、X-Forwarded、X-Forwarded-Host 和 X-Forwarded-Proto 
    // 将被删除，在调用 Rewrite 之前
    // Rewrite 函数也可以将传入 URL 的 RawQuery 复制到出站 URL 中以保留原始的参数字符串。
    // 但请注意，如果代理服务器对查询参数的解释与下游服务器不匹配，则会导致安全问题。
    // 在该结构体中，Rewrite 和 Director 最多只能设置一个。
    Rewrite func(*ProxyRequest)

    // Director 是用于修改请求并通过 Transport 发送新请求的函数
    // 得到的响应被完整复制并反回给原客户端，服务器返回后不能再对 Request 做额外处理
    // 默认请求头 X-Forwarded-For 设为客户端 IP 地址，若已经存在则将 IP 追加其后
    // 如果 Request.Header map 中 存在 X-Forwarded-For 且为 nil， 则不会修改
    // 为防止 IP 欺骗应删除客户端或代理请求头中的 X-Forwarded-For
    // Director 返回后 hop-by-hop(逐跳) headers 将被删除，可能会删除 Director 添加的头
    // 为了确保对请求的修改得以保留，请改用 Rewrite 函数。
    // 在该结构体中，Rewrite 和 Director 最多只能设置一个。
    Director func(*http.Request)

    // Transport 用于执行代理请求。如果为 nil，则使用 http.DefaultTransport。
    Transport http.RoundTripper

    // 设置刷新响应体的时间间隔，如果为0则不定期刷新；如果是负数则每次向客户端写入后都立即刷新；如果是正数则按照指定时间间隔定期刷新，该成员在 ReverseProxy 识别到响应体为流式响应或者其 ContentLength 为-1 时将被忽略。
    FlushInterval time.Duration

    // 设置一个可选的日志记录器，用于记录代理请求过程中发生的错误，如果为 nil，则使用 log 包的标准记录器进行记录。
    ErrorLog *log.Logger

    // 设置一个可选的缓冲池，用于提供 io.CopyBuffer 方法中需要的字节片，以便复制 HTTP 响应体。
    BufferPool BufferPool

    // 是一个可选的函数，用于修改来自后端的响应。无论后端返回什么 HTTP 状态码，只要它返回响应，就会调用 ModifyResponse。如果无法到达后端，则会调用可选的 ErrorHandler，而不调用 ModifyResponse。
    ModifyResponse func(*http.Response) error

    // 是一个可选的函数，用于处理到达后端的错误或 ModifyResponse 中的错误。如果为 nil，则使用默认实现记录提供的错误，并返回一个 502 Bad Gateway 响应。
    ErrorHandler func(http.ResponseWriter, *http.Request, error)
}
```

##### func NewSingleHostReverseProxy

`func NewSingleHostReverseProxy(target *url.URL) *ReverseProxy`

- 函数NewSingleHostReverseProxy会返回一个新的ReverseProxy对象，该对象将URL路由到target指定的协议、主机和基本路径。例如，如果target的路径是"/base"，而传入的请求路径是"/dir"，那么目标请求将是/base/dir。

- NewSingleHostReverseProxy不会重写Host头部。

- 如果要超出NewSingleHostReverseProxy提供的范围自定义ReverseProxy的行为，则可以直接使用ReverseProxy并使用Rewrite函数。

- ProxyRequest SetURL方法可用于路由出站请求。(请注意，与NewSingleHostReverseProxy不同，SetURL默认情况下会重写出站请求的Host头部。)
