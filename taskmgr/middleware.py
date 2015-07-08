import pygeoip

from django.conf import settings

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class GeoIP(object):

	def __init__(self, ip):
		self.ip = ip
		self.geoip = pygeoip.GeoIP(settings.GEOIP_COUNTRY, pygeoip.MEMORY_CACHE)

	@property
	def country_code(self):
		return self.geoip.country_code_by_name(self.ip)


class TimezoneMiddleware(object):

    def process_request(self, request):
        # Get IP from middleware
        ip = request.session.get('ip', get_client_ip(request))

        try:

            if settings.DEBUG:
                # Private IP
                tz = settings.TIME_ZONE
                request.session['country_code'] = settings.COUNTRY_CODE
            else:
                # Get Country Code from GeoIP
                country_code = GeoIP(ip).country_code
                request.session['country_code'] = country_code

                # Get TimeZone from Country Code
                tz = pytz.country_timezones[country_code][0]

            timezone.activate(tz)

        except Exception as e:
            # GEO IP coudn't find country for IP
            pass