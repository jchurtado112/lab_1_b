#Jesus Hurtado, CS 2302 - Data Structures, Lab1 Option B, Fall 2018
#Recursively retrieve comments from a Reddit app and classify them negative, neutral or positive.

# Importing nltk and praw libraries
import time
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw


#Information needed to be able to retrieve data from Reddit
reddit = praw.Reddit(client_id='__4mOrgmt2Yrkg',
                     client_secret='OWntaIo7NBKlEMYzdQl0zQcZoIE',
                     user_agent='jchurtado'
                     )

#Python module that will enable us to access comments
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

#Checking if negative
def get_text_negative_proba(text):
   return sid.polarity_scores(text)['neg']

#Checking if neutral
def get_text_neutral_proba(text):
   return sid.polarity_scores(text)['neu']

#Checking if positive
def get_text_positive_proba(text):
   return sid.polarity_scores(text)['pos']

#Retrieving submission comments from reddit
def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()

    return submission.comments

#Recursive method to iterate, classify and store comments
def process_comments(comments, negative, neutral, positive):
    
    for comment in comments:    #Iterate through the comments
        if len(comment.replies) > 0:    #Checks if there are more replies
            
            #Checks if negative, neutral or positive
            if get_text_negative_proba(comment.body) > 0.5:
                negative.append(comment.body)
            elif get_text_neutral_proba(comment.body) > 0.5:
                neutral.append(comment.body)
            else:
                if get_text_positive_proba(comment.body) > 0.5:
                    positive.append(comment.body)
                    
            #Recursive method is called to iterate to the next reply available
            process_comments(comment.replies, negative, neutral, positive)
                    
                    
    return   #Returns to main
                
    
def main():
    comm = get_submission_comments('https://www.reddit.com/r/nba/comments/9epqq4/say_a_positive_thing_about_a_player_you_hate/')
    
    negative_comments_list=[]   #Lists to store comments according to behavior
    neutral_comments_list=[]
    positive_comments_list=[] 
  
    #Calls method to start retrieving, classifying and storing comments
    start = time.time() #Starts the time
    process_comments(comm, negative_comments_list, neutral_comments_list, positive_comments_list)
    end = time.time()   #Ends the time
    time_elapsed = end - start
    
    #Prints the running time 
    print()
    print('##################################################################')
    print()
    print("This is the running time in seconds: {time}".format(time=round(time_elapsed, 4)))
    print()
    print('##################################################################')
    
    if len(negative_comments_list) > 0: #Will print negative comments if found
        print()
        print("-------------------------------------------------------------")
        print("Negative comments: ")
        for i in negative_comments_list:
            print()
            print(i)
   
    if len(neutral_comments_list) > 0:  #Will print neutral comments if found
        print()
        print("-------------------------------------------------------------")
        print("Neutral comments: ")
        for j in neutral_comments_list:
            print()
            print(j)
        
    if len(positive_comments_list) > 0: #Will print positive comments if found
        print()
        print("-------------------------------------------------------------")
        print("Positive comments: ") 
        for k in positive_comments_list:
            print()
            print(k)     
   
    
   
      
       
       
   
   

main()  #Calls main method
