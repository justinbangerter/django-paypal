#!/usr/bin/env python
# -*- coding: utf-8 -*-
from string import split as L
from django.contrib import admin
from paypal.pro.models import PayPalNVP


class PayPalNVPAdmin(admin.ModelAdmin):
    list_display = ('user', 'ipaddress', 'method', 'flag', 'flag_code', 'created_at')
    list_filter = ('flag', 'created_at')
    search_fields = ('user__email', 'ip_address', 'flag', 'firstname', 'lastname')
    
    def queryset(self, request):
        return super(PayPalNVPAdmin, self).queryset(request).prefetch_related('user')

admin.site.register(PayPalNVP, PayPalNVPAdmin)
