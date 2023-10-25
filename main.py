from instagram_bot import InstagramDriver
import time


def main():
    insta_bot = InstagramDriver()
    try:
        insta_bot.login()  # not needed if already logged in
    finally:
        insta_bot.navigate_to_profile()
    followers_list = insta_bot.get_list_of('followers')
    following_list = insta_bot.get_list_of('following')

    not_following_back_list = list(set(following_list)-set(followers_list))
    not_following_back_list_count = len(not_following_back_list)

    print(f"You have {not_following_back_list_count} people not following back")

    with open("users_not_following_back.txt", "w") as file:
        for person in not_following_back_list:
            file.write(person + "\n")

    time.sleep(100)


if __name__ == "__main__":
    main()