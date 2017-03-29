# main method
import copy
import xx
# from Instagram-API-python/InstagramAPI import InstagramAPI
import pymongo
import queue
import time
import os
import sys
from bson.objectid import ObjectId
import pprint
sys.path.append('Instagram-API-python')
from InstagramAPI import InstagramAPI
import dictionaries
import getpass

# main routine for instagram ascertain & repost
def main():

    # choose post dictionary
    post_dictionary = dictionaries.choose_dictionary()

    # acquire all new content from dictionary, fill queue for posting
    xx.acquire_all(post_dictionary)


    # login to session throigh instagram api
    print('input username')
    IGUSER = input()


    print('input password')
    # PASSWD = input()
    PASSWD = getpass.getpass()


    # call to api
    igapi = InstagramAPI(IGUSER,PASSWD)

    # start the mongo client, access the posts database
    client = pymongo.MongoClient()
    db = client.post_database
    posts = db.posts

    # declare & fill the queue with ObjectId types, corresponding to the values contained in the post_map
    q = queue.Queue()

    # q = fill_queue(q)
    with open("post_map", "r") as f:
        map_content = f.readlines()

    # print(map_content)
    for x in map_content:
        # print('x : ', x)
        # y = x.clone()
        y = copy.copy(x)
        y = y.replace("\n", "")
        q.put(ObjectId(y))


    # igapi.login() # login
    i=0
    igapi.login() # login
    while not q.empty():

        # pprint.pprint(posts.find_one({"_id":q.get()}))
        entry = q.get()
        p = posts.find_one({"_id":entry})

        entry_filter = str(entry)
        # print('map content : ', map_content)
        # print('entry filter: ', entry_filter)
        # entry_filter = entry_filter.replace("ObjectId('", "")
        # entry_filter = entry_filter.replace("'", "")
        # remove the dequeued() entry from the list
        map_content.remove(entry_filter+"\n")

        # open the post_map file, and write back the remaining entries
        with open("post_map", "w") as f:
            for x in map_content:
                f.write(x)

        print('posting next, #'+str(i))
        print(p['image_path'])

        # filter hashtags from description
        descript_list = p['description'].split(' ')
        for x in descript_list:
            if x[:1] == '#'
        igapi.uploadPhoto(p['image_path'], "source : @"+p['username']+" - '"+p['description']+"'")

        # media_id = igapi.uploadPhoto(p['image_path'], p['username']+" - "+p['description'])
        # with open("live_posts", "a") as f:
        #     f.write(media_id+"\n")


        # sleep until next post

        time.sleep(40)
        i+=1
    # log out of session
    igapi.logout()

def fill_queue(q):
    with open("post_map", "r") as f:
        map_content = f.readlines()

    # print(map_content)
    for x in map_content:
        # print('x : ', x)
        x = x.replace("\n", "")
        q.put(ObjectId(x))


    # pprint.pprint(posts.find_one({"_id":pidd}))

    return q
if __name__=="__main__":
    main()
