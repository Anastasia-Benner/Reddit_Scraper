import praw, utils, time
import pandas as pd

def main():
    ## 1 load configuration and parameters
    parameters = utils.readJSONasDict('parameters.json')
    bot_config = utils.readJSONasDict('config.json')
    print('Loading parameters....', '\n', 'Loading config....')
    ## 2 use parameters to get list of post id's
    print('Gathering post id\'s....')
    post_list = []
    for sub in parameters['target_subs']:
        print(f'Scraping Sub :{sub}')
        if parameters['keywords'] == None:
            print('No Keywords in Parameters')
            post_list += utils.submissionIDList(sub=sub, before=parameters['before'], after=parameters['after'])
        else:
            for keyword in parameters['keywords']:
                print(f"Query term: {keyword}")
                post_list += utils.submissionIDList(sub=sub, q=keyword, before=parameters['before'], after=parameters['after'])
                time.sleep(1)
    print('Done')
    ## 2.5 remove duplicate id's
    post_list = utils.removeDupes(post_list)
    ## 3 use list of id's to get posts and write to files

    reddit = praw.Reddit(client_id=bot_config['client_id'],
                        client_secret=bot_config['client_secret'],
                        user_agent=bot_config['user_agent'],
                        password=bot_config['password'],
                        username=bot_config['username'])

    postDF = pd.DataFrame(columns=['post_id','post_selftext','post_title','post_score','subreddit', 'post_created_time'])
    commentDF = pd.DataFrame(columns=['comment_id', 'comment_text', 'post_id', 'parent_comment_id', 'comment_score'])

    for post in post_list:
        p = reddit.submission(id=post)
        print("Working on sumbission: ", post)
        df_row = pd.DataFrame({'post_id': [post],
                               'post_selftext': [p.selftext],
                               'post_title': [p.title],
                               'post_score': [p.score],
                               'subreddit': [p.subreddit.display_name],
                               'post_created_time': [p.created_utc]})

        postDF = postDF.append(df_row, ignore_index=True)
        print('Collecting comments for submission: ', post)
        p.comments.replace_more(limit=0)
        for comment in p.comments.list():
            df_row = pd.DataFrame({'comment_id': [comment.id],
                                   'comment_text':[comment.body],
                                   'post_id':[comment.link_id],
                                   'parent_comment_id':[comment.parent_id],
                                   'comment_score':[comment.score]})
            commentDF = commentDF.append(df_row, ignore_index=True)

    ## 4 save files
    print('Saving...')

    if parameters['convert_timestamp']:
        postDF['post_created_time'] = pd.to_datetime(postDF['post_created_time'], unit='s')

    postDF.to_csv('output/' + parameters['posts_filename'], mode=parameters['save_mode'])
    commentDF.to_csv('output/' + parameters['comments_filename'], mode=parameters['save_mode'])

    print('Done')

if __name__ == "__main__":
    main()
