AI research runs many rounds of tries. Exploring decides whether that compute pays off: where to branch, how many lines at once, when to stop. That strategy is usually hand-written. Changing it means a whole new run.

Dream-RSI, from Google, has one idea: **a finished run is already a simulator.** The code isn't out yet; this is from the paper.

**The tree.** A node is one try: workspace, program, score. Picking the root opens a new branch; picking a leaf takes the next step.

![](tree.svg)

**1. Explore online.** Each round the policy picks up to W nodes. A coding agent reads the past tries, then continues from each. An evaluator scores it. The tree joins the pool.

![](explore.svg)

**2. Replay.** A new policy walks an old tree its own way. Results are saved, so nothing reruns. The score counts the best result, the tries spent and how parallel they ran.

![](replay.svg)

**3. Dream.** Another agent rewrites the policy M times. Each version is replayed on every tree, and its scores guide the next. The top scorer ships. The current one competes too, so the replay score never drops.

![](dream.svg)

The policy is code. It also sets how wide and deep the next run goes. While dreaming it only sees what it has revealed. The model and evaluator never change.

![](policy.svg)

**Results.** Eight tasks, against a fixed policy. On Lasso: 1.7× fewer calls, and 162× fewer than SimpleTES.

![](results.svg)

The learned policy saves while scores climb and spends more when they stall. Turning history into prompt tips did worse than replay.

![](behavior.svg)
