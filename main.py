import gspread
import os
import openai
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
load_dotenv()

def getSpredsheetData(client) -> list:
    """
    Get data from Google Spredsheet data.
    Args:
        client: gspread client
    Returns
        sheetdata: list
    """
    workbook = client.open_by_key(os.getenv('SHEET_ID'))
    worksheet = workbook.worksheet(os.getenv('BASE_DATA_SHEET_NAME'))

    return worksheet.get_all_records()

def updateSpredsheet(client, record, gptResponse) -> None:
    """
    Update sales mail template to spredsheet
    Args:
        client: gspread client
        record: input base data record
        gptResponse: str : gpt response
    Returns:
        None
    """
    workbook = client.open_by_key(os.getenv('SHEET_ID'))
    worksheet = workbook.worksheet(os.getenv('OUTPUT_SHEET_NAME'))

    celldata = [
        gptResponse
    ]
    worksheet.append_row(celldata)

def callGpt(content: str) -> str:
    """
    Call Chat-GPT
    Args:
        content: str : order text to gpt
    Returns:
        responce: str
    """
    openai.api_key = os.getenv('OPEN_AI_API_KEY')
    response = openai.ChatCompletion.create(
        model = os.getenv('GPT_MODEL'),
        # temperature = 0.5,
        messages=[
            {
                "role": "user",
                "content": content
            },
        ],
    )
    return response.choices[0]["message"]["content"].strip()

def makeOrderContent(record):
    """
    make order text to gpt
    """
    filename = '/app/order.txt'
    with open(filename, 'r') as f:
        body = f.read()
    output = f'''\
        {body.format(
            hoge = record['hoge'],
            fuga = record['fuga'],
        )}
    '''.strip()
    return output

def main():
    jsonfile = '/app/' + os.getenv('JSON_KEY_FILE')
    scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(jsonfile, scope)
    client = gspread.authorize(creds)

    sheetdata = getSpredsheetData(client)
    for record in sheetdata:
        content = makeOrderContent(record)
        response = callGpt(content)
        updateSpredsheet(client, record, response)

if __name__ == "__main__":
    main()
