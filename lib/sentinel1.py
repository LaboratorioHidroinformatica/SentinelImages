from pathlib import Path
import geopandas as gpd
from pprint import pprint
from ost import Generic  # Biblioteca principal para gerenciar o processo
from shapely import wkt  # Importando para utilizar o método de conversão para WKT
import os 

# ----------------------------
# Area of interest (AOI)
# ----------------------------

areaOfInterest = os.path.dirname(os.path.realpath(__file__)).replace('\\', "//") + "//bacia_tatu_simples.geojson"
aoi = gpd.read_file(areaOfInterest) 

exit()

# Get the WKT representation of the first geometry
aoi_wkt = aoi.geometry.iloc[0].wkt

# Convert the WKT string back to a Shapely geometry object
geometry = wkt.loads(aoi_wkt)

# Verificar se a conversão funcionou
print(aoi_wkt)


# Caminho para o arquivo 'naturalearth_lowres' que você baixou
naturalearth_path = Path(r"C://Users//Usuario//Desktop//Sentinel1Scripts//ne_110m_admin_0_countries//ne_110m_admin_0_countries.shp")

# Carregar o arquivo de países do Natural Earth (substituindo a busca no GeoPandas)
world = gpd.read_file(naturalearth_path)

# ----------------------------
# Time of interest (TOI)
# ----------------------------
start = '2017-01-01'  # Data de início
end = '2017-12-31'    # Data de término

# ----------------------------
# Diretório do projeto
# ----------------------------
home = Path.home()  # Diretório inicial do usuário
project_dir = home.joinpath('Sentinel1', 'baciatatu')  # Diretório onde os dados serão armazenados

# Criação do diretório, se não existir
project_dir.mkdir(parents=True, exist_ok=True)

# Exibindo as configurações para conferência
print('AOI: ', aoi_wkt)
print('TOI start: ', start)
print('TOI end: ', end)
print('Project Directory: ', project_dir)

# ----------------------------
# Iniciar o download de imagens Sentinel-1
# ----------------------------
ost_generic = Generic(aoi=aoi_wkt, start=start, end=end, project_dir=project_dir)

# Default config as created by the class initialisation
print(' Before customisation')
print('---------------------------------------------------------------------')
pprint(ost_generic.config_dict)
print('---------------------------------------------------------------------')

# customisation
ost_generic.config_dict['download_dir'] = '/download'
ost_generic.config_dict['temp_dir'] = '/tmp'

print('')
print(' After customisation (note the change in download_dir and temp_dir)')
print('---------------------------------------------------------------------')
pprint(ost_generic.config_dict)

# the import of the Sentinel1 class
from ost import Sentinel1

# initialize the Sentinel1 class
ost_s1 = Sentinel1(
    project_dir=project_dir,
    aoi=aoi_wkt, 
    start=start, 
    end=end,
    product_type='GRD',
    beam_mode='IW'
)

# product_type='GRD',
#    beam_mode='IW',
#    polarisation='*'

# search command
ost_s1.search()

# uncomment in case you have issues with the registration procedure 
#ost_s1.search(base_url='https://scihub.copernicus.eu/dhus')

# we plot the full Inventory on a map
ost_s1.plot_inventory(transparency=.1)

print('-----------------------------------------------------------------------------------------------------------')
print(' INFO: We found a total of {} products for our project definition'.format(len(ost_s1.inventory)))
print('-----------------------------------------------------------------------------------------------------------')
print('')
# combine OST class attribute with pandas head command to print out the first 5 rows of the 
print('-----------------------------------------------------------------------------------------------------------')
print('The columns of our inventory:')
print('')
print(ost_s1.inventory.columns)
print('-----------------------------------------------------------------------------------------------------------')

print('')
print('-----------------------------------------------------------------------------------------------------------')
print(' The last 5 rows of our inventory:')
print(ost_s1.inventory.tail(5))

ost_s1.refine_inventory()

import matplotlib.pyplot as plt
import pylab
pylab.rcParams['figure.figsize'] = (19, 19)

key = 'DESCENDING_VVVH'
ost_s1.refined_inventory_dict[key]
ost_s1.plot_inventory(ost_s1.refined_inventory_dict[key], 0.1)

if __name__ == '__main__':
    ost_s1.download(ost_s1.refined_inventory_dict[key], concurrent=1)