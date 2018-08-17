import tweepy

# from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from wagtail.core.signals import page_published

from webapp.blog.models import EntryPage


class AdminTwitter:
    "Classe per gestionar la api de twitter"
    # api = []

    def __init__(self, requestor):
        twitter_consumer_key = ''
        twitter_consumer_secret = ''
        twitter_access_key = ''
        twitter_access_secret = ''
        try:
            self.blog_page = requestor
            blog_page = self.blog_page
            if blog_page.twitter_enable_publish:
                twitter_consumer_secret = blog_page.twitter_consumer_secret if blog_page.twitter_consumer_secret \
                    else getattr(settings, 'TWITTER_CONSUMER_SECRET', '')
                twitter_consumer_key = blog_page.twitter_consumer_key if blog_page.twitter_consumer_key \
                    else getattr(settings, 'TWITTER_CONSUMER_KEY', '')
                twitter_access_secret = blog_page.twitter_api_secret if blog_page.twitter_api_secret \
                    else getattr(settings, 'TWITTER_ACCESS_SECRET', '')
                twitter_access_key = blog_page.twitter_api_key if blog_page.twitter_api_key \
                    else getattr(settings, 'TWITTER_ACCESS_KEY', '')
        except:
            print('Error! Failed on AdminTwitter class.')
            pass
        auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
        auth.set_access_token(twitter_access_key, twitter_access_secret)
        self.api = tweepy.API(auth)

    def send_tweet(self, message):
        api = self.api
        blog_page = self.blog_page
        api.update_status(status=message)

    # TODO buscar, seguidors i amics
    def get_public_tweets(self):
        api = self.api
        public_tweets = api.home_timeline()
        return public_tweets

    def get_twitter_followers(self):
        api = self.api
        blog_page = self.blog_page
        user = api.get_user(blog_page.twitter_owner)
        print (user.screen_name)
        print (user.followers_count)
        for friend in user.friends():
            print(friend.screen_name)

    def get_hastags(self,search_term, search_number=5):
        api = self.api
        # search_term = "#gamedev"
        # search_number = 2
        search_result = api.search(search_term, rpp=search_number)
        for i in search_result:
            print(i.text)


def receiver(sender, **kwargs):
    EntryPage = kwargs['instance']
    blog_page = EntryPage.blog_page
    m_hashtag = '#melindro_org'
    message = '"%s" %s %s' % (EntryPage.title[:135 - len(EntryPage.full_url) - len(m_hashtag)], m_hashtag, EntryPage.full_url)
    # public_t = AdminTwitter(blog_page).get_public_tweets()
    # for tweet in public_t:
    #    print tweet.text
    # AdminTwitter(blog_page).get_twitter_followers()
    if blog_page.twitter_enable_publish:
        AdminTwitter(blog_page).send_tweet(message)


# Register listeners for each page model class
# To listen to a signal, implement page_published.connect(receiver, sender, **kwargs).
# http://docs.wagtail.io/en/v1.6.2/reference/signals.html?highlight=signals
page_published.connect(receiver, sender=EntryPage)
