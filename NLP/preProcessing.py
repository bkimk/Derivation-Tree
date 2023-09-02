from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

url = 'file:///C:/Users/brian/Desktop/Derivation-Tree/NLP/articles/0907.2648.html'
html = urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

# Chug all math equations into a array of mathml
results = soup.findAll("math", {"display" : "block"})

for result in results:
    with open('list.json', 'w') as file:
        json.dump(str(result), file)
    break

# Replace MathML with the text "mathequation"
for script in soup(['math']):
    script.string = 'mathequation'

# Get rid of annoying citations
for script in soup(['cite']):
    script.extract()            # Removed

# Adding paragraph break markers (parabreak) before each paragraph
for script in soup(['p']):                      # For all the tags that have 'p'
    if script.get('class') == ['ltx_p']:        # If class tag is labelled with 'ltx_p'
        script.insert_before("parabreak")       # Insert marker before each paragraph

# Adding edge markers (edge) before each equation
for script in soup(['a']):                      # For all the tags that have 'a'
    if script.get('class') == ['ltx_ref']:      # If class tag is labelled with 'ltx_ref'
        script.insert_before("equationlink")       # Insert marker before each equation

# get text
text = soup.get_text(' ', strip=True)           #  strip whitespace from the beginning and end of each bit of text; No more '\n' in text

# Debugging for printing entire text
# print(text)

# Output for string array; temp for holding strings 
output = []
temp = ''

# Converting to string array format opposed to char
for i in range(len(text)):
    temp += (text[i])                   # Adding chars together until find a space
    if text[i] == ' ':                  # Once space is found,
        output.append(temp[:-1])        # Add string to output array 
        temp = ''
        continue

# Debugging for printing string array
# print(output)

# eqno array holds (equation #, line number) pair
eqno = []
idx = 1             # All equations start from 1
asc = 97            # Ascii for 'a'

# Checking for equations + line number
for i in range(len(output)):
    if output[i] == 'References' or output[i] == 'references':      # Marks the end of paper
        break
    temp = str(idx)                     # Equation Number
    tempascii = str(idx) + chr(asc)     # Equation Number w/ subequation
    nextTemp = str(idx+1)               # Next Equation Number 
    nextAscii = str(idx+1) + 'a'        # Next Equation Number w/ subequation
    if i >= 1 and temp in output[i] and output[i-1] == 'mathequation':                       # Equation is regular
        eqno.append([idx, i])
        idx += 1
        continue
    if i >= 1 and tempascii in output[i] and output[i-1] == 'mathequation':                  # Equation has subequation
        eqno.append([str(idx)+chr(asc), i])
        asc += 1
        continue
    if i >= 1 and nextTemp in output[i] and output[i-1] == 'mathequation':           # Next equation no longer has a, b, c etc.
        eqno.append([idx+1, i])
        idx += 2
        asc = 97
        continue
    if i >= 1 and nextAscii in output[i] and output[i-1] == 'mathequation':          # Next equation moves onto next idx w/ subequation
        eqno.append([str((idx+1))+'a', i])
        idx += 2
        asc = 98
        continue

# Debugging for 
# print(eqno)

# Insert Paragraph Breaks into the (Eq #, idx #) output array 

paraBreak = []                                  # New array with paragraph breaks
counter = 0                                     # Counter for current Word in PDF
temp = 0                                        # Placeholder for latest occurence of a paragraph break before equation
paragraph = 'parabreak'                         # Marker placed to locate paragraph breaks
for i in range(len(eqno)):                       # Iterating through (Eq, idx number) pairs
    for idx in range(counter, eqno[i][1]-1):     # Iterating through idx between previous Eq and current Eq
        currWord = output[idx]
        if paragraph == currWord:                   # If there is a parabreak marker...
            temp = idx                              # Set latest occurence of paragraph break
    paraBreak.append([(str(i+1)+'start'), temp])    # Append index to paragraph break list
    counter = eqno[i][1]                            # Set counter to start of next equation
    temp = eqno[i][1]                               # Set latest occurence of paragraph break to start of next equation

# Extend range of text from end of equation to one sentence after
exten = []                                      # List for holding the chunks of text after the equation
for idx, eqNum in enumerate(eqno):
    startIdx = eqNum[1]                         # Start of the portion of text AFTER the equation
    while '.' not in output[startIdx]:
        if startIdx+2 < len(output)-1 and ('Eq' in output[startIdx+1] or 'Fig' in output[startIdx+1] or 'i.e.' in output[startIdx+1]):      # Break when there is period but also no Eq or Fig
            startIdx += 2
            continue
        if idx+1 < eqno[len(eqno)-1][0] and startIdx+1 == paraBreak[idx+1][1]:       # If next index exists and If the paragraph for the next equation comes right after, skip this equation
            break
        startIdx += 1
    exten.append([str(eqno[idx][0])+'end',startIdx])      # Append current index as end of section



# Debugging for paragraph breaks
# print("Paragraph breaks: ", paraBreak)
# print("No Paragraph breaks: ", eqno)
# print("Paragraph extension: ", exten)
