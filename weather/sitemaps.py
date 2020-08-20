from weatherapp.models import City

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse, translate_url


class ForecastSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    i18n = True

    def __get(self, name, obj, default=None):   # Sitemap method from django.contrib.sitemaps
        try:
            attr = getattr(self, name)
        except AttributeError:
            return default
        if callable(attr):
            return attr(obj)
        return attr

    def _urls(self, page, protocol, domain):  # modified Sitemap method from django.contrib.sitemaps
        urls = []
        latest_lastmod = None
        all_items_lastmod = True  # track if all items have a lastmod
        for item in self.paginator.page(page).object_list:
            loc = "%s://%s%s" % (protocol, domain, self.__get('location', item))
            priority = self.__get('priority', item)
            lastmod = self.__get('lastmod', item)
            if all_items_lastmod:
                all_items_lastmod = lastmod is not None
                if (all_items_lastmod and (latest_lastmod is None or lastmod > latest_lastmod)):
                    latest_lastmod = lastmod
            url_info = {
                'item': item,
                'location': loc,
                'lastmod': lastmod,
                'changefreq': self.__get('changefreq', item),
                'priority': str(priority if priority is not None else ''),
            }
            # adding link translations to all LANGUAGES
            translations = {}
            for lang_code in settings.LANGUAGES:
                lng = lang_code[0]
                translations[lng] = translate_url(loc, lng)
            url_info['translations'] = translations
            # added
            urls.append(url_info)
        if all_items_lastmod and latest_lastmod:
            self.latest_lastmod = latest_lastmod
        return urls

    def items(self):
        return City.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()


class StaticSitemap(Sitemap):
    priority = 1
    changefreq = 'daily'
    i18n = True

    def items(self):
        return ['weatherapp:index']

    def location(self, item):
        return reverse(item)
