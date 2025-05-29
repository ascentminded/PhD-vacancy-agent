import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import ollama


# Google Sheets Access
# --------------------------

def connect_to_google_sheet(service_account_path: str, spreadsheet_name: str, worksheet_name: str) -> pd.DataFrame:
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(service_account_path, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open(spreadsheet_name).worksheet(worksheet_name)
    #data = sheet.get_all_records() #You can do more steps here, return a df directly, but I commented this out for greater flexibility during execution.
    return sheet

# LLaMA Query
# --------------------------

def query_llama(system_prompt: str, user_prompt: str, model: str = 'llama3.2') -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    print("LLaMa is chewing it over...")
    response = ollama.chat(model=model, messages=messages)
    print("Responded.")
    return response['message']['content']

# --------------------------
#Formatting : The following format applies for the PhD vacancy site that I used. Based on how you have saved your data in the google sheet, the headings may differ
# --------------------------

def format_jobs(data: pd.DataFrame) -> str:
    return "\n\n".join([
        f"{i+1}. Title: {row['title']}\n"
        f"   URL: {row['url']}\n"
        f"   Description: {row['description']}\n"
        f"   Requirements: {row['requirements']}\n"
        f"   Additional info: {row['additional_info']}"
        for i, row in data.iterrows()
    ])

#The following prompt is the user prompt, and it can be fine tuned.
def create_user_prompt(jobs_chunk: pd.DataFrame) -> str:
    return f"""Check the following list of PhD/postdoc positions and return **only those** relevant to my experience in AI, cognition, psychology, deep learning, and brain science. Exclude ecology or physical science unless they mention AI, cognition, or neuroscience directly.

Here are the jobs:

{format_jobs(jobs_chunk)}"""

# --------------------------

# System Prompt
# --------------------------

system_prompt = """You are helping a cognitive scientist and AI researcher identify relevant PhD and postdoc positions from a large list.

The user has expertise in:
- Cognitive science
- Deep learning and modeling
- Neuroimaging
- Decision making
- Attention
- Psychology
- Predictive processing
- Human-computer interaction

Return only those positions clearly or tangentially related to these areas. Do NOT include anything in ecology, plant biology, physics, material science, or unrelated fields unless there’s a brain/AI/cognition aspect.

Respond only with a list of matching job titles and URLs. Do not include summaries or reasoning.
"""



#the following splits up a large dataframe so that the prompt isn't overwhelmed
def chunk_dataframe(data: pd.DataFrame, chunk_size: int):
    for i in range(0, len(data), chunk_size):
        yield data.iloc[i:i + chunk_size]


# Save to HTML: Entirely optional, but LLaMa outputs tend to be in markdown and reading it in terminal is a pain, thus:
# --------------------------

def save_response_as_html(text: str, filepath: str):
    html_text = text.replace("\n", "<br>")
    html_text = html_text.replace(" **", "<b>").replace("** ", "</b>").replace("**:", "</b>:")
    html = f"<html><head><title>LLaMA Output</title></head><body>{html_text}</body></html>"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML file saved to {filepath}")



