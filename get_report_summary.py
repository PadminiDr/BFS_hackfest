import os
import PyPDF2
import time
import json
from IPython.display import clear_output
from openai import AzureOpenAI
    
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-05-01-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

assistant = client.beta.assistants.create(
  name="Financial Analyst Assistant",
  instructions="""
    As a Financial Analyst, you will leverage your expertise to generate tailored Financial Analysis Reports that cater to the specific requirements of clients. This role involves in-depth analysis of financial statements and market data to uncover insights into a company's financial performance and stability.
You will engage directly with clients to gather essential information and refine the report based on their feedback, ensuring that the final product precisely meets their needs and expectations.

Key Objectives:

Analytical Precision: Utilize analytical skills to interpret financial data, identify trends, and detect anomalies.
Effective Communication: Simplify and convey complex financial information in a clear and actionable manner for non-specialist audiences.
Client Focus: Tailor reports dynamically based on client feedback, aligning the analysis with their strategic goals.
Quality Assurance: Maintain the highest standards of quality and integrity in report generation, adhering to established benchmarks for analytical rigor.
Performance Indicators:

The effectiveness of the Financial Analysis Report is measured by its ability to provide actionable insights that support corporate decision-making, identify areas for operational improvement, and evaluate the company's financial health. Success is reflected in the report's contribution to informed investment decisions and strategic planning.
""",
  model=os.getenv("DEPLOYMENT_NAME"),
  # tools=[{"type": "file_search"}],
  temperature=0
)

# Create a thread
thread = client.beta.threads.create()


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.

    Args:
    pdf_path (str): Path to the PDF file.

    Returns:
    str: Extracted text from the PDF.
    """
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

input_context = extract_text_from_pdf("company/VLO-3Q23-Earnings-Release.pdf")

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"""The report will include the following sections and I want to extract the capital expenditure and other metric like 

Operating Activities "Change in Working Capital",
        "Net Cash from Operating Activities"
Investing Activities has "Acquisition of Fixed Assets & Intangibles",
        "Net Cash from Investing Activities"
Financing Activities includes "Dividends Paid",
        "Cash from (Repayment of) Debt",
        "Net Cash from Financing Activities",
Net Change includes  Net Change in Cash
Metadata includes "Report Date", "Publish Date", "Source"
Profitability Metrics like "EBITDA",
        "Gross Profit Margin",
        "Operating Margin",
        "Net Profit Margin",
        "Return on Equity",
        "Return on Assets",
        "Return On Invested Capital",
Liquidity Metrics include Current Ratio
Solvency Metrics like  "Total Debt", "Liabilities to Equity Ratio", "Debt Ratio",
Cash Flow Metrics like "Free Cash Flow", "Free Cash Flow to Net Income", "Cash Return On Invested Capital",
Other Important Metrics like "Piotroski F-Score", "Net Debt / EBITDA", "Dividend Payout Ratio
Capital Expenditure    

```Document
{input_context}
```
"""
)

thread_messages = client.beta.threads.messages.list(thread.id)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  #instructions="New instructions" #You can optionally provide new instructions but these will override the default instructions
)



start_time = time.time()

status = run.status

while status not in ["completed", "cancelled", "expired", "failed"]:
    time.sleep(5)
    run = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
    print("Elapsed time: {} minutes {} seconds".format(int((time.time() - start_time) // 60), int((time.time() - start_time) % 60)))
    status = run.status
    print(f'Status: {status}')
    clear_output(wait=True)

messages = client.beta.threads.messages.list(
  thread_id=thread.id
) 

print(f'Status: {status}')
print("Elapsed time: {} minutes {} seconds".format(int((time.time() - start_time) // 60), int((time.time() - start_time) % 60)))
# print(messages.model_dump_json(indent=2))

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

# print(messages.model_dump_json(indent=2))

data = json.loads(messages.model_dump_json(indent=2))  # Load JSON data into a Python object
op = data['data'][0]['content'][0]['text']['value']

print(op)  # Outputs: assistant-1YGVTvNzc2JXajI5JU9F0HMD