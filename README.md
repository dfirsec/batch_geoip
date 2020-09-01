# Batch GeoIP

![Generic badge](https://img.shields.io/badge/python-3.7-blue.svg) [![Twitter](https://img.shields.io/badge/Twitter-@pulsecode-blue.svg)](https://twitter.com/pulsecode)
Python script to gather IP address geolocation information from different geolocation services.

Sources:
- *freegeoip.live*
- *tools.keycdn.com*
- *ipgeolocation.io*
- *ip-api.com*

# Installation

```text
git clone https://github.com/dfirsec/batch_geoip.git
cd batch_geoip
pip install -r requirements.txt
```

# Usage

```console
$ python batch_geoip.py 68.66.224.31


Freegeoip Results
--------------------------------------------------
Ip             : 68.66.224.31
Country Code   : US
Country Name   : United States
Region Code    : MI
Region Name    : Michigan
City           : Ann Arbor
Zip Code       : 48106
Time Zone      : America/Detroit
Latitude       : 42.2503
Longitude      : -83.8393
Metro Code     : 505

KeyCDN Results
--------------------------------------------------
Host           : 68.66.224.31
Ip             : 68.66.224.31
Rdns           : az1-ls8.a2hosting.com
Asn            : 55293
Isp            : A2HOSTING
Country Name   : United States
Country Code   : US
Continent Name : North America
Continent Code : NA
Latitude       : 37.751
Longitude      : -97.822
Timezone       : America/Chicago
Datetime       : 2020-09-01 06:16:53

IP Geolocation Results
--------------------------------------------------
IP                                 : 68.66.224.31
Continent Code                     : NA
Continent Name                     : North America
Country Code (ISO 3166-1 alpha-2)  : US
Country Code (ISO 3166-1 alpha-3)  : USA
Country Name                       : United States
Country Capital                    : Washington
State/Province                     : Michigan
District/County                    : Bach
City                               : Ann Arbor
Zip Code                           : 48104
Latitude & Longitude of City       : 42.28080 , -83.74300
Geoname ID                         : 4984247
Is EU?                             : false
Calling Code                       : +1
Country TLD                        : .us
Languages                          : en-US,es-US,haw,fr
ISP                                : A2 Hosting
Organization                       : A2 Hosting, Inc.
AS Number                          : AS55293
Currency                           : US Dollar
Currency Code                      : USD
Currency Symbol                    : $
Timezone                           : America/Detroit
Timezone Offset                    : -5
Current Time                       : 2020-09-01 07:16:53.501-0400
Current Time Unix                  : 1.598959013501E9
Is DST?                            : true
DST Savings                        : 1

IP-API Results
--------------------------------------------------
Status         : success
Country        : United States
Countrycode    : US
Region         : MI
Regionname     : Michigan
City           : Ann Arbor
Zip            : 48106
Lat            : 42.2583
Lon            : -83.6814
Timezone       : America/Detroit
Isp            : A2 Hosting, Inc.
Org            : A2 Hosting, Inc
As             : AS55293 A2 Hosting, Inc.
Query          : 68.66.224.31
```
