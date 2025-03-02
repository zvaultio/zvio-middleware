import asyncio
import errno
import json
import socket
import tempfile
import time

import aiohttp
import async_timeout
from middlewared.schema import Bool, Dict, Str, accepts
from middlewared.service import CallError, ConfigService, ValidationErrors
import middlewared.sqlalchemy as sa
from middlewared.utils.network import INTERNET_TIMEOUT

ADDRESS = 'support-proxy.zvault.io'


async def post(url, data, timeout=INTERNET_TIMEOUT):
    try:
        async with async_timeout.timeout(timeout):
            async with aiohttp.ClientSession(
                raise_for_status=True, trust_env=True,
            ) as session:
                req = await session.post(url, headers={"Content-Type": "application/json"}, data=data)
    except asyncio.TimeoutError:
        raise CallError('Connection timed out', errno.ETIMEDOUT)
    except aiohttp.ClientResponseError as e:
        raise CallError(f'Invalid proxy server response: {e}', errno.EBADMSG)

    try:
        return await req.json()
    except aiohttp.client_exceptions.ContentTypeError:
        raise CallError('Invalid proxy server response', errno.EBADMSG)


class SupportModel(sa.Model):
    __tablename__ = 'system_support'

    id = sa.Column(sa.Integer(), primary_key=True)
    enabled = sa.Column(sa.Boolean(), nullable=True, default=True)
    name = sa.Column(sa.String(200))
    title = sa.Column(sa.String(200))
    email = sa.Column(sa.String(200))
    phone = sa.Column(sa.String(200))
    secondary_name = sa.Column(sa.String(200))
    secondary_title = sa.Column(sa.String(200))
    secondary_email = sa.Column(sa.String(200))
    secondary_phone = sa.Column(sa.String(200))


class SupportService(ConfigService):

    class Config:
        datastore = 'system.support'

    @accepts(Dict(
        'support_update',
        Bool('enabled', null=True),
        Str('name'),
        Str('title'),
        Str('email'),
        Str('phone'),
        Str('secondary_name'),
        Str('secondary_title'),
        Str('secondary_email'),
        Str('secondary_phone'),
        update=True
    ))
    async def do_update(self, data):
        """
        Update Proactive Support settings.
        """

        config_data = await self.config()
        config_data.update(data)

        verrors = ValidationErrors()
        if config_data['enabled']:
            for key in ['name', 'title', 'email', 'phone']:
                for prefix in ['', 'secondary_']:
                    field = prefix + key
                    if not config_data[field]:
                        verrors.add(f'support_update.{field}', 'This field is required')
        if verrors:
            raise verrors

        await self.middleware.call(
            'datastore.update',
            self._config.datastore,
            config_data['id'],
            config_data,
        )

        return await self.config()

    @accepts()
    async def is_available(self):
        """
        Returns whether Proactive Support is available for this product type and current license.
        """

        return False

    @accepts()
    async def is_available_and_enabled(self):
        """
        Returns whether Proactive Support is available and enabled.
        """

        return False

    @accepts()
    async def fields(self):
        """
        Returns list of pairs of field names and field titles for Proactive Support.
        """

        return (
            ("name", "Contact Name"),
            ("title", "Contact Title"),
            ("email", "Contact E-mail"),
            ("phone", "Contact Phone"),
            ("secondary_name", "Secondary Contact Name"),
            ("secondary_title", "Secondary Contact Title"),
            ("secondary_email", "Secondary Contact E-mail"),
            ("secondary_phone", "Secondary Contact Phone"),
        )
