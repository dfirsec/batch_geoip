# Batch GeoIP

![Generic badge](https://img.shields.io/badge/python-3.12-blue.svg) 

Python script to gather IP address geolocation information from different geolocation services.

Results are written to console and file (geo_results.txt).

Sources:

- *tools.keycdn.com*
- *ip-api.com*

## Recommended Installation & Usage

```console
└ $ git clone https://github.com/dfirsec/batch_geoip.git

└ $ cd batch_geoip

└ $ poetry install

└ $ poetry shell
```

```console
└ $ python batch_geoip.py 68.66.224.31

Combined Results
--------------------------------------------------
Ip             : 68.66.224.31
As             : AS55293 A2 Hosting, Inc.
Isp            : A2 Hosting, Inc.
Rdns           : az1-ls8.a2hosting.com
Country        : United States
Countrycode    : US
Regionname     : Arizona
Region         : AZ
City           : Phoenix
Zip            : 85001
Continent Name : North America
Continent Code : NA
Lat            : 33.4484
Lon            : -112.074
Timezone       : America/Phoenix
Datetime       : 2023-11-02 07:14:36
```
