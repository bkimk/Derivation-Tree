from PyPDF2 import PdfReader
from string import ascii_lowercase as alc

reader = PdfReader('Barnett10.pdf')

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
eqno = []
inner_vec = []
idx = 1             # All equations start from 1
asc = 97            # Ascii for 'a'


# Checking for equations
for i in range(len(output)):
    temp = '(' + str(idx) + ')'
    tempascii = '(' + str(idx) + chr(asc) + ')'
    nextTemp = '(' + str(idx+1) + ')'
    nextAscii = '(' + str(idx+1) + 'a' + ')'
    if temp in output[i]:
        inner_vec = [idx, i]
        eqno.append(inner_vec)
        idx += 1
        continue
    if tempascii in output[i]:
        inner_vec = [str(idx)+chr(asc), i]
        eqno.append(inner_vec)
        asc += 1
        continue
    if nextTemp in output[i]:           # Next equation no longer has a, b, c etc.
        inner_vec = [idx+1, i]
        eqno.append(inner_vec)
        idx += 2
        asc = 97
        continue
    if nextAscii in output[i]:          # Next equation moves onto next idx
        inner_vec = [str((idx+1))+'a', i]
        eqno.append(inner_vec)
        idx += 2
        asc = 98
        continue


print(eqno)                             # Debugging
