import os
from openai import AzureOpenAI
import PyPDF2

def get_json(file_path):

    client = AzureOpenAI(
      azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
      api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
      api_version="2024-02-01"
    )

    # file_path = "company/VLO-3Q23-Earnings-Release.pdf"

    def extract_text_from_pdf(pdf_path):
        text = ""
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        return text

    input_context = extract_text_from_pdf(file_path)

    instructions = """
        As a Financial Analyst, you will leverage your expertise to generate tailored Financial Analysis Reports that cater to the specific requirements of clients. This role involves in-depth analysis of financial statements and market data to uncover insights into a company's financial performance and stability.
    You will engage directly with clients to gather essential information and refine the report based on their feedback, ensuring that the final product precisely meets their needs and expectations.

    Key Objectives:

    Analytical Precision: Utilize analytical skills to interpret financial data, identify trends, and detect anomalies.
    Effective Communication: Simplify and convey complex financial information in a clear and actionable manner for non-specialist audiences.
    Client Focus: Tailor reports dynamically based on client feedback, aligning the analysis with their strategic goals.
    Quality Assurance: Maintain the highest standards of quality and integrity in report generation, adhering to established benchmarks for analytical rigor.
    Performance Indicators:

    The effectiveness of the Financial Analysis Report is measured by its ability to provide actionable insights that support corporate decision-making, identify areas for operational improvement, and evaluate the company's financial health. Success is reflected in the report's contribution to informed investment decisions and strategic planning.
    """

    user_content = f"""The report will include the following sections and I want to extract the capital expenditure and other metric like 

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

    final_content = """Please provide the  company name, year and quarter, capital expenditure value in billions of US dollars in JSON format.
    Note: Only Json Data is required no other text is required.
    ```json

    """

    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": user_content}
    ]
    response = client.chat.completions.create(
        model = os.getenv("DEPLOYMENT_NAME"),
        messages = messages,
    )

    response = response.choices[0].message.content

    messages.append({"role": "assistant", "content":response.choices[0].message.content})
    messages.append({"role": "user", "content":final_content})

    response = client.chat.completions.create(
        model = os.getenv("DEPLOYMENT_NAME"),
        messages = messages,
    )   
    return response.choices[0].message.content
