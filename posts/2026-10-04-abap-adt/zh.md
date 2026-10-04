ADT 是在 SAP GUI 之外写 ABAP 的工具。以前只有 Eclipse，2026 年起也有 VS Code。客户端没有重写。

1. **IDE**：Eclipse 直接跑 ADT 插件。VS Code 装 ADT 扩展，用 LSP 连 **ADT Language Server**，它就是去掉界面的 Eclipse 插件，和 VS Code 的 Java 扩展包着 Eclipse JDT 一个办法。VS Code 里按文件编辑，对象还存在服务器上。
2. **客户端层**：没有界面的那部分。封装 ADT REST API，带调试器、测试运行、ATC、跟踪，也负责兼容旧版本服务器。共 290 万行，SAP 估计能复用 60%。
3. **ABAP 服务器**：默认走 RFC，也可以走 HTTP（ICF 服务 `adt`）。7.3 EHP1 SP04 起所有版本同一套 API，Eclipse 能连的系统 VS Code 也能连。
4. **脚本**：REST API 就是普通 HTTP，不开 IDE 也能调：先取 CSRF 令牌，再读源码、跑检查、激活。sapcli（Python）、abap-adt-api（TypeScript）就这么做。没有客户端层，各版本的差异得脚本自己处理。

![](editors.svg)

另一个难点是编辑器。以前每种对象类型一个编辑器：客户端用 Java 写界面，服务器用 ABAP 写持久化。光 SAP BTP ABAP 环境就有 88 个。2020 年起新类型改成服务器驱动：界面在服务器上用 ABAP 描述，客户端用表单类或源码类两个渲染器之一画出来。接一个新 IDE 只要两个编辑器，不是 88 个。

VS Code 第一版主攻 RAP UI 服务，至少 12 种对象类型。
