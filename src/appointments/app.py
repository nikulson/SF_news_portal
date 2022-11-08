from django.apps import AppConfig
import redis


class AppointmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.appointments'


red = redis.Redis(
    host='redis-11378.c241.us-east-1-4.ec2.cloud.redislabs.com',
    port=11378,
    password='LphfNOPZi0kxReGtJTMmVjVrjFbDY7s8'
)
