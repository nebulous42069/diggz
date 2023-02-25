# -*- coding: utf-8 -*-

import sys, os, re, time, base64, sqlite3
from datetime import datetime

from core import filetools, jsontools
from core.item import Item
from platformcode import config, logger, platformtools

PY3 = sys.version_info[0] >= 3
# Funciones auxiliares

# Devuelve el nombre de la base de datos de tracking activa (sin el sufijo .sqlite)
def get_current_dbname():
    return config.get_setting('tracking_current_dbname', default = 'default')

# Establece el nombre de la base de datos de tracking activa (sin el sufijo .sqlite)
def set_current_dbname(dbname):
    config.set_setting('tracking_current_dbname', dbname.replace('.sqlite', ''))

# Devuelve la ruta dónde se guardan las bases de datos de tracking
def get_tracking_path():
    # TODO path configurable !? ... puede dar problemas con sqlite ...
    tracking_path = filetools.join(config.get_data_path(), 'tracking_dbs')
    if not filetools.exists(tracking_path): filetools.mkdir(tracking_path)
    return tracking_path

# Convierte fecha para guardar en la bd como AAAA-MM-DD para poder ordenar por ella
def date_for_db(fecha, sin_fecha='0000-00-00'):
    if fecha == '': return sin_fecha
    if '/' in fecha: aux = fecha.split('/')
    elif '-' in fecha: aux = fecha.split('-')
    else: return sin_fecha
    if len(aux) != 3: return sin_fecha
    if len(aux[0]) == 4: return '%s-%s-%s' % (aux[0], aux[1], aux[2])
    else: return '%s-%s-%s' % (aux[2], aux[1], aux[0])


# Clase para cargar y guardar en la bd de tracking
class TrackingData:
    def __init__(self, filename = None):

        # Si no se especifica ningún fichero se usa la bd activa (si no existe se crea vacía)
        if filename is None: filename = get_current_dbname()
        if not filename.endswith('.sqlite'): filename += '.sqlite'

        self.filename = filetools.join(get_tracking_path(), filename)

        self.conn = sqlite3.connect(self.filename)
        self.cur = self.conn.cursor()

        try:
            # PRAGMA user_version para identificar versión de las tablas y crear/alterar en consecuencia
            self.cur.execute('PRAGMA user_version')
            db_user_version = self.cur.fetchone()[0]

            if db_user_version == 0:
                self.create_tables()
                self.cur.execute('PRAGMA user_version=1')
                db_user_version = 1
                logger.info('Base de datos %s actualizada a versión %d' % (self.filename, int(db_user_version)))

            if db_user_version == 1:
                self.cur.execute('ALTER TABLE seasons ADD reverseorder INTEGER')
                self.cur.execute('PRAGMA user_version=2')
                db_user_version = 2
                logger.info('Base de datos %s actualizada a versión %d' % (self.filename, int(db_user_version)))

            if db_user_version == 2:
                logger.debug('Base de datos %s ok con última versión (%d)' % (self.filename, int(db_user_version)))
        except:
            logger.debug('Fallo en PRAGMA... %s' % self.filename)
            pass

    def create_tables(self):
        # - En las tablas movies, shows, seasons, episodes se guardan los infolabels.
        #   Los campos updated, title, aired se usan para poder ordenar los registros ya que los infolabels están b64encodeados.
        # - En las tablas channels_* se guardan los enlaces de cada canal agregado.
        # - La tabla tracking_shows se usa para gestionar las actualizaciones para buscar nuevos episodios.
        #   updated: cuando se actualiza el tracking. lastscrap: timestamp último scrap hecho. 
        #   periodicity: cada cuantas horas hay que scrapear. tvdbinfo: si hay que llamar a tvdb para episodios nuevos.

        self.cur.execute('CREATE TABLE IF NOT EXISTS movies (tmdb_id TEXT, infolabels TEXT, updated TEXT, title TEXT, aired TEXT)')
        self.cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS ix_movie ON movies (tmdb_id)')
        self.cur.execute('CREATE INDEX IF NOT EXISTS ix_movie_updated ON movies (updated)')
        self.cur.execute('CREATE INDEX IF NOT EXISTS ix_movie_title ON movies (title)')
        self.cur.execute('CREATE INDEX IF NOT EXISTS ix_movie_aired ON movies (aired)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS channels_movies (channel TEXT, tmdb_id TEXT, url TEXT, updated TEXT)')
        self.cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS ix_channel_movie ON channels_movies (channel, tmdb_id)')


        self.cur.execute('CREATE TABLE IF NOT EXISTS shows (tmdb_id TEXT, infolabels TEXT, updated TEXT, title TEXT, aired TEXT)')
        self.cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS ix_show ON shows (tmdb_id)')
        self.cur.execute('CREATE INDEX IF NOT EXISTS ix_show_updated ON shows (updated)')
        self.cur.execute('CREATE INDEX IF NOT EXISTS ix_show_title ON shows (title)')
        self.cur.execute('CREATE INDEX IF NOT EXISTS ix_show_aired ON shows (aired)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS seasons (tmdb_id TEXT, season INTEGER, infolabels TEXT, updated TEXT)')
        self.cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS ix_season ON seasons (tmdb_id, season)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS episodes (tmdb_id TEXT, season INTEGER, episode INTEGER, infolabels TEXT, updated TEXT, aired TEXT)')
        self.cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS ix_episode ON episodes (tmdb_id, season, episode)')
        self.cur.execute('CREATE INDEX IF NOT EXISTS ix_episode_updated ON shows (updated)')
        self.cur.execute('CREATE INDEX IF NOT EXISTS ix_episode_aired ON shows (aired)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS channels_shows (channel TEXT, tmdb_id TEXT, url TEXT, updated TEXT)')
        self.cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS ix_channel_show ON channels_shows (channel, tmdb_id)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS channels_seasons (channel TEXT, tmdb_id TEXT, season INTEGER, url TEXT, updated TEXT)')
        self.cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS ix_channel_season ON channels_seasons (channel, tmdb_id, season)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS channels_episodes (channel TEXT, tmdb_id TEXT, season INTEGER, episode INTEGER, url TEXT, updated TEXT)')
        self.cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS ix_channel_episode ON channels_episodes (channel, tmdb_id, season, episode)')


        self.cur.execute('CREATE TABLE IF NOT EXISTS tracking_shows (tmdb_id TEXT, updated TEXT, periodicity TEXT, tvdbinfo INTEGER, lastscrap TEXT)')
        self.cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS ix_tracking_show ON tracking_shows (tmdb_id)')


    def close(self, commit=False, rollback=False):
        if commit: self.conn.commit()
        elif rollback: self.conn.rollback()
        self.conn.close()

    # Table: movies

    def movie_exists(self, tmdb_id=''):
        self.cur.execute('SELECT tmdb_id FROM movies WHERE tmdb_id=?', (tmdb_id,))
        row = self.cur.fetchone()
        return True if row else False

    def get_movie(self, tmdb_id=''):
        self.cur.execute('SELECT infolabels FROM movies WHERE tmdb_id=?', (tmdb_id,))
        row = self.cur.fetchone()
        if row:
            return jsontools.load(base64.b64decode(row[0]))
        else:
            return None

    def save_movie(self, tmdb_id='', infolabels='', commit=False):
        try:
            title = infolabels['title'].decode('utf-8')
        except:
            title = infolabels['title']
        aired = date_for_db(infolabels['release_date'])
        self.cur.execute('INSERT OR REPLACE INTO movies (tmdb_id, infolabels, updated, title, aired) VALUES (?, ?, ?, ?, ?)',
                                  (tmdb_id, base64.b64encode(jsontools.dump(infolabels).encode('utf-8')) if PY3 else base64.b64encode(jsontools.dump(infolabels)), datetime.now(), title, aired ))
        if commit: self.conn.commit()

    def delete_movie(self, tmdb_id='', commit=False):
        self.cur.execute('DELETE FROM movies WHERE tmdb_id=?', (tmdb_id,))
        self.cur.execute('DELETE FROM channels_movies WHERE tmdb_id=?', (tmdb_id,))
        if commit: self.conn.commit()

    def get_movies(self, orden='updated DESC', desde=0, numero=10):
        self.cur.execute('SELECT tmdb_id, infolabels FROM movies ORDER BY %s LIMIT %d, %d' % (orden, int(desde), int(numero)))
        rows = self.cur.fetchall()
        return [ [row[0], jsontools.load(base64.b64decode(row[1]))] for row in rows]

    def get_movies_count(self):
        self.cur.execute('SELECT COUNT() FROM movies')
        return self.cur.fetchone()[0]

    # Table: channels_movies

    def movie_channel_exists(self, tmdb_id='', channel=''):
        self.cur.execute('SELECT tmdb_id FROM channels_movies WHERE channel=? AND tmdb_id=?', (channel, tmdb_id))
        row = self.cur.fetchone()
        return True if row else False

    def get_movie_channels(self, tmdb_id=''):
        self.cur.execute('SELECT channel, url FROM channels_movies WHERE tmdb_id=?', (tmdb_id,))           
        rows = self.cur.fetchall()
        return rows

    def get_movie_channel(self, tmdb_id='', channel=''):
        self.cur.execute('SELECT url FROM channels_movies WHERE channel=? AND tmdb_id=?', (channel, tmdb_id))
        row = self.cur.fetchone()
        if row:
            return row[0]
        else:
            return None

    def save_movie_channel(self, tmdb_id='', channel='', url='', commit=False):
        self.cur.execute('INSERT OR REPLACE INTO channels_movies (channel, tmdb_id, url, updated) VALUES (?, ?, ?, ?)',
                                  (channel, tmdb_id, url, datetime.now() ))
        if commit: self.conn.commit()

    def delete_movie_channel(self, tmdb_id='', channel='', commit=False):
        self.cur.execute('DELETE FROM channels_movies WHERE channel=? AND tmdb_id=?', (channel, tmdb_id))
        if commit: self.conn.commit()

    # Table: shows

    def show_exists(self, tmdb_id=''):
        self.cur.execute('SELECT tmdb_id FROM shows WHERE tmdb_id=?', (tmdb_id,))
        row = self.cur.fetchone()
        return True if row else False

    def get_show(self, tmdb_id=''):
        self.cur.execute('SELECT infolabels FROM shows WHERE tmdb_id=?', (tmdb_id,))
        row = self.cur.fetchone()
        if row:
            return jsontools.load(base64.b64decode(row[0]))
        else:
            return None

    def save_show(self, tmdb_id='', infolabels='', commit=False):
        try:
            title = infolabels['title'].decode('utf-8')
        except:
            title = infolabels['title']
        aired = date_for_db(infolabels['aired'])
        self.cur.execute('INSERT OR REPLACE INTO shows (tmdb_id, infolabels, updated, title, aired) VALUES (?, ?, ?, ?, ?)',
                                  (tmdb_id, base64.b64encode(jsontools.dump(infolabels).encode('utf-8')) if PY3 else base64.b64encode(jsontools.dump(infolabels)), datetime.now(), title, aired ))
        if commit: self.conn.commit()

    def delete_show(self, tmdb_id='', commit=False):
        self.cur.execute('DELETE FROM shows WHERE tmdb_id=?', (tmdb_id,))
        self.cur.execute('DELETE FROM seasons WHERE tmdb_id=?', (tmdb_id,))
        self.cur.execute('DELETE FROM episodes WHERE tmdb_id=?', (tmdb_id,))
        self.cur.execute('DELETE FROM channels_shows WHERE tmdb_id=?', (tmdb_id,))
        self.cur.execute('DELETE FROM channels_seasons WHERE tmdb_id=?', (tmdb_id,))
        self.cur.execute('DELETE FROM channels_episodes WHERE tmdb_id=?', (tmdb_id,))
        self.cur.execute('DELETE FROM tracking_shows WHERE tmdb_id=?', (tmdb_id,))
        if commit: self.conn.commit()

    def get_shows(self, orden='updated DESC', desde=0, numero=10):
        self.cur.execute('SELECT tmdb_id, infolabels FROM shows ORDER BY %s LIMIT %d, %d' % (orden, int(desde), int(numero)))
        rows = self.cur.fetchall()
        return [ [row[0], jsontools.load(base64.b64decode(row[1]))] for row in rows]

    def get_shows_count(self):
        self.cur.execute('SELECT COUNT(*) FROM shows')
        return self.cur.fetchone()[0]

    # Table: channels_shows

    def show_channel_exists(self, tmdb_id='', channel=''):
        self.cur.execute('SELECT tmdb_id FROM channels_shows WHERE channel=? AND tmdb_id=?', (channel, tmdb_id))
        row = self.cur.fetchone()
        return True if row else False

    def get_show_channels(self, tmdb_id=''):
        self.cur.execute('SELECT channel, url FROM channels_shows WHERE tmdb_id=?', (tmdb_id,))           
        rows = self.cur.fetchall()
        return rows

    def get_show_channel(self, tmdb_id='', channel=''):
        self.cur.execute('SELECT url FROM channels_shows WHERE channel=? AND tmdb_id=?', (channel, tmdb_id))
        row = self.cur.fetchone()
        if row:
            return row[0]
        else:
            return None

    def save_show_channel(self, tmdb_id='', channel='', url='', commit=False):
        self.cur.execute('INSERT OR REPLACE INTO channels_shows (channel, tmdb_id, url, updated) VALUES (?, ?, ?, ?)',
                                  (channel, tmdb_id, url, datetime.now() ))
        if commit: self.conn.commit()

    def delete_show_channel(self, tmdb_id='', channel='', commit=False):
        self.cur.execute('DELETE FROM channels_shows WHERE channel=? AND tmdb_id=?', (channel, tmdb_id))
        self.cur.execute('DELETE FROM channels_seasons WHERE channel=? AND tmdb_id=?', (channel, tmdb_id))
        self.cur.execute('DELETE FROM channels_episodes WHERE channel=? AND tmdb_id=?', (channel, tmdb_id))
        if commit: self.conn.commit()

    # Table: seasons

    def season_exists(self, tmdb_id='', season=0):
        self.cur.execute('SELECT tmdb_id FROM seasons WHERE tmdb_id=? AND season=?', (tmdb_id, int(season)))
        row = self.cur.fetchone()
        return True if row else False

    def get_season(self, tmdb_id='', season=0):
        self.cur.execute('SELECT infolabels FROM seasons WHERE tmdb_id=? AND season=?', (tmdb_id, int(season)))
        row = self.cur.fetchone()
        if row:
            return jsontools.load(base64.b64decode(row[0]))
        else:
            return None

    def save_season(self, tmdb_id='', season=0, infolabels='', commit=False):
        self.cur.execute('INSERT OR REPLACE INTO seasons (tmdb_id, season, infolabels, updated) VALUES (?, ?, ?, ?)',
                                  (tmdb_id, int(season), base64.b64encode(jsontools.dump(infolabels).encode('utf-8')) if PY3 else base64.b64encode(jsontools.dump(infolabels)), datetime.now() ))
        if commit: self.conn.commit()

    def delete_season(self, tmdb_id='', season=0, commit=False):
        self.cur.execute('DELETE FROM seasons WHERE tmdb_id=? AND season=?', (tmdb_id, int(season)))
        self.cur.execute('DELETE FROM episodes WHERE tmdb_id=? AND season=?', (tmdb_id, int(season)))
        self.cur.execute('DELETE FROM channels_seasons WHERE tmdb_id=? AND season=?', (tmdb_id, int(season)))
        self.cur.execute('DELETE FROM channels_episodes WHERE tmdb_id=? AND season=?', (tmdb_id, int(season)))
        if commit: self.conn.commit()

    def get_seasons(self, tmdb_id=''):
        self.cur.execute('SELECT season, infolabels FROM seasons WHERE tmdb_id=? ORDER BY season ASC', (tmdb_id,))
        rows = self.cur.fetchall()
        return [ [row[0], jsontools.load(base64.b64decode(row[1]))] for row in rows]

    # Table: channels_seasons

    def season_channel_exists(self, tmdb_id='', season=0, channel=''):
        self.cur.execute('SELECT tmdb_id FROM channels_seasons WHERE channel=? AND tmdb_id=? AND season=?', (channel, tmdb_id, int(season)))
        row = self.cur.fetchone()
        return True if row else False

    def get_season_channels(self, tmdb_id='', season=0):
        self.cur.execute('SELECT channel, url FROM channels_seasons WHERE tmdb_id=? AND season=?', (tmdb_id, int(season)))           
        rows = self.cur.fetchall()
        return rows

    def get_season_channel(self, tmdb_id='', season=0, channel=''):
        self.cur.execute('SELECT url FROM channels_seasons WHERE channel=? AND tmdb_id=? AND season=?', (channel, tmdb_id, int(season)))
        row = self.cur.fetchone()
        if row:
            return row[0]
        else:
            return None

    def save_season_channel(self, tmdb_id='', season=0, channel='', url='', commit=False):
        self.cur.execute('INSERT OR REPLACE INTO channels_seasons (channel, tmdb_id, season, url, updated) VALUES (?, ?, ?, ?, ?)',
                                  (channel, tmdb_id, int(season), url, datetime.now() ))
        if commit: self.conn.commit()

    def delete_season_channel(self, tmdb_id='', season=0, channel='', commit=False):
        self.cur.execute('DELETE FROM channels_seasons WHERE channel=? AND tmdb_id=? AND season=?', (channel, tmdb_id, int(season)))
        self.cur.execute('DELETE FROM channels_episodes WHERE channel=? AND tmdb_id=? AND season=?', (channel, tmdb_id, int(season)))
        if commit: self.conn.commit()

    # Table: episodes

    def episode_exists(self, tmdb_id='', season=0, episode=0):
        self.cur.execute('SELECT tmdb_id FROM episodes WHERE tmdb_id=? AND season=? AND episode=?', (tmdb_id, int(season), int(episode)))
        row = self.cur.fetchone()
        return True if row else False

    def get_episode(self, tmdb_id='', season=0, episode=0):
        self.cur.execute('SELECT infolabels FROM episodes WHERE tmdb_id=? AND season=? AND episode=?', (tmdb_id, int(season), int(episode)))
        row = self.cur.fetchone()
        if row:
            return jsontools.load(base64.b64decode(row[0]))
        else:
            return None

    def save_episode(self, tmdb_id='', season=0, episode=0, infolabels='', commit=False):
        aired = date_for_db(infolabels['aired'])
        self.cur.execute('INSERT OR REPLACE INTO episodes (tmdb_id, season, episode, infolabels, updated, aired) VALUES (?, ?, ?, ?, ?, ?)',
                                  (tmdb_id, int(season), int(episode), base64.b64encode(jsontools.dump(infolabels).encode('utf-8')) if PY3 else base64.b64encode(jsontools.dump(infolabels)), datetime.now(), aired ))
        if commit: self.conn.commit()

    def delete_episode(self, tmdb_id='', season=0, episode=0, commit=False):
        self.cur.execute('DELETE FROM episodes WHERE tmdb_id=? AND season=? AND episode=?', (tmdb_id, int(season), int(episode)))
        self.cur.execute('DELETE FROM channels_episodes WHERE tmdb_id=? AND season=? AND episode=?', (tmdb_id, int(season), int(episode)))
        if commit: self.conn.commit()

    def get_episodes(self, tmdb_id='', season=-1, reverse_order=False):
        episode_sort = 'DESC' if reverse_order else 'ASC'
        if season == -1:
            self.cur.execute('SELECT season, episode, infolabels FROM episodes WHERE tmdb_id=? ORDER BY season ASC, episode ' + episode_sort, (tmdb_id,))
        else:
            self.cur.execute('SELECT season, episode, infolabels FROM episodes WHERE tmdb_id=? AND season=? ORDER BY episode ' + episode_sort, (tmdb_id, int(season)))
        rows = self.cur.fetchall()
        return [ [row[0], row[1], jsontools.load(base64.b64decode(row[2]))] for row in rows]

    def get_episodes_count(self):
        self.cur.execute('SELECT COUNT() FROM episodes')
        return self.cur.fetchone()[0]

    def get_all_episodes(self, orden='updated DESC', desde=0, numero=10):
        self.cur.execute('SELECT tmdb_id, season, episode, infolabels FROM episodes ORDER BY %s LIMIT %d, %d' % (orden, int(desde), int(numero)))
        rows = self.cur.fetchall()
        return [ [row[0], row[1], row[2], jsontools.load(base64.b64decode(row[3]))] for row in rows]

    # Table: channels_episodes

    def episode_channel_exists(self, tmdb_id='', season=0, episode=0, channel=''):
        self.cur.execute('SELECT tmdb_id FROM channels_episodes WHERE channel=? AND tmdb_id=? AND season=? AND episode=?', (channel, tmdb_id, int(season), int(episode)))
        row = self.cur.fetchone()
        return True if row else False

    def get_episode_channels(self, tmdb_id='', season=0, episode=0):
        self.cur.execute('SELECT channel, url FROM channels_episodes WHERE tmdb_id=? AND season=? AND episode=?', (tmdb_id, int(season), int(episode)))           
        rows = self.cur.fetchall()
        return rows

    def get_episode_channel(self, tmdb_id='', season=0, episode=0, channel=''):
        self.cur.execute('SELECT url FROM channels_episodes WHERE channel=? AND tmdb_id=? AND season=? AND episode=?', (channel, tmdb_id, int(season), int(episode)))
        row = self.cur.fetchone()
        if row:
            return row[0]
        else:
            return None

    def save_episode_channel(self, tmdb_id='', season=0, episode=0, channel='', url='', commit=False):
        self.cur.execute('INSERT OR REPLACE INTO channels_episodes (channel, tmdb_id, season, episode, url, updated) VALUES (?, ?, ?, ?, ?, ?)',
                                  (channel, tmdb_id, int(season), int(episode), url, datetime.now() ))
        if commit: self.conn.commit()

    def delete_episode_channel(self, tmdb_id='', season=0, episode=0, channel='', commit=False):
        self.cur.execute('DELETE FROM channels_episodes WHERE channel=? AND tmdb_id=? AND season=? AND episode=?', (channel, tmdb_id, int(season), int(episode)))
        if commit: self.conn.commit()

    # Table: tracking_shows

    def tracking_show_exists(self, tmdb_id=''):
        self.cur.execute('SELECT tmdb_id FROM tracking_shows WHERE tmdb_id=?', (tmdb_id,))
        row = self.cur.fetchone()
        return True if row else False

    def get_tracking_show(self, tmdb_id=''):
        self.cur.execute('SELECT periodicity, tvdbinfo, lastscrap FROM tracking_shows WHERE tmdb_id=?', (tmdb_id,))
        row = self.cur.fetchone()
        return row

# Funciones scrap para películas y series
    # Los infoLabels se guardan en las tablas de movies, shows, seasons, episodes.
    # Las urls (el item con el que se llamará al canal) se guardan en las tablas channels_*.
    # Las urls se guardan sin infoLabels para aligerar y pq ya se almacenan en las tablas de movies, shows, seasons, episodes.

    # Variable update_infolabels: True siempre actualiza los infolabels con los datos recibidos. False: solamente actualiza si no existe previamente.
    # Variable update_urls: True siempre actualiza con los enlaces recibidos. False: solamente actualiza si no existen previamente.

    # Cuando se guarda una peli/serie/temporada/episodio desde un canal, se hace scrap con update_infolabels=False, update_urls=True
    # Sólo se actualizan los infolabels si no existen, y siempre se actualizan las urls del canal.

    # Cuando desde una serie se buscan nuevos episodios, se hace scrap con update_infolabels=False, update_urls=False
    # Sólo se actualizan los infolabels si no existen, y sólo se actualizan las urls del canal si no existen.
    # Además en este caso la rutina devolverá un msg con las novedades.

    # Lo de no actualizar infolabels si ya existen es para conservar los existentes por si el usuario los ha cambiado.


def scrap_and_save_movie(item, op='add'):
    # Al añadir una película se guardan sus infolabels, y los enlaces al canal desde dónde se añade.
    # El item recibido tiene que tener tmdb_id informado y ser 'movie'.
    # También se requiere el channel+action y los parámetros necesarios para hacer la llamada al canal.
    #
    # Devuelve True si se completa ok y False en caso contrario, más un texto con la información del error o proceso ok
    #

    logger.info()
    tmdb_id = item.infoLabels['tmdb_id']

    if not tmdb_id: return False, 'Se requiere id de TMDB'
    if item.contentType != 'movie': return False, 'contentType no contemplado!'

    # Tipo de scrap a realizar

    if op == 'add':
        # Al añadir una película desde el menú contextual, actualizar siempre urls, infolabels solamente si no existen.
        update_infolabels = False
        update_urls = True
    else: 
        return False, 'Invalid op!'

    # Conexión bd
    db = TrackingData()

    # Datos a nivel de la película
    if update_infolabels or not db.movie_exists(tmdb_id):
        db.save_movie(tmdb_id, item.infoLabels)

    # Datos a nivel de película+canal
    if update_urls or not db.movie_channel_exists(tmdb_id, item.channel):
        db.save_movie_channel(tmdb_id, item.channel, item.clone(infoLabels={}).tourl())

    # Cerrar conexión bd
    db.close(commit=True)

    return True, 'Seguimiento película con tmdb_id: %s' % tmdb_id


def scrap_and_save_tvshow(item, op='add', tvdbinfo=False):
    # Al añadir una serie se guardan los infolabels de serie + temporadas + episodios, y los enlaces al canal desde dónde se añade.
    # El item recibido tiene que tener tmdb_id informado y ser 'tvshow', 'season' o 'episode'.
    # También se requiere el channel+action y los parámetros necesarios para hacer la llamada al canal.
    # Con tvdbinfo=True, para cada episodio añadido se llama a tvdb para recuperar la info de allí.
    #
    # 'tvshow' : Se llama al canal para recuperar todas las temporadas, y para cada una de ellas todos sus capítulos.
    # 'season' : Se llama al canal para una temporada concreta y se obtienen todos sus capítulos.
    # 'episode' : Se llama al canal para un episodio concreto.
    #
    # Los datos recogidos al llamar a esta rutina dependerán de lo que devuelva el canal y de si se pasa una serie, una temporada o un episodio.
    # Ej: Si un canal solamente devuelve una temporada para una serie, se añade esa temporada. Si otro canal (o el mismo desde otro enlace)
    #     devuelve dos temporadas para la misma serie, se completan los datos nuevos.
    # Ej: Si se llama para un episodio suelto desde algún listado de últimos capítulos, y la serie no está trackeada todavía, se añade el
    #     enlace del canal al episodio, pero como no se dispone de la "url" para listar todas las temporadas o una temporada concreta, no 
    #     se puede añadir más. En cambio si se llama para la serie entera, se disponen de los enlaces a cada temporada y se pueden guardar.
    #
    # Devuelve True si se completa ok y False en caso contrario, más un texto con la información del error o proceso ok
    #

    logger.info()
    tmdb_id = item.infoLabels['tmdb_id']

    if not tmdb_id: return False, 'Se requiere id de TMDB'
    if item.contentType not in ['tvshow', 'season', 'episode']: return False, 'contentType no contemplado!'

    # Tipo de scrap a realizar
    if op == 'add':
        # Al añadir una serie/temp/epi desde el menú contextual, actualizar siempre urls, infolabels solamente si no existen.
        update_infolabels = False
        update_urls = True
    elif op == 'new_episodes':
        # Al buscar nuevos episodios, actualizar urls e infolabels solamente si no existen (episodios nuevos).
        update_infolabels = False
        update_urls = False
    else:
        return False, 'Invalid op!'

    # Conexión bd
    db = TrackingData()
    cambios = [] # Para apuntar los cambios hechos en caso de refresco para buscar nuevos episodios

    # Datos a nivel de la serie
    if not db.show_exists(tmdb_id):  # Si no existe dar de alta
        if item.contentType == 'tvshow': # Si proviene de una serie ya se tienen los infolabels
            db.save_show(tmdb_id, item.infoLabels)
        else: # Sino buscar en tmdb
            it = Item( title='', contentType='tvshow', contentSerieName=item.contentSerieName, infoLabels={'tmdb_id': tmdb_id} )
            from core import tmdb
            tmdb.set_infoLabels_item(it)
            db.save_show(tmdb_id, it.infoLabels)

    # Datos a nivel de serie+canal
    if item.contentType == 'tvshow': # Si proviene de serie, guardar su url
        if update_urls or not db.show_channel_exists(tmdb_id, item.channel):
            db.save_show_channel(tmdb_id, item.channel, item.clone(infoLabels={}).tourl())

    # Cargar itemlist a tratar
    if item.contentType in ['season', 'episode']:
        itemlist = [item]

    elif item.contentType == 'tvshow':
        try:
            canal = __import__('channels.' + item.channel, fromlist=[''])
        except:
            return False, 'El canal %s ya no existe' % item.channel

        # Si el canal tiene tracking_all_episodes usarlo para ir más rápido. 
        # Excepción con newpct1, usar sólo tracking_all al añadir para que recorra todos los episodios, pero para actualizar mirar solamente en la primera página de episodios.
        if item.channel == 'newpct1' and op == 'new_episodes': buscar_tracking_all = False
        else: buscar_tracking_all = True

        if buscar_tracking_all and hasattr(canal, 'tracking_all_episodes'):
            itemlist = getattr(canal, 'tracking_all_episodes')(item)
        else:
            if hasattr(canal, item.action):
                itemlist = getattr(canal, item.action)(item)
            else:
                return False, 'En el canal %s ya no existe %s' % (item.channel, item.action)

    if itemlist is None or len(itemlist) == 0:
        db.close()
        return False, 'El canal no devuelve resultados'

    # Si es una actualización y el canal devuelve temporadas en lugar de episodios, solamente buscar episodios nuevos en la última temporada
    if op == 'new_episodes' and itemlist[0].contentType == 'season' and len(itemlist) > 1:
        itemlist = itemlist[-1:]

    # Datos a nivel de temporadas/episodios

    # Si el canal devuelve una lista de temporadas
    if itemlist[0].contentType == 'season':
        try:
            canal = __import__('channels.' + item.channel, fromlist=[''])
        except:
            return False, 'El canal %s ya no existe' % item.channel

        for it in itemlist:
            # ~ logger.debug(it)
            if it.contentType != 'season': continue
            if it.infoLabels['tmdb_id'] != tmdb_id: continue
            
            # Guardar datos de la temporada
            if update_infolabels or not db.season_exists(tmdb_id, it.contentSeason):
                db.save_season(tmdb_id, it.contentSeason, it.infoLabels)

            # Guardar url para temporada+canal
            if update_urls or not db.season_channel_exists(tmdb_id, it.contentSeason, it.channel):
                db.save_season_channel(tmdb_id, it.contentSeason, it.channel, it.clone(infoLabels={}).tourl())
                cambios.append('T%d' % int(it.contentSeason))

            # Llamar al canal para obtener episodios de la temporada
            if hasattr(canal, it.action):
                itemlist_epi = getattr(canal, it.action)(it)
            else:
                itemlist_epi = []

            for it_epi in itemlist_epi:
                if it_epi.contentType != 'episode': continue
                if it_epi.contentSeason != it.contentSeason: continue
                if it_epi.infoLabels['tmdb_id'] != tmdb_id: continue

                # Guardar datos del episodio
                if update_infolabels or not db.episode_exists(tmdb_id, it_epi.contentSeason, it_epi.contentEpisodeNumber):
                    if tvdbinfo and it_epi.infoLabels['tvdb_id']:
                        from core import tvdb
                        tvdb.set_infoLabels_item(it_epi)
                    db.save_episode(tmdb_id, it_epi.contentSeason, it_epi.contentEpisodeNumber, it_epi.infoLabels)

                # Guardar url para episodio+canal
                if update_urls or not db.episode_channel_exists(tmdb_id, it_epi.contentSeason, it_epi.contentEpisodeNumber, it_epi.channel):
                    db.save_episode_channel(tmdb_id, it_epi.contentSeason, it_epi.contentEpisodeNumber, it_epi.channel, it_epi.clone(infoLabels={}).tourl())
                    cambios.append('%dx%d' % (int(it_epi.contentSeason), int(it_epi.contentEpisodeNumber)))

    # Si el canal devuelve una lista de episodios
    elif itemlist[0].contentType == 'episode':
        ant_season = -1 # para no repetir llamadas mientras sea la misma temporada
        for it_epi in itemlist:
            # ~ logger.debug(it_epi)
            if it_epi.contentType != 'episode': continue
            if not it_epi.contentSeason: continue
            if it_epi.infoLabels['tmdb_id'] != tmdb_id: continue

            # Si no hay datos guardados de la temporada, buscarlos en tmdb y darlos de alta
            if ant_season != it_epi.contentSeason:
                if not db.season_exists(tmdb_id, it_epi.contentSeason):
                    it = Item( title='', contentType='season', contentSerieName=it_epi.contentSerieName, contentSeason=it_epi.contentSeason, infoLabels={'tmdb_id': tmdb_id} )
                    from core import tmdb
                    tmdb.set_infoLabels_item(it)
                    db.save_season(tmdb_id, it.contentSeason, it.infoLabels)
                    cambios.append('T%d' % int(it_epi.contentSeason))
                ant_season = it_epi.contentSeason

            # Guardar datos del episodio
            if update_infolabels or not db.episode_exists(tmdb_id, it_epi.contentSeason, it_epi.contentEpisodeNumber):
                if tvdbinfo and it_epi.infoLabels['tvdb_id']:
                    from core import tvdb
                    tvdb.set_infoLabels_item(it_epi)
                db.save_episode(tmdb_id, it_epi.contentSeason, it_epi.contentEpisodeNumber, it_epi.infoLabels)

            # Guardar url para episodio+canal
            if update_urls or not db.episode_channel_exists(tmdb_id, it_epi.contentSeason, it_epi.contentEpisodeNumber, it_epi.channel):
                db.save_episode_channel(tmdb_id, it_epi.contentSeason, it_epi.contentEpisodeNumber, it_epi.channel, it_epi.clone(infoLabels={}).tourl())
                cambios.append('%dx%d' % (int(it_epi.contentSeason), int(it_epi.contentEpisodeNumber)))

    else:
        db.close()
        return False, 'El canal no devuelve temporadas ni episodios válidos'


    # Si es una actualización y ha habido cambios, actualizar updated de la tabla shows para que conste como actualizada
    if op == 'new_episodes' and len(cambios) > 0:
        db.cur.execute('UPDATE shows SET updated=? WHERE tmdb_id=?', (datetime.now(), tmdb_id))


    # Cerrar conexión bd
    db.close(commit=True)

    # Si es una actualización informar de los cambios
    if op == 'new_episodes':
        return True, cambios
        # ~ if len(cambios) == 0:
            # ~ return False, 'No se detectan temporadas ni episodios nuevos.'
        # ~ else:
            # ~ return True, 'Añadidos enlaces para: [COLOR limegreen]%s[/COLOR]' % ', '.join(cambios)

    return True, 'Seguimiento serie con tmdb_id: %s' % tmdb_id


# Funciones para buscar nuevos episodios de una serie

# Si se llama desde el menú contextual de una serie, se muestra el progreso y el resultado.
# Si se llama desde un servicio, no se muestra progreso. Notification final configurable?

# En una serie concreta, para cada canal buscar enlace de nivel superior (serie sino última temporada) para recorrerlo. 
def search_new_episodes(tmdb_id, show_progress=False, tvdbinfo=False):
    logger.info('tmdb_id: %s' % tmdb_id)

    if show_progress:
        tit = 'Buscando episodios'
        progreso = platformtools.dialog_progress(tit, 'Iniciando la búsqueda de nuevos episodios ...')

    itemlist = [] # lista de items para actualizar cada canal
    tot_cambios = {} # cambios hechos en cada canal

    db = TrackingData()

    # Enlaces a nivel de la serie
    db.cur.execute('SELECT channel, url FROM channels_shows WHERE tmdb_id=?', (tmdb_id,))
    canales = db.cur.fetchall()

    for channel, url in canales:
        it_update = Item().fromurl(url)
        it_update.infoLabels = db.get_show(tmdb_id)
        itemlist.append(it_update)
        tot_cambios[channel] = None

    # Enlaces a nivel de temporadas (Última temporada para cada canal)
    db.cur.execute('SELECT channel, MAX(season) FROM channels_seasons WHERE tmdb_id=? GROUP BY channel', (tmdb_id,))
    canales_temp = db.cur.fetchall()
    # Descartar canales ya tratados a nivel de serie
    canales_temp[:] = [x for x in canales_temp if x[0] not in [ch for (ch,url) in canales]]

    for channel, season in canales_temp:
        it_update = Item().fromurl(db.get_season_channel(tmdb_id, season, channel.encode('utf-8')))
        it_update.infoLabels = db.get_season(tmdb_id, season)
        itemlist.append(it_update)
        tot_cambios[channel] = None

    db.close()

    if len(itemlist) == 0:
        return False, 'No hay enlaces de ningún canal para actualizar.'

    if show_progress:
        progreso.update(0, muestra_cambios_canales(tot_cambios))

    n = 0; n_tot = len(itemlist)
    for it_update in itemlist:
        done, cambios = scrap_and_save_tvshow(it_update, op='new_episodes', tvdbinfo=tvdbinfo)
        logger.info('Actualizados enlaces para tmdb_id: %s en el canal %s. Resultado: %s' % (tmdb_id, it_update.channel, cambios))
        if done:
            tot_cambios[it_update.channel] = cambios
        else:
            tot_cambios[it_update.channel] = 'Error'

        if show_progress:
            n += 1
            perc = int(n / n_tot * 100)
            progreso.update(perc, muestra_cambios_canales(tot_cambios))
            if progreso.iscanceled(): break


    if show_progress:
        progreso.close()
        platformtools.dialog_ok(it_update.contentSerieName, 'Actualización completada.', muestra_cambios_canales(tot_cambios))
        logger.info(muestra_cambios_canales(tot_cambios))


    # Actualizar lastscrap si la serie está en tracking_shows
    db = TrackingData()
    commit = False
    db.cur.execute('SELECT tmdb_id FROM tracking_shows WHERE tmdb_id=?', (tmdb_id,))
    row = db.cur.fetchone()
    if row is not None:
        db.cur.execute('UPDATE tracking_shows SET lastscrap=? WHERE tmdb_id=?', (time.time(), tmdb_id))
        commit = True
    db.close(commit=commit)

    # devolver si ha habido cambios
    n_cambios = 0
    for ch, cambios in tot_cambios.items():
        if cambios is not None and cambios != 'Error' and len(cambios) > 0:
            n_cambios += 1

    return True, n_cambios #'Actualización completada.'


def muestra_cambios_canales(tot_cambios):
    itemlist = []
    for ch, cambios in tot_cambios.items():
        if cambios is None:
            itemlist.append('[COLOR gray]%s: pendiente[/COLOR]' % ch)
        elif cambios == 'Error':
            itemlist.append('[COLOR red]%s: error[/COLOR]' % ch)
        elif len(cambios) == 0:
            itemlist.append('[COLOR green]%s: sin novedades[/COLOR]' % ch)
        else:
            itemlist.append('[COLOR gold]%s: %s[/COLOR]' % (ch, ','.join(cambios)))
    return ', '.join(itemlist)


# Comprobar las series que tienen activada la búsqueda automática de nuevos episodios y efectuarla si procede
def check_and_scrap_new_episodes(notification=True):
    logger.info()
    config.set_setting('addon_tracking_lastscrap', str(time.time()))

    dt_hoy = datetime.now()

    db = TrackingData()
    db.cur.execute('SELECT tmdb_id, periodicity, tvdbinfo, lastscrap FROM tracking_shows')
    series = db.cur.fetchall()
    db.close()
    logger.debug(series)

    n_series = 0; n_cambios = 0
    for tmdb_id, periodicity, tvdbinfo, lastscrap in series:
        if lastscrap is None:
            tratar = True
        else:
            dt_scrap = datetime.fromtimestamp(float(lastscrap))
            dt_diff = dt_hoy - dt_scrap
            horas_dif = (dt_diff.days * 24) + (dt_diff.seconds / 3600)
            tratar = int(horas_dif) >= int(periodicity)
            logger.info('tmdb_id: %s se actualizó hace %d horas. Tratar ahora: %s. Periodicidad serie: %d' % (tmdb_id.encode('utf-8') if not PY3 else tmdb_id, int(horas_dif), tratar, int(periodicity)))

        if tratar:
            n_series += 1
            done, msg = search_new_episodes(tmdb_id, show_progress=False, tvdbinfo=tvdbinfo)
            if isinstance(msg, int) and msg > 0: n_cambios += 1

    tit = 'Búsqueda efectuada en %d series.' % int(n_series)
    if n_cambios == 0: tit += ' Sin novedades.'
    else: tit += ' Novedades en %d de ellas.' % int(n_cambios)
    logger.info(tit)
    if notification:
        platformtools.dialog_notification('Nuevos episodios', tit)


# Funciones para actualizar solamente infoLabels

def update_infolabels_movie(tmdb_id):
    logger.info()
    from core import tmdb

    db = TrackingData()

    infolabels = db.get_movie(tmdb_id)
    it = Item(infoLabels = infolabels)
    tmdb.set_infoLabels_item(it)
    if base64.b64encode(jsontools.dump(infolabels)) == base64.b64encode(jsontools.dump(it.infoLabels)):
        commit = False
        msg = 'Sin cambios en los datos de la película.'
    else:
        db.save_movie(tmdb_id, it.infoLabels)
        commit = True
        msg = 'Actualizados los datos de la película.'

    db.close(commit=commit)
    return True, msg


def update_infolabels_show(tmdb_id, with_tvdb=False):
    logger.info()
    if with_tvdb:
        from core import tvdb as scrapper
    else:
        from core import tmdb as scrapper

    tit = 'Actualizando datos desde ' + ('TVDB' if with_tvdb else 'TMDB')
    progreso = platformtools.dialog_progress(tit, 'Serie y temporadas ...')

    db = TrackingData()
    cambios = []

    # Serie
    infolabels = db.get_show(tmdb_id)
    it = Item(infoLabels = infolabels)
    # ~ logger.debug(it)
    scrapper.set_infoLabels_item(it)
    # ~ logger.debug(it)
    if base64.b64encode(jsontools.dump(infolabels)) != base64.b64encode(jsontools.dump(it.infoLabels)):
        db.save_show(tmdb_id, it.infoLabels)
        cambios.append('Serie')

    # Temporadas
    rows = db.get_seasons(tmdb_id)
    num_rows = len(rows)
    n = 0
    for season, infolabels in rows:
        it = Item(infoLabels = infolabels)
        # ~ logger.debug(it)
        scrapper.set_infoLabels_item(it)
        # ~ logger.debug(it)
        if base64.b64encode(jsontools.dump(infolabels)) != base64.b64encode(jsontools.dump(it.infoLabels)):
            db.save_season(tmdb_id, season, it.infoLabels)
            cambios.append('T%d' % int(season))

        n += 1
        perc = int(n / num_rows * 100)
        progreso.update(perc, tit, 'Procesada temporada %d' % int(season))
        if progreso.iscanceled(): break

    # Para episodios podrían ser demasiadas llamadas a tmdb, mejor hacerlo por una temporada concreta

    progreso.close()

    commit = True if len(cambios) > 0 else False
    db.close(commit=commit)

    msg = 'Sin cambios en la serie ni en las temporadas.' if not commit else 'Actualizados cambios en %s.' % ', '.join(cambios)
    logger.info(msg)
    return commit, msg


# season != -1 y episode != -1 para un episodio concreto.
# season != -1 y episode == -1 para todos los episodios de una temporada.
# season == -1 para todos los episodios de todas las temporadas. No recomendado pq puede ser largo, mejor fijar temporada al llamar a la rutina.
def update_infolabels_episodes(tmdb_id, season=-1, episode=-1, with_tvdb=False):
    logger.info()
    if with_tvdb:
        from core import tvdb as scrapper
    else:
        from core import tmdb as scrapper

    tit = 'Actualizando episodios desde ' + ('TVDB' if with_tvdb else 'TMDB')
    if season == -1: subtit = 'Todas las temporadas ...'
    elif episode == -1: subtit = 'Temporada %d ...' % int(season)
    else: subtit = 'Temporada %d Episodio %d ...' % (int(season), int(episode))
    progreso = platformtools.dialog_progress(tit, subtit)

    db = TrackingData()
    cambios = []

    if season > 0 and episode > 0:
        rows = [ [season, episode, db.get_episode(tmdb_id, season, episode)] ]
    else:
        rows = db.get_episodes(tmdb_id, season)
    num_rows = len(rows)
    n = 0
    for season, episode, infolabels in rows:
        it = Item(infoLabels = infolabels)
        scrapper.set_infoLabels_item(it)
        if base64.b64encode(jsontools.dump(infolabels)) != base64.b64encode(jsontools.dump(it.infoLabels)):
            db.save_episode(tmdb_id, season, episode, it.infoLabels)
            cambios.append('%dx%d' % (int(season), int(episode)))

        n += 1
        perc = int(n / num_rows * 100)
        progreso.update(perc, tit, 'Procesado episodio %dx%d' % (int(season), int(episode)))
        if progreso.iscanceled(): break

    progreso.close()

    commit = True if len(cambios) > 0 else False
    db.close(commit=commit)

    msg = 'Sin cambios en los episodios.' if not commit else 'Episodios actualizados: %s.' % ', '.join(cambios)
    logger.info(msg)
    return commit, msg


# Funciones para actualizar marcas de visto/no visto en la bd de Kodi

# season = -1 para todos los episodios de una serie. != -1 para todos los episodios de una temporada concreta
def update_season_watched(tmdb_id, season=-1, watched=False):
    logger.info()

    # Buscar idPath de plugin://plugin.video.balandro/
    n, results = platformtools.execute_sql_kodi('SELECT idPath FROM path WHERE strPath=?', (config.__base_url,))
    if n == 0:
        logger.error('No encontrado idPath para %s en la bd de Kodi!' % config.__base_url)
        return False
    idPath = results[0][0]

    db = TrackingData()
    rows = db.get_episodes(tmdb_id, season)
    db.close()

    for season, episode, infolabels in rows:

        it_minimo = Item( channel = 'tracking', action = 'findvideos', folder = False, title='', contentType = 'episode', 
                          infoLabels = {'tmdb_id': tmdb_id, 'season': season, 'episode': episode} )
        item_url = config.build_url(it_minimo)

        n, results = platformtools.execute_sql_kodi('SELECT idFile, playCount FROM files WHERE idPath=? AND strFilename=?', (idPath, item_url))
        if n == 0:
            if watched:
                platformtools.execute_sql_kodi('INSERT INTO files (idPath, strFilename, playCount) VALUES (?, ?, ?)', (idPath, item_url, 1))
                logger.info('Marcado como visto %dx%d' % (int(season), int(episode)))
        else:
            idFile = results[0][0]
            if results[0][1] is None and watched:
                platformtools.execute_sql_kodi('UPDATE files SET playCount=? WHERE idFile=?', (1, idFile))
                logger.info('Marcado como visto %dx%d idFile: %s' % (int(season), int(episode), idFile))

            elif results[0][1] is not None and not watched:
                platformtools.execute_sql_kodi('UPDATE files SET playCount=? WHERE idFile=?', (None, idFile))
                logger.info('Marcado como NO visto %dx%d idFile: %s' % (int(season), int(episode), idFile))

    return True


# Funciones para recuperar datos de una peli / episodio

# A un item mínimo (contentType,tmdb_id,season,episode) asignarle los infoLabels guardados
def set_infolabels_from_min(item):
    db = TrackingData()

    if item.contentType == 'movie': 
        infolabels = db.get_movie(item.infoLabels['tmdb_id'])
    else: 
        infolabels = db.get_episode(item.infoLabels['tmdb_id'], item.infoLabels['season'], item.infoLabels['episode'])

    db.close()

    item.infoLabels = infolabels
    try:
        if item.infoLabels['thumbnail']: item.thumbnail = item.infoLabels['thumbnail']
    except: pass
    try:
        if item.infoLabels['fanart']: item.fanart = item.infoLabels['fanart']
    except: pass

