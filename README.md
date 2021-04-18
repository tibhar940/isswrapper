# isswrapper
Simple wrapper for [Moscow Exchange](http://moex.com)  API (ISS Queries)

[ISS Queries documentation](https://iss.moex.com/iss/reference)

# Installation
TODO

# Colab example
TODO

# Modules

## isswrapper.helpers
TODO

## isswrapper.plots
TODO

## isswrapper.loaders
### isswrapper.loaders.securities
- `q` - function for finding securities list by query. Related ISS method - [/iss/securities](https://iss.moex.com/iss/reference/5)
- `security_description` - function for getting security description by query. Related ISS method - [/iss/securities/[security]](https://iss.moex.com/iss/reference/13)
- `security_boards` - function for getting security traded boards by query. Related ISS method - [/iss/securities/[security]](https://iss.moex.com/iss/reference/13)
- `security_indices` - function for getting security related indices by query. Related ISS method - [/iss/securities/[security]/indices](https://iss.moex.com/iss/reference/160)
- `security_aggregates` - function for getting security aggregates by query. Related ISS method - [/iss/securities/[security]/aggregates](https://iss.moex.com/iss/reference/214)
- `security_bondyields` - function for getting security (bonds) yields by query. Related ISS method - [/iss/securities/[security]/bondyields](https://iss.moex.com/iss/reference/713)

### isswrapper.loaders.trades
- `trades` - function for loading trades. Related ISS methods:
    - [/iss/engines/[engine]/markets/[market]/securities/[security]/trades](https://iss.moex.com/iss/reference/55)
    - [/iss/engines/[engine]/markets/[market]/trades](https://iss.moex.com/iss/reference/35)
    - [/iss/engines/[engine]/markets/[market]/boards/[board]/securities/[security]/trades](https://iss.moex.com/iss/reference/56)
    - [/iss/engines/[engine]/markets/[market]/boards/[board]/trades](https://iss.moex.com/iss/reference/34)
- `Trades` - class for loading trades

### isswrapper.loaders.candles
- `candles` - function for loading candles. Related ISS methods:
  - [/iss/engines/[engine]/markets/[market]/securities/[security]/candles](https://iss.moex.com/iss/reference/155)
  - [/iss/engines/[engine]/markets/[market]/boards/[board]/securities/[security]/candles](https://iss.moex.com/iss/reference/46)
- `Candles` - class for loading candles

### isswrapper.loaders.sitenews
- `sitenews` - function for loading site news. Related ISS method - [/iss/sitenews](https://iss.moex.com/iss/reference/191)
- `sitenews_body` - function for loading site news body by news id. Related ISS method - [/iss/sitenews/[news_id>]](https://iss.moex.com/iss/reference/192)
- `SiteNews` - class for loading site news
