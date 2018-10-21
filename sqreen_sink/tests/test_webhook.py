import mock


class TestWebhook():

    def test_signature_fail(self, client):

        response = client.post('/sqreen/notify/', json={})

        assert response.status_code == 400
        assert response.json['error'] == 'BadRequest: Invalid signature'

    @mock.patch('sqreen_sink.api.resources.SqreenWebhook._dispatch', return_value={})
    def test_valid_signature(self, mock_dispatch, client):

        signature = '252b14d418fa12e80248769e2a5410f711c63d5bcc0d440dcdfcfab33f276e49'

        response = client.post('/sqreen/notify/', json={}, headers={'X-Sqreen-Integrity': signature})

        mock_dispatch.assert_called_once()
        assert response.status_code == 200

    def test_webhook_success(self, client, monkeypatch):

        monkeypatch.setattr(
            'sqreen_sink.dispatch_backends.FileBackend.dispatch',
            lambda *args: True
        )

        monkeypatch.setattr(
            'sqreen_sink.dispatch_backends.MailBackend.dispatch',
            lambda *args: True
        )

        monkeypatch.setattr(
            'sqreen_sink.dispatch_backends.LogBackend.dispatch',
            lambda *args: True
        )

        signature = '252b14d418fa12e80248769e2a5410f711c63d5bcc0d440dcdfcfab33f276e49'
        response = client.post('/sqreen/notify/', json={}, headers={'X-Sqreen-Integrity': signature})

        assert response.status_code == 200
        assert response.json['FileBackend'] is True
        assert response.json['MailBackend'] is True
        assert response.json['LogBackend'] is True
