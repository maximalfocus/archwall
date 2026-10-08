RAG (retrieval-augmented generation) lets an LLM answer from your documents, not only from what it learned in training. It looks things up first, then answers. This post follows a survey that sums up over 100 RAG studies.

**Three kinds.** Naive RAG indexes, retrieves and generates. Advanced RAG adds steps before and after the search. Modular RAG lets you add, swap and reorder parts.

![](paradigms.svg)

**The index.** Clean the files, split them into chunks, tag them with metadata, turn each chunk into a vector and store it.

![](index.svg)

**The question.** A vague question finds the wrong chunks. Expand it, rewrite it, or route it to the right pipeline.

![](query.svg)

**The search** compares the question's vector with each chunk's and keeps the top K. Keyword and vector search help each other.

![](search.svg)

**The answer.** Too many chunks bury the key facts. Rerank and trim them, then the LLM answers from one prompt.

![](generate.svg)

**How often to search.** Once is the most common. Harder questions search again and again, or let the LLM decide when.

![](flows.svg)

**Modules.** Modular RAG adds parts such as search, memory and routing, and changes how they connect.

![](modular.svg)

**RAG or fine-tuning?** RAG suits facts that change and shows its sources. Fine-tuning suits style and format. They can work together.

![](compare.svg)

**Checking it.** Test the search and the answer apart: is the context relevant, does the answer stick to it and fit the question?

![](eval.svg)
