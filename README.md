# PhD-vacancy-agent (n8n Workflow)
---
(With additional LLaMa options - filter_functions and filter_run, see below)

## Why I Built This

Finding relevant academic jobs can be time-consuming. This workflow automates the search, intelligently filters by research interests using OpenAI, and organizes results in one place — giving me (and you!) a weekly head start on suitable opportunities. This agent outputs these vacancies to a google sheet, so I can find all the positions that fit my interests in one place.

## What It Does

* Pulls recent PhD vacancies from [AcademicTransfer.com](https://www.academictransfer.com)
* Parses and cleans English-language listings
* Uses OpenAI to match listings to your interests
* Sends relevant jobs to a connected Google Sheet

## How to Use

1. **Import the Workflow (PhD-vacancy-workflow.json)**

   * Open your n8n instance
   * Click **Import Workflow**
   * Paste in the full JSON file

2. **Plug in Required Values**

   * **AcademicTransfer Bearer Token**
   * **OpenAI API credentials**
   * **Google Sheets Service Account**

3. **Getting the AcademicTransfer API Token**

   * AcademicTransfer doesn’t have a public developer dashboard
   *   Reach out via [their contact form](https://www.academictransfer.com/en/contact/) and request API access
   *   Mention your use case (e.g. research automation) and ask for a bearer token for `https://api.academictransfer.com`
   *   Once you get the token, paste it into the HTTP Request node headers.
   * Note: If public API access is unavailable, advanced users may inspect browser fetch requests (google dev tools/ F12, Bearer <token>` string under headers -> authorisation) to retrieve temporary tokens — though this method is not officially supported and may violate site policies -- they may also change any time.
---

4. **Customizing your research interests**
The filtering logic is driven by your interests, which are hardcoded in the **"Generate prompt"** node. To change them:
* Open the **Generate prompt** node
*  Find the line like:
```js
const interests = "cognition, psychology, AI, deep learning, reinforcement learning";
```
* Replace that string with your own research interests
This helps GPT shortlist only the most relevant job titles for you.

5. **Google Sheets Setup (Service Account)**

   * Use a service account (or change it to OAut, and configure the n8n node accordingly)
   * Share your target Google Sheet with the service account email (e.g. `my-service-account@project-id.iam.gserviceaccount.com`)
   * In n8n, use the **Google Sheets API (Service Account)** credentials
   * Fill in the correct `sheetId` and sheet name/range in the node
  
## LLaMa integration
As an Ollama enthusiast, I also went ahead and tried filtering with LLaMa 3.2. The prompt engineering needs some work, but after the initial step of collecting all vacancies in one spreadsheet, the python code provided (filter_functions and filter_run), along with a file called SHEET_AUTH.json (containing your google sheet credentials) will filter the jobs and provide an HTML file with selected jobs. I am currently working on counteracting LLaMa's tendency to get 'overwhelmed' by the amount of data in a spreadsheet by chunking it and engineering prompts better, so stay tuned.

## Final note:
---
- As with all n8n workflows, this can be expanded on, with Cron scheduling, email notifications, more complex AI calls, and more -- for instance, I've set my Google sheet to notify me whenever there's an update, but n8n could send an email summarising the new updates too.
- While n8n makes API integration a lot easier, this can be done using pure python code as well (check out [my other work](https://github.com/ascentminded/llama-agent) if you're interested in a primer).
- If you don't want to pay for GPT API access, you can use Ollama or Gemini (with Gemini being very similar to the GPT api usage).
- Have fun, and good luck in your search!

~ NB (Ascentminded)


