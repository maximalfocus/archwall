OpenConnector 是开源网关，连接 AI 智能体和你用的应用。账号只连一次，智能体就能跑现成的动作，但看不到密码和令牌。

**一次调用**从 MCP、HTTP API 或 Web 控制台进来。网关查令牌和允许、禁止规则，选账号、查输入，跑服务的代码，记一条脱敏日志。

![](action-run.svg)

**连接。** API 密钥和 OAuth 令牌存在网关的数据库里，设了加密密钥才加密。有些服务不用账号。Marketplace 的动作用一把密钥在 OOMOL 那边跑。SaaS OAuth 账号的令牌留在 OOMOL。

![](connections.svg)

**安全护栏。** 管理令牌守着控制台。每个调用方令牌带自己的授权。每一层都放行才能调用，禁止规则永远优先。请求到不了内网地址，除非打开开关。

![](safety.svg)

**目录。** 每个服务一个文件夹：一份定义，加上调它 API 的代码。脚本把定义生成目录。代码第一次用到时才加载。

![](catalog.svg)

**触发器**用轮询或 webhook，把服务那边的事件交给 Open Flow，那是另一个工作流引擎。

![](triggers.svg)

**部署在哪：** Node 服务（Docker、单个可执行文件、Helm）、Cloudflare Workers、嵌进你自己的应用当库用，或者用 OOMOL 托管。

![](deploy.svg)
