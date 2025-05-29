from filter_functions import *
import gspread
# Running the Pipeline (Starting with a google sheet where you store all the job vacancies, and the .json file downloaded when you make a service account with GSHeets)
# --------------------------

def run():
    # 1. Load data (# This is output as a raw sheet, refer filter_functions for more infor) [Replace Agent_output and Data with your spreadsheet and sheet name]
    sheet = connect_to_google_sheet(
        service_account_path="Auths/SHEET_AUTH.json",
        spreadsheet_name="Agent_output",
        worksheet_name="Data"
    )
    data = sheet.get_all_records()  # The sheet is parsed, and turned into a pandas dataframe in the next line
    df = pd.DataFrame(data)

    # 2. The df is chunked (the LLM, especially older versions of LLaMa tend to get 'overwhelmed' by too much input at a time)
    #Therefore, by chunking the data from the google sheet, it can filter out unsuitable positions, one manageable chunk at a time.
    results = []
    for chunk in chunk_dataframe(df, 25):
        user_prompt = create_user_prompt(chunk)
        result = query_llama(system_prompt, user_prompt)
        results.append(result)

    # 3. Merge and save
    final_output = "\n\n".join(results)
    save_response_as_html(final_output, "html_output.htm")

if __name__ == "__main__":
    run()