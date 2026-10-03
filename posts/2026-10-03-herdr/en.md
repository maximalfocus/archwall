You run Claude Code, Codex and the rest in terminals. Close the laptop or drop SSH and they die. Run five at once and you keep hunting for the one that's waiting on you.

herdr is one Rust binary, split like tmux: **the server owns the terminals, clients just draw**.

1. **Clients**: the local TUI, a remote client over SSH, or a direct attach to one terminal. `ctrl+b q` detaches. The work keeps going.
2. **Server**: one per session. Each pane is a real PTY running your agent, and its output feeds a terminal state built on libghostty-vt. To tell who's stuck, a detector reads the bottom of each screen against per-agent manifests (22 so far) and marks the pane working, blocked, done or idle. Agents can also report their own state; a sequence number stops a late report from overwriting a newer one.
3. **Control API**: the server also serves a socket API that agents and scripts use. An agent in one pane can spawn panes, prompt another agent, and `herdr agent wait` until that one is really blocked.
4. **If the server stops**, the processes are gone. herdr brings back what it can: live handoff during updates (opt-in, processes survive), the agent's own resume command like `claude --resume <id>`, pane history if you turned it on, and the saved layout in `session.json`.

The rule in the code: shared facts live in the server and go out through the API; how things look stays in the client. That's why your laptop can draw panes that live on another machine.
