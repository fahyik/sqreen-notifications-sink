import mock
import os

from ..dispatch_backends import MailBackend, LogBackend, FileBackend


class TestFileBackend():

    @mock.patch.object(FileBackend, '_write_to_file', mock.Mock(return_value=True))
    def test_save_to_file(self):
        assert FileBackend(mock.Mock()).dispatch()

    def test_write_to_file(self, mock_webhook_request):

        test_path_to_file = "./test.json"

        FileBackend(mock_webhook_request)._write_to_file(test_path_to_file)

        assert os.path.isfile(test_path_to_file)
        os.remove(test_path_to_file)

    @mock.patch.object(FileBackend, '_write_to_file', mock.Mock(side_effect=Exception))
    @mock.patch('sqreen_sink.dispatch_backends.logger.fatal')
    def test_write_fail(self, mock_logger):

        assert not FileBackend(mock.Mock()).dispatch()
        mock_logger.assert_called_once()
        mock_logger.assert_called_with("File dispatch failed", exc_info=True)


class TestLogBackend():

    @mock.patch('sqreen_sink.dispatch_backends.logger.info')
    def test_log_to_console(self, console_logger, mock_webhook_request):

        assert LogBackend(mock_webhook_request).dispatch()
        console_logger.assert_called_once()

    @mock.patch('sqreen_sink.dispatch_backends.logger.info', mock.Mock(side_effect=Exception))
    @mock.patch('sqreen_sink.dispatch_backends.logger.fatal')
    def test_log_to_console_fail(self, mock_logger):

        assert not LogBackend(mock.Mock()).dispatch()
        mock_logger.assert_called_once()
        mock_logger.assert_called_with("Log dispatch failed", exc_info=True)


class TestMailBackend():

    @mock.patch.object(MailBackend, '_send_mail', mock.Mock(return_value=True))
    def test_send(self):

        assert MailBackend(mock.Mock()).dispatch()

    def test_send_mail_success(self, app, mock_webhook_request):

        with app.app_context():

            from sqreen_sink import mail
            with mail.record_messages() as outbox:

                # trigger send mail
                MailBackend(mock_webhook_request)._send_mail("timestamp")

                assert len(outbox) == 1
                assert outbox[0].subject == "[SQREEN] Notifications timestamp"
                assert outbox[0].recipients == app.config.get('DISPATCH_MAIL_RECIPIENTS')

    @mock.patch.object(MailBackend, '_send_mail', mock.Mock(side_effect=Exception))
    @mock.patch('sqreen_sink.dispatch_backends.logger.fatal')
    def test_send_mail_fail(self, mock_logger):

        assert not MailBackend(mock.Mock()).dispatch()
        mock_logger.assert_called_once()
        mock_logger.assert_called_with("Email dispatch failed", exc_info=True)
