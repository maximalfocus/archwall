ADT is SAP's toolset for writing ABAP outside SAP GUI. Until now that meant Eclipse. From 2026 it comes to VS Code too, and SAP didn't write the client twice.

The IDE shows the UI. Under it, a client layer with no UI wraps the ADT REST APIs and holds the debugger, test runner, ATC and tracing. It reaches the ABAP server over RFC or HTTP, one API for every release from 7.3 EHP1 SP04.

**Why it was hard.** Users kept asking for VS Code. But each new IDE needed its own client layer, 2.9 million lines, and 88 editors in the SAP BTP ABAP environment alone.

![](problem.svg)

**Fix 1: reuse the client.** In 2018 SAP tried a new language server in TypeScript and dropped it: two codebases to maintain. The VS Code Java extension wraps Eclipse's Java tools in a language server. SAP did the same: VS Code talks LSP to the ADT Language Server, the Eclipse plug-ins without their UI. SAP puts the possible reuse at 60%.

![](reuse.svg)

**Fix 2: server-driven editors.** An editor used to need a Java UI on the client and ABAP on the server. Since 2020, starting with number range objects, every new object type is described in ABAP on the server. The client draws it with a form-based or source-based renderer. A new IDE needs two editors, not 88.

![](editors.svg)

**Files.** In VS Code you edit objects as files, since AI tools work best on files. The objects stay on the server, behind a virtual workspace that not every AI tool supports yet.

![](files.svg)

**First release.** It targets RAP UI services in ABAP Cloud: around 12+ object types. Dynpro isn't planned. Other work still needs Eclipse, and VS Code catches up release by release.

![](release.svg)

![](timeline.svg)
