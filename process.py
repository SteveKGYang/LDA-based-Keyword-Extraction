with open("stoppedWords.txt","r") as sf:
    words = sf.read()
    words = words[1:-1]
    finalwords = words.split("\",\"")
    with open("swords.txt","a") as f:
        for word in finalwords:
            f.write(word+"\n")
    f.close()
    sf.close()
