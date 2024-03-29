from abc import abstractmethod, ABC
from cement import Interface, Handler

import geoip2.database
from pprint import pprint


class GeoInterface(Interface):
    class Meta:
        interface = 'geoIf'

    @abstractmethod
    def get_geo(self, ip, domain):
        """
        Get all geographic information about a domain
        :param domain: The domain
        :param ip: The domain ip
        :return: A dict with all information
        """


class GeoHandler(GeoInterface, Handler, ABC):
    class Meta:
        label = 'geo'

    def get_geo(self, ip, domain):
        try:
            reader_city = geoip2.database.Reader('./geodb/GeoLite2-City/GeoLite2-City.mmdb')
            reader_asn = geoip2.database.Reader('./geodb/GeoLite2-ASN/GeoLite2-ASN.mmdb')
            res_city = reader_city.city(ip)
            res_asn = reader_asn.asn(ip)
            geo_info = {'continent': res_city.continent.names['en'], 'country': res_city.country.names['en'],
                        'ip': ip, 'domain': domain, 'latitude': res_city.location.latitude,
                        'longitude': res_city.location.longitude,
                        'organization': res_asn.autonomous_system_organization
                        }
            reader_city.close()
            reader_asn.close()

            return geo_info
        except Exception as e:
            self.app.log.error("[GEO]")
            self.app.log.error("Exception", e)
