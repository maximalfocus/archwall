midPoint 是开源的身份治理系统（IGA）。它从 HR 读出谁在职，算出每人该有什么，让各系统账号跟上。

**组成。** 界面、REST API 和自写代码都调用 Model API。改动都过模型，数据存 PostgreSQL。

![](components.svg)

**同步。** 实时同步、对账和导入带进变化。midPoint 给账号找主人再反应，拿不准由人定。

![](sync.svg)

**一次修改。** clockwork 先算出用户和账号的样子，查过才写出去。

![](clockwork.svg)

**角色。** 用户申请或按规则拿到角色。业务角色引入应用角色，再建出账号和组。

![](roles.svg)

**策略规则**把条件（比如两个角色不能兼得）配上动作：拦下、审批或打标记。

![](policies.svg)

**审批。** 申请就是修改本身。规则定谁审，分阶段。代理人可代审，到期可升级。

![](approvals.svg)

**认证**请经理或角色所有者确认或撤销权限。修复设为自动才收回。

![](certification.svg)

**预配**经连接器写出，或给人开工单。做不成的改动存在影子里重试。

![](provisioning.svg)

**安全。** 按通道走认证模块。没允许就拒绝。改动都进审计。

![](security.svg)

**模拟**先用 preview 模式试配置，再启用。

![](simulation.svg)

**运行。** 一个 Java 服务，8080 端口。设 `clustered` 为 true，多节点共用仓库。

![](ops.svg)
