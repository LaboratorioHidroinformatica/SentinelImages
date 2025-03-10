# Requirements

Antes de tudo, certifique-se que possui um versão do Microsoft Visual C++ maior que 14.0.

É muito importante que se crie um ambiente virtual (recomendo usar anaconda), 
no qual se instale todas as necessidades do código.

Também é preciso instalar o SNAP: https://step.esa.int/main/download/snap-download/

conda create --name lhi python=3.10

conda activate lhi

conda install -c conda-forge gdal

conda install --yes --file requirements.txt

Em alguns casos vai ser preciso colocar o caminho do executável do SNAP
Para deixar salvo, basta ir no arquivo lib/ost/helpers/settings.py e adicionar o caminho na linha 120
Caminho Padrão do SNAP:
C:\Program Files\esa-snap\bin\gpt.exe