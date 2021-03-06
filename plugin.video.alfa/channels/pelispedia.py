# -*- coding: utf-8 -*-

import re
import urllib
import urlparse
import json

from channelselector import get_thumb
from core import channeltools
from core import httptools
from core import scrapertools
from core import servertools
from core import tmdb
from core.item import Item
from platformcode import config, logger
from platformcode import platformtools
from core import filetools

__channel__ = "pelispedia"

CHANNEL_HOST = "http://www.pelispedia.tv/"

# Configuracion del canal
try:
    __modo_grafico__ = config.get_setting('modo_grafico', __channel__)
except:
    __modo_grafico__ = True


parameters = channeltools.get_channel_parameters(__channel__)
fanart_host = parameters['fanart']
thumbnail_host = parameters['thumbnail']


def mainlist(item):
    logger.info()

    itemlist = list()
    itemlist.append(Item(channel=__channel__, title="Películas", fanart=fanart_host, folder=False,
                         thumbnail=thumbnail_host, text_bold=True))

    itemlist.append(Item(channel=__channel__, action="listado", title="    Novedades", 
             url=urlparse.urljoin(CHANNEL_HOST, "movies/all/"), extra="movies",
             viewcontent="movies", viewmode="movie_with_plot", fanart=fanart_host,
             thumbnail="https://raw.githubusercontent.com/master-1970/resources/master/images/genres/0/Directors%20Chair.png"))

    itemlist.append(Item(channel=__channel__, action="listado_alfabetico", title="    Por orden alfabético",
             url=urlparse.urljoin(CHANNEL_HOST, "movies/all/"), extra="movies",
             viewmode="thumbnails", fanart=fanart_host,
             thumbnail="https://raw.githubusercontent.com/master-1970/resources/master/images/genres/0/A-Z.png"))

    itemlist.append(Item(channel=__channel__, action="listado_genero", title="    Por género",
             url=urlparse.urljoin(CHANNEL_HOST, "movies/all/"), extra="movies", 
             fanart=fanart_host,
             thumbnail="https://raw.githubusercontent.com/master-1970/resources/master/images/genres/0/Genre.png"))

    itemlist.append(Item(channel=__channel__, action="listado_anio", title="    Por año",
             url=urlparse.urljoin(CHANNEL_HOST, "movies/all/"), extra="movies", 
             fanart=fanart_host,
             thumbnail="https://raw.githubusercontent.com/master-1970/resources/master/images/genres/0/Year.png"))

    itemlist.append(Item(channel=__channel__, action="local_search", title="    Buscar...",
             url=urlparse.urljoin(CHANNEL_HOST, "buscar/?sitesearch=pelispedia.tv&q="), extra="movies", 
             fanart=fanart_host, thumbnail=get_thumb('search', auto=True)))


    itemlist.append(Item(channel=__channel__, title="Series", fanart=fanart_host, folder=False,
                         thumbnail=thumbnail_host, text_bold=True))

    itemlist.append(
        Item(channel=__channel__, action="listado", title="    Novedades",
             url=urlparse.urljoin(CHANNEL_HOST, "series/all/"), extra="serie",
             viewcontent="tvshows", viewmode="movie_with_plot", fanart=fanart_host,
             thumbnail="https://raw.githubusercontent.com/master-1970/resources/master/images/genres/0/TV%20Series.png"))

    itemlist.append(Item(channel=__channel__, action="listado_alfabetico", title="    Por orden alfabético",
             url=urlparse.urljoin(CHANNEL_HOST, "series/all/"), extra="serie",
             viewmode="thumbnails", fanart=fanart_host, 
             thumbnail="https://raw.githubusercontent.com/master-1970/resources/master/images/genres/0/A-Z.png"))

    itemlist.append(Item(channel=__channel__, action="listado_genero", title="    Por género",
             url=urlparse.urljoin(CHANNEL_HOST, "series/all/"), extra="serie",
             fanart=fanart_host,
             thumbnail="https://raw.githubusercontent.com/master-1970/resources/master/images/genres/0/Genre.png"))

    itemlist.append(Item(channel=__channel__, action="listado_anio", title="    Por año",
             url=urlparse.urljoin(CHANNEL_HOST, "series/all/"), extra="serie",
             fanart=fanart_host,
             thumbnail="https://raw.githubusercontent.com/master-1970/resources/master/images/genres/0/Year.png"))

    itemlist.append(Item(channel=__channel__, action="local_search", title="    Buscar...",
             url=urlparse.urljoin(CHANNEL_HOST, "series/buscar/?sitesearch=pelispedia.tv&q="), extra="serie", 
             fanart=fanart_host, thumbnail=get_thumb('search', auto=True)))


    # ~ itemlist.append(Item(channel=__channel__, title="", fanart=fanart_host, folder=False, thumbnail=thumbnail_host))

    # ~ itemlist.append(Item(channel=__channel__, action="settings", title="Configuración",
                         # ~ fanart=fanart_host, text_bold=True,
                         # ~ thumbnail=get_thumb("setting_0.png")))

    return itemlist


def settings(item):
    return platformtools.show_channel_settings()


def listado_alfabetico(item):
    logger.info()

    itemlist = []

    for letra in '0ABCDEFGHIJKLMNOPQRSTUVWXYZ':

        cadena = "series/letra/"
        if item.extra == "movies":
            cadena = 'movies/all/?letra='
            viewcontent = "movies"
            if letra == '0':
                cadena += "Num"
            else:
                cadena += letra
        else:
            viewcontent = "tvshows"
            if letra == '0':
                cadena += "num/"
            else:
                cadena += letra + "/"

        itemlist.append(
            Item(channel=__channel__, action="listado", title=letra, url=urlparse.urljoin(CHANNEL_HOST, cadena),
                 extra=item.extra, fanart=fanart_host, viewcontent=viewcontent,
                 thumbnail="https://raw.githubusercontent.com/master-1970/resources/master/images/genres/0/A-Z.png"))

    return itemlist


def listado_genero(item):
    logger.info()

    itemlist = []

    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s", "", data)

    if item.extra == "movies":
        cadena = 'movies/all/?gender='
        viewcontent = "movies"
        patron = '<select name="gender" id="genres" class="auxBtn1">.*?</select>'
        data = scrapertools.find_single_match(data, patron)
        patron = '<option value="([^"]+)".+?>(.*?)</option>'

    else:
        cadena = "series/genero/"
        viewcontent = "tvshows"
        patron = '<select id="genres">.*?</select>'
        data = scrapertools.find_single_match(data, patron)
        patron = '<option name="([^"]+)".+?>(.*?)</option>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for key, value in matches[1:]:
        cadena2 = cadena + key
        if item.extra != "movies":
            cadena2 += "/"

        itemlist.append(
            Item(channel=__channel__, action="listado", title=value, url=urlparse.urljoin(CHANNEL_HOST, cadena2),
                 extra=item.extra, fanart=fanart_host, viewcontent=viewcontent,
                 thumbnail="https://raw.githubusercontent.com/master-1970/resources/master/images/genres/0/Genre.png"))

    return itemlist


def listado_anio(item):
    logger.info()

    itemlist = []

    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s", "", data)

    if item.extra == "movies":
        cadena = 'movies/all/?year='
        viewcontent = "movies"
        patron = '<select name="year" id="years" class="auxBtn1">.*?</select>'
        data = scrapertools.find_single_match(data, patron)
        patron = '<option value="([^"]+)"'
        titulo = 'Películas del año '
    else:
        cadena = "series/anio/"
        viewcontent = "tvshows"
        patron = '<select id="year">.*?</select>'
        data = scrapertools.find_single_match(data, patron)
        patron = '<option name="([^"]+)"'
        titulo = 'Series del año '

    matches = re.compile(patron, re.DOTALL).findall(data)

    for value in matches[1:]:
        cadena2 = cadena + value

        if item.extra != "movies":
            cadena2 += "/"

        itemlist.append(
            Item(channel=__channel__, action="listado", title=titulo + value, url=urlparse.urljoin(CHANNEL_HOST, cadena2),
                 extra=item.extra, fanart=fanart_host, viewcontent=viewcontent,
                 thumbnail="https://raw.githubusercontent.com/master-1970/resources/master/images/genres/0/Year.png"))

    return itemlist


def local_search(item):
    logger.info()
    text = ""
    # ~ if config.get_setting("save_last_search", item.channel):
        # ~ text = config.get_setting("last_search", item.channel)

    from platformcode import platformtools
    texto = platformtools.dialog_input(default=text, heading="Buscar en Pelispedia")
    if texto is None:
        return

    # ~ if config.get_setting("save_last_search", item.channel):
        # ~ config.set_setting("last_search", texto, item.channel)

    return search(item, texto)


def search(item, texto):
    logger.info()
    if '/buscar/?' not in item.url:
        item.url = CHANNEL_HOST if item.extra == 'movies' else CHANNEL_HOST + 'series/'
        item.url += 'buscar/?sitesearch=pelispedia.tv&q='
    item.url += texto.replace(" ", "+")

    try:
        return listado(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def newest(categoria):
    item = Item()
    try:
        if categoria == 'peliculas':
            item.url = urlparse.urljoin(CHANNEL_HOST, "movies/all/")
            item.extra = "movies"

        else:
            return []

        itemlist = listado(item)
        if itemlist[-1].action == "listado":
            itemlist.pop()

    # Se captura la excepción, para no interrumpir al canal novedades si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

    return itemlist


def listado(item):
    logger.info()
    itemlist = []

    action = "findvideos"
    content_type = "movie"

    if item.extra == 'serie':
        action = "temporadas"
        content_type = "tvshow"

    # ~ data = httptools.downloadpage(item.url).data
    data = obtener_data(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s", "", data)
    # logger.info("data -- {}".format(data))

    patron = '<li[^>]+><a href="([^"]+)" alt="([^<|\(]+).*?<img src="([^"]+).*?>.*?<span>\(([^)]+).*?' \
             '<p class="font12">(.*?)</p>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail, scrapedyear, scrapedplot in matches[:28]:
        title = "%s (%s)" % (scrapertools.unescape(scrapedtitle.strip()), scrapedyear)
        plot = scrapertools.entityunescape(scrapedplot)

        new_item = Item(channel=__channel__, title=title, url=urlparse.urljoin(CHANNEL_HOST, scrapedurl), action=action,
                        thumbnail=scrapedthumbnail, plot=plot, context="", extra=item.extra,
                        contentType=content_type, fulltitle=title)

        if item.extra == 'serie':
            new_item.show = scrapertools.unescape(scrapedtitle.strip())
            # fix en algunos casos la url está mal
            new_item.url = new_item.url.replace(CHANNEL_HOST + "pelicula", CHANNEL_HOST + "serie")
        else:
            new_item.fulltitle = scrapertools.unescape(scrapedtitle.strip())
            new_item.infoLabels = {'year': scrapedyear}
            # logger.debug(new_item.tostring())

        itemlist.append(new_item)

    # Obtenemos los datos basicos de todas las peliculas mediante multihilos
    tmdb.set_infoLabels(itemlist, __modo_grafico__)

    # numero de registros que se muestran por página, se fija a 28 por cada paginación
    if len(matches) >= 28 and '/buscar/?' not in item.url:

        file_php = "666more"
        tipo_serie = ""

        if item.extra == "movies":
            anio = scrapertools.find_single_match(item.url, "(?:year=)(\w+)")
            letra = scrapertools.find_single_match(item.url, "(?:letra=)(\w+)")
            genero = scrapertools.find_single_match(item.url, "(?:gender=|genre=)(\w+)")
            params = "letra=%s&year=%s&genre=%s" % (letra, anio, genero)

        else:
            tipo2 = scrapertools.find_single_match(item.url, "(?:series/|tipo2=)(\w+)")
            tipo_serie = "&tipo=serie"

            if tipo2 != "all":
                file_php = "letra"
                tipo_serie += "&tipo2=" + tipo2

            genero = ""
            if tipo2 == "anio":
                genero = scrapertools.find_single_match(item.url, "(?:anio/|genre=)(\w+)")
            if tipo2 == "genero":
                genero = scrapertools.find_single_match(item.url, "(?:genero/|genre=)(\w+)")
            if tipo2 == "letra":
                genero = scrapertools.find_single_match(item.url, "(?:letra/|genre=)(\w+)")

            params = "genre=%s" % genero

        url = "http://www.pelispedia.tv/api/%s.php?rangeStart=28&rangeEnd=28%s&%s" % (file_php, tipo_serie, params)

        if "rangeStart" in item.url:
            ant_inicio = scrapertools.find_single_match(item.url, "rangeStart=(\d+)&")
            inicio = str(int(ant_inicio) + 28)
            url = item.url.replace("rangeStart=" + ant_inicio, "rangeStart=" + inicio)

        itemlist.append(Item(channel=__channel__, action="listado", title=">> Página siguiente", extra=item.extra,
                             url=url, thumbnail=thumbnail_host, fanart=fanart_host))

    return itemlist


def episodios(item):
    logger.info()

    itemlist = []

    # ~ data = httptools.downloadpage(item.url).data
    data = obtener_data(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s", "", data)

    patron = '<li class="clearfix gutterVertical20"><a href="([^"]+)".*?><small>(.*?)</small>.*?' \
             '<span class.+?>(.*?)</span>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedname in matches:
        # logger.info("scrap {}".format(scrapedtitle))
        patron = 'Season\s+(\d),\s+Episode\s+(\d+)'
        match = re.compile(patron, re.DOTALL).findall(scrapedtitle)
        season, episode = match[0]

        if 'season' in item.infoLabels and int(item.infoLabels['season']) != int(season):
            continue

        title = "%sx%s: %s" % (season, episode.zfill(2), scrapertools.unescape(scrapedname))
        new_item = item.clone(title=title, url=scrapedurl, action="findvideos", fulltitle=title,
                              contentType="episode")
        if 'infoLabels' not in new_item:
            new_item.infoLabels = {}

        new_item.infoLabels['season'] = season
        new_item.infoLabels['episode'] = episode.zfill(2)

        itemlist.append(new_item)

    # TODO no hacer esto si estamos añadiendo a la videoteca
    if not item.extra:
        # Obtenemos los datos de todos los capitulos de la temporada mediante multihilos
        tmdb.set_infoLabels(itemlist, __modo_grafico__)
        for i in itemlist:
            if i.infoLabels['title']:
                # Si el capitulo tiene nombre propio añadirselo al titulo del item
                i.title = "%sx%s %s" % (i.infoLabels['season'], i.infoLabels['episode'], i.infoLabels['title'])
            if i.infoLabels.has_key('poster_path'):
                # Si el capitulo tiene imagen propia remplazar al poster
                i.thumbnail = i.infoLabels['poster_path']

    itemlist.sort(key=lambda it: int(it.infoLabels['episode']),
                  reverse=config.get_setting('orden_episodios', __channel__))

    # Opción "Añadir esta serie a la videoteca"
    if config.get_videolibrary_support() and len(itemlist) > 0:
        itemlist.append(Item(channel=__channel__, title="Añadir esta serie a la videoteca", url=item.url,
                             action="add_serie_to_library", extra="episodios", show=item.show, category="Series",
                             thumbnail=thumbnail_host, fanart=fanart_host))

    return itemlist


def temporadas(item):
    logger.info()
    itemlist = []

    # ~ data = httptools.downloadpage(item.url).data
    data = obtener_data(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s", "", data)

    if not item.fanart:
        patron = '<div class="hero-image"><img src="([^"]+)"'
        item.fanart = scrapertools.find_single_match(data, patron)

    patron = '<h3 class="pt15 pb15 dBlock clear seasonTitle">([^<]+).*?'
    patron += '<div class="bpM18 bpS25 mt15 mb20 noPadding"><figure><img src="([^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)

    if len(matches) > 1:
        for scrapedseason, scrapedthumbnail in matches:
            temporada = scrapertools.find_single_match(scrapedseason, '(\d+)')
            new_item = item.clone(action="episodios", season=temporada, thumbnail=scrapedthumbnail)
            new_item.infoLabels['season'] = temporada
            new_item.extra = ""
            itemlist.append(new_item)

        # Obtenemos los datos de todas las temporadas de la serie mediante multihilos
        tmdb.set_infoLabels(itemlist, __modo_grafico__)
        for i in itemlist:
            i.title = "%s. %s" % (i.infoLabels['season'], i.infoLabels['tvshowtitle'])
            if i.infoLabels['title']:
                # Si la temporada tiene nombre propio añadirselo al titulo del item
                i.title += " - %s" % (i.infoLabels['title'])
            if i.infoLabels.has_key('poster_path'):
                # Si la temporada tiene poster propio remplazar al de la serie
                i.thumbnail = i.infoLabels['poster_path']

        itemlist.sort(key=lambda it: it.title)

        # Opción "Añadir esta serie a la videoteca"
        if config.get_videolibrary_support() and len(itemlist) > 0:
            itemlist.append(Item(channel=__channel__, title="Añadir esta serie a la videoteca", url=item.url,
                                 action="add_serie_to_library", extra="episodios", show=item.show, category="Series",
                                 thumbnail=thumbnail_host, fanart=fanart_host))

        return itemlist
    else:
        return episodios(item)


def findvideos(item):
    logger.info()
    logger.info("item.url %s" % item.url)
    itemlist = []

    # ~ data = httptools.downloadpage(item.url).data
    data = obtener_data(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s", "", data)

    patron = '<iframe src=".+?id=(\d+)'
    key = scrapertools.find_single_match(data, patron)
    url = CHANNEL_HOST + 'api/iframes.php?id=%s&update1.1' % key

    headers = dict()
    headers["Referer"] = item.url
    data = httptools.downloadpage(url, headers=headers).data

    patron = '<a href="([^"]+)".+?><img src="/api/img/([^.]+)'
    matches = scrapertools.find_multiple_matches(data, patron)

    for scrapedurl, scrapedtitle in matches:

        if scrapedurl.startswith("https://cloud.pelispedia.vip/html5.php"):
            parms = dict(re.findall('[&|\?]{1}([^=]*)=([^&]*)', scrapedurl))
            for cal in ['360', '480', '720', '1080']:
                if parms[cal]:
                    url_v = 'https://pelispedia.video/v.php?id=%s&sub=%s&active=%s' % (parms[cal], parms['sub'], cal)
                    title = "Ver video en [HTML5 " + cal + "p]"
                    new_item = item.clone(title=title, url=url_v, action="play", referer=item.url)
                    itemlist.append(new_item)

        elif scrapedurl.startswith("https://load.pelispedia.vip/embed/"):
            if scrapedtitle == 'vid': scrapedtitle = 'vidoza'
            elif scrapedtitle == 'fast': scrapedtitle = 'fastplay'
            title = "Ver video en [" + scrapedtitle + "]"
            new_item = item.clone(title=title, url=scrapedurl, action="play", referer=item.url)
            itemlist.append(new_item)


    # Opción "Añadir esta pelicula a la videoteca"
    if item.extra == "movies" and config.get_videolibrary_support() and len(itemlist) > 0:
        itemlist.append(Item(channel=__channel__, title="Añadir esta película a la videoteca", url=item.url,
                             infoLabels=item.infoLabels, action="add_pelicula_to_library", extra="findvideos",
                             fulltitle=item.title))

    return itemlist


def play(item):
    logger.info("url=%s" % item.url)
    itemlist = []

    if item.url.startswith("https://pelispedia.video/v.php"):

        headers = {'Referer': item.referer}
        resp = httptools.downloadpage(item.url, headers=headers, cookies=False)
        
        for h in resp.headers:
            ck = scrapertools.find_single_match(resp.headers[h], '__cfduid=([^;]*)')
            if ck:
                gsv = scrapertools.find_single_match(resp.data, '<meta name="google-site-verification" content="([^"]*)"')
                token = generar_token(gsv, 'b0a8c83650f18ccc7c87b16e3c460474'+'yt'+'b0a8c83650f18ccc7c87b16e3c460474'+'2653')
                playparms = scrapertools.find_single_match(resp.data, 'Play\("([^"]*)","([^"]*)","([^"]*)"')
                if playparms:
                    link = playparms[0]
                    subtitle = '' if playparms[1] == '' or playparms[2] == '' else playparms[2] + playparms[1] + '.srt'
                else:
                    link = scrapertools.find_single_match(item.url, 'id=([^;]*)')
                    subtitle = ''
                # ~ logger.info("gsv: %s token: %s ck: %s link: %s" % (gsv, token, ck, link))

                post = "link=%s&token=%s" % (link, token)
                headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': '__cfduid=' + ck}
                data = httptools.downloadpage("https://pelispedia.video/plugins/gkpedia.php", post=post, headers=headers, cookies=False).data
                
                mp4 = scrapertools.find_single_match(data, '"link":"([^"]*)')
                if mp4:
                    mp4 = mp4.replace('\/', '/')
                    if 'chomikuj.pl/' in mp4: mp4 += "|Referer=%s" % item.referer
                    itemlist.append(['.mp4', mp4, 0, subtitle])
                
                break


    elif item.url.startswith("https://load.pelispedia.vip/embed/"):
        
        headers = {'Referer': item.referer}
        resp = httptools.downloadpage(item.url, headers=headers, cookies=False)

        for h in resp.headers:
            ck = scrapertools.find_single_match(resp.headers[h], '__cfduid=([^;]*)')
            if ck:
                gsv = scrapertools.find_single_match(resp.data, '<meta name="google-site-verification" content="([^"]*)"')
                token = generar_token(gsv, '4fe554b59d760c9986c903b07af8b7a4'+'yt'+'4fe554b59d760c9986c903b07af8b7a4'+'785446346')
                url = item.url.replace('/embed/', '/stream/') + '/' + token
                # ~ logger.info("gsv: %s token: %s ck: %s" % (gsv, token, ck))

                headers = {'Referer': item.url, 'Cookie': '__cfduid=' + ck}
                data = httptools.downloadpage(url, headers=headers, cookies=False).data
                
                url = scrapertools.find_single_match(data, '<meta (?:name|property)="og:url" content="([^"]+)"')
                srv = scrapertools.find_single_match(data, '<meta (?:name|property)="og:sitename" content="([^"]+)"')
                if srv == '' and 'rapidvideo.com/' in url: srv = 'rapidvideo'

                if url != '' and srv != '':
                    itemlist.append(item.clone(url=url, server=srv.lower()))

                elif '<title>Vidoza</title>' in data or '|fastplay|' in data:
                    if '|fastplay|' in data:
                        packed = scrapertools.find_single_match(data, "<script type='text/javascript'>(eval\(.*?)</script>")
                        from lib import jsunpack
                        data = jsunpack.unpack(packed)
                        data = data.replace("\\'", "'")

                    matches = scrapertools.find_multiple_matches(data, 'file\s*:\s*"([^"]+)"\s*,\s*label\s*:\s*"([^"]+)"')
                    subtitle = ''
                    for fil, lbl in matches:
                        if fil.endswith('.srt') and not fil.endswith('empty.srt'):
                            subtitle = fil
                            if not subtitle.startswith('http'):
                                domi = scrapertools.find_single_match(data, 'aboutlink\s*:\s*"([^"]*)')
                                subtitle = domi + subtitle
                            break

                    for fil, lbl in matches:
                        if not fil.endswith('.srt'):
                            itemlist.append([lbl, fil, 0, subtitle])

                break


    else:
        itemlist = servertools.find_video_items(data=item.url)
        for videoitem in itemlist:
            videoitem.title = item.title
            videoitem.channel = __channel__

    logger.info("retorna itemlist: %s" % itemlist)
    return itemlist



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def obtener_data(url, referer=''):
    headers = {}
    if referer != '': headers['Referer'] = referer
    data = httptools.downloadpage(url, headers=headers).data
    if "Javascript is required" in data:
        ck = decodificar_cookie(data)
        logger.info("Javascript is required. Cookie necesaria %s" % ck)
        
        headers['Cookie'] = ck
        data = httptools.downloadpage(url, headers=headers).data

        # Guardar la cookie y eliminar la que pudiera haber anterior
        cks = ck.split("=")
        cookie_file = filetools.join(config.get_data_path(), 'cookies.dat')
        cookie_data = filetools.read(cookie_file)
        cookie_data = re.sub(r"www\.pelispedia\.tv\tFALSE\t/\tFALSE\t\tsucuri_(.*)\n", "", cookie_data)
        cookie_data += "www.pelispedia.tv\tFALSE\t/\tFALSE\t\t%s\t%s\n" % (cks[0], cks[1])
        filetools.write(cookie_file, cookie_data)
        logger.info("Añadida cookie %s con valor %s" % (cks[0], cks[1]))

    return data


def rshift(val, n): return val>>n if val >= 0 else (val+0x100000000)>>n

def decodificar_cookie(data):
    S = re.compile("S='([^']*)'").findall(data)[0]
    A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    s = {}
    l = 0
    U = 0
    L = len(S)
    r = ''

    for u in range(0, 64):
        s[A[u]] = u

    for i in range(0, L):
        if S[i] == '=': continue
        c = s[S[i]]
        U = (U << 6) + c
        l += 6
        while (l >= 8):
            l -= 8
            a = rshift(U, l) & 0xff
            r += chr(a)

    r = re.sub(r"\s+|/\*.*?\*/", "", r)
    r = re.sub("\.substr\(([0-9]*),([0-9*])\)", r"[\1:(\1+\2)]", r)
    r = re.sub("\.charAt\(([0-9]*)\)", r"[\1]", r)
    r = re.sub("\.slice\(([0-9]*),([0-9*])\)", r"[\1:\2]", r)
    r = r.replace("String.fromCharCode", "chr")
    r = r.replace("location.reload();", "")

    pos = r.find("document.cookie")
    nomvar = r[0]
    l1 = r[2:pos-1]
    l2 = r[pos:-1].replace("document.cookie=", "").replace("+"+nomvar+"+", "+g+")

    g = eval(l1)
    return eval(l2).replace(";path=/;max-age=86400", "")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def evpKDF(passwd, salt, key_size=8, iv_size=4, iterations=1, hash_algorithm="md5"):
    import hashlib
    target_key_size = key_size + iv_size
    derived_bytes = ""
    number_of_derived_words = 0
    block = None
    hasher = hashlib.new(hash_algorithm)
    while number_of_derived_words < target_key_size:
        if block is not None:
            hasher.update(block)

        hasher.update(passwd)
        hasher.update(salt)
        block = hasher.digest()
        hasher = hashlib.new(hash_algorithm)

        for i in range(1, iterations):
            hasher.update(block)
            block = hasher.digest()
            hasher = hashlib.new(hash_algorithm)

        derived_bytes += block[0: min(len(block), (target_key_size - number_of_derived_words) * 4)]

        number_of_derived_words += len(block)/4

    return {
        "key": derived_bytes[0: key_size * 4],
        "iv": derived_bytes[key_size * 4:]
    }

def obtener_cripto(password, plaintext):
    import os, base64, json
    SALT_LENGTH = 8
    BLOCK_SIZE = 16
    KEY_SIZE = 32

    salt = os.urandom(SALT_LENGTH)
    iv = os.urandom(BLOCK_SIZE)

    paddingLength = 16 - (len(plaintext) % 16)
    paddedPlaintext = plaintext+chr(paddingLength)*paddingLength

    kdf = evpKDF(password, salt)

    try: # Intentar con librería AES del sistema
        from Crypto.Cipher import AES
        cipherSpec = AES.new(kdf['key'], AES.MODE_CBC, iv)
    except: # Si falla intentar con librería del addon 
        import jscrypto
        cipherSpec = jscrypto.new(kdf['key'], jscrypto.MODE_CBC, iv)
    ciphertext = cipherSpec.encrypt(paddedPlaintext)

    return json.dumps({'ct': base64.b64encode(ciphertext), 'iv': iv.encode("hex"), 's': salt.encode("hex")}, sort_keys=True, separators=(',', ':'))

def generar_token(gsv, pwd):
    txt = obtener_cripto(pwd, gsv)

    _0x382d28 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

    valors = [0, 0, 0]
    cicle = 0
    retorn = ''
    for ch in txt:
        valors[cicle] = ord(ch)
        cicle += 1
        if cicle == 3:
            primer = _0x382d28[valors[0] >> 0x2]
            segon  = _0x382d28[((valors[0] & 0x3) << 0x4) | (valors[1] >> 0x4)]
            tercer = _0x382d28[((valors[1] & 0xf) << 0x2) | (valors[2] >> 0x6)]
            quart  = _0x382d28[valors[2] & 0x3f]
            retorn += primer + segon + tercer + quart
            
            valors = [0, 0, 0]
            cicle = 0

    return retorn
