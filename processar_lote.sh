#!/bin/bash

# parametros fixos
DIRETORIO_ENTRADA="./corpus"
DIRETORIO_SAIDA="./preparacao"
ARQUIVO_DATABASE="./database.db"

if [ ! -d "${DIRETORIO_ENTRADA}" ]
then
	echo "ERRO: diretorio '${DIRETORIO_ENTRADA}' de entrada nao encontrado!"
	exit 1;
fi;

if [ ! -d "${DIRETORIO_SAIDA}" ]
then
	echo "ERRO: diretorio '${DIRETORIO_SAIDA}' de entrada nao encontrado!"
	exit 1;
fi;

echo '------------------------------------------'
echo 'Inicio do processamento em lote' 
echo '------------------------------------------'
date
echo '------------------------------------------'

echo '------------------------------------------'
echo 'Limpando diretorio de saida'
echo '------------------------------------------'
find "${DIRETORIO_SAIDA}" -type f -name "*.txt" -delete;
find "${DIRETORIO_SAIDA}" -type f -name "*.txt.preparado" -delete;

echo '------------------------------------------'
echo 'Copiando dos arquivos'
echo '------------------------------------------'
find "${DIRETORIO_ENTRADA}" -type f -name "*.txt" -exec cp -v {} "${DIRETORIO_SAIDA}/" \;

echo '------------------------------------------'
echo 'Preparando os arquivos'
echo '------------------------------------------'
find "${DIRETORIO_SAIDA}" -type f -name "*.txt" -exec bash -c './preparar_texto.sh "'{}'" "'{}'.preparado"' \;

echo '------------------------------------------'
echo 'Criando base de dados'
echo '------------------------------------------'
if [ -f "${ARQUIVO_DATABASE}" ]
then
	echo "AVISO: renomeando o arquivo '${ARQUIVO_DATABASE}' existente."
	mv "${ARQUIVO_DATABASE}" "${ARQUIVO_DATABASE}".`date --iso-8601=seconds | sed "s/\://g"`
fi;
/usr/bin/python3 ./criar_database.py "${ARQUIVO_DATABASE}"

echo '------------------------------------------'
echo 'Processando os arquivos'
echo '------------------------------------------'
find "${DIRETORIO_SAIDA}" -type f -name "*.txt.preparado" | sort | while read line; do
	bash -c "/usr/bin/python3 ./processar_texto.py '${line}'";
done;

echo '------------------------------------------'
echo 'Processando os calculos'
echo '------------------------------------------'
/usr/bin/python3 ./processar_calculos.py

echo '------------------------------------------'
echo 'Fim do processamento em lote' 
echo '------------------------------------------'
date
echo '------------------------------------------'







