import praw
import pandas as pd

reddit = praw.Reddit(client_id='L9-zt9QYUdTufg', client_secret='RobVVmWuwz4Ec25a-Ngvt5p8wW8', user_agent='gangstalking_comments')

subreddit = reddit.subreddit('GangStalking')

comm_list = []
selftext_list = []
header_list = []
id_list = []
author_list = []

i = 0
for submission in reddit.subreddit('gangstalking').new(limit=10):
    submission.comments.replace_more(limit=None)
    comment_queue = submission.comments[:]  # Seed with top-level
    while comment_queue:
        header_list.append(submission.title)
        author_list.append(submission.author.name)
        id_list.append(submission.id)
        selftext_list.append(submission.selftext) #Here I AM trying to get the selftext
        comment = comment_queue.pop(0)
        comm_list.append(comment.body)
        t = []
        t.extend(comment.replies)
        while t:
            header_list.append(submission.title)
            author_list.append(submission.author.name)
            id_list.append(submission.id)
            selftext_list.append(submission.selftext)
            reply = t.pop(0)
            comm_list.append(reply.body)

df = pd.DataFrame(header_list)
df['selftext_list'] = selftext_list
df['author_list'] = author_list
df['id_list'] = id_list
df['comm_list'] = comm_list

df.columns = ['header','selftext','id','author','comments']
df['comments'] = df['comments'].apply(lambda x : x.replace('\n',''))
df['selftext'] = df['selftext'].apply(lambda x : x.replace('\n',''))
df['id'] = df['id'].apply(lambda x : x.replace('\n',''))
df['author_list'] = df['author'].apply(lambda x : x.replace('\n',''))
df.to_csv('GangStalking_comments_sept_4.csv',index = False)
