import os

# os.system("python3 preprocessSentence.py")
# os.system("python3 runTagger.py") 
# print('Sentences Tagged!!')

# os.system("python3 clauseBoundary.py")
os.system("python3 postProcessing.py")
os.system("python3 segregateTaggedData.py") 
os.system("python3 storeClause.py")
os.system("python3 processInvalid.py")
print('Processing completed!!')