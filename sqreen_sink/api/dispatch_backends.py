from abc import ABC, abstractmethod

import datetime
import logging
import json
import os
import pytz

from flask import current_app
from flask_mail import Message

from .. import mail

logger = logging.getLogger(__name__)


class BaseTarget(ABC):

    def __init__(self, request):
        self.request = request

    @abstractmethod
    def dispatch(self) -> bool:
        pass


class FileBackend(BaseTarget):
    """
    Saves the payload to file
    TODO: Persist to a DB instead
    """

    def dispatch(self):
        return self._save_to_file()

    def _save_to_file(self):

        try:
            folder = os.path.abspath('sqreen_sink/notifications_filestore')
            timestamp = pytz.UTC.localize(datetime.datetime.utcnow())
            output_path = f'{folder}/notifications-{timestamp}.json'

            self._write_to_file(output_path)

            return True

        except Exception as e:

            logger.fatal("File dispatch failed", exc_info=True)
            return False

    def _write_to_file(self, output_path):

        with open(output_path, 'w') as file:
            file.write(
                json.dumps(
                    self.request.get_json(),
                    indent=4,
                    sort_keys=True
                )
            )


class LogBackend(BaseTarget):
    """
    Logs the payload onto the console
    """

    def dispatch(self):
        return self._log_to_console()

    def _log_to_console(self):

        try:
            logger.info(
                json.dumps(
                        self.request.get_json(),
                        indent=4,
                        sort_keys=True
                    )
            )

        except Exception as e:

            logger.fatal("Log dispatch failed", exc_info=True)
            return False

        return True


class MailBackend(BaseTarget):
    """
    Sends the payload as a json attachment to
    emails specified in config
    """

    def dispatch(self):
        return self._send()

    def _send(self):

        try:
            timestamp = pytz.UTC.localize(datetime.datetime.utcnow().replace(microsecond=0))

            self._send_mail(timestamp)

            return True

        except Exception as e:

            logger.fatal("Email dispatch failed", exc_info=True)
            return False

    def _send_mail(self, timestamp):

        recipients = current_app.config['DISPATCH_MAIL_RECIPIENTS']

        msg = Message(
            f"[SQREEN] Notifications {timestamp}",
            recipients=recipients
        )
        msg.attach(f'notifications-{timestamp}.json', 'application/json', self.request.get_data())
        mail.send(msg)
