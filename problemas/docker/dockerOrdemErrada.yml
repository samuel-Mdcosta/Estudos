#codigo errado
FROM python:3.11

COPY . .
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app"]

#codigo certo

from python:3.11

WORKDIR /app

copy requirementes.txt .
run pip install -r requirements.txt
copi ..
CMD ["uvicorn", "main:app"]

#em um arquivo docker a ordem dos comando e importante pois se a instalacao das dependeicas vier depois da copa do codigo 
#toda modificaca no codigo tera que reinstalar as dependencias, isso gera um tempo de build muito maior
#workdir e para definir o diretorio de trabalho dentro do container, assim podendo ter um container para front, back, banco tudo dentro do mesma pasta