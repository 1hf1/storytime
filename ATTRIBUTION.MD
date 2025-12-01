# Attribution

## Resources
### Langchain
This project was inspired and built on top of agentic frameworks, particularly the out-of-the-box Langchain agent class (created with the create_agent function) which is used to operate both the newsAgent and testerAgent. These resources streamline agent memory management, automatically allow chain of thought reasoning, integrate python functions as agentic tools and all modularity in this project.

### Perplexity AI
Both the RAG pipeline that allows for accurate news stories to be generated and the fact and citation-checking functionality of the testerAgent rely on the Perplexity AI websearch API. The API returns snippets of text relevant to search queries, along with their title and URL, allowing straightforward information retrieval and validation.

## AI Contributions
LLMs were used extensively to draft, edit and help debug code for this project. LLMs with access to the codebase (Cursor) were consulted in a way consistent with homework guidelines, providing only ideas for how to approach a problem and relevant libraries rather than code, for the creation of the newsAgent's prompts, agent class (newsAgent.py) and for the creation of the story structure. LLMs were then used to draft additional utility functions in the story_structure.py file, including functions to access, edit and save specific fields in the story structure and to draft the tool interface that allows the newsAgent to use these story structure utilities to edit the story in the stories database. The testerAgent.py was drafted by AI to mirror the hand-written newsAgent functionality, with the added ability to ingest a pre-written story for evaluation purposes. The testAgent system prompt was initially written by hand, and then iterated on with Cursor over the course of the testing process, yielding a more organized, formulaic final prompt. Finally, the testerAgent tools were drafted by AI to match the story tools interface, but with a new focus on writing evaluation reports. The evaluation report class was written  by hand, as was the run_simulation_testing function designed to perform batch evaluation. 

The frontend was built in Bolt.new, an AI web generation platform, due to my limited frontend experience.

Overall, AI was ussed to extend well-defined objects and help them integrate with each other (eg linking the newsAgent to the story structure by drafing tools), and to refine and iterate on agents (particularly their prompts) when they were not working reliably.

