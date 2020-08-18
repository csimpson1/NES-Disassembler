from bs4 import BeautifulSoup
from collections import OrderedDict
from datetime import datetime
import ntpath
import re
import requests
import textwrap

def get_fname(fPath):
    """
    Get just the filename of the path. Will run into issues if we try
    to parse windows filepaths on linux using the os module so we 
    use ntpath instead
    """
    
    splitPath = ntpath.split(fPath)
    return splitPath[1] or ntpath.basename(splitPath[0])

def format_string(s):
    newString = s.replace(',', '_')
    newString = re.sub(r'\W+', '', newString)
    return newString

def get_opcodes(url):
    """
    Scrape the page at the URL and return a dictionary
    containing opcode information
    """
    nesCpuOpcodeRef = requests.get(url)
    soup = BeautifulSoup(nesCpuOpcodeRef.text, 'html.parser')
    
    opcodeHeadings = soup.find_all('h3')
    tables = soup.find_all('table')[1:]
    
    #opcodes = {}
    opcodes = [0 for i in range(256)]
    
    
    for i in range(len(opcodeHeadings)):
        heading = opcodeHeadings[i]
        textToParse = heading.text.split('-')
        opName = textToParse[0]
        opShortDesc = textToParse[1]
        
        
        #TODO: include the register effects somewhere
        #opRegEffects = tables[2*i]
        opHexCodes = tables[2*i+1]
        
        
        for row in opHexCodes.find_all('tr')[1:]:
            cols = row.find_all('td')
            #print(cols)
            """
            Page layout:
            Addressing Mode | Opcode | Bytes | Cycles
            
            We only care about the additional number of bytes the operation will take
            and for now we have no use for the cycles
            """
            
            
            
            addressingMode = format_string(cols[0].text)
            opcode = int('0x' + format_string(cols[1].text), 16)
            additionalBytes = int(cols[2].text) - 1
            
            
            """
            When we eventually access this data in the disassembler, we'll be accessing based on the hex opcode value.
            We'll flatten the data to make getting all of the information we need one call, at the expense of duplicating 
            some data
            """
            
            opcodes[opcode] = {
                'opName':opName,
                'opShortDesc':opShortDesc,
                'addressingMode': addressingMode,
                'additionalBytes': additionalBytes
                }
    
    #TODO: Implment the unofficial opcodes
    for i in range(len(opcodes)):        
        if opcodes[i] == 0:
            opcodes[i] = {
                'opName':'SCF',
                'opShortDesc':' Stop, Catch Fire: Illegal Opcode',
                'addressingMode':'None',
                'additionalBytes':0
                }
    
    
    
    return opcodes

def store_opcodes(opcodes,fPath,url):
    """
    opcodes: A dictionary of opcodes for the 6502 processor
    fname: A location to store the dictionary
    
    Convert a python dictionary into a file containing an equivalent c struct
    """
    
    currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #Get just the file name, ignoring any path (windows or linux)
    
    fName = get_fname(fPath)
    #print(fName)
    
    header = f'''
    /*
    * {fName} was last generated from the data at {url} on {currentTime} 
    */
    
    '''
    
    
    opcodeStructDef ='''
    struct opcode {
        char opName[4];
        char opShortDesc[70];
        char addressingMode[15];
        int additionalBytes;
    };
    '''
    
    opcodesArrayDef = '''
    struct opcode opcodes[256] = {
    '''
   
    mainDef = '''
    int main() {
        return 0;
    }'''
    
    with open(fPath, 'w') as f:
        f.write(textwrap.dedent(header))
        f.write(textwrap.dedent(opcodeStructDef))
        f.write(textwrap.dedent(opcodesArrayDef))
        
        numOfOpcodes = len(opcodes)-1
        
        for i in range(numOfOpcodes):
            f.write(f'''{{"{opcodes[i]['opName']}", "{opcodes[i]['opShortDesc']}", "{opcodes[i]['addressingMode']}", {opcodes[i]['additionalBytes']}}},\n''')
            
        f.write(f'''    {{"{opcodes[numOfOpcodes]['opName']}", "{opcodes[numOfOpcodes]['opShortDesc']}", "{opcodes[numOfOpcodes]['addressingMode']}"}}\n''')
        f.write('};')
        
    
if __name__ == "__main__":
    url = 'http://obelisk.me.uk/6502/reference.html'
    opcodes = get_opcodes(url)
    store_opcodes(opcodes,'../src/opcodes.c',url)

