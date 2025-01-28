# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Sabeel B (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from odoo import http
from odoo.http import request


class UserSwitch(http.Controller):
    """This is a controller to switch user and switch back to admin
        user_switch:
            this function is to check weather the user is admin or not
        switch_admin:
            function to switch back to admin
    """

    def _check_admin_access(self):
        if not request.env.user.has_group('login_as_any_user.group_login_as_any_user'):
            return False
        return True

    @http.route('/switch/user', type='json', auth='user')
    def user_switch(self):
        """
            Summary:
                function to check weather the user is admin
            Return:
                weather the current user is admin or not
        """
        if not self._check_admin_access():
            return {'error': 'Access Denied'}
        return request.env.user._is_admin()

    @http.route('/switch/admin', type='json', auth='user')
    def switch_admin(self):
        """
            Summary:
                function to move back to admin
            Return:
                the home page to be loaded
                """
        if not self._check_admin_access():
            return {'error': 'Access Denied'}
        session = request.session
        pre_user = request.env['res.users'].browse(session.previous_user)
        if pre_user and pre_user._is_admin:
            session.authenticate_without_password(request.env.cr.dbname,
                                                  pre_user.login, request.env)
            return {
                'type': 'ir.actions.act_url',
                'url': '/',
                'target': 'self'
            }
        return True
