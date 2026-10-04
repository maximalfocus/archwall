ADT is how you write ABAP outside SAP GUI. Until now that meant Eclipse; from 2026 VS Code too. SAP got there without writing the client twice.

1. **IDEs**: Eclipse runs the ADT plug-ins. VS Code runs an ADT extension that talks LSP to the **ADT Language Server**: the Eclipse plug-ins without their UI, the trick the VS Code Java extension uses with Eclipse JDT. In VS Code editing is file-based; the objects still live on the server.
2. **Client layer**: the part with no UI. It wraps the ADT REST APIs, holds the debugger, test runner, ATC and tracing, and keeps old server releases working. 2.9 million lines; SAP puts the possible reuse at 60%.
3. **ABAP server**: reached over RFC by default, or over HTTP through the `adt` ICF service. One API for every release from SAP NetWeaver 7.3 EHP1 SP04, so VS Code reaches the same systems Eclipse does.
4. **Scripts**: the REST APIs are plain HTTP, so a script can call them with no IDE at all: fetch a CSRF token, then read source, run checks, activate. sapcli (Python) and abap-adt-api (TypeScript) do this. They call the REST APIs directly, with no client layer.

![](editors.svg)

The second problem was editors. Each object type used to need its own: UI in Java on the client, persistence in ABAP on the server. The SAP BTP ABAP environment alone has 88. Today all new object types are server-driven; number range objects came first, in 2020. The server describes the UI in ABAP, and the client draws it with one of two renderers, form-based or source-based. A new IDE now needs two editors, not 88.

The first VS Code release targets RAP UI services, at least 12 object types.
