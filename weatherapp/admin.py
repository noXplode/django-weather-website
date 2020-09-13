from .models import City, Weather, Forecast, Popularity

from django import forms
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from django.contrib.sessions.models import Session

from modeltranslation.admin import TranslationAdmin
import csv
import pprint


class JsonImportForm(forms.Form):
    json_file = forms.FileField()


class CityAdmin(TranslationAdmin):
    list_display = ('pk', 'name_en', 'name_ru', 'name_uk', 'country', 'opw_id', 'coord_lon', 'coord_lat')
    list_filter = ['country']
    fields = ['name', 'country', 'opw_id', ('coord_lon', 'coord_lat')]
    search_fields = ['name', 'opw_id']
    actions = ['export_as_csv', 'export_as_json']
    change_list_template = "weatherapp/admin_action_buttons.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-json/', self.import_json, name='import_json'),
        ]
        return my_urls + urls

    def import_json(self, request):
        if request.method == "POST":
            json_file = request.FILES["json_file"]
            cnt = 0
            for obj in serializers.deserialize("json", json_file):
                cnt += 1
                obj.save()
            self.message_user(request, f"Your json file has been imported, {cnt} cities saved")
            return redirect("..")
            pass
        form = JsonImportForm()
        return render(request, "weatherapp/admin_json_form.html", {"form": form})

    def export_as_csv(self, request, queryset):     # model csv export method

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=cities.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    def export_as_json(self, request, queryset):
        response = HttpResponse(content_type="application/json")
        response['Content-Disposition'] = 'attachment; filename=cities.json'
        serializers.serialize("json", queryset, ensure_ascii=False, stream=response)
        return response

    export_as_csv.short_description = " CSV Export Selected"
    export_as_json.short_description = " JSON Export Selected"


class WeatherAdmin(admin.ModelAdmin):
    list_display = ('city', 'loadingtime', 'is_actual')
    fields = ['city', 'loadingtime', 'weatherdata']
    readonly_fields = ['city', 'loadingtime']
    search_fields = ['city']


class ForecastAdmin(admin.ModelAdmin):
    list_display = ('city', 'loadingtime', 'is_actual')
    fields = ['city', 'loadingtime', 'forecastdata', 'citydata']
    readonly_fields = ['city', 'loadingtime']
    search_fields = ['city']


class PopularityAdmin(admin.ModelAdmin):
    list_display = ('city', 'pickeddate')


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')
    _session_data.allow_tags = True
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    exclude = ['session_data']
    date_hierarchy = 'expire_date'


admin.site.register(City, CityAdmin)
admin.site.register(Weather, WeatherAdmin)
admin.site.register(Forecast, ForecastAdmin)
admin.site.register(Popularity, PopularityAdmin)
admin.site.register(Session, SessionAdmin)
