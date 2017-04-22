   #INSTABOTS#

# Imports requests library for handling HTTP requests.
import requests


# Access Token generated from Instabot servers.
Access_Token="2338013941.3fe8729.65d7a6c1f3f84fdbb2e2ac56150b5934"

# Base URL for every URL used in the file.
base_url="https://api.instagram.com/v1"


# information of owner #
def self_info():
    request_url=base_url+"/users/self/?access_token="+Access_Token
    my_info= requests.get(request_url).json()

    print" my user_name is :" + my_info['data']['full_name']
    #print my_info['data']['id']
    print "my profile picture is :" + my_info['data']['profile_picture']
    print("Media Shared            : ", my_info['data']['counts']['media'])
    print("Followed By             : ", my_info['data']['counts']['followed_by'])
    print("Followers               : ", my_info['data']['counts']['follows'])

self_info()
#https://api.instagram.com/v1/users/search?q=jack&access_token=ACCESS-TOKEN


#information of other users
def insta_users_search(user_name):
     # get user id
    if user_name not in ['gobind.gobind', 'just_rawat']:
         print"you enter wrong wrong username"
         return
    else:
            url_user = base_url + "/users/search?q=" + user_name + "&access_token=" + Access_Token  # https://api.instagram.com/v1/users/search?q=jack&access_token=ACCESS-TOKEN
            user_info = requests.get(url_user).json()
            sucess = user_info["meta"]["code"]
            if sucess == 200:  # checking url
                print "successsfully found user id "
                print"the insta_username is :" + user_info['data'][0]['full_name']
            else:
                print "unsucsessfull plz try again"
            return user_info["data"][0]["id"]

            # returning user id
    #print user_info['data'][0]['profile_picture']
#insta_users_search(user_name="gobind.gobind")



# recent post of users
def recent_post(insta_username):
    user_id=insta_users_search(insta_username)
    url_user = base_url + "/users/" + user_id + "/media/recent/?access_token=" + Access_Token   #https://api.instagram.com/v1/users/self/media/recent/?access_token=ACCESS-TOKEN
    #print url_user
    recent_posts=requests.get(url_user).json()
    print "recent posts of your entered user is :" + recent_posts['data'][1]['link']
    return recent_posts['data'][1]['id']

#recent_post(insta_username="just_rawat")


# function for like the post of ypur user added
def like_post(insta_username):
    post_id=recent_post(insta_username)
    #print post_id
    payload={"access_token":Access_Token}
    request_url=base_url+ "/media/" + post_id + "/likes"
    response_to_like=requests.post(request_url,payload).json()
    if response_to_like['meta']['code'] == 200:
        print("The post has been liked.")
        #print response_to_like
    else:
        print("Some error occurred! Try Again.")



#to post a comment on the recent post of the user
def post_comment(insta_username):
    media_id=recent_post(insta_username)
    payload=(base_url+"/media/%s/comments?access_token=%s") %(media_id,Access_Token)
    request_data={"access_token":Access_Token,'text':raw_input("enter your comment here")}
    comment_request=requests.post(payload,request_data).json()
    if comment_request['meta']['code'] == 200:
        print("your comment is successfully added.")
        print comment_request#["data"]["text"]
    else:
        print("Some error occurred! Try Again.")
    return comment_request['data']["id"]

#post_comment(insta_username="gobind.gobind")



#to read the comments on the post
#https://api.instagram.com/v1/media/{media-id}/comments?access_token=ACCESS-TOKEN
def get_comments(insta_username):
    media_id=recent_post(insta_username)
    request_data=base_url+ "/media/" + media_id +"/comments?access_token="+Access_Token
    comment=requests.get(request_data).json()
    return comment['data'][0]['id']
    print comment['data'][0]['text']
#get_comments(insta_username="gobind.gobind")




# to delete ypur comment on the post
#https://api.instagram.com/v1/media/{media-id}/comments/{comment-id}?access_token=Access_Token
def comment_del(insta_username):
    media_id = recent_post(insta_username)
    comment_id=post_comment(insta_username)
    #print comment_id
    request_url=base_url+ "/media/" + media_id + "/comments/" + comment_id+ "?access_token=" + Access_Token
    comments=requests.delete(request_url).json()
    if comments['meta']['code'] == 200:
        print("your comment is deleted. syccesfully")
        #print comments
    else:
        print("Some error occurred! Try Again.")
        print comments

def search_in_comment(username):
     word_to_be_searched = raw_input("Enter the word you want to search in comments of most popular post : ")
     post_id = recent_post(username)
     print(post_id)
     url = base_url + "/media/" + str(post_id) + "/comments/?access_token=" + Access_Token
     print(url)
     payload = requests.get(url).json()
     print(payload)
     list_of_comments = []
     for comment in payload['data']:
         list_of_comments.append(comment['text'])
     print(list_of_comments)


# Function to find Average Number of Words per Comment.
def find_average(post_id):
    no_of_words = 0
    list_of_comments = []
    comment_id = []
    url =base_url+"/media/"+str(post_id)+"/comments/?access_token="+Access_Token
    data = requests.get(url).json()
    if len(data['data']) == 0:
        print("no comments on this post")
        return
    else:
        for comment in data['data']:
            list_of_comments.append(comment['text']) #making a list if comments
            #print list_of_comments
            no_of_words += len(comment['text'].split())# calculating words in comment without counting spaces
            #print no_of_words
        average_words = float(no_of_words)/len(list_of_comments)
        print("\nAverage on the post = %.2f" % average_words)
        return








# Menu for the User to interact with the Instabot.

print("\nHello User! Welcome to the Instabot Environment.")
choice = 1
while choice != '9':
    print("\nWhat do you want to do using the bot?")
    print("1. Get the Details of the owner.")
    print("2. Get the username of the  Insta_User.")
    print("3. Get the recent post of the User.")
    print("4. Like a post of the User.")
    print("5. Comment on post of the User.")
    print("6. Delete the comment containing a particular word.")
    print("7. Get the average no. of words per comment in most insteresting post.")
    print("8. Exit.\n\n")

    choice = input("Enter Your Choice(1-9) : ")

    user_name = raw_input("enter users from the following  1.gobind.gobind and 2. just_rawat")

    # Perform Actions Depending on the User's Choice. Runs Until User wishes to Exit.
    #if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
    if int(choice) == 1:
        self_info()

    elif int(choice) == 2:
        insta_users_search(user_name)

    elif int(choice) == 3:
        recent_post(user_name)


    elif int(choice) == 4:
        like_post(user_name)

    elif int(choice) == 5:
        post_comment(user_name)

    elif int(choice) == 6:
        comment_del(user_name)

    elif int(choice) == 7:
        find_average(recent_post(user_name))
    print("\nWant to do more using Instabot?")
    ch = 'P'
    flag = 0
    while ch not in ['Y', 'N']:
        if flag != 0:
            print("Wrong Choice Entered. Try Again...")
        ch = input("\nEnter your choice (Y/N) :").upper()
        flag = 1
        if ch == 'N':
            break
    if ch == 'N':
        break
    elif choice == 8:
        pass
    else:
        print("\nWrong choice entered.... Try Again.")