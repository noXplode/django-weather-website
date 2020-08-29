# django-weather-website
Weather forecast website. Multilingual Django website, with autocomplete search field, IP geolocation, API using django rest framework. Adaptive design via Bootstrap. With useful weather forecast graph, XML sitemap for multilingual website.
Live at [noxplode.pythonanywhere.com](https://noxplode.pythonanywhere.com/)

## Description
Weather and forecast data is requested using [Openweathermap.com API](https://openweathermap.org/api). IP geolocation data provided by GeoLite2, from [maxmind.com](https://dev.maxmind.com/geoip/geoip2/geolite2/). Website is multilingual: EN, RU, UA. Main page contains autocomplete field with search available in all three languages. Cities picked by user are saved in django sessions. User`s city detected by IP geolocation is stored in sessions automatically. So user can add cities to his list and delete cities from it. Forecast page has a table with 24 hour forecast, and 5 days forecast graph using [Zingchart](https://www.zingchart.com). Added [DRF](https://www.django-rest-framework.org/) API to get cities list, city weather and city forecast.

Website has 15000+ cities in database.
GeoIP location will not work without GeoLite2 databases (GeoLite2-City.mmdb and GeoLite2-Country.mmdb)
Users IP detection is made for pythonanywhere: request.META.get('HTTP_X_REAL_IP') 





