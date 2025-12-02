# README

## What it does
This project's goal is to give people a simple, engaging way to interact with the news and historical events. By translating story requests on 
news and historical topics into storybook-style digests, with narrative descriptions of the context, characters and outcomes of a story topic and cartoonified
visuals, StoryTime aims to make news more accessible for everyone. This is an important goal because as media becomes increasingly entertainment-oriented, information needs to take more appealing forms (eg a storybook) to be consumed by a wide audience and inform how people and countries make decisions. 

These stories are created automatically upon user request, when a newsAgent with access to internet search, illustration and StoryTime database editing tools begins working on the final article. The agent does deep background research on the topic to understand the context, characters and outcomes of the story, and then begins writing a story to a well-defined StoryTime story schema complete with images and citations. The project also provides functionality for evaluating the StoryTime platform: the testerAgent read over stories and fact-checks claims and ensures that citations are accurate and reference the correct information, scoring the story on these metrics, and batch-simulation can be run to test a wide-range of plausible stories quickly.

## Quick start
You can start using the StoryTime platform relatively quickly using the following instructions:
1. Read and complete the SETUP.md instructions to ensure all dependencies are installed
2. Run the following command to start the StoryTime API:
'''bash
uvicorn src.backend.api.main:app --reload
'''
3. Then run this command in a separate terminal to start the StoryTime frontend:
'''bash
cd src/frontend
npm run dev
'''
4. A link to the frontend UI will be printed to the console, from that linked frontend you will be able to read
existing stories and create new stories.

## Video Links
Public Demo:
https://youtu.be/uYE_jvL18uY
Technical Walkthrough: 
https://youtu.be/Vdjmn90tIxE

## Evaluation
In its current version, the StoryTime platform uses two metrics to ensure stories are reliable: claim accuracy and citation accuracy. The claim accuracy
metric, measured by the testerAgent when reviewing a story, records the proportion of claims in the story that are true. It is calculated by fact-checking each claim with internet search results, and taking the number of verified claims over the total number of factual claims in the story. The citation accuracy metric, also measured by the testerAgent during review, records the proportion of citations in the story's citations that are valid and relevant to the story. If a citation was hallucinated, as has been a problem with LLM systems in the past, it would be picked up by this evaluation layer, which verfies sources the same way a human evaluator would. 

## Individual Contributions
This project was completed in its entirety by Harrison Fazzone.