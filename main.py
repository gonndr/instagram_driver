from instagram_bot import InstagramBot

insta_bot = InstagramBot()

handle = insta_bot.login()

followers = insta_bot.find_followers(handle)

following = insta_bot.find_following(handle)

print("Followers: ", len(followers))
print("Following: ", len(following))

# common_people = list(set(following).intersection(followers))

people_not_following_back = list(set(following)-set(followers))

print(people_not_following_back)

with open("people_not_following_back.txt", "w") as file:
    for person in people_not_following_back:
        file.write(person + "\n")
