import re
import json
text = open("raw.txt", encoding="utf-8").read()
prices = re.findall(r"\d+(?:[ \.,]\d{3})*,\d{2}", text)
# e.g., ['154,00', '308,00', '51,00', ..., '18 009,00']

lines = text.splitlines()
#merge lines ending with '-' (if a product name is hyphenated):
merged = []
i = 0
while i < len(lines):
    if lines[i].endswith('-'):
        merged.append(lines[i][:-1] + lines[i+1])
        i += 2
    else:
        merged.append(lines[i])
        i += 1

products = []
for idx, line in enumerate(merged):
    if re.match(r'^\d+\.$', line):
        #next line is product name:
        products.append(merged[idx+1].strip())
print(products)

total_match = re.search(r"ИТОГО:\s*([\d ]+,\d{2})", text)
if total_match:
    total = total_match.group(1)  # e.g. "18 009,00"
    print("Total:", total)

dt_match = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})", text)
if dt_match:
    datetime = dt_match.group(1)  # e.g. "18.04.2019 11:13:58"

method = None
if "Наличные" in text:
    method = "Наличные"
elif "Банковская карта" in text:
    method = "Банковская карта"
print("Payment method:", method)

parsed_data = {
    "prices": prices,
    "products": products,
    "total": total,
    "datetime": datetime,
    "payment_method": method
}
print(json.dumps(parsed_data, ensure_ascii=False, indent=2))