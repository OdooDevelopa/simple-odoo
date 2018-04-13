# -*- coding: utf-8 -*-
# Copyright (C) 2006 Serenco JSC (<http://serenco.net>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from datetime import datetime
from datetime import timedelta
from odoo.addons.website.models.website import slug
import pytz
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT


class Website(models.Model):
    _inherit = 'website'

    def convert_utcdatetime_userdatetime(self, source_datetime):
        user_tz = self.env.user.tz or 'Asia/Ho_Chi_Minh'

        local = pytz.timezone(user_tz)
        dest_datetime = datetime.strptime(source_datetime,
                                          DEFAULT_SERVER_DATETIME_FORMAT)
        dest_datetime = pytz.utc.localize(
            dest_datetime).astimezone(local)
        dest_datetime = datetime.strftime(
            dest_datetime, "%H:%M %d-%m-%Y")
        return dest_datetime

    @api.model
    def get_last_7day_calendar_event(self):
        def change_date_format(source_date):
            res = datetime.strptime(source_date, '%Y-%m-%d')
            res = res.strftime('%d-%m-%Y')
            return res
        title = self.sudo().env['ir.config_parameter'].\
            get_param("calendar_title", "odooGlobal")

        event_obj = self.sudo().env['calendar.event']
        current_datetime = datetime.now()
        current_date = current_datetime.strftime('%Y-%m-%d')
        current_date_plus_7 = datetime.now() + timedelta(days=7)
        current_date_plus_7 = current_date_plus_7.strftime('%Y-%m-%d')
        event_s = event_obj.search(
            [('start_datetime', '>=', current_date),
             ('start_datetime', '<=', current_date_plus_7 + ' 23:59:59')],
            order='start_datetime')
        event_dict = {}
        week_day_dict = {}
        for index in range(1, 8):
            next_date = datetime.now() + timedelta(days=index)
            next_date_string = next_date.strftime('%Y-%m-%d')
            event_dict[change_date_format(next_date_string)] = []
            week_day_dict[index] = (change_date_format(next_date_string),
                                    next_date.weekday() + 2)

        for event in event_s:
            event_start_datetime = event.start_datetime
            event_start_datetime = datetime.strptime(
                event_start_datetime,
                '%Y-%m-%d %H:%M:%S')
            event_start_date = event_start_datetime.strftime('%Y-%m-%d')
            if change_date_format(event_start_date) not in event_dict.keys():
                continue

            event_dict[change_date_format(event_start_date)].append(event)

        res = {
            'title': title,
            'event_dict': event_dict,
            'week_day_dict': week_day_dict
        }
        return res

    @api.model
    def get_blog_data(self):
        limit = 7
        blog_blog_1 = self.sudo().env.ref(
            'website_blog.blog_blog_1')
        post_domain = [('blog_id', '=', blog_blog_1.id)]
        post_s = self.env['blog.post'].search(
            post_domain, limit=limit)
        base_url = '/blog/our-blog-{}/post/'.format(
            slug(blog_blog_1),
        )
        res = {}

        for post in post_s:
            name = post.name or 'Our post'
            url = base_url + slug(post)
            res[post.id] = (name, url)
        return res
