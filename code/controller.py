import feedbin
import pinboard


feedbin_email = ''
feedbin_password = '' # base64 encode your password
pinboard_api_token = '' # base64 encode your api token

fb = feedbin.Feedbin(feedbin_email, feedbin_password)
pb = pinboard.Pinboard(pinboard_api_token)

fb.parse_stars()

for bookmark in fb.to_boomark:
    pb.add_post(bookmark)

fb.write_cache_data()

