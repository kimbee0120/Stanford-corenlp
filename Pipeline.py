from pycorenlp import StanfordCoreNLP
import json
import stanza
import csv

# java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,parse,sentiment" -port 9000 -timeout 50000

nlp = StanfordCoreNLP('http://localhost:9000')
nlp2 = stanza.Pipeline('en') # initialize English neural pipeline


list = [["subreddit","score","body","date_time","stanford_coreNLP", "stanford_each_score", "stanza", "stanza_score"]]

file_name = '2020-01-24.csv'

#file open & read
with open('./Jan2020/2020-01-24.csv','r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    try:
        for row in reader:
            text = row['body']
            text = text.replace("%", " ")
            result = nlp.annotate(text,
                            properties={
                                'annotators': 'sentiment, ner, pos',
                                'outputFormat': 'json',
                                'timeout': 50000,
                            })
            avg = 0
            per_score = ""
            #Sentiment Analysis 
            for sentence in result["sentences"]:
                avg += int(sentence["sentimentValue"])-1
                per_score = per_score + str(int(sentence["sentimentValue"])-1)
            
            
            per_score = ','.join(per_score) #stanford each score
            avg = avg/len(result["sentences"]) #stanford avg

            #stanza
            doc = nlp2(text)

            stanza_avg = 0
            stanza_score = ""

            for i, sentence in enumerate(doc.sentences):
                stanza_avg += int(sentence.sentiment)
                stanza_score = stanza_score + str(sentence.sentiment)

            stanza_score = ','.join(stanza_score) #stanza each score
            stanza_avg = stanza_avg/len(doc.sentences) #stanza avg

            # list = [["subreddit","score","body","date_time","stanford_coreNLP", "stanford_each_score", "stanza", "stanza_score"]]

            sublist = [row['subreddit'],row['score'],row['body'],row['date_time'], str(avg), per_score, str(stanza_avg), stanza_score]
            print(sublist)

            list.append(sublist)
    except Exception as e:
        print(e)

# write csv file
with open("./NewData/Jan2020/"+file_name, 'w', newline='')as file:
        writer = csv.writer(file)
        writer.writerows(list)


# for s in result["sentences"]:
#     print("{}: '{}': {} (Sentiment Value) {} (Sentiment)".format(
#     s["index"],
#     " ".join([t["word"] for t in s["tokens"]]),
#     s["sentimentValue"], s["sentiment"]))

# #stanza
# nlp = stanza.Pipeline('en') # initialize English neural pipeline
# doc = nlp("Barack Obama was born in Hawaii.")

# for i, sentence in enumerate(doc.sentences):
#     print(i, sentence.sentiment) #0,1,2  0==neg 2==pos


# with open("/Users/JennyKim/Documents/Stanford-corenlp/result/test.txt", 'w', newline='')as file:
#         json.dump(result, file)



# StandfordCoreNLP-------------------------------------------
# #lemmatized
# for sentence in result["sentences"]:
#     for word in sentence["tokens"]:
#         print(word["word"] + " => " + word["lemma"])
# print("\n")

# #POS Tagging
# for sentence in result["sentences"]:
#     for word in sentence["tokens"]:
#         print (word["word"] + "=>" + word["pos"])

# print("\n")