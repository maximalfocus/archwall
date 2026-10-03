When an AI does research, the expensive part is **exploring**: what to try next, how many lines to run at once, when to give up. That strategy is a piece of code, usually hand-written and fixed. Tuning it live means running a whole discovery run to see if a change helped. Too slow, too costly.

Dream-RSI's trick: **old runs are a simulator**.

1. **Explore online**: the current policy steers a coding agent, which grows a discovery tree. Each node is one attempt with its real result.
2. **Build a replay simulator**: a new policy just walks the same tree in a different order. Every result is already there, so nothing reruns. Each round adds a tree to the pool.
3. **Dream**: another agent revises the policy one version at a time. Each version is scored by replaying it over the whole pool, at zero execution cost, and the scores and traces feed the next revision. After a few rounds the best version ships. The current one competes too, so it never gets worse.

The new policy goes places the old one didn't and brings back new trees. That's the recursive part.

Result: about 1.7× fewer agent calls than a fixed policy, and up to 162× fewer than SimpleTES on Lasso.
