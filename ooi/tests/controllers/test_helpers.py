# -*- coding: utf-8 -*-

# Copyright 2015 Spanish National Research Council
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import uuid

import mock
import six
import webob

from ooi.api import helpers
import ooi.tests.base
from ooi.tests.controllers import base as controller_base
from ooi.tests import fakes

import webob.exc


class TestExceptionHelper(ooi.tests.base.TestCase):
    @staticmethod
    def get_fault(code):
        return {
            "computeFault": {
                "code": code,
                "message": "Fault!",
                "details": "Error Details..."
            }
        }

    def test_exception(self):
        code_and_exception = {
            400: webob.exc.HTTPBadRequest,
            401: webob.exc.HTTPUnauthorized,
            403: webob.exc.HTTPForbidden,
            404: webob.exc.HTTPNotFound,
            405: webob.exc.HTTPMethodNotAllowed,
            406: webob.exc.HTTPNotAcceptable,
            409: webob.exc.HTTPConflict,
            413: webob.exc.HTTPRequestEntityTooLarge,
            415: webob.exc.HTTPUnsupportedMediaType,
            429: webob.exc.HTTPTooManyRequests,
            501: webob.exc.HTTPNotImplemented,
            503: webob.exc.HTTPServiceUnavailable,
            # Any other thing should be a 500
            500: webob.exc.HTTPInternalServerError,
            507: webob.exc.HTTPInternalServerError,
        }

        for code, exception in six.iteritems(code_and_exception):
            fault = self.get_fault(code)
            resp = fakes.create_fake_json_resp(fault, code)
            ret = helpers.exception_from_response(resp)
            self.assertIsInstance(ret, exception)
            self.assertEqual(fault["computeFault"]["message"], ret.explanation)

    def test_error_handling_exception(self):
        fault = {}
        resp = fakes.create_fake_json_resp(fault, 404)
        ret = helpers.exception_from_response(resp)
        self.assertIsInstance(ret, webob.exc.HTTPInternalServerError)


class TestOpenStackHelper(controller_base.TestController):
    def setUp(self):
        super(TestOpenStackHelper, self).setUp()
        self.helper = helpers.OpenStackHelper(mock.MagicMock(), None)

    @mock.patch.object(helpers.OpenStackHelper, "_get_index_req")
    def test_index(self, m):
        resp = fakes.create_fake_json_resp({"servers": ["FOO"]}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.index(None)
        self.assertEqual(["FOO"], ret)
        m.assert_called_with(None)

    @mock.patch("ooi.api.helpers.exception_from_response")
    @mock.patch.object(helpers.OpenStackHelper, "_get_index_req")
    def test_index_with_exception(self, m, m_exc):
        fault = {"computeFault": {"message": "bad", "code": 500}}
        resp = fakes.create_fake_json_resp(fault, 500)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        m_exc.return_value = webob.exc.HTTPInternalServerError()
        self.assertRaises(webob.exc.HTTPInternalServerError,
                          self.helper.index,
                          None)
        m.assert_called_with(None)
        m_exc.assert_called_with(resp)

    @mock.patch.object(helpers.OpenStackHelper, "_get_flavors_req")
    def test_flavors(self, m):
        resp = fakes.create_fake_json_resp({"flavors": ["FOO"]}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.get_flavors(None)
        self.assertEqual(["FOO"], ret)
        m.assert_called_with(None)

    @mock.patch("ooi.api.helpers.exception_from_response")
    @mock.patch.object(helpers.OpenStackHelper, "_get_flavors_req")
    def test_flavors_with_exception(self, m, m_exc):
        fault = {"computeFault": {"message": "bad", "code": 500}}
        resp = fakes.create_fake_json_resp(fault, 500)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        m_exc.return_value = webob.exc.HTTPInternalServerError()
        self.assertRaises(webob.exc.HTTPInternalServerError,
                          self.helper.get_flavors,
                          None)
        m.assert_called_with(None)
        m_exc.assert_called_with(resp)

    @mock.patch.object(helpers.OpenStackHelper, "_get_images_req")
    def test_images(self, m):
        resp = fakes.create_fake_json_resp({"images": ["FOO"]}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.get_images(None)
        self.assertEqual(["FOO"], ret)
        m.assert_called_with(None)

    @mock.patch("ooi.api.helpers.exception_from_response")
    @mock.patch.object(helpers.OpenStackHelper, "_get_images_req")
    def test_images_with_exception(self, m, m_exc):
        fault = {"computeFault": {"message": "bad", "code": 500}}
        resp = fakes.create_fake_json_resp(fault, 500)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        m_exc.return_value = webob.exc.HTTPInternalServerError()
        self.assertRaises(webob.exc.HTTPInternalServerError,
                          self.helper.get_images,
                          None)
        m.assert_called_with(None)
        m_exc.assert_called_with(resp)

    @mock.patch.object(helpers.OpenStackHelper, "_get_volumes_req")
    def test_volumes(self, m):
        resp = fakes.create_fake_json_resp({"volumes": ["FOO"]}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.get_volumes(None)
        self.assertEqual(["FOO"], ret)
        m.assert_called_with(None)

    @mock.patch("ooi.api.helpers.exception_from_response")
    @mock.patch.object(helpers.OpenStackHelper, "_get_volumes_req")
    def test_volumes_with_exception(self, m, m_exc):
        fault = {"computeFault": {"message": "bad", "code": 500}}
        resp = fakes.create_fake_json_resp(fault, 500)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        m_exc.return_value = webob.exc.HTTPInternalServerError()
        self.assertRaises(webob.exc.HTTPInternalServerError,
                          self.helper.get_volumes,
                          None)
        m.assert_called_with(None)
        m_exc.assert_called_with(resp)

    @mock.patch.object(helpers.OpenStackHelper, "_get_floating_ips_req")
    def test_floating_ips(self, m):
        resp = fakes.create_fake_json_resp({"floating_ips": ["FOO"]}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.get_floating_ips(None)
        self.assertEqual(["FOO"], ret)
        m.assert_called_with(None)

    @mock.patch("ooi.api.helpers.exception_from_response")
    @mock.patch.object(helpers.OpenStackHelper, "_get_floating_ips_req")
    def test_floating_ips_with_exception(self, m, m_exc):
        fault = {"computeFault": {"message": "bad", "code": 500}}
        resp = fakes.create_fake_json_resp(fault, 500)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        m_exc.return_value = webob.exc.HTTPInternalServerError()
        self.assertRaises(webob.exc.HTTPInternalServerError,
                          self.helper.get_floating_ips,
                          None)
        m.assert_called_with(None)
        m_exc.assert_called_with(resp)

    @mock.patch.object(helpers.OpenStackHelper, "_get_floating_ip_pools_req")
    def test_floating_ip_pools(self, m):
        resp = fakes.create_fake_json_resp({"floating_ip_pools": ["FOO"]}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.get_floating_ip_pools(None)
        self.assertEqual(["FOO"], ret)
        m.assert_called_with(None)

    @mock.patch("ooi.api.helpers.exception_from_response")
    @mock.patch.object(helpers.OpenStackHelper, "_get_floating_ip_pools_req")
    def test_floating_ip_pools_with_exception(self, m, m_exc):
        fault = {"computeFault": {"message": "bad", "code": 500}}
        resp = fakes.create_fake_json_resp(fault, 500)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        m_exc.return_value = webob.exc.HTTPInternalServerError()
        self.assertRaises(webob.exc.HTTPInternalServerError,
                          self.helper.get_floating_ip_pools,
                          None)
        m.assert_called_with(None)
        m_exc.assert_called_with(resp)

    @mock.patch.object(helpers.OpenStackHelper, "_get_flavors_req")
    def test_get_flavors(self, m):
        resp = fakes.create_fake_json_resp({"flavors": ["FOO"]}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.get_flavors(None)
        self.assertEqual(["FOO"], ret)
        m.assert_called_with(None)

    @mock.patch("ooi.api.helpers.exception_from_response")
    @mock.patch.object(helpers.OpenStackHelper, "_get_flavors_req")
    def test_get_flavors_with_exception(self, m, m_exc):
        fault = {"computeFault": {"message": "bad", "code": 500}}
        resp = fakes.create_fake_json_resp(fault, 500)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        m_exc.return_value = webob.exc.HTTPInternalServerError()
        self.assertRaises(webob.exc.HTTPInternalServerError,
                          self.helper.get_flavors,
                          None)
        m.assert_called_with(None)
        m_exc.assert_called_with(resp)

    @mock.patch.object(helpers.OpenStackHelper, "_get_delete_req")
    def test_delete(self, m):
        resp = fakes.create_fake_json_resp(None, 204)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        server_uuid = uuid.uuid4().hex
        ret = self.helper.delete(None, server_uuid)
        self.assertEqual(None, ret)
        m.assert_called_with(None, server_uuid)

    @mock.patch("ooi.api.helpers.exception_from_response")
    @mock.patch.object(helpers.OpenStackHelper, "_get_delete_req")
    def test_delete_with_exception(self, m, m_exc):
        fault = {"computeFault": {"message": "bad", "code": 500}}
        resp = fakes.create_fake_json_resp(fault, 500)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        server_uuid = uuid.uuid4().hex
        m_exc.return_value = webob.exc.HTTPInternalServerError()
        self.assertRaises(webob.exc.HTTPInternalServerError,
                          self.helper.delete,
                          None,
                          server_uuid)
        m.assert_called_with(None, server_uuid)
        m_exc.assert_called_with(resp)

    @mock.patch.object(helpers.OpenStackHelper, "_get_run_action_req")
    def test_run_action(self, m):
        resp = fakes.create_fake_json_resp(None, 202)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        server_uuid = uuid.uuid4().hex
        action = "start"
        ret = self.helper.run_action(None, action, server_uuid)
        self.assertEqual(None, ret)
        m.assert_called_with(None, action, server_uuid)

    @mock.patch("ooi.api.helpers.exception_from_response")
    @mock.patch.object(helpers.OpenStackHelper, "_get_run_action_req")
    def test_run_action_with_exception(self, m, m_exc):
        fault = {"computeFault": {"message": "bad", "code": 500}}
        resp = fakes.create_fake_json_resp(fault, 500)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        server_uuid = uuid.uuid4().hex
        action = "bad action"
        m_exc.return_value = webob.exc.HTTPInternalServerError()
        self.assertRaises(webob.exc.HTTPInternalServerError,
                          self.helper.run_action,
                          None,
                          action,
                          server_uuid)
        m.assert_called_with(None, action, server_uuid)
        m_exc.assert_called_with(resp)

    @mock.patch.object(helpers.OpenStackHelper, "_get_server_req")
    def test_get_server(self, m):
        resp = fakes.create_fake_json_resp({"server": "FOO"}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        server_uuid = uuid.uuid4().hex
        ret = self.helper.get_server(None, server_uuid)
        self.assertEqual("FOO", ret)
        m.assert_called_with(None, server_uuid)

    @mock.patch("ooi.api.helpers.exception_from_response")
    @mock.patch.object(helpers.OpenStackHelper, "_get_server_req")
    def test_get_server_with_exception(self, m, m_exc):
        fault = {"computeFault": {"message": "bad", "code": 500}}
        resp = fakes.create_fake_json_resp(fault, 500)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        server_uuid = uuid.uuid4().hex
        m_exc.return_value = webob.exc.HTTPInternalServerError()
        self.assertRaises(webob.exc.HTTPInternalServerError,
                          self.helper.get_server,
                          None,
                          server_uuid)
        m.assert_called_with(None, server_uuid)
        m_exc.assert_called_with(resp)

    @mock.patch.object(helpers.OpenStackHelper, "_get_image_req")
    def test_get_image(self, m):
        resp = fakes.create_fake_json_resp({"image": "FOO"}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        image_uuid = uuid.uuid4().hex
        ret = self.helper.get_image(None, image_uuid)
        self.assertEqual("FOO", ret)
        m.assert_called_with(None, image_uuid)

    @mock.patch("ooi.api.helpers.exception_from_response")
    @mock.patch.object(helpers.OpenStackHelper, "_get_image_req")
    def test_get_image_with_exception(self, m, m_exc):
        fault = {"computeFault": {"message": "bad", "code": 500}}
        resp = fakes.create_fake_json_resp(fault, 500)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        image_uuid = uuid.uuid4().hex
        m_exc.return_value = webob.exc.HTTPInternalServerError()
        self.assertRaises(webob.exc.HTTPInternalServerError,
                          self.helper.get_image,
                          None,
                          image_uuid)
        m.assert_called_with(None, image_uuid)
        m_exc.assert_called_with(resp)

    @mock.patch.object(helpers.OpenStackHelper, "_get_flavor_req")
    def test_get_flavor(self, m):
        resp = fakes.create_fake_json_resp({"flavor": "FOO"}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        flavor_uuid = uuid.uuid4().hex
        ret = self.helper.get_flavor(None, flavor_uuid)
        self.assertEqual("FOO", ret)
        m.assert_called_with(None, flavor_uuid)

    @mock.patch("ooi.api.helpers.exception_from_response")
    @mock.patch.object(helpers.OpenStackHelper, "_get_flavor_req")
    def test_get_flavor_with_exception(self, m, m_exc):
        fault = {"computeFault": {"message": "bad", "code": 500}}
        resp = fakes.create_fake_json_resp(fault, 500)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        flavor_uuid = uuid.uuid4().hex
        m_exc.return_value = webob.exc.HTTPInternalServerError()
        self.assertRaises(webob.exc.HTTPInternalServerError,
                          self.helper.get_flavor,
                          None,
                          flavor_uuid)
        m.assert_called_with(None, flavor_uuid)
        m_exc.assert_called_with(resp)

    @mock.patch.object(helpers.OpenStackHelper, "_get_volume_req")
    def test_get_volume(self, m):
        resp = fakes.create_fake_json_resp({"volume": "FOO"}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        volume_uuid = uuid.uuid4().hex
        ret = self.helper.get_volume(None, volume_uuid)
        self.assertEqual("FOO", ret)
        m.assert_called_with(None, volume_uuid)

    @mock.patch("ooi.api.helpers.exception_from_response")
    @mock.patch.object(helpers.OpenStackHelper, "_get_volume_req")
    def test_get_volume_with_exception(self, m, m_exc):
        fault = {"computeFault": {"message": "bad", "code": 500}}
        resp = fakes.create_fake_json_resp(fault, 500)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        volume_uuid = uuid.uuid4().hex
        m_exc.return_value = webob.exc.HTTPInternalServerError()
        self.assertRaises(webob.exc.HTTPInternalServerError,
                          self.helper.get_volume,
                          None,
                          volume_uuid)
        m.assert_called_with(None, volume_uuid)
        m_exc.assert_called_with(resp)

    @mock.patch.object(helpers.OpenStackHelper, "_get_server_volumes_link_req")
    def test_get_server_volume_links(self, m):
        resp = fakes.create_fake_json_resp({"volumeAttachments": ["FOO"]}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        server_uuid = uuid.uuid4().hex
        ret = self.helper.get_server_volumes_link(None, server_uuid)
        self.assertEqual(["FOO"], ret)
        m.assert_called_with(None, server_uuid)

    @mock.patch("ooi.api.helpers.exception_from_response")
    @mock.patch.object(helpers.OpenStackHelper, "_get_server_volumes_link_req")
    def test_get_server_volume_links_with_exception(self, m, m_exc):
        fault = {"computeFault": {"message": "bad", "code": 500}}
        resp = fakes.create_fake_json_resp(fault, 500)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        server_uuid = uuid.uuid4().hex
        m_exc.return_value = webob.exc.HTTPInternalServerError()
        self.assertRaises(webob.exc.HTTPInternalServerError,
                          self.helper.get_server_volumes_link,
                          None,
                          server_uuid)
        m.assert_called_with(None, server_uuid)
        m_exc.assert_called_with(resp)

    @mock.patch.object(helpers.OpenStackHelper, "_get_create_server_req")
    def test_create_server(self, m):
        resp = fakes.create_fake_json_resp({"server": "FOO"}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        name = uuid.uuid4().hex
        image = uuid.uuid4().hex
        flavor = uuid.uuid4().hex
        user_data = "foo"
        ret = self.helper.create_server(None, name, image, flavor,
                                        user_data=user_data)
        self.assertEqual("FOO", ret)
        m.assert_called_with(None, name, image, flavor, user_data=user_data)

    @mock.patch("ooi.api.helpers.exception_from_response")
    @mock.patch.object(helpers.OpenStackHelper, "_get_create_server_req")
    def test_create_server_with_exception(self, m, m_exc):
        fault = {"computeFault": {"message": "bad", "code": 500}}
        resp = fakes.create_fake_json_resp(fault, 500)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        name = uuid.uuid4().hex
        image = uuid.uuid4().hex
        flavor = uuid.uuid4().hex
        user_data = "foo"
        m_exc.return_value = webob.exc.HTTPInternalServerError()
        self.assertRaises(webob.exc.HTTPInternalServerError,
                          self.helper.create_server,
                          None,
                          name,
                          image,
                          flavor,
                          user_data=user_data)
        m.assert_called_with(None, name, image, flavor, user_data=user_data)
        m_exc.assert_called_with(resp)


class TestOpenStackHelperReqs(controller_base.TestController):
    def setUp(self):
        super(TestOpenStackHelperReqs, self).setUp()
        self.helper = helpers.OpenStackHelper(mock.MagicMock(), None)

    def _build_req(self, tenant_id, **kwargs):
        m = mock.MagicMock()
        m.user.project_id = tenant_id
        environ = {"keystone.token_auth": m}
        return webob.Request.blank("/whatever", environ=environ, **kwargs)

    def test_os_index_req(self):
        tenant = fakes.tenants["foo"]
        req = self._build_req(tenant["id"])
        os_req = self.helper._get_index_req(req)
        path = "/%s/servers" % tenant["id"]

        self.assertExpectedReq("GET", path, "", os_req)

    def test_os_delete_req(self):
        tenant = fakes.tenants["foo"]
        server_uuid = uuid.uuid4().hex
        req = self._build_req(tenant["id"])
        os_req = self.helper._get_delete_req(req, server_uuid)
        path = "/%s/servers/%s" % (tenant["id"], server_uuid)

        self.assertExpectedReq("DELETE", path, "", os_req)

    def test_os_action_req(self):
        tenant = fakes.tenants["foo"]
        req = self._build_req(tenant["id"])
        server_uuid = uuid.uuid4().hex

        actions_map = {
            "stop": {"os-stop": None},
            "start": {"os-start": None},
            "restart": {"reboot": {"type": "SOFT"}},
        }

        path = "/%s/servers/%s/action" % (tenant["id"], server_uuid)

        for act, body in six.iteritems(actions_map):
            os_req = self.helper._get_run_action_req(req, act, server_uuid)
            self.assertExpectedReq("POST", path, body, os_req)

    def test_get_os_server_req(self):
        tenant = fakes.tenants["foo"]
        server_uuid = uuid.uuid4().hex
        req = self._build_req(tenant["id"])
        os_req = self.helper._get_server_req(req, server_uuid)
        path = "/%s/servers/%s" % (tenant["id"], server_uuid)

        self.assertExpectedReq("GET", path, "", os_req)

    def test_get_os_flavors_req(self):
        tenant = fakes.tenants["foo"]
        req = self._build_req(tenant["id"])
        os_req = self.helper._get_flavors_req(req)
        path = "/%s/flavors/detail" % tenant["id"]

        self.assertExpectedReq("GET", path, "", os_req)

    def test_get_os_flavor_req(self):
        tenant = fakes.tenants["foo"]
        flavor_uuid = uuid.uuid4().hex
        req = self._build_req(tenant["id"])
        os_req = self.helper._get_flavor_req(req, flavor_uuid)
        path = "/%s/flavors/%s" % (tenant["id"], flavor_uuid)

        self.assertExpectedReq("GET", path, "", os_req)

    def test_get_os_images_req(self):
        tenant = fakes.tenants["foo"]
        req = self._build_req(tenant["id"])
        os_req = self.helper._get_images_req(req)
        path = "/%s/images/detail" % tenant["id"]

        self.assertExpectedReq("GET", path, "", os_req)

    def test_get_os_image_req(self):
        tenant = fakes.tenants["foo"]
        image_uuid = uuid.uuid4().hex
        req = self._build_req(tenant["id"])
        os_req = self.helper._get_image_req(req, image_uuid)
        path = "/%s/images/%s" % (tenant["id"], image_uuid)

        self.assertExpectedReq("GET", path, "", os_req)

    def test_get_os_volume_links_req(self):
        tenant = fakes.tenants["foo"]
        server_uuid = uuid.uuid4().hex
        req = self._build_req(tenant["id"])
        os_req = self.helper._get_server_volumes_link_req(req, server_uuid)
        path = "/%s/servers/%s/os-volume_attachments" % (tenant["id"],
                                                         server_uuid)

        self.assertExpectedReq("GET", path, "", os_req)

    def test_get_os_volumes_req(self):
        tenant = fakes.tenants["foo"]
        req = self._build_req(tenant["id"])
        os_req = self.helper._get_volumes_req(req)
        path = "/%s/os-volumes" % tenant["id"]

        self.assertExpectedReq("GET", path, "", os_req)

    def test_get_os_volume_req(self):
        tenant = fakes.tenants["foo"]
        vol_uuid = uuid.uuid4().hex
        req = self._build_req(tenant["id"])
        os_req = self.helper._get_volume_req(req, vol_uuid)
        path = "/%s/os-volumes/%s" % (tenant["id"], vol_uuid)

        self.assertExpectedReq("GET", path, "", os_req)

    def test_get_os_floating_ips(self):
        tenant = fakes.tenants["foo"]
        req = self._build_req(tenant["id"])
        os_req = self.helper._get_floating_ips_req(req)
        path = "/%s/os-floating-ips" % tenant["id"]

        self.assertExpectedReq("GET", path, "", os_req)

    def test_get_os_floating_ip_pools(self):
        tenant = fakes.tenants["foo"]
        req = self._build_req(tenant["id"])
        os_req = self.helper._get_floating_ip_pools_req(req)
        path = "/%s/os-floating-ip-pools" % tenant["id"]

        self.assertExpectedReq("GET", path, "", os_req)

    def test_get_os_get_server_create(self):
        tenant = fakes.tenants["foo"]
        req = self._build_req(tenant["id"])
        name = "foo server"
        image = "bar image"
        flavor = "baz flavor"

        body = {
            "server": {
                "name": name,
                "imageRef": image,
                "flavorRef": flavor,
            }
        }

        path = "/%s/servers" % tenant["id"]
        os_req = self.helper._get_create_server_req(req, name, image, flavor)
        self.assertExpectedReq("POST", path, body, os_req)

    def test_get_os_get_server_create_with_user_data(self):
        tenant = fakes.tenants["foo"]
        req = self._build_req(tenant["id"])
        name = "foo server"
        image = "bar image"
        flavor = "baz flavor"
        user_data = "bazonk"

        body = {
            "server": {
                "name": name,
                "imageRef": image,
                "flavorRef": flavor,
                "user_data": user_data,
            },
        }

        path = "/%s/servers" % tenant["id"]
        os_req = self.helper._get_create_server_req(req, name, image, flavor,
                                                    user_data=user_data)
        self.assertExpectedReq("POST", path, body, os_req)