from urllib.request import urlopen
from bs4 import BeautifulSoup
from mathMLtoOP import *
import json
import nltk
import urllib.parse
import mathml2omml
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# unnecessary attributes to remove from mathml string
REMOVE_ATTRIBUTES = ["id", "xref", "type", "cd", "encoding"]

# Set up Beautiful Soup Parser
url = 'file:///C:/Users/brian/Desktop/MLP/Derivation-Tree/articles/0907.2648.html'
html = urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

########################################################
# SUMEDH'S PROGRAM To Parse MathML Block Equations     #
########################################################
'''
# Parse the URL to extract the local file path
url_parts = urllib.parse.urlparse(url)
local_path = urllib.parse.unquote(url_parts.path)

# Remove leading '/' if it exists
if local_path.startswith('/'):
    local_path = local_path[1:]

def toMathMLStrings(url):
    # Open the local file using the extracted path
    with open(url, "r", encoding="utf-8") as f:
        xml = f.read()
    
    soup = BeautifulSoup(xml, features='lxml')
    mathml_strings = []
    
    for mms in soup.find_all("math"):
        if "display" in mms.attrs and mms["display"] != "block":
            # Skip non-block equations
            continue

        for attr in REMOVE_ATTRIBUTES:
            # Remove unnecessary attributes
            [s.attrs.pop(attr) for s in mms.find_all() if attr in s.attrs]

        mathml_strings.append([mms.prettify(), mms.get("alttext", "")])

    return mathml_strings

mathml_strings = toMathMLStrings(local_path)

'''

########################################################

# Parse all block/numbered equations within Math paper
results = soup.findAll("math", {"display" : "block"})

# Test Trees
string2 = str(results[0])
string3 = str(results[1])

# Convert into OP Trees
root2 = toOpTree(string2)
root3 = toOpTree(string3)

# Custom In Order Traversal of Tree to parse through all Children nodes in order
def IOT(root):

    if root is None:
        return

    if root.children:
        # Traverse the leftmost subtree
        IOT(root.children[0])

        try:
            # Attempt to print the root.value, encoding and decoding as necessary
            print(root.value.encode('utf-8').decode('utf-8', 'ignore'))
        except UnicodeEncodeError:
            # Handle the UnicodeEncodeError gracefully
            print("Unable to print root.value due to encoding issue")

        # Traverse the next subtree, if it exists
        for i in range(1, len(root.children)):
            # Print the root value again
            try:
                # Attempt to print the root.value, encoding and decoding as necessary
                print(root.value.encode('utf-8').decode('utf-8', 'ignore'))
            except UnicodeEncodeError:
                # Handle the UnicodeEncodeError gracefully
                print("Unable to print root.value due to encoding issue")

            # Traverse the next subtree
            IOT(root.children[i])
    else:
        # If there are no children, just print the root value
        try:
            # Attempt to print the root.value, encoding and decoding as necessary
            print(root.value.encode('utf-8').decode('utf-8', 'ignore'))
        except UnicodeEncodeError:
            # Handle the UnicodeEncodeError gracefully
            print("Unable to print root.value due to encoding issue")

########################################################
# Previous IOT Attempt                                 #
########################################################
           
'''
    if root == None:
        return
    if len(root.children) > 0:
        IOT(root.children[0])
    try:
        # Attempt to print the root.value, encoding and decoding as necessary
        print(root.value.encode('utf-8').decode('utf-8', 'ignore'))
    except UnicodeEncodeError:
        # Handle the UnicodeEncodeError gracefully
        print("Unable to print root.value due to encoding issue")
    for i in range(1, len(root.children)):
        IOT(root.children[i])
        if i != len(root.children)-1:
            try:
                # Attempt to print the root.value, encoding and decoding as necessary
                print(root.value.encode('utf-8').decode('utf-8', 'ignore'))
            except UnicodeEncodeError:
                # Handle the UnicodeEncodeError gracefully
                print("Unable to print root.value due to encoding issue")
'''

########################################################

# Print in order traversal of Tree
IOT(root2)
#IOT(root3)

#TODO: Compare Trees to check for similar subtrees -> If similar to a certain degree, derivation is tree

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
for script in soup(['a']):                          # For all the tags that have 'a'
    if script.get('class') == ['ltx_ref']:          # If class tag is labelled with 'ltx_ref'
        script.insert_before("equationlink")        # Insert marker before each equation

# Get final processed text
text = soup.get_text(' ', strip=True)           # Strip whitespace from the beginning and end of each bit of text; No more '\n' in text
# Debugging for printing entire text
# print('Full Text: ', text)

# Remove References (Last) section
text = text.split("References")     # Split string at "References"
text = text[0]                      # Take only string before "References"

# Split String on Sentences
tokenized = sent_tokenize(text)
# Debugging for printing entire text w/o references AND split into sentences
# print('Text Split into Sentences: ', tokenized)

wordCount = []                                                  # Keeps track of # of words in each sentence; Use for para interval extension
for sentence in tokenized:                                      # For Each sentence in the text:
    totalWordCount = len(sentence.split())                      # Split the sentence on spaces and count # of words
    if len(wordCount) > 0:                                      # If sentence idx > 0,
        wordCount.append(totalWordCount+wordCount[-1])          # Add current word count with word count of setence previous
    else:           
        wordCount.append(totalWordCount)                        # Else, append normally

# Debugging for number of words in each sentence
# print(wordCount)

########################################################
# KEEP FOR NOW JUST IN CASE PART OF SPEECH IS NECESSARY#
########################################################

#for i in tokenized:
     
    # Word tokenizers is used to find the words
    # and punctuation in a string
    #wordsList = nltk.word_tokenize(i)
 
    #  Using a Tagger. Which is part-of-speech
    # tagger or POS-tagger.
    #tagged = nltk.pos_tag(wordsList)
 
    #print(tagged)
    
########################################################

# Converting entire text to an array of strings/words
output = []
temp = ''
# Converting to array of strings
for i in range(len(text)):
    temp += (text[i])                   # Adding chars together until find a space
    if text[i] == ' ':                  # Once space is found,
        output.append(temp[:-1])        # Add string to output array 
        temp = ''
        continue
# Debugging for printing string array
# print('Text to Array of Strings: ', output)

# Creating an array of (equation #, line number) pairs
eqno = []
idx = 1                                 # All equations start from 1
asc = 97                                # Ascii for 'a'
# Checking for equations + line number
for i in range(len(output)):
    temp = str(idx)                     # Equation Number
    tempascii = str(idx) + chr(asc)     # Equation Number w/ subequation
    nextTemp = str(idx+1)               # Next Equation Number 
    nextAscii = str(idx+1) + 'a'        # Next Equation Number w/ subequation
    if i >= 1 and temp in output[i] and output[i-1] == 'mathequation':          # Equation is regular
        eqno.append([idx, i])
        idx += 1
        continue
    if i >= 1 and tempascii in output[i] and output[i-1] == 'mathequation':     # Equation has subequation
        eqno.append([str(idx)+chr(asc), i])
        asc += 1
        continue
    if i >= 1 and nextTemp in output[i] and output[i-1] == 'mathequation':      # Next equation no longer has a, b, c etc.
        eqno.append([idx+1, i])
        idx += 2
        asc = 97
        continue
    if i >= 1 and nextAscii in output[i] and output[i-1] == 'mathequation':     # Next equation moves onto next idx w/ subequation
        eqno.append([str((idx+1))+'a', i])
        idx += 2
        asc = 98
        continue
# Debugging for eqno
# print('Equation # + Index Pair: ', eqno)

# Insert Paragraph Breaks into the (Eq #, idx #) output array 
paraBreak = []                                      # New array with paragraph breaks
counter = 0                                         # Counter for current Word in PDF
temp = 0                                            # Placeholder for latest occurence of a paragraph break before equation
paragraph = 'parabreak'                             # Marker placed to locate paragraph breaks
for i in range(len(eqno)):                          # Iterating through (Eq, idx number) pairs
    for idx in range(counter, eqno[i][1]-1):        # Iterating through idx between previous Eq and current Eq
        currWord = output[idx]
        if paragraph == currWord:                   # If there is a parabreak marker...
            temp = idx                              # Set latest occurence of paragraph break
    paraBreak.append([(str(i+1)+'start'), temp])    # Append index to paragraph break list
    counter = eqno[i][1]                            # Set counter to start of next equation
    temp = eqno[i][1]                               # Set latest occurence of paragraph break to start of next equation

# Extend range of text from end of equation to one sentence after
exten = []                                                      # List for holding the chunks of text after the equation
for idx, eqNum in enumerate(eqno):                              # Index and (eq#, idx#) pair
    startIdx = eqNum[1]                                         # Start of the portion of text AFTER the equation

    ########################################################
    # SAVE CODE SINCE MAY NEED TO REVERT AND HARDCODE      #
    ########################################################
    #while '.' not in output[startIdx]:
        #if startIdx+2 < len(output)-1 and ('Eq' in output[startIdx+1] or 'Fig' in output[startIdx+1] or 'i.e.' in output[startIdx+1]):      # Break when there is period but also no Eq or Fig
            #startIdx += 2
            #continue
        #if idx+1 < eqno[len(eqno)-1][0] and startIdx+1 == paraBreak[idx+1][1]:       # If next index exists and If the paragraph for the next equation comes right after, skip this equation
            #break
    #startIdx += 1
    ########################################################

    wordIDX = 0                                                 # Counter for idx of wordCount array
    while wordCount[wordIDX] < startIdx:                        # Iterate through wordCount array until total words exceed current index (startIdx)
        wordIDX +=1                                             # Interval will go one more then necessary so
    sentenceEndIdx = wordCount[wordIDX]                         # Set end interval to wordCount[wordIDX-1]
    exten.append([str(eqno[idx][0])+'end', sentenceEndIdx])     # Append current index as end of section

# Debugging for paragraph breaks
#print("Paragraph breaks: ", paraBreak)
#print("No Paragraph breaks: ", eqno)
#print("Paragraph extension: ", exten)

'''
root = toOpTree(string2)

def IOT(root):
    if root == None:
        return
    # numsChildren = len(root.children)
    print('hello')
    #IOT(root.children[0])
    print(root.value.encode('utf-8').decode('utf-8', 'ignore'))
    for i in range(len(root.children)):
        IOT(root.children[i])
        print(root.value.encode('utf-8').decode('utf-8', 'ignore'))
'''

