#!/bin/bash

ENTRADA="${1}"
SAIDA="${2}"

if [ ! -f "$ENTRADA" ]
then
	echo 'ERRO: arquivo de entrada nao encontrado!'
	exit 1;
fi;

if [ -z "$SAIDA" ]
then
	echo 'ERRO: arquivo de saida nao informado!'
	exit 1;
fi;

TEMPORARIO=`mktemp`

echo "Preparando texto '${ENTRADA}'"

# fazer copia temporaria para edicao
cat "${ENTRADA}" > "${TEMPORARIO}"

# substituir sinais de pontuacao por quebras de linha
sed -i 's/[,.?!;:]\+/\n/g' "${TEMPORARIO}"

# remover algarismos romanos até 89, exceto I, V, X, L
# sed -i 's/[IVXL][IVXL]\+//g' "${TEMPORARIO}"

# remover caracteres que não são alfanuméricos, preservando hífen e espaço
sed -i 's/[^a-zA-Z -]//g' "${TEMPORARIO}"

# remover travessoes de obras obtidas do Projeto Gutemberg, substituindo-os por espacos simples
sed -i 's/--/ /g' "${TEMPORARIO}"

# substituir letras maiusculas por letras minusculas
cat "${TEMPORARIO}" | tr 'A-ZÇÁÀÂÃÉÊÍÓÔÕÚÜ' 'a-zçáàâãéêíóôõúü' > "${TEMPORARIO}".lower
mv "${TEMPORARIO}".lower "${TEMPORARIO}"

# remover espacos duplicados que porventura existam
sed -i 's/[ ]\+/ /g' "${TEMPORARIO}"

# remover espacos nos inicios e finais de linhas
sed -i 's/^[ ]\+//g' "${TEMPORARIO}"
sed -i 's/[ ]\+$//g' "${TEMPORARIO}"

# remover linhas em branco
sed -i '/^$/d' "${TEMPORARIO}"

# remover as primeiras 100 linhas
tail -n +100 "${TEMPORARIO}" > "${TEMPORARIO}".tail
mv "${TEMPORARIO}".tail "${TEMPORARIO}"

# remover as ultimas 100 linhas
head -n -100 "${TEMPORARIO}" > "${TEMPORARIO}".head
mv "${TEMPORARIO}".head "${TEMPORARIO}"

# gravar o arquivo de saida
cat "${TEMPORARIO}" > "${SAIDA}"

