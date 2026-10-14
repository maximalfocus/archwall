World Monitor 把新闻、市场、追踪与事件数据放进地图和面板。Railway 采集，Redis 共享数据，Convex 保存账户与情报历史。

中继、定时采集和价格爬虫各自发布；启动接口批量加载缓存，健康检查揭示过期和缺失。

![](ingestion.svg)

契约生成领域接口，网关检查权限、限流和缓存。运维与 MCP 另有入口。

![](gateway.svg)

AppContext 连接加载器、面板和地图。存储保留偏好与历史；隐藏标签页暂停轮询，返回后补刷。

![](browser.svg)

分析与评分合并信号，RSS 与警笛分开告警。浏览器模型需设置开启或桌面模式；接口新闻摘要需权益与配置，T5 可兜底。

![](intelligence.svg)

Clerk 识别用户，Dodo 支付更新 Convex 权益，支撑偏好、通知、密钥和智能体访问。

![](accounts.svg)

Tauri 用系统密钥库启动 Node 服务，部分接口优先云端。容器可代理云端或运行本地接口。

![](desktop.svg)

检查、部署、发行各有工作流；探针和 Sentry 跟踪生产。

![](ops.svg)
