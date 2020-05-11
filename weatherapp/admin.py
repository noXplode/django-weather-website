from django.contrib import admin
from .models import City, Forecast, Popularity
from .forms import CityForm
from modeltranslation.admin import TranslationAdmin
import csv
from django.http import HttpResponse

#admin.site.register(City)

class ExportCsvMixin:   #model csv export class
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response
        
    export_as_csv.short_description = " CSV Export Selected"

class CityAdmin(TranslationAdmin, ExportCsvMixin):
    list_display = ('name_en', 'name_ru', 'name_uk', 'country', 'opw_id', 'coord_lon', 'coord_lat')
    list_filter = ['country']
    fields = ['name', 'country', 'opw_id', ('coord_lon', 'coord_lat')]
    search_fields = ['name', 'opw_id']
    actions = ["export_as_csv"]

class ForecastAdmin(admin.ModelAdmin):
    list_display = ('city', 'loadingtime', 'is_actual')
    fields = ['city', 'loadingtime', 'forecastdata']
    readonly_fields = ['city', 'loadingtime']
    search_fields = ['city']

class PopularityAdmin(admin.ModelAdmin):
    list_display = ('city', 'pickeddate')

admin.site.register(City, CityAdmin)
admin.site.register(Forecast, ForecastAdmin)
admin.site.register(Popularity, PopularityAdmin)




    

