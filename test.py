from tweety import Twitter


def main():
    tw = Twitter('bth')
    uinfo = tw.get_user_info('elonmusk')
    print(uinfo.profile_image_url_https)

if __name__ == "__main__":
    main()