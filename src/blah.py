with open("temp.txt") as f:
    acro_list = f.readlines()

acro_list = sorted(["\"" + acro.split('-')[0].strip() + "\"" + "," + "\n" for acro in acro_list])

with open("temp2.txt", "w") as f:
    f.writelines(acro_list)


acronyms = {
    "ADTV",
    "AMEX",
    "APR",
    "ARM",
    "BEA",
    "CAGR",
    "CAO",
    "CAPEX",
    "CB",
    "CD",
    "CFA",
    "CFM",
    "CFO",
    "CIA",
    "CISA",
    "CMA",
    "CMO",
    "CMP",
    "COB",
    "COO",
    "CPA",
    "CPP",
    "CSO",
    "CTO",
    "DJIA",
    "EFT",
    "EPS",
    "ETF",
    "FDIC",
    "FOREX",
    "FRB",
    "GDP",
    "GMP",
    "GNP",
    "IPO",
    "IRA",
    "IRA",
    "LLC",
    "LOI",
    "MMKT",
    "MTD",
    "NASDAQ",
    "NAV",
    "NCND",
    "NDA",
    "NEER",
    "NYSE",
    "P&L",
    "P/E",
    "PE",
    "PFD",
    "PPP",
    "PSP",
    "QTD",
    "QTE",
    "RBI",
    "REIT",
    "ROA",
    "ROCE",
    "ROE",
    "ROI",
    "ROIC",
    "RONA",
    "ROS",
    "SBA",
    "SEC",
    "SIV",
    "TSA",
    "TSR",
    "USA",
    "WC",
    "YTD",
    "YTM",
}

acronyms = sorted(["\"" + acro.lower() + "\"" + "," + "\n" for acro in acronyms])

with open("temp3.txt", "w") as f:
    f.writelines(acronyms)

word = "Minority-Owned"
if "-" in word:
    dash_pos = word.index("-")
    new_word = word[:dash_pos + 1] + word[dash_pos + 1].lower() + word[dash_pos + 2:]

print(new_word)
# text = 'abc-defg'
# print(text.index("-"))
# print(text[:4])
# print(text[5:])
# text = text[:4] + 'Z' + text[5:]
# print(text)