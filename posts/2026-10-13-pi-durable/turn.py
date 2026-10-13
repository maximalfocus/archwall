"""pi-durable: A model and tool turn. Source: earendil-works/pi at 7d75a0e3eb273dff753d49c066ea29fbe7b3b6f6; packages/durable/src/harness/generation.ts; src/harness/tool.ts:112-186; README.md:408-483. Run: python3 turn.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram

d = Diagram('A model and tool turn', 'Input is durably admitted and, when the conversation is busy, queued as a steer or follow-up. Generation prepares context, prompt sections and offered tools. Compaction summarizes older context when needed. pi-ai calls or polls the model; streamed progress and the response are committed. Tool calls become tasks with validated arguments and before/after hooks. Tool calls may use the host-provided ExecutionEnv; the built-in coding tools require it. Committed tool results feed the next model request unless the round ends the run; when every result of the round sets control.terminate = true, the run ends instead. An answer without further tool calls ends the turn. At the final boundary, the input settles unless an eligible onYield continuation starts a new generation. Retry and deferred-provider polling are generation phases.')
d.pill(24,16,1152,48,"Input → model → tools → another model turn or final answer")
d.group(24,84,552,380,"Admit input",1)
d.column(24,84,[("Submission|store input and request ID", "write"),("Busy inbox|steer or follow-up", "plan"),("User entry|start or join a run", "data")])
d.group(624,84,552,380,"Prepare context",2)
d.column(624,84,[("Context · agent|transcript and chosen model", "data"),("Prompt · tools|selected extension sections", "write"),("Auto compaction|settings.compaction.enabled", "coding")])
d.group(624,500,552,364,"Ask the model",3)
d.column(624,500,[("pi-ai provider|request or poll", "coding"),("Committed response|text · thinking · tool calls", "write"),("Final answer|settle or hook continues", "write")])
d.group(24,500,552,364,"Run requested tools",4)
d.column(24,500,[("Tool task|validate · hooks · intent", "review"),("Tool implementation|env for coding tools", "coding"),("Committed result|output · details · usage", "write")])
d.notes(24,500,364,"All results: control.terminate = true → end run")
d.arrow("M576 260H622",label="input",at=(600,248))
d.arrow("M1000 464V498",label="prompt · tools",at=(1000,488))
d.arrow("M624 660H578",label="tool calls",at=(600,648))
d.arrow("M576 780H600V350H622",back=True,label="results · if continuing",at=(600,480))

d.save(Path(__file__).with_name("turn.svg"))
