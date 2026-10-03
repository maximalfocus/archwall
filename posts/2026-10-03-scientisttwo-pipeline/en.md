ScientistTwo runs the full research cycle on its own: it generates and evolves ideas, validates them experimentally, isolates what actually works, writes the manuscript, then peer-reviews it, looping until the work clears a publication bar.

Six agent groups form one loop:

1. **Idea Generator**: proposes ideas from the limitations of existing work and checks novelty; good and bad experimental results flow back to evolve new ideas.
2. **Evaluator**: screens ideas on representative benchmark subsets before full-scale runs; at each stage a coding agent and a critic agent iterate.
3. **Analyzer**: designs its own ablations, isolates each component's contribution, prunes what does not help, and sends the sharpened idea back for full-set runs.
4. **Writer**: an initial drafter, then a draft enhancer.
5. **Peer Review**: a review agent critiques; a rebuttal agent answers with new, targeted experiments, not just edited text.
6. **Meta-Review**: supervises the cycle and sends the work back to analysis until acceptance criteria are met.

The design idea: **two compute-saving filters** (subset before full set; ablation before writing) and **one strict exit** (no pass, no paper).

Result: it beats human state of the art on 86 of 107 research problems, with a 25.2% average relative gain.
