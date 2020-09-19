# # Research_Scraping
Scraping reddit posts by keywords and collecting comment text

*Getting Started:*
To begin make sure you have Python 3 installed on your machine with pip.
Then use your terminal to navigate to the Research_Scraping directory and run:

    pip install -r requirements.txt

This will install the libraries that this program needs.

(if you have multiple versions of python you may need to specify as:
  pip3 install -r requirements.txt)


*Configuration:*
Notice the files config.json and parameters.json

Config.json stores authentication information. It currently has my own credentials,
but if you want to add your own follow the steps here:

https://docs.google.com/forms/d/e/1FAIpQLSezNdDNK1-P8mspSbmtC2r86Ee9ZRbC66u929cG2GX0T9UMyw/viewform

https://www.reddit.com/prefs/apps


Parameters.json hold the values used to query posts. The values are as follows:

  target_subs - list of subreddits to query. Must be in the form of:
      ["sub1", "sub2", "sub3"]

  before/after - The query will return posts between these dates.

  convert_timestamp - if true, stores post_created_time in the format yyyy-MM-dd hh:mm:ss
    if false stores value in unix time

  keywords - list of search terms to query. Terms should follow the same format as
      target_subs. i.e. ["term", "word", "other words"].
      To make a query without keyword searches set it as null.

  comments_filename/posts_filename - Stores the file names for the comments and posts.
      files will always be placed in the output folder so only give the file names and not a full path.

  save_mode - if the file already exists this value dictates the save behavior.

    "a": append mode will add values to the file.

    "w": write mode will overwrite the file.


*Running:*
In terminal, navigate to the Research_Scraping directory and run:

    py main.py

    (if this doesn't work try: python main.py)
