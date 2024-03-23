import chardet

with open("data.csv", 'rb') as f: 
    print(chardet.detect(f.read()))
    