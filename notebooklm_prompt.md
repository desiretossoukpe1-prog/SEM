# Optional step: AI-written discussion with NotebookLM (manual, with citations)

NotebookLM answers from the sources you give it and shows which source each statement came from.
Google does not offer an official way to run it automatically from GitHub, so this step is done by hand.

1. Create a notebook and upload your SEM sources (PDFs of the articles and book chapters you trust).
2. Paste the generated report (the `.md` file in `reports/`) into the chat with this prompt:

> Using ONLY the uploaded sources, write a short results discussion for the report below.
> Support every interpretive claim with a citation to an uploaded source and give the page when possible.
> If the sources do not support a claim, write "no supporting source found" instead of citing anything.
> Do not change any number in the report.

3. Check every citation against the original source before putting it in your paper.
