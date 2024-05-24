"""
Test custom Django management commands
"""
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error # type: ignore # noqa
from django.core.management import call_command # type: ignore # noqa
from django.db.utils import OperationalError # type: ignore # noqa
from django.test import SimpleTestCase # type: ignore # noqa


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_readt(self, patched_check):
        """Test waiting for database if database is ready"""
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 2 + [True]

        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 5)
        patched_check.assert_called_with(databases=['default'])
