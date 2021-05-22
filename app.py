from flask import *
import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import re
from string import punctuation
from num2words import num2words
import pyttsx3

app=Flask(__name__) # #instance of this flask class __name__ return main if u r at this python script whereas if import to other python script then will return name of that script 



@app.route("/") #'/ = if we r at current directory '
def upload():
    
    return render_template("file_upload.html") #return whole html file 


@app.route("/success",methods=["POST"])
def success():
    global file
    f=request.files['file']
    file=f.filename
    f.save(file)
    return render_template("success.html",name=file)

@app.route("/convert",methods=["GET"])
def convert():
    pdfReader=PyPDF2.PdfFileReader(file)  
    mytext=""
    for pageNum in range(pdfReader.numPages):
        pageObj=pdfReader.getPage(pageNum)   
    
        mytext +=pageObj.extractText()
    tokenized_text=sent_tokenize(mytext)
    stop_words=set(stopwords.words("english"))
    filtered_sent=[]
    for w in tokenized_text:
        if w not in stop_words:
            filtered_sent.append(w)
            
    ps = PorterStemmer()

    stemmed_words=[]
    for w in filtered_sent:
        stemmed_words.append(ps.stem(w))
    listToStr = ' '.join([str(elem) for elem in stemmed_words])    
    story_str=listToStr
    
    def remove_urls(text):

        url_pattern = r'https?://\S+|www\.\S+'
        without_urls = re.sub(pattern=url_pattern, repl=' ', string=text)
        return without_urls
    ex_urls =story_str
    urls_result = remove_urls(ex_urls)
    
    
    def remove_punctuation(text):
        return text.translate(str.maketrans('', '', punctuation))
    ex_punct = story_str
    punct_result = remove_punctuation(ex_punct)
    
    # Python3 code to demonstrate working of 
    # Add space between Numbers and Alphabets in String 
    # using regex + sub() + lambda 
    test_str = punct_result

    # using sub() to solve the problem, lambda used tp add spaces 
    res = re.sub("[A-Za-z]+", lambda ele: " " + ele[0] + " ", test_str) 
    sep_str=str(res)
    
    def num_to_words(text):

    # splitting text into words with space
        after_spliting = text.split()

        for index in range(len(after_spliting)):
            if after_spliting[index].isdigit():
                after_spliting[index] = num2words(after_spliting[index])

        # joining list into string with space
        numbers_to_words = ' '.join(after_spliting)
        return numbers_to_words

    # example text which contain numbers in it
    ex_numbers = sep_str
    # calling remove_numbers function with example text (ex_numbers)
    numners_result = num_to_words(ex_numbers)
    
    contraction = { 
    "ain't": "am not / are not / is not / has not / have not",
    "aren't": "are not / am not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he had / he would",
    "he'd've": "he would have",
    "he'll": "he shall / he will",
    "he'll've": "he shall have / he will have",
    "he's": "he has / he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how has / how is / how does",
    "I'd": "I had / I would",
    "I'd've": "I would have",
    "I'll": "I shall / I will",
     "I'll've": "I shall have / I will have",
     "I'm": "I am",
    "I've": "I have",
    "isn't": "is not",
    "it'd": "it had / it would",
    "it'd've": "it would have",
    "it'll": "it shall / it will",
    "it'll've": "it shall have / it will have",
    "it's": "it has / it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she had / she would",
    "she'd've": "she would have",
    "she'll": "she shall / she will",
    "she'll've": "she shall have / she will have",
    "she's": "she has / she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so as / so is",
    "that'd": "that would / that had",
    "that'd've": "that would have",
    "that's": "that has / that is",
    "there'd": "there had / there would",
    "there'd've": "there would have",
    "there's": "there has / there is",
    "they'd": "they had / they would",
    "they'd've": "they would have",
    "they'll": "they shall / they will",
    "they'll've": "they shall have / they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we had / we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what shall / what will",
    "what'll've": "what shall have / what will have",
    "what're": "what are",
    "what's": "what has / what is",
    "what've": "what have",
    "when's": "when has / when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where has / where is",
    "where've": "where have",
    "who'll": "who shall / who will",
    "who'll've": "who shall have / who will have",
    "who's": "who has / who is",
    "who've": "who have",
    "why's": "why has / why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you had / you would",
    "you'd've": "you would have",
    "you'll": "you shall / you will",
    "you'll've": "you shall have / you will have",
    "you're": "you are",
    "you've": "you have"
    }
    contractions_re = re.compile('(%s)' % '|'.join(contraction.keys())) 
    def expand_contractions(s, contractions_dict=contraction):
        def replace(match):
            return contractions_dict[match.group(0)]
        return contractions_re.sub(replace, s)
    expand_contractions(numners_result)
    final_story=expand_contractions(numners_result)
    
    def text_to_speech(text, gender):
 
        voice_dict = {'Male': 0, 'Female': 1}
        code = voice_dict[gender]

        engine = pyttsx3.init()

        # Setting up voice rate
        engine.setProperty('rate', 125)

        # Setting up volume level  between 0 and 1
        engine.setProperty('volume', 0.8)

        # Change voices: 0 for male and 1 for female
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[code].id)

        #engine.say(text)
        engine.save_to_file(text, 'convert.mp3')
        engine.runAndWait()
     
    text = final_story
    gender = 'Female'  # Voice assistant 
    text_to_speech(text, gender)
    speech=text_to_speech(text, gender)

    
    return render_template("convert.html",text=speech)
        
   
if __name__ == "__main__":
    import warnings
    warnings.warn("use 'python -m nltk', not 'python -m nltk.downloader'",         DeprecationWarning)
    app.run_server(debug=True)
    

