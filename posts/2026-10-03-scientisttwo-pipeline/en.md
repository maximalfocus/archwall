ScientistTwo is an AI that does research by itself. Give it a direction and it comes up with ideas, runs experiments, writes the paper and reviews it. If the review fails, it goes back and fixes it.

Top row: does the idea work?

1. **Idea**: find where current methods fall short and check the idea is new. Experiment results come back and the idea gets revised.
2. **Experiment**: try it on a small slice of data first, then the full set. One agent writes code, another looks for problems, back and forth.
3. **Take it apart**: run ablations to see which parts matter. Cut the rest.

Bottom row: does the paper pass?

4. **Write**: a first draft, then a cleanup.
5. **Review**: one agent finds problems, another answers them with new experiments, not new wording.
6. **Gatekeep**: not good enough? Back to step 3.

Why it works: small before big, take it apart before writing it up. That saves compute. No pass, no paper.

Result: it beat the best human result on 86 of 107 problems.
