from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import static
import settings
from manager.views import *
from django.contrib.auth.decorators import login_required
from filebrowser.sites import site



urlpatterns = [

   url(r'', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^signup/', signup_view, name='registration'),

    url(r'^admin/', admin.site.urls),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^$', get_lot_activities, name='home'),
    url(r'^lot_exists', login_required(TemplateView.as_view(template_name='manager/lot_exists.html'))),
    url(r'^rei_message', login_required(TemplateView.as_view(template_name='manager/rei_message.html'))),
    url(r'^crop_message', login_required(TemplateView.as_view(template_name='manager/crop_message.html'))),

    url(r'^lots', login_required(LotView.as_view()), name='lots'),
    url(r'^new/lot/', login_required(CreateLot.as_view()), name='createlot' ),
    url(r'^lot/(?P<pk>\d+)/$', login_required(UpdateLot.as_view()), name='updatelot' ),

    url(r'^crops', login_required(CropView.as_view()), name='crops'),
    url(r'^new/crop/', login_required(CreateCrop.as_view()), name='createcrop' ),
    url(r'^crop/(?P<crop_id>\d+)/$', update_crop, name='updatecrop' ),

    url(r'^inputs', login_required(InputView.as_view()), name='inputs'),
    url(r'^new/input/', login_required(CreateInput.as_view()), name='createinput' ),
    url(r'^input/(?P<pk>\d+)/$', login_required(UpdateInput.as_view()), name='updateinput' ),

    url(r'^brands', login_required(BrandView.as_view()), name='brands'),
    url(r'^new/brand/', login_required(CreateBrand.as_view()), name='createbrand' ),
    url(r'^delete_brand/(?P<pk>[0-9]+)/$', login_required(DeleteBrand.as_view()), name='delete_brand'),
    url(r'^brand/(?P<brand_id>\d+)/$', update_brand, name='updatebrand' ),
    url(r'^brand/list', get_brands, name='brand-list'),

    url(r'^brandgroups', get_brandgroups, name='groupbrands'),
    url(r'^brandgroup/$', login_required(CreateBrandGroup.as_view()), name='brandgroup'),
    url(r'^brandgroup/(?P<pk>\d+)/$', login_required(UpdateBrandGroup.as_view()), name='updatebrandgroup' ),
    url(r'^delete_brandgroup/(?P<pk>[0-9]+)/$', login_required(DeleteBrandGroup.as_view()), name='delete_brandgroup'),
    url(r'^history', get_history, name='history'),
    url(r'^wps', get_history, name='wps'),
    url(r'^rup_history', get_rup_history, name='rup_history'),
    url(r'^advanced_history', advanced_history, name='advanced_history'),
    
    url(r'^treatments', login_required(PestView.as_view()), name='pests'),
    url(r'^new/treatment/', login_required(CreatePest.as_view()), name='createpest' ),
    url(r'^treatment/(?P<pk>\d+)/$', login_required(UpdatePest.as_view()), name='updatepest' ),

    url(r'^new/propagation/', login_required(CreatePropagation.as_view()), name='createpropagation' ),
    url(r'^new/method/$', create_method, name='createmethod' ),
    url(r'^new/method/(?P<lot_name>[\w\-]+)/$', create_method, name='createmethod2' ),
    url(r'^new/transplanting/$', login_required(CreateTransplanting.as_view()), name='createtransplanting' ),
    url(r'^new/transplanting/(?P<lot_name>[\w\-]+)/$',login_required(CreateTransplanting.as_view()), name='createtransplanting2'),
    url(r'^new/harvest/$', login_required(CreateHarvest.as_view()), name='createharvest' ),
    url(r'^new/harvest/(?P<lot_name>[\w\-]+)/$', login_required(CreateHarvest.as_view()), name='createharvest' ),
    url(r'^new/cleaning/$', login_required(CreateCleaning.as_view()), name='createharvest' ),
    url(r'^new/cleaning/(?P<lot_name>[\w\-]+)/$', login_required(CreateCleaning.as_view()), name='createharvest' ),

    url(r'^propagation/(?P<pk>\d+)/$', login_required(UpdatePropagation.as_view()), name='updatepropagation' ),
    url(r'^transplanting/(?P<pk>\d+)/$', login_required(UpdateTransplanting.as_view()), name='updatetransplanting' ),
    url(r'^harvest/(?P<pk>\d+)/$', login_required(UpdateHarvest.as_view()), name='updateharvest' ),
    url(r'^cleaning/(?P<pk>\d+)/$', login_required(UpdateCleaning.as_view()), name='updatecleaning' ),

    url(r'^map', load_json_data),

    url(r'^lot_activities/(?P<field>[\w\-]+)/$', get_json_lot_activities),
    url(r'^lot_status/(?P<field>[\w\-]+)/$', get_lot_status),

    url(r'^settings/$', login_required(SettingsView.as_view()), name='settings'),
    url(r'^settings/(?P<pk>\d+)/$', login_required(UpdateSettings.as_view()), name='updatesettings' ),

   # url(r'^planner/', include('planner.urls')),

    url(r'^orders/', include('orders.urls')),


    url(r'^items/', include('inventory.urls')),

    #API URLs

   # url(r'^api/', include('api.urls')),

    ] + static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS)
