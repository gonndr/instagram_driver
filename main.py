from instagram_bot import InstagramBot
import os


def main():
    insta_bot = InstagramBot()
    insta_bot.login()

    handle = os.environ["USERNAME"]

    followers = insta_bot.find_followers(handle)

    following = insta_bot.find_following(handle)

    # common_people = list(set(following).intersection(followers))

    people_not_following_back = list(set(following)-set(followers))

    print(f"You have {0} people not following back", len(people_not_following_back))

    with open("people_not_following_back.txt", "w") as file:
        for person in people_not_following_back:
            file.write(person + "\n")


if __name__ == "__main__":
    main()