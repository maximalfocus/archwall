Automic Vault guards developer credentials on a Mac. It moves tokens out of files into the Keychain. After that, every command that needs one is checked first, whether you or an AI agent runs it.

**Set up.** `av scan` finds exposed credentials. `av harden` moves them and changes how the tool asks for them. `av doctor` checks the result.

![](setup.svg)

**One request.** The Mac checks who is asking and the whole command. A rule may allow it; otherwise you approve or deny. A record is saved before the secret goes out.

![](request.svg)

**Who is asking.** Identity comes from the app's code signature, checked live on every request. An unsigned CLI can get a Launcher Bundle.

![](launchers.svg)

**Access rules.** Each tool's gate has Access Levels. The docs suggest Read Only for agents. Unknown commands always ask.

![](policy.svg)

**Approval** happens on the Mac, with Touch ID, or on an iPhone. The Mac checks every answer.

![](approval.svg)

**Secrets and history.** Secrets stay in the Keychain. Each use is logged on the Mac, encrypted, for up to 30 days within a size cap.

![](custody.svg)

**Other ways** to use a secret: reviewed scripts, `av inject`, the Secret Proxy and Varlock.

![](mechanisms.svg)

**Signing, SSH and Homebrew** have their own gates.

![](gates.svg)

**The pieces:** the `av` command and its helpers, a menu bar app that owns the Keychain, and an optional iPhone app with a relay.

![](components.svg)
