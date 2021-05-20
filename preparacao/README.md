
Diretório que guarda uma cópia da coleção de documentos a serem processados.

Neste diretório tembém são geradas versões pré-processadas dos arquivos origiais, nomeados com a terminação ".txt.preparado".

As seguintes operações são feitas para gerar os arquivos pré-processados:

- substituição de sinais de pontuação (,.?!;:) por quebras de linha (line feed);
- remoção de caracteres que não são alfanuméricos, preservando o hífen e o espaço
- substituição das letras maiúsculas por suas correspondentes minúsculas
- remoção de espaços duplicados entre as palavras
- remoção de espaços nos inícios e finais de cada linha
- remoção de linhas vazias
- remoção das primerias 100 linhas de cada texto (informação pré-textual, por exemplo, informações catalográficas de livros)
- remoção das últimas 100 linhas de cada texto (informação pós-textual, por exemplo, índices no final de livros)

