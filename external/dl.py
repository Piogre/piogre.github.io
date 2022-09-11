import urllib.request
import html.parser
html_parser = html.parser.HTMLParser()
#set these things
print("Set code for lookup (lower case):")
setcodesmall = input()
print("Set code for saving (UPPER CASE):")
setcodebig = input()
#good

#find card names and numbers
try:
    response = urllib.request.urlopen('https://scryfall.com/sets/' + setcodesmall + '?as=grid')
except:
    print("couldn't retrieve set page")
    quit()
lines = response.readlines()
response.close()
setnumberlist=[]
repeatlist={}
for line in lines:
    line = str(line)
    line = line[2:]
    line = line.strip()
    if line[0:63] == '<a class="card-grid-item-card" href="https://scryfall.com/card/':
        line=line[64+len(setcodesmall):]
        line=line[:line.index('/')]
        setnumberlist.append(line)
    if line[0:64] == '<span class="card-grid-item-invisible-label" aria-hidden="true">':
        line=line[64:]
        line=line[:line.index('<')]
        if line in repeatlist:
            repeatlist[line] = repeatlist[line]+1
        else:
            repeatlist[line] = 1

#get each card image
imagecounter={}
for i in setnumberlist:
    if True:
        number = i
        name = "error" + number
        url = "error" + number
        try:
            response = urllib.request.urlopen('http://scryfall.com/card/' + setcodesmall + '/' + number + '.html')
        except:
            print("oops", number)
        lines = response.readlines()
        response.close()
        for line in lines:
            line = str(line)
            line = line.strip()
            if line[0:37] == "b\'<meta property=\"og:title\" content=\"":
                endgap = -7
                name = line[37:endgap]
                name = html_parser.unescape(name)
                if name in repeatlist:
                    if repeatlist[name] > 1:
                        if name in imagecounter:
                            imagecounter[name] = imagecounter[name]+1
                        else:
                            imagecounter[name] = 1
                        name = name+str(imagecounter[name])
            elif line[0:74] == "b\'<meta property=\"og:image\" content=\"https://img.scryfall.com/cards/large/":
                endgap = -18
                url = "https://img.scryfall.com/cards/border_crop/" + line[74:endgap]
        print("getting card: " + name)
        try:
            urllib.request.urlretrieve(url, "C:\\Users\\Piogre\\AppData\\Local\\Forge\\Cache\\pics\\cards\\" + setcodebig + "\\" + name + ".full.jpg")
        except:
            print("oops", name)