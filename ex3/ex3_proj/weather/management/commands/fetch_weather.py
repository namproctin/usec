import requests

from django.core.management.base import BaseCommand
import channels.layers
from asgiref.sync import async_to_sync
from weather.models import Weather


class Command(BaseCommand):
    help = "Fetch weather"

    def add_arguments(self, parser):
        parser.add_argument("location", nargs="+", type=str)

    def handle(self, *args, **options):

        channel_layer = channels.layers.get_channel_layer()
        for location in options["location"]:
            res = requests.get(
                "http://wttr.in/%s?0" % location,
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
                },
            )
            if res.status_code == 200:
                try:
                    weather = Weather.objects.get(location=location)
                except Weather.DoesNotExist:
                    weather = Weather(location=location)
                data_start_index = res.text.find("<pre>")
                data_end_index = res.text.find("</pre>", data_start_index)
                if data_start_index < 0 or data_end_index < 0:
                    self.stdout.write(
                        self.style.ERROR(
                            'Failed fetch weather of location "%s"' % location
                        )
                    )
                    continue
                weather.data = res.text[
                    data_start_index + len("<pre>") : data_end_index
                ]
                weather.save()
                async_to_sync(channel_layer.group_send)(
                    "weather", {"type": "weather_message", "message": "update"}
                )
            else:
                self.stdout.write(
                    self.style.ERROR('Failed fetch weather of location "%s"' % location)
                )

            self.stdout.write(
                self.style.SUCCESS('Success fetch weather of location "%s"' % location)
            )
