import time
import json
import random
import re

def main():
    
    dataID = 0
    data = {}
    
    with open('data.txt') as infile:
        line = infile.readline()
        while line:
            results = re.findall(r'N(\d+), ((-|\d|\.|)+), ((-|\d|\.|)+), ((-|\d|\.|)+), ((-|\d|\.|)+), ((-|\d|\.|)+), ((-|\d|\.|)+),', line)
            
            for result in results:
                data[dataID] = {
                'time': result[0],
                'xa': result[1],
                'ya': result[3],
                'za': result[5],
                'xg': result[7],
                'yg': result[9],
                'zg': result[11]
                }
                dataID += 1
            line = infile.readline()
        
   
    with open('../transferToAzure/data.json', 'w') as outfile:
        json.dump(data, outfile)
    
    print('\nOutput json data to file.')

if __name__ == "__main__":
    main()
