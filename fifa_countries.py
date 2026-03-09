"""
Base de datos completa de códigos FIFA (211 asociaciones nacionales)
Mapeo automático: Código FIFA (3 letras) → Código ISO2 (para banderas) + Nombre

Fuente: FIFA Official Members
Última actualización: Marzo 2026
"""

# Diccionario principal: Código FIFA → (ISO2, Nombre en español)
FIFA_COUNTRIES = {
    # UEFA (Europa) - 55 miembros
    'ALB': ('al', 'Albania'), 'AND': ('ad', 'Andorra'), 'ARM': ('am', 'Armenia'),
    'AUT': ('at', 'Austria'), 'AZE': ('az', 'Azerbaiyán'), 'BLR': ('by', 'Bielorrusia'),
    'BEL': ('be', 'Bélgica'), 'BIH': ('ba', 'Bosnia-Herzegovina'), 'BUL': ('bg', 'Bulgaria'),
    'CRO': ('hr', 'Croacia'), 'CYP': ('cy', 'Chipre'), 'CZE': ('cz', 'República Checa'),
    'DEN': ('dk', 'Dinamarca'), 'ENG': ('gb-eng', 'Inglaterra'), 'EST': ('ee', 'Estonia'),
    'FRO': ('fo', 'Islas Feroe'), 'FIN': ('fi', 'Finlandia'), 'FRA': ('fr', 'Francia'),
    'GEO': ('ge', 'Georgia'), 'GER': ('de', 'Alemania'), 'GIB': ('gi', 'Gibraltar'),
    'GRE': ('gr', 'Grecia'), 'HUN': ('hu', 'Hungría'), 'ISL': ('is', 'Islandia'),
    'ISR': ('il', 'Israel'), 'ITA': ('it', 'Italia'), 'KAZ': ('kz', 'Kazajistán'),
    'KVX': ('xk', 'Kosovo'), 'LVA': ('lv', 'Letonia'), 'LIE': ('li', 'Liechtenstein'),
    'LTU': ('lt', 'Lituania'), 'LUX': ('lu', 'Luxemburgo'), 'MKD': ('mk', 'Macedonia del Norte'),
    'MLT': ('mt', 'Malta'), 'MDA': ('md', 'Moldavia'), 'MNE': ('me', 'Montenegro'),
    'NED': ('nl', 'Países Bajos'), 'NIR': ('gb-nir', 'Irlanda del Norte'), 'NOR': ('no', 'Noruega'),
    'POL': ('pl', 'Polonia'), 'POR': ('pt', 'Portugal'), 'IRL': ('ie', 'República de Irlanda'),
    'ROU': ('ro', 'Rumania'), 'RUS': ('ru', 'Rusia'), 'SMR': ('sm', 'San Marino'),
    'SCO': ('gb-sct', 'Escocia'), 'SRB': ('rs', 'Serbia'), 'SVK': ('sk', 'Eslovaquia'),
    'SVN': ('si', 'Eslovenia'), 'ESP': ('es', 'España'), 'SWE': ('se', 'Suecia'),
    'SUI': ('ch', 'Suiza'), 'TUR': ('tr', 'Turquía'), 'UKR': ('ua', 'Ucrania'),
    'WAL': ('gb-wls', 'Gales'),
    
    # CONMEBOL (Sudamérica) - 10 miembros
    'ARG': ('ar', 'Argentina'), 'BOL': ('bo', 'Bolivia'), 'BRA': ('br', 'Brasil'),
    'CHI': ('cl', 'Chile'), 'COL': ('co', 'Colombia'), 'ECU': ('ec', 'Ecuador'),
    'PAR': ('py', 'Paraguay'), 'PER': ('pe', 'Perú'), 'URU': ('uy', 'Uruguay'),
    'VEN': ('ve', 'Venezuela'),
    
    # CONCACAF (Norte-Centro América y Caribe) - 41 miembros
    'CAN': ('ca', 'Canadá'), 'USA': ('us', 'Estados Unidos'), 'MEX': ('mx', 'México'),
    'BLZ': ('bz', 'Belice'), 'CRC': ('cr', 'Costa Rica'), 'SLV': ('sv', 'El Salvador'),
    'GUA': ('gt', 'Guatemala'), 'HON': ('hn', 'Honduras'), 'NCA': ('ni', 'Nicaragua'),
    'PAN': ('pa', 'Panamá'),
    'ATG': ('ag', 'Antigua y Barbuda'), 'ARU': ('aw', 'Aruba'), 'BAH': ('bs', 'Bahamas'),
    'BRB': ('bb', 'Barbados'), 'BER': ('bm', 'Bermudas'), 'BOE': ('bq', 'Bonaire'),
    'VGB': ('vg', 'Islas Vírgenes Británicas'), 'CAY': ('ky', 'Islas Caimán'),
    'CUB': ('cu', 'Cuba'), 'CUW': ('cw', 'Curazao'), 'DMA': ('dm', 'Dominica'),
    'DOM': ('do', 'República Dominicana'), 'GRN': ('gd', 'Granada'),
    'GLP': ('gp', 'Guadalupe'), 'GUY': ('gy', 'Guyana'), 'HAI': ('ht', 'Haití'),
    'JAM': ('jm', 'Jamaica'), 'MTQ': ('mq', 'Martinica'), 'MSR': ('ms', 'Montserrat'),
    'PUR': ('pr', 'Puerto Rico'), 'SKN': ('kn', 'San Cristóbal y Nieves'),
    'LCA': ('lc', 'Santa Lucía'), 'VIN': ('vc', 'San Vicente y las Granadinas'),
    'SXM': ('sx', 'Sint Maarten'), 'SUR': ('sr', 'Surinam'),
    'TRI': ('tt', 'Trinidad y Tobago'), 'TCA': ('tc', 'Islas Turcas y Caicos'),
    'VIR': ('vi', 'Islas Vírgenes de EE.UU.'),
    
    # AFC (Asia) - 47 miembros
    'AFG': ('af', 'Afganistán'), 'AUS': ('au', 'Australia'), 'BHR': ('bh', 'Baréin'),
    'BAN': ('bd', 'Bangladés'), 'BHU': ('bt', 'Bután'), 'BRU': ('bn', 'Brunéi'),
    'CAM': ('kh', 'Camboya'), 'CHN': ('cn', 'China'), 'TPE': ('tw', 'Taipéi Chino'),
    'GUM': ('gu', 'Guam'), 'HKG': ('hk', 'Hong Kong'), 'IND': ('in', 'India'),
    'IDN': ('id', 'Indonesia'), 'IRN': ('ir', 'Irán'), 'IRQ': ('iq', 'Irak'),
    'JPN': ('jp', 'Japón'), 'JOR': ('jo', 'Jordania'), 'PRK': ('kp', 'Corea del Norte'),
    'KOR': ('kr', 'Corea del Sur'), 'KUW': ('kw', 'Kuwait'), 'KGZ': ('kg', 'Kirguistán'),
    'LAO': ('la', 'Laos'), 'LIB': ('lb', 'Líbano'), 'MAC': ('mo', 'Macao'),
    'MAS': ('my', 'Malasia'), 'MDV': ('mv', 'Maldivas'), 'MNG': ('mn', 'Mongolia'),
    'MYA': ('mm', 'Myanmar'), 'NEP': ('np', 'Nepal'), 'OMA': ('om', 'Omán'),
    'PAK': ('pk', 'Pakistán'), 'PLE': ('ps', 'Palestina'), 'PHI': ('ph', 'Filipinas'),
    'QAT': ('qa', 'Qatar'), 'KSA': ('sa', 'Arabia Saudita'), 'SIN': ('sg', 'Singapur'),
    'SRI': ('lk', 'Sri Lanka'), 'SYR': ('sy', 'Siria'), 'TJK': ('tj', 'Tayikistán'),
    'THA': ('th', 'Tailandia'), 'TLS': ('tl', 'Timor Oriental'), 'TKM': ('tm', 'Turkmenistán'),
    'UAE': ('ae', 'Emiratos Árabes Unidos'), 'UZB': ('uz', 'Uzbekistán'),
    'VIE': ('vn', 'Vietnam'), 'YEM': ('ye', 'Yemen'),
    
    # CAF (África) - 54 miembros
    'ALG': ('dz', 'Argelia'), 'ANG': ('ao', 'Angola'), 'BEN': ('bj', 'Benín'),
    'BOT': ('bw', 'Botsuana'), 'BFA': ('bf', 'Burkina Faso'), 'BDI': ('bi', 'Burundi'),
    'CMR': ('cm', 'Camerún'), 'CPV': ('cv', 'Cabo Verde'), 'CTA': ('cf', 'República Centroafricana'),
    'CHA': ('td', 'Chad'), 'COM': ('km', 'Comoras'), 'CGO': ('cg', 'Congo'),
    'COD': ('cd', 'RD Congo'), 'CIV': ('ci', 'Costa de Marfil'), 'DJI': ('dj', 'Yibuti'),
    'EGY': ('eg', 'Egipto'), 'EQG': ('gq', 'Guinea Ecuatorial'), 'ERI': ('er', 'Eritrea'),
    'ETH': ('et', 'Etiopía'), 'GAB': ('ga', 'Gabón'), 'GAM': ('gm', 'Gambia'),
    'GHA': ('gh', 'Ghana'), 'GUI': ('gn', 'Guinea'), 'GNB': ('gw', 'Guinea-Bisáu'),
    'KEN': ('ke', 'Kenia'), 'LES': ('ls', 'Lesoto'), 'LBR': ('lr', 'Liberia'),
    'LBY': ('ly', 'Libia'), 'MAD': ('mg', 'Madagascar'), 'MWI': ('mw', 'Malaui'),
    'MLI': ('ml', 'Mali'), 'MTN': ('mr', 'Mauritania'), 'MRI': ('mu', 'Mauricio'),
    'MAR': ('ma', 'Marruecos'), 'MOZ': ('mz', 'Mozambique'), 'NAM': ('na', 'Namibia'),
    'NIG': ('ne', 'Níger'), 'NGA': ('ng', 'Nigeria'), 'RWA': ('rw', 'Ruanda'),
    'STP': ('st', 'Santo Tomé y Príncipe'), 'SEN': ('sn', 'Senegal'), 'SEY': ('sc', 'Seychelles'),
    'SLE': ('sl', 'Sierra Leona'), 'SOM': ('so', 'Somalia'), 'RSA': ('za', 'Sudáfrica'),
    'SSD': ('ss', 'Sudán del Sur'), 'SUD': ('sd', 'Sudán'), 'TAN': ('tz', 'Tanzania'),
    'TOG': ('tg', 'Togo'), 'TUN': ('tn', 'Túnez'), 'UGA': ('ug', 'Uganda'),
    'ZAM': ('zm', 'Zambia'), 'ZIM': ('zw', 'Zimbabue'),
    
    # OFC (Oceanía) - 11 miembros
    'ASA': ('as', 'Samoa Americana'), 'COK': ('ck', 'Islas Cook'), 'FIJ': ('fj', 'Fiyi'),
    'NCL': ('nc', 'Nueva Caledonia'), 'NZL': ('nz', 'Nueva Zelanda'), 'PNG': ('pg', 'Papúa Nueva Guinea'),
    'SAM': ('ws', 'Samoa'), 'SOL': ('sb', 'Islas Salomón'), 'TAH': ('pf', 'Tahití'),
    'TGA': ('to', 'Tonga'), 'VAN': ('vu', 'Vanuatu'),
}

def get_country_iso2(fifa_code):
    """Devuelve código ISO2 para mostrar bandera"""
    if not fifa_code or fifa_code in ['xx', '']:
        return 'xx'
    
    # Placeholders de eliminación directa
    if any(fifa_code.startswith(x) for x in ['1A', '1B', '1C', '1D', '1E', '1F', '1G', '1H', '1I', '1J', '1K', '1L',
                                               '2A', '2B', '2C', '2D', '2E', '2F', '2G', '2H', '2I', '2J', '2K', '2L',
                                               '3A', '3B', '3C', '3D', '3E', '3F', 'W', 'L', 'IC', 'Path']):
        return 'xx'
    
    country_data = FIFA_COUNTRIES.get(fifa_code.upper())
    return country_data[0] if country_data else 'xx'

def get_country_name(fifa_code):
    """Devuelve nombre completo del país en español"""
    if not fifa_code:
        return ''
    
    # Devolver placeholders tal cual
    if any(fifa_code.startswith(x) for x in ['1A', '1B', '1C', '1D', '1E', '1F', '1G', '1H', '1I', '1J', '1K', '1L',
                                               '2A', '2B', '2C', '2D', '2E', '2F', '2G', '2H', '2I', '2J', '2K', '2L',
                                               '3A', '3B', '3C', '3D', '3E', '3F', 'W', 'L', 'IC', 'Path']):
        return fifa_code
    
    country_data = FIFA_COUNTRIES.get(fifa_code.upper())
    return country_data[1] if country_data else fifa_code

# Crear diccionario inverso: Nombre español → Código FIFA
COUNTRY_NAMES_TO_FIFA = {name: code for code, (_, name) in FIFA_COUNTRIES.items()}

# Agregar algunos alias comunes
COUNTRY_ALIASES = {
    'Holanda': 'NED',
    'EEUU': 'USA',
    'EE.UU.': 'USA',
    'Estados Unidos': 'USA',
    'Catar': 'QAT',
    'Haití': 'HAI',
    'Haiti': 'HAI',
    'Curazao': 'CUW',
    'Uzbekistan': 'UZB',
    'Jordan': 'JOR',
    'Cape Verde': 'CPV',
    'Scotland': 'SCO',
    'Curacao': 'CUW',
}

def get_fifa_code(country_name):
    """Convierte nombre de país en español a código FIFA"""
    if not country_name:
        return ''
    
    # Si ya es un código FIFA válido, devolverlo
    if len(country_name) <= 4 and country_name.upper() in FIFA_COUNTRIES:
        return country_name.upper()
    
    # Placeholders
    if any(country_name.startswith(x) for x in ['1A', '1B', '1C', '1D', '1E', '1F', '1G', '1H', '1I', '1J', '1K', '1L',
                                                  '2A', '2B', '2C', '2D', '2E', '2F', '2G', '2H', '2I', '2J', '2K', '2L',
                                                  '3A', '3B', '3C', '3D', '3E', '3F', 'W', 'L', 'IC', 'Path']):
        return country_name
    
    # Buscar en aliases
    if country_name in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[country_name]
    
    # Buscar en nombres
    if country_name in COUNTRY_NAMES_TO_FIFA:
        return COUNTRY_NAMES_TO_FIFA[country_name]
    
    # Si no se encuentra, intentar con las primeras 3 letras en mayúsculas
    return country_name[:3].upper()
