import nanoid
from typing import Any, Dict, List

from pydantic import AnyHttpUrl, BaseSettings, validator


class KafkaSettings(BaseSettings):
    KAFKA_BROKERS: str = ''
    KAFKA_CLIENT_ID: str = str(nanoid.generate())
    KAFKA_GROUP_ID: str = ''

    KAFKA_SECURITY_PROTOCOL: str = 'PLAINTEXT'
    KAFKA_SASL_MECHAMISM: str = ''
    KAFKA_API_KEY: str = ''
    KAFKA_API_SECRET: str = ''
    KAFKA_CA_CERT_PATH: str = ''
    KAFKA_ACCESS_KEY_PATH: str = ''
    KAFKA_ACCESS_CERT_PATH: str = ''

    KAFKA_PRODUCER_CONFIG: dict = {}
    KAFKA_CONSUMER_CONFIG: dict = {}
    KAFKA_ADMIN_CONFIG: dict = {}

    @staticmethod
    def get_kafka_common_cfg(value):
        security_conf = {}
        if not value.get('KAFKA_SECURITY_PROTOCOL', None) is None and value.get('KAFKA_SECURITY_PROTOCOL') != '':
            security_conf['security.protocol'] = value.get('KAFKA_SECURITY_PROTOCOL')
        if not value.get('KAFKA_SASL_MECHAMISM', None) is None and value.get('KAFKA_SASL_MECHAMISM') != '':
            security_conf['sasl.mechanisms'] = value.get('KAFKA_SASL_MECHAMISM')
        if not value.get('KAFKA_API_KEY', None) is None and value.get('KAFKA_API_KEY') != '':
            security_conf['sasl.username'] = value.get('KAFKA_API_KEY')
        if not value.get('KAFKA_API_SECRET', None) is None and value.get('KAFKA_API_SECRET') != '':
            security_conf['sasl.password'] = value.get('KAFKA_API_SECRET')

        if not value.get('KAFKA_CA_CERT_PATH', None) is None and value.get('KAFKA_CA_CERT_PATH') != '':
            security_conf['ssl.ca.location'] = value.get('KAFKA_CA_CERT_PATH')
        if not value.get('KAFKA_ACCESS_KEY_PATH', None) is None and value.get('KAFKA_ACCESS_KEY_PATH') != '':
            security_conf['ssl.key.location'] = value.get('KAFKA_ACCESS_KEY_PATH')
        if not value.get('KAFKA_ACCESS_CERT_PATH', None) is None and value.get('KAFKA_ACCESS_CERT_PATH') != '':
            security_conf['ssl.certificate.location'] = value.get('KAFKA_ACCESS_CERT_PATH')

        if value['KAFKA_CLIENT_ID'] == '':
            value['KAFKA_CLIENT_ID'] = str(nanoid.generate())
        return {
            "bootstrap.servers": value['KAFKA_BROKERS'],
            "client.id": value['KAFKA_CLIENT_ID'],
            **security_conf
        }

    @validator('KAFKA_PRODUCER_CONFIG', pre=True)
    def assemble_producer_cfg(
        cls, value: str, values: Dict[str, Any],  # noqa: N805, WPS110
    ) -> dict:
        return {
            **KafkaSettings.get_kafka_common_cfg(values),
            'acks': 'all',
            "socket.keepalive.enable": "true",
            "retries": "1000000",
            "message.timeout.ms": "300000",
            "socket.timeout.ms": "30000",
            "max.in.flight.requests.per.connection": "5",
            "heartbeat.interval.ms": "3000",
            "enable.idempotence": "true"
        }

    @validator('KAFKA_CONSUMER_CONFIG', pre=True)
    def assemble_consumer_cfg(
        cls, value: str, values: Dict[str, Any],  # noqa: N805, WPS110
    ) -> dict:
        return {
            **KafkaSettings.get_kafka_common_cfg(values),
            "group.id": values.get('KAFKA_GROUP_ID')
        }

    @validator('KAFKA_ADMIN_CONFIG', pre=True)
    def assemble_admin_cfg(
        cls, value: str, values: Dict[str, Any],  # noqa: N805, WPS110
    ) -> dict:
        return {
            **KafkaSettings.get_kafka_common_cfg(values),
        }
    