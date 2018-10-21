from abc import ABC, abstractmethod

import datetime
import logging
import json
import os
import pytz

from flask_mail import Message

from . import mail

logger = logging.getLogger(__name__)


class BaseTarget(ABC):

    def __init__(self, request):
        self.request = request

    @abstractmethod
    def dispatch(self) -> bool:
        pass


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

        msg = Message(
            f"[SQREEN] Notifications {timestamp}",
            recipients=['fahyik.sqreen@gmail.com']
        )
        msg.attach(f'notifications-{timestamp}.json', 'application/json', self.request.get_data())
        mail.send(msg)


class FileBackend(BaseTarget):
    """
    Saves the payload to file
    TODO: Persist to a DB instead
    """

    def dispatch(self):
        return self._save_to_file()

    def _save_to_file(self):

        try:
            output_path = os.path.abspath('sqreen_sink/notifications_filestore')
            timestamp = pytz.UTC.localize(datetime.datetime.utcnow())

            self._write_to_file(output_path, timestamp)

            return True

        except Exception as e:

            logger.fatal("File dispatch failed", exc_info=True)
            return False

    def _write_to_file(self, output_path, timestamp):

        with open(f'{output_path}/notifications-{timestamp}.json', 'w') as file:
            file.write(
                json.dumps(
                    self.request.get_json(),
                    indent=4,
                    sort_keys=True
                )
            )
