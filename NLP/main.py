from PyPDF2 import PdfReader

reader = PdfReader('Barnett.pdf')

# Holds char array of pdf
output = []

# Extracting text data
for i in range(len(reader.pages)):
    page = reader.pages[i]
    output.append(page.extract_text())

# Combining all pages of Mathematical Text
text = str(output)

# Output for string array; temp for holding strings; idx for current index 
output.clear()
temp = ''
idx = 0

# Converting to string array format opposed to char
for i in range(len(text)):
    temp += (text[i])
    if text[i] == ' ':
        output.append(temp[:-1])
        temp = ''
        continue
    if "\\n" in temp:
        output.append(temp[:-2])
        temp = ''
        continue

# Dictionary for key (eq. #) and value (index) is eqno
eqno = {}
idx = 1

# Checking for equations
for i in range(len(output)):
    temp = '(' + str(idx) + ')'
    if temp in output[i]:
        eqno[idx] = i
        idx += 1
        continue

print("done")

# Printing all strings to txt file
# with open("example.txt", "w") as f:
  # print(output, file=f)