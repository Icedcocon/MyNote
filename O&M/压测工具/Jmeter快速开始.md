# Jmeter快速开始

## 一、安装

### 1. 拉取镜像

```bash
docker pull justb4/jmeter:5.5
./test.sh
```

## 二、使用

### 1. jmx 文件详解

#### 1.1 linux 修改 jmeter 文件

- 在linux中更改Jmeter参数须先编辑jmx文件。可以参数化一些常用的变量，直接在Jmeter命令行进行设置

- 参数 -J 和 -G
  
  - 格式：-J变量名=值  -G变量名=值
  
  - 相同之处：设置jmeter属性，例如线程数、循环次数、ramp up-time等
  
  - 不同之处：-J是设置本地jmeter属性；-G是设置server的jmeter属性（只有设置了远程机，开启了远程服务，才需要用到-G）

- 用法： `-J, --jmeterproperty <argument>=<value>`
  
  - `JTARGET_HOST=${TARGET_HOST} -JTARGET_PORT=${TARGET_PORT}`

- jml 文件中对应参数用 `${}` 包裹，如 `${TARGET_HOST}`

```xml
<ConfigTestElement guiclass="HttpDefaultsGui" testclass="ConfigTestElement" testname="HTTP Request Defaults" enabled="true">
  <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">
    <collectionProp name="Arguments.arguments"/>
  </elementProp>
  <stringProp name="HTTPSampler.domain">${TARGET_HOST}</stringProp>
  <stringProp name="HTTPSampler.port">${TARGET_PORT}</stringProp>
  <stringProp name="HTTPSampler.connect_timeout">5000</stringProp>
  <stringProp name="HTTPSampler.response_timeout">30000</stringProp>
  <stringProp name="HTTPSampler.protocol"></stringProp>
  <stringProp name="HTTPSampler.contentEncoding"></stringProp>
  <stringProp name="HTTPSampler.path">${TARGET_PATH}</stringProp>
  <stringProp name="HTTPSampler.implementation">HttpClient4</stringProp>
  <stringProp name="TestPlan.comments">Notice Timeouts: 30s to 5s</stringProp>
  <stringProp name="HTTPSampler.concurrentPool">4</stringProp>
</ConfigTestElement>
```

#### 1.2 jmx 文件结构

面按结构自上而下讲解各个部分再.jmx文件中的表示：

文件结构:

1. TestPlan (测试计划)
   - ThreadGroup (线程组)
     - ConfigTestElement (HTTP请求默认值)
     - HTTPSamplerProxy (HTTP请求采样器)
       - ResponseAssertion (响应断言)
     - TestAction (测试操作 - 思考时间)
       - UniformRandomTimer (均匀随机定时器)
     - Arguments (用户定义的变量)
   - ResultCollector (结果收集器)

##### 1.2.1 TestPlan (测试计划)

- a. testname：
  
  - 当前值："TrivialTest"
  - 这是测试计划的名称，可以根据需要修改。

- b. enabled：
  
  - 当前值：true
  - 可以设置为false来禁用整个测试计划。

- c. TestPlan.functional_mode：
  
  - 当前值：false
  - 如果设置为true，将启用功能测试模式。

- d. TestPlan.serialize_threadgroups：
  
  - 当前值：false
  - 如果设置为true，线程组将按顺序执行，而不是并行执行。

- e. TestPlan.comments：
  
  - 当前值：空
  - 可以添加注释来描述测试计划。

- f. TestPlan.user_define_classpath：
  
  - 当前值：空
  - 可以添加自定义的类路径，如果测试需要额外的Java类。

- g. User Defined Variables：
  
  - 当前是一个空集合。
  
  - 可以在这里添加测试计划级别的用户定义变量。

```xml
<TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname=${TEST_PLAN_NAME} enabled="true">
  <stringProp name="TestPlan.comments"></stringProp>
  <boolProp name="TestPlan.functional_mode">false</boolProp>
  <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
  <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">
    <collectionProp name="Arguments.arguments"/>
  </elementProp>
  <stringProp name="TestPlan.user_define_classpath"></stringProp>
</TestPlan>
```

常用变量包含： testname, enabled(true启用，false禁用)

##### 1.2.2 ThreadGroup (线程组)

- testname：
  - 当前值："Scenario 1"
  - 可以修改为更具描述性的名称。
- ThreadGroup.on_sample_error：
  - 当前值："continue"
  - 可选值：continue, start_next_thread, stop_thread, stop_test, stop_test_now
  - 定义当样本错误时的行为。
- LoopController.continue_forever：
  - 当前值：false
  - 如果设为true，将无限循环执行。
- LoopController.loops：
  - 当前值："2"
  - 可以修改循环次数。
- ThreadGroup.num_threads：
  - 当前值：${THREADS}（变量）
  - 设置线程（虚拟用户）数量。
- ThreadGroup.ramp_time：
  - 当前值："2"
  - 设置全部线程启动所需的时间（秒）。
- ThreadGroup.scheduler：
  - 当前值：true
  - 是否启用调度器。
- ThreadGroup.duration：
  - 当前值："60"
  - 测试持续时间（秒）。
- ThreadGroup.delay：
  - 当前值："5"
  - 测试开始前的延迟时间（秒）。
- ThreadGroup.start_time 和 ThreadGroup.end_time：
  - 可以设置具体的开始和结束时间戳。
- TestPlan.comments：
  - 可以修改或添加注释来描述此线程组的用途。

```javascript
<ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="Scenario 1" enabled="true">
  <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
  <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="Loop Controller" enabled="true">
    <boolProp name="LoopController.continue_forever">false</boolProp>
    <stringProp name="LoopController.loops">2</stringProp>
  </elementProp>
  <stringProp name="ThreadGroup.num_threads">${THREADS}</stringProp>
  <stringProp name="ThreadGroup.ramp_time">2</stringProp>
  <longProp name="ThreadGroup.start_time">1373789594000</longProp>
  <longProp name="ThreadGroup.end_time">1373789594000</longProp>
  <boolProp name="ThreadGroup.scheduler">true</boolProp>
  <stringProp name="ThreadGroup.duration">60</stringProp>
  <stringProp name="ThreadGroup.delay">5</stringProp>
  <stringProp name="TestPlan.comments">Virtual Users Running Scenario 1. Make test last 1 minute (see Scheduler)</stringProp>
</ThreadGroup>
```

##### 1.2.3 ConfigTestElement (HTTP请求默认值)

- testname：
  - 当前值："HTTP Request Defaults"
  - 可以修改为更具描述性的名称。
- HTTPSampler.domain：
  - 当前值：${TARGET_HOST}（变量）
  - 设置目标服务器的域名或IP地址。
- HTTPSampler.port：
  - 当前值：${TARGET_PORT}（变量）
  - 设置目标服务器的端口号。
- HTTPSampler.connect_timeout：
  - 当前值："5000"（毫秒）
  - 设置连接超时时间。
- HTTPSampler.response_timeout：
  - 当前值："30000"（毫秒）
  - 设置响应超时时间。
- HTTPSampler.protocol：
  - 当前值：空
  - 可以设置为"http"或"https"。
- HTTPSampler.contentEncoding：
  - 当前值：空
  - 可以设置内容编码（如"UTF-8"）。
- HTTPSampler.path：
  - 当前值：${TARGET_PATH}（变量）
  - 设置请求的默认路径。
- HTTPSampler.implementation：
  - 当前值："HttpClient4"
  - 可以选择其他HTTP客户端实现。
- HTTPSampler.concurrentPool：
  - 当前值："4"
  - 设置并发连接池的大小。
- TestPlan.comments：
  - 可以修改或添加注释来描述这些默认设置。
- HTTPsampler.Arguments：
  - 当前是一个空集合。
  - 可以在这里添加默认的HTTP参数。

```jsx
 <ConfigTestElement guiclass="HttpDefaultsGui" testclass="ConfigTestElement" testname="HTTP Request Defaults" enabled="true">
   <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">
     <collectionProp name="Arguments.arguments"/>
   </elementProp>
   <stringProp name="HTTPSampler.domain">${TARGET_HOST}</stringProp>
   <stringProp name="HTTPSampler.port">${TARGET_PORT}</stringProp>
   <stringProp name="HTTPSampler.connect_timeout">5000</stringProp>
   <stringProp name="HTTPSampler.response_timeout">30000</stringProp>
   <stringProp name="HTTPSampler.protocol"></stringProp>
   <stringProp name="HTTPSampler.contentEncoding"></stringProp>
   <stringProp name="HTTPSampler.path">${TARGET_PATH}</stringProp>
   <stringProp name="HTTPSampler.implementation">HttpClient4</stringProp>
   <stringProp name="TestPlan.comments">Notice Timeouts: Read to 30s Connect to 5s</stringProp>
   <stringProp name="HTTPSampler.concurrentPool">4</stringProp>
 </ConfigTestElement>
```

##### 1.2.4 HTTPSamplerProxy (HTTP请求采样器)

- testname：
  - 当前值："HTML Page Test"
  - 可以修改为更具描述性的名称。
- HTTPsampler.Arguments：
  - 当前是一个空集合。
  - 可以添加HTTP请求参数。
- HTTPSampler.domain：
  - 当前值：空
  - 可以设置特定的目标域名，覆盖默认值。
- HTTPSampler.port：
  - 当前值：空
  - 可以设置特定的端口号，覆盖默认值。
- HTTPSampler.connect_timeout：
  - 当前值：空
  - 可以设置特定的连接超时时间，覆盖默认值。
- HTTPSampler.response_timeout：
  - 当前值：空
  - 可以设置特定的响应超时时间，覆盖默认值。
- HTTPSampler.protocol：
  - 当前值：空
  - 可以设置为"http"或"https"，覆盖默认值。
- HTTPSampler.contentEncoding：
  - 当前值：空
  - 可以设置特定的内容编码，覆盖默认值。
- HTTPSampler.path：
  - 当前值："/"
  - 可以修改为其他路径。
- HTTPSampler.method：
  - 当前值："GET"
  - 可以修改为其他HTTP方法，如"POST"、"PUT"等。
- HTTPSampler.follow_redirects：
  - 当前值：true
  - 控制是否跟随重定向。
- HTTPSampler.auto_redirects：
  - 当前值：false
  - 控制是否自动处理重定向。
- HTTPSampler.use_keepalive：
  - 当前值：true
  - 控制是否使用keep-alive连接。
- HTTPSampler.DO_MULTIPART_POST：
  - 当前值：false
  - 控制是否使用multipart格式发送POST请求。
- HTTPSampler.monitor：
  - 当前值：false
  - 控制是否使用监视器模式。
- HTTPSampler.embedded_url_re：
  - 当前值：空
  - 可以设置嵌入式资源URL的正则表达式。

```jsx
<HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="HTML Page Test" enabled="true">
  <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="Variables pré-définies" enabled="true">
    <collectionProp name="Arguments.arguments"/>
  </elementProp>
  <stringProp name="HTTPSampler.domain"></stringProp>
  <stringProp name="HTTPSampler.port"></stringProp>
  <stringProp name="HTTPSampler.connect_timeout"></stringProp>
  <stringProp name="HTTPSampler.response_timeout"></stringProp>
  <stringProp name="HTTPSampler.protocol"></stringProp>
  <stringProp name="HTTPSampler.contentEncoding"></stringProp>
  <stringProp name="HTTPSampler.path">/</stringProp>
  <stringProp name="HTTPSampler.method">GET</stringProp>
  <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
  <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
  <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
  <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
  <boolProp name="HTTPSampler.monitor">false</boolProp>
  <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
</HTTPSamplerProxy>
```

#### JDBCDataSource

代码语言：javascript

复制

```javascript
<JDBCDataSource guiclass="TestBeanGUI" testclass="JDBCDataSource" testname="数据库连接信息配置" enabled="true">
          <boolProp name="autocommit">true</boolProp>
          <stringProp name="checkQuery">Select 1</stringProp>
          <stringProp name="connectionAge">5000</stringProp>　　-- 最大连接age
          <stringProp name="dataSource">mysql</stringProp>　　-- 资源池变量
          <stringProp name="dbUrl">jdbc:mysql://localhost/db</stringProp>　　--jdbc连接
          <stringProp name="driver">com.mysql.jdbc.Driver</stringProp>　　-- jdbc驱动（可以设置为常量）
          <boolProp name="keepAlive">true</boolProp>
          <stringProp name="password">root</stringProp>　　-- db密码
          <stringProp name="poolMax">10</stringProp>　　-- 最大连接数
          <stringProp name="timeout">10000</stringProp>
          <stringProp name="transactionIsolation">DEFAULT</stringProp>
          <stringProp name="trimInterval">60000</stringProp>
          <stringProp name="username">name</stringProp>　　-- 用户名
        </JDBCDataSource>
```

#### HTTP请求默认值

代码语言：javascript

复制

```javascript
   <ConfigTestElement guiclass="HttpDefaultsGui" testclass="ConfigTestElement" testname="HTTP请求默认值" enabled="true">
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
          <collectionProp name="Arguments.arguments"/>
          </elementProp>
          <stringProp name="HTTPSampler.domain">host</stringProp>　　-- host  服务器IP
          <stringProp name="HTTPSampler.port">port</stringProp>　　-- port端口
          <stringProp name="HTTPSampler.connect_timeout">100000</stringProp>　　-- 连接超时时间
          <stringProp name="HTTPSampler.response_timeout">100000</stringProp>　　-- 请求超时时间
          <stringProp name="HTTPSampler.protocol">http</stringProp>　　-- 协议类型（变量可填）
          <stringProp name="HTTPSampler.contentEncoding">utf-8</stringProp>
          <stringProp name="HTTPSampler.path"></stringProp>
          <stringProp name="HTTPSampler.implementation">HttpClient4</stringProp>　　-- 可选择（java\HttpCliet4）
          <stringProp name="HTTPSampler.concurrentPool">4</stringProp>
        </ConfigTestElement>
```

#### HTTP信息头管理器(http请求头设置，key-value对应)

代码语言：javascript

复制

```javascript
        <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="HTTP信息头管理器" enabled="true">
          <collectionProp name="HeaderManager.headers">
            <elementProp name="" elementType="Header">
              <stringProp name="Header.name">Content-Type</stringProp>
              <stringProp name="Header.value">application/json</stringProp>
            </elementProp>
          </collectionProp>
        </HeaderManager>
```

#### **用户定义的变量**

代码语言：javascript

复制

```javascript
  <Arguments guiclass="ArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
          <collectionProp name="Arguments.arguments">
            <elementProp name="accessToken" elementType="Argument">
              <stringProp name="Argument.name">accessToken</stringProp>
              <stringProp name="Argument.value">${accessToken}</stringProp>
              <stringProp name="Argument.metadata">=</stringProp>
              <stringProp name="Argument.desc">description</stringProp>
            </elementProp>
          </collectionProp>
  </Arguments>
```

#### 仅一次控制器（循环控制器）

代码语言：javascript

复制

```javascript
        <OnceOnlyController guiclass="OnceOnlyControllerGui" testclass="OnceOnlyController" testname="组织管理" enabled="true"/>
```

#### 查看结果树（该部分为固定项）

代码语言：javascript

复制

```javascript
         <ResultCollector guiclass="ViewResultsFullVisualizer" testclass="ResultCollector" testname="察看结果树" enabled="true">
            <boolProp name="ResultCollector.error_logging">false</boolProp>
            <objProp>
              <name>saveConfig</name>
              <value class="SampleSaveConfiguration">
                <time>true</time>
                <latency>true</latency>
                <timestamp>true</timestamp>
                <success>true</success>
                <label>true</label>
                <code>true</code>
                <message>true</message>
                <threadName>true</threadName>
                <dataType>true</dataType>
                <encoding>false</encoding>
                <assertions>true</assertions>
                <subresults>true</subresults>
                <responseData>false</responseData>
                <samplerData>false</samplerData>
                <xml>false</xml>
                <fieldNames>false</fieldNames>
                <responseHeaders>false</responseHeaders>
                <requestHeaders>false</requestHeaders>
                <responseDataOnError>false</responseDataOnError>
                <saveAssertionResultsFailureMessage>false</saveAssertionResultsFailureMessage>
                <assertionsResultsToSave>0</assertionsResultsToSave>
                <bytes>true</bytes>
                <url>true</url>
                <hostname>true</hostname>
                <threadCounts>true</threadCounts>
                <sampleCount>true</sampleCount>
              </value>
            </objProp>
            <stringProp name="filename"></stringProp>
          </ResultCollector>
```

#### **HTTP请求（Sampler，此处为Json写法，因为请求类型为Application/Json）**

代码语言：javascript

复制

```javascript
<HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="operatorLogin_操作员登录" enabled="true">
            <boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
            <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
              <collectionProp name="Arguments.arguments">
                <elementProp name="" elementType="HTTPArgument">
                  <boolProp name="HTTPArgument.always_encode">false</boolProp>
                  <stringProp name="Argument.value">{"operatorNo":"${operatorNo}", "password":"${password}", "verifyCode":"${verifyCode}"}</stringProp>
                  <stringProp name="Argument.metadata">=</stringProp>
                </elementProp>
              </collectionProp>
            </elementProp>
            <stringProp name="HTTPSampler.domain"></stringProp>
            <stringProp name="HTTPSampler.port"></stringProp>
            <stringProp name="HTTPSampler.connect_timeout"></stringProp>
            <stringProp name="HTTPSampler.response_timeout"></stringProp>
            <stringProp name="HTTPSampler.protocol"></stringProp>
            <stringProp name="HTTPSampler.contentEncoding"></stringProp>
            <stringProp name="HTTPSampler.path">/operatorLogin</stringProp> 　　-- 请求路径
            <stringProp name="HTTPSampler.method">POST</stringProp>
            <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
            <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
            <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
            <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
            <boolProp name="HTTPSampler.monitor">false</boolProp>
            <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
          </HTTPSamplerProxy>
```

#### 响应断言

代码语言：javascript

复制

```javascript
<ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="响应断言" enabled="true">
              <collectionProp name="Asserion.test_strings">
                <stringProp name="-1610171759">"errorCode":"0","errorMsg":"操作成功！"</stringProp>
              </collectionProp>
              <stringProp name="Assertion.test_field">Assertion.response_data</stringProp>
              <boolProp name="Assertion.assume_success">false</boolProp>
              <intProp name="Assertion.test_type">2</intProp>
              <stringProp name="Assertion.scope">all</stringProp>
              <stringProp name="Scope.variable">count_1</stringProp>
            </ResponseAssertion>
```

#### Debuger Sampler(固定样式)

代码语言：javascript

复制

```javascript
  <DebugSampler guiclass="TestBeanGUI" testclass="DebugSampler" testname="Debug Sampler" enabled="true">
            <boolProp name="displayJMeterProperties">false</boolProp>
            <boolProp name="displayJMeterVariables">true</boolProp>
            <boolProp name="displaySystemProperties">false</boolProp>
          </DebugSampler>
```

## 参考资料

- docker-jmeter

https://github.com/justb4/docker-jmeter
