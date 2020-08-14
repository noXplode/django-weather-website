from .models import City, Forecast, Popularity
from .forms import CityForm

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.gis.geoip2 import GeoIP2
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.db import connections

import requests
from dal import autocomplete
from datetime import datetime, timedelta
import pandas as pd
import json
import csv
import pycountry


class CityAutocomplete(autocomplete.Select2QuerySetView):       #autocomplete field class
    def get_queryset(self):
        qs = City.objects.all()
        if self.q:
            qs = qs.filter( Q(name_en__istartswith=self.q) | Q(name_ru__istartswith=self.q.capitalize()) | Q(name_uk__istartswith=self.q.capitalize()) ) 
            # search in 3 languages
        return qs

def GetCityIdbyName(cityname):
    try:     
        res = City.objects.filter(name_en=cityname)
        return res[0].id
    except:
        pass
         

def GetGeoIPCity(ip):
    g = GeoIP2()                            # geoipdict = {'city': 'Kharkiv', 'continent_code': 'EU', 'continent_name': 'Europe', 
                                            #'country_code': 'UA', 'country_name': 'Ukraine', 'dma_code': None,
                                            # 'is_in_european_union': False, 'latitude': 49.982, 'longitude': 36.2566, 
                                            # 'postal_code': '61145', 'region': '63', 'time_zone': 'Europe/Kiev'} 
    try:
        geoipdict = g.city(ip)
    except:
        geoipdict = {}            
    return geoipdict

def getwinddir(spd):
    if 0 <= spd <= 22.5:
        spdstr = _('С')
    elif 22.5 < spd <= 67.5: 
        spdstr = _('СВ')
    elif 67.5 < spd <= 112.5: 
        spdstr = _('В')
    elif 112.5 < spd <= 157.5: 
        spdstr = _('ЮВ')
    elif 157.5 < spd <= 202.5: 
        spdstr = _('Ю')
    elif 202.5 < spd <= 247.5: 
        spdstr = _('ЮЗ')
    elif 247.5 < spd <= 292.5: 
        spdstr = _('З')
    elif 292.5 < spd <= 337.5: 
        spdstr = _('СЗ')
    elif 337.5 < spd <= 360: 
        spdstr = _('С')
    else:
        spdstr = ''
    return spdstr

def getpopulars(days=365):  #gets last 30 picked cities for popular block
    l = Popularity.objects.filter(pickeddate__gt=timezone.now() - timedelta(days=days))[:30]
    l = list(set([i.city for i in l]))
    return l
    

def index(request):

    current_lang = get_language()
    url = 'https://api.openweathermap.org/data/2.5/weather'
    prms = {'id' : '',
            'units' : 'metric',
            'lang' : current_lang,
            'appid' : settings.OPW_API_KEY #API key
    }

    #c_ip = request.META['REMOTE_ADDR'] 
    c_ip = request.META.get('HTTP_X_REAL_IP')   #client ip discovery for pythonanywhere
    #c_ip = ''  #ip for django dev server

    added_cities = request.session.get('added_cities', [])

    geoipdata = GetGeoIPCity(c_ip)
    if geoipdata:
        print(geoipdata)
    if geoipdata and geoipdata['city'] is not None:           #if theres geoip city data for users ip
        if GetCityIdbyName(geoipdata['city']):      #looking for geoip cityname in db
            geoipdata['id'] = GetCityIdbyName(geoipdata['city'])
            if geoipdata['id'] not in added_cities:         #viewing geoip city by default
                added_cities = [geoipdata['id']] + added_cities
                request.session['added_cities'] = added_cities
    else:
        geoipdata = {}  #if theres no geoip data or no city in data
    
    #print(request.session['added_cities'])

    view_cities = []
    for cityid in added_cities:
        try:
            c = City.objects.get(pk=cityid)
        except City.DoesNotExist:
            messages.add_message(request, messages.WARNING , _('Несуществующий id. Обратитесь к администратору'))
            continue
        else:
            prms['id'] = c.opw_id     # OPW id
            try:
                res = requests.get(url, params=prms)
            except requests.ConnectionError:
                messages.add_message(request, messages.WARNING , _('Ошибка соединения'))
                continue
            else:
                #print(res.url)
                if res.status_code == 200:
                    res2 = res.json()
                    #print(res2)
                    winfo = {
                        'cityid': cityid,
                        'city': c.name, #res2['name'], 
                        'country': c.country, 
                        'descr': res2['weather'][0]['description'],
                        'icon': res2['weather'][0]['icon'],
                        'temp': res2['main']['temp'],
                        'temp_feels_like': res2['main']['feels_like'],
                        'pressure': round(res2['main']['pressure'] * 0.75006375541921),
                        'hum':res2['main']['humidity'],
                        'winds': round(res2['wind']['speed']),
                        'city_sunrise' : datetime.utcfromtimestamp(res2['sys']['sunrise'] + res2['timezone']).strftime("%H:%M") ,
                        'city_sunset' : datetime.utcfromtimestamp(res2['sys']['sunset'] + res2['timezone']).strftime("%H:%M")      
                    }
                    if 'deg' in res2['wind'] :
                        winfo['winddir'] = getwinddir( res2['wind']['deg'] )

                    if 'gust' in res2['wind'] and round(res2['wind']['gust']) > round(res2['wind']['speed']):
                        winfo['gust'] = round(res2['wind']['gust'])
                    
                    if 'rain' in res2 :
                        if '1h' in res2['rain']:
                            winfo['rain'] = res2['rain']['1h']
                        else:
                            winfo['rain'] = res2['rain']['3h']
                    view_cities.append(winfo)
                else:
                    messages.add_message(request, messages.WARNING , _('Ошибка запроса. Попробуйте позже'))
            
    form = CityForm()   # autocomplete form

    populars = getpopulars()

    context = { 'city_info' : view_cities, 
                'geoipdata' : geoipdata,  
                'form' : form ,
                'populars' : populars  } 

    return render(request, 'weatherapp/weather.html', context)

def addcityform(request):
    if request.method == 'POST' :
        return HttpResponseRedirect( reverse('weatherapp:addcity', args=(int(request.POST['picked_city'] ), ) ) )  
    else:
        return HttpResponseRedirect( reverse('weatherapp:index' ) )


def addcity(request, city_id):
    try:
        c = City.objects.get(pk = city_id)
    except City.DoesNotExist:
        messages.add_message(request, messages.WARNING , _('Несуществующий id. Обратитесь к администратору'))
    else:
        added_cities = request.session.get('added_cities', [])
        if c.pk not in added_cities:
            added_cities.append(c.pk)
            request.session['added_cities'] = added_cities
            Popularity(city = c).save()
            messages.add_message(request, messages.SUCCESS , str(_('Вы добавили ')) + c.name)
        else:
            messages.add_message(request, messages.INFO, c.name + str(_(' уже добавлен. Попробуйте другой')))
    finally:
        return HttpResponseRedirect(reverse('weatherapp:index'))

def deletecity(request, city_id):
    added_cities = request.session.get('added_cities', [])
    if city_id in added_cities:
        added_cities.remove(city_id)
        request.session['added_cities'] = added_cities
        messages.add_message(request, messages.INFO, City.objects.get(pk = city_id).name + str(_(' удален')))
    return HttpResponseRedirect(reverse('weatherapp:index'))

def getforecast(request, c):
    if c.forecast_set.all().order_by('-loadingtime').exists():
        f = c.forecast_set.all().order_by('-loadingtime')[0]
        if f.is_actual():       #if latest forecast is actual load form db
            res = f.forecastdata
            print('db')
        else:
            print('db to web')      #if latest forecast is outdated ask OPW
            res = getOPWforecast(request, c)
    else:
        print('web')    #if no forecast in db ask OPW
        res = getOPWforecast(request, c)

    if Forecast.objects.count() > 100:  #made for pythnoanywhere restrict db growth
        ids = Forecast.objects.values_list('pk', flat=True)[25:]
        Forecast.objects.filter(pk__in = ids).delete()
    return res
    

def getOPWforecast(request, c):
    current_lang = get_language()
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    prms = {'id' : c.opw_id,
            'units' : 'metric',
            'lang' : current_lang,
            'appid' : settings.OPW_API_KEY #API key
    }
    
    try:
        res = requests.get(url, params=prms).json()
    except requests.ConnectionError:
        messages.add_message(request, messages.WARNING , _('Ошибка соединения'))
        res = {}
    else:
        frct = Forecast(city=c, forecastdata=res)
        frct.save()
    finally:
        return res


def forecast(request, city_id): 
    try:
        c = City.objects.get(pk=city_id)
    except City.DoesNotExist:
        messages.add_message(request, messages.WARNING , _('Несуществующий id. Обратитесь к администратору')) 
        return HttpResponseRedirect( reverse('weatherapp:index' ) )
    else:
        res = getforecast(request, c)
        if res:
            city = {    'city_timeshift' : res['city']['timezone'],
                        'city_name' : c.name, # res['city']['name'],
                        'city_country' : c.country, 
                        'city_sunrise' : datetime.utcfromtimestamp(res['city']['sunrise'] + res['city']['timezone']).strftime("%H:%M") ,
                        'city_sunset' : datetime.utcfromtimestamp(res['city']['sunset'] + res['city']['timezone']).strftime("%H:%M")        }
            
            forecast = []

            for datapoint in res['list']:
                winfo = {
                        'timetext': datetime.utcfromtimestamp(datapoint['dt'] + city['city_timeshift']).strftime('%H:%M') ,
                        'datetext': datetime.utcfromtimestamp(datapoint['dt'] + city['city_timeshift']).strftime('%d.%m') ,
                        'timeunix': (datapoint['dt'] + city['city_timeshift']) * 1000 ,
                        'temp': datapoint['main']['temp'],
                        'icon': datapoint['weather'][0]['icon'],
                        'pressure': round(datapoint['main']['pressure'] * 0.75006375541921),
                        'humidity': datapoint['main']['humidity'],
                        'descr': datapoint['weather'][0]['description'],
                        'winds': datapoint['wind']['speed'],
                        'winddir': getwinddir( datapoint['wind']['deg'] ) ,
                    }
                if 'rain' in datapoint :
                    if '1h' in datapoint['rain']:
                        winfo['rain'] = datapoint['rain']['1h']
                    else:
                        winfo['rain'] = datapoint['rain']['3h']
                else:
                    winfo['rain'] = 0

                forecast.append(winfo)

            oneday = forecast[:9]   #first 9 for 24 hours

            forecastdf = pd.DataFrame(forecast)

            tempdata = list(forecastdf['temp'])
            timedata = list(forecastdf['timeunix'])     #graph x scale 
            raindata = list(forecastdf['rain'])
            pressuredata = list(forecastdf['pressure'])
            windsdata = list(forecastdf['winds'])

            xstart = timedata[0] // 43200000 * 43200000     #getting nearest 00:00 or 12:00 before first forecast in list UNIX format
            if timedata[-1] % 43200000 == 0:    #getting nearest 00:00 or 12:00 after last forecast in list UNIX format
                xfinish = timedata[-1]
            else:
                xfinish = timedata[-1] // 43200000 * 43200000 + 43200000

            temp_list = [ [timedata[i], tempdata[i]] for i in range(0, len(tempdata)) ]     #x,y data for graph
            rain_list = [ [timedata[i], raindata[i]] for i in range(0, len(raindata)) ] 
            pressure_list = [ [timedata[i], pressuredata[i]] for i in range(0, len(pressuredata)) ]
            winds_list = [ [timedata[i], windsdata[i]] for i in range(0, len(windsdata)) ]
            axis = [ _('Температура, °C') , _('Осадки, мм')  , _('Давление, мм.рт.ст.'), _('Ветер, м/с')]
            
            graph = { 'xstart' : xstart,
                    'xfinish' : xfinish,
                    'temp_list' : temp_list,
                    'rain_list' : rain_list,  
                    'pressure_list' : pressure_list,
                    'winds_list' : winds_list,
                    'axis' : axis
                    }

            context = {
                'city': city,
                'frcst': oneday,
                'graph': graph
            }

        else:
            context = {}

        return render(request, 'weatherapp/forecast.html', context) 
    


def robots_txt(request):    #for robots.txt
    lines = [
        "User-Agent: *",
        "Disallow:",
        "Sitemap: " +  request.build_absolute_uri(reverse('sitemap')),
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain") 

def dosm(request):
    return HttpResponseRedirect(reverse('weatherapp:index'))

def vacuum_db(request, using='default'):
    cursor = connections[using].cursor()
    cursor.execute("VACUUM")    
    return HttpResponseRedirect(reverse('weatherapp:index'))
   

def checkjson():    #checks city.list.json, gets {'county_alpha2_code': {'count': number, 'country_name' : str}}
    with open('city.list.json', 'r', encoding='utf-8') as read_file:
        data = json.load(read_file)
    
    cntrs = {}
    for city_in_data in data:
        t = city_in_data['country'] 
        if t in cntrs:
            cntrs[t]['count'] += 1
        else:
            cntrs[t] = {'count' : 1, 'name' : ''}
            
    for ccode in cntrs.keys():
        t = pycountry.countries.get(alpha_2=ccode)
        if t:
            cntrs[ccode]['name'] = t.name
    print(cntrs)   
    
def citiesfilldb():
    with open('city.list.json', 'r', encoding='utf-8') as read_file:
        data = json.load(read_file)

    with open('cities15000.txt', 'r' , newline='', encoding='utf-8') as read_file:  #cities15000.txt from geonames.org   https://download.geonames.org/export/dump/
        csvdata = csv.reader(read_file, delimiter='\t')
        l = list(csvdata)
    
    clist = ['GB', 'GR', 'FI', 'LV', 'LT', 'SE', 'BY', 'PL', 'NO', 'PT', 'AT', 'DK', 'CH', 'NL', 'BE', 'LU']    #countrycode ALPHA-2 format https://www.iban.com/country-codes
    for city_data in data:
        if city_data['country'] in clist :
            for line in l:
                if line[1] == city_data['name'] and line[8] == city_data['country'] and int(line[14]) > 50000:
                    print( f'adding {city_data["name"]} - {int(line[14])}' )
                    newcity = City.objects.create(
                        name=city_data['name'], 
                        opw_id = city_data['id'], 
                        country = city_data['country'], 
                        state = city_data['state'], 
                        coord_lon = city_data['coord']['lon'], 
                        coord_lat = city_data['coord']['lat']
                        )
                    newcity.save()


def emptynamesfill():   #больше не нужно, т.к. все три поля заполняются изначально
    with connection.cursor() as cursor:
        cursor.execute("UPDATE weatherapp_city SET name_en = name_ru, name_uk = name_ru ")
        row = cursor.fetchone()

def translatecities(): 
    qs = City.objects.filter(country='CH')
    i = 0
    for city in qs:
        i += 1
        city.name_ru = getYAtranslation(city.name_en, 'en-ru')
        city.name_uk = getYAtranslation(city.name_en, 'en-uk')
        city.save()
        print(str(i) +' ' + city.name_ru +' ' + city.name_uk)
       

def getYAtranslation(text, direction):  #direction format 'en-ru'
    #yandex translate API
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    prms = {'key' : 'trnsl.1.1.20200505T224605Z.d3008b6d6a264e08.c3faf34dbf3b21ba93b54ef276fef996495a1c31', #api key
            'text' : text,
            'lang' : direction,       
    }
    res = requests.get(url, params=prms)
    if res.status_code == 200:
        res2 = res.json()
        return res2['text'][0]

def citypopulation(cityname, countrycode):  #countrycode ALPHA-2 format https://www.iban.com/country-codes
    #gets city population via geonames.org API   http://api.geonames.org/searchJSON?q=london&maxRows=10&username=demo
    #geonames.org has 1000 requests per hour, 12000 per day restriction for free accounts
    url = 'http://api.geonames.org/searchJSON'
    prms = {'name_equals' : cityname, 
            'maxRows' : 1,
            'country' : countrycode, 
            'username' : 'corbendallas'  ,
            'featureClass' : 'P'    
    }
    try:
        res = requests.get(url, params=prms)
        res2 = res.json()
        population = res2['geonames'][0]['population']
        print( f'{cityname} - { population }' )
        return population
    except:
        print(res.text)
        return 0

