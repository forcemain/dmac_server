# -*- coding: utf-8 -*-


import os


from socket import gaierror
from geoip2.database import Reader
from geoip2.errors import GeoIP2Error


COUNTRIES_CODE = {
    'Asia': [
        'CN', 'HK', 'TW', 'MO', 'KR', 'SG', 'VN',
        'ID', 'IL', 'BH', 'JO', 'IR', 'IQ', 'YE',
        'SY', 'UZ', 'BN', 'TM', 'TH', 'TJ', 'LK',
        'CX', 'SA', 'JP', 'PW', 'NP', 'BD', 'MN',
        'MY', 'MV', 'LB', 'LA', 'KW', 'QA', 'KH',
        'KZ', 'PH', 'TL', 'TP', 'KP', 'BT', 'PK',
        'AZ', 'OM', 'AE', 'AF', 'IN', 'MM'
    ],
    'Europe': [
        'RU', 'ES', 'CH', 'GB', 'DE', 'FR', 'DK',
        'FI', 'NO', 'BE', 'SE', 'NL', 'CW', 'AM',
        'BG', 'GI', 'JE', 'UK', 'IT', 'HU', 'GR',
        'UA', 'TR', 'SJ', 'TV', 'SB', 'SI', 'SK',
        'SM', 'CY', 'YU', 'CS', 'PT', 'EU', 'MC',
        'FM', 'MK', 'MT', 'IM', 'RO', 'LU', 'LI',
        'LT', 'LV', 'HR', 'CZ', 'AN', 'GL', 'GG',
        'VA', 'FO', 'BA', 'PL', 'IS', 'BY', 'PS',
        'AX', 'AT', 'AD', 'EE', 'IE', 'AL', 'RS',
        'MD'
    ],
    'America': [
        'US', 'PR', 'VI', 'BO', 'CA', 'CL', 'JM',
        'UY', 'VE', 'VG', 'GT', 'TT', 'TC', 'SR',
        'VC', 'PM', 'LC', 'KN', 'SV', 'GE', 'PN',
        'NI', 'GS', 'MX', 'PE', 'MS', 'UM', 'AS',
        'MQ', 'CC', 'KY', 'HN', 'HT', 'GY', 'GU',
        'GP', 'CU', 'GD', 'CR', 'CO', 'CD', 'CG',
        'FK', 'GF', 'EC', 'DO', 'DM', 'MP', 'BM',
        'BR', 'PA', 'PY', 'BS', 'BB', 'AG', 'AI',
        'AC', 'AW', 'AR'
    ],
    'Africa': [
        'ZA', 'BW', 'NE', 'GA', 'MZ', 'DZ', 'GH',
        'TN', 'MA', 'EG', 'KE', 'CM', 'SN', 'SZ',
        'ZW', 'NA', 'NG', 'SD', 'ZM', 'TZ', 'MU',
        'MG', 'ML', 'AO', 'LS', 'MW', 'BF', 'GM',
        'UG', 'LY', 'MR', 'CF', 'EH', 'SO', 'SH',
        'ST', 'SC', 'SL', 'YT', 'RW', 'RE', 'LR',
        'CI', 'KM', 'GW', 'GN', 'KG', 'DJ', 'CV',
        'ER', 'TG', 'GQ', 'BV', 'BI', 'IO', 'BJ',
        'ET'
    ],
    'Oceania': [
        'AU', 'NZ', 'NC', 'VU', 'WF', 'TK', 'TO',
        'WS', 'NF', 'NU', 'NR', 'MH', 'CK', 'KI',
        'HM', 'FJ', 'TF', 'PF', 'PG'
    ]
}


class GeoIP2(Reader):
    def __init__(self, mmdb_path):
        super(GeoIP2, self).__init__(mmdb_path)

    def city(self, query):
        result = None
        try:
            city_info = super(GeoIP2, self).city(query)
        except (gaierror, GeoIP2Error):
            return result
        # for region
        if city_info.country.iso_code is None:
            return result
        for area in COUNTRIES_CODE.keys():
            if city_info.country.iso_code in COUNTRIES_CODE[area]:
                result = area
                break
        if result is None:
            return result
        # for country
        if city_info.country.name is not None:
            result = '_'.join([result, city_info.country.name])
        # for city
        if city_info.city.name is not None:
            result = '_'.join([result, city_info.city.name])

        return result


__db_name = 'geoip'
__db_path = os.path.join(os.path.dirname(__file__), '{0}.mmdb'.format(__db_name))
geoip_ins = GeoIP2(__db_path)



