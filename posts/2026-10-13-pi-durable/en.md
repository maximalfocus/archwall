pi-durable is an experimental agent runtime inside Pi. It commits conversations, task checkpoints and JSON documents together, then publishes progress to the UI.

Input starts a model run or enters its inbox. Generation prepares context and prompt sections, calls pi-ai, then schedules requested tools. Their results feed the next turn. Compaction summarizes older context; settings enable automatic compaction.

![](turn.svg)

External work sits between an intent commit and an outcome commit. Reopening resumes stored checkpoints. An interrupted tool reruns only when its stored and current replay policies both say safe; otherwise it returns an interruption error. External effects still need idempotency.

![](durability.svg)

Forks continue from a chosen entry. Reset keeps stored history. Documents hold configuration, progress and application state. Chord views and events expose committed changes. Tasks own child work; background tasks (`background: true`) form an abort boundary.

![](state.svg)

The host installs extensions and supplies execution environments. CodingTools needs installation; image processing, tool-search and codemode are optional. Codemode needs a sandbox and journals results for deterministic replay. Reinstall extension code after restart.

![](extensions.svg)

Memory is temporary. SQLite, JSONL and Durable Object SQLite provide persistence with different failure boundaries. Local persistence does not guarantee the latest commit survives power loss. One process owns a store. Storage errors close the Harness; reopen to recover.

![](storage.svg)
