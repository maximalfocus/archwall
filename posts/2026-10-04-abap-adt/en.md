ADT is how you write ABAP outside SAP GUI. Until now that meant Eclipse; from 2026 VS Code too. SAP got there without writing the client twice.

1. **IDEs**: Eclipse runs the ADT plug-ins. VS Code runs an ADT extension that talks LSP to the **ADT Language Server**. That server is the Eclipse plug-ins without their UI, the same trick the VS Code Java extension uses with Eclipse JDT. In VS Code editing is file-based, using the ABAP file formats; the objects still live on the server.
2. **Client layer**: the part with no UI. It wraps the ADT REST APIs and holds client-side tools: debugger, test runner, ATC, tracing. It also keeps old server releases working. It is 2.9 million lines; SAP puts the possible reuse at 60%. One codebase, both IDEs.
3. **ABAP server**: the client reaches it over RFC by default, or over HTTP through the `adt` ICF service. The REST APIs are one API for every release from SAP NetWeaver 7.3 EHP1 SP04, so VS Code can connect to the same systems Eclipse can.

![](editors.svg)

The second problem was editors. Each object type used to need its own: UI in Java on the client, persistence in ABAP on the server. The SAP BTP ABAP environment alone has 88 of them. That didn't scale. Since 2020 new object types are server-driven: the server describes the UI in ABAP, and the client draws it with one of two renderers, form-based or source-based. Number range objects came first. A new IDE now needs two editors, not 88.

The first VS Code release targets RAP UI services, about 12 object types.
