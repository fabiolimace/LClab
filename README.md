# quem-escreveu

### Como usar

1. incluir arquivos em texto puro, no formato TXT, dentro do diretório `corpus`;
2. iniciar o processamento, executando o arquivo bash `run.sh`.

No final do processamento, haverá um arquivo com o nome `database.db` que conterá todos os tokens extraídos do corpus. O arquivo é uma base de dados SQLite3. Os tokens são n-gramas até 3. Cada token conterá os valores calculados de TF, IDF e TFIDF.

### Schema da base de dados

Definição do schema da base `database.db`:

```
CREATE TABLE tb_token (
	tokid   integer primary key, -- hash(token)
	token   text not null,       -- 1, 2 or 3 words
	ng      integer,             -- NGRAM: 1, 2 or 3
	df      integer,             -- DF: document frequence
	idf     real                 -- IDF = LOG ( DOCUMENTS_TOTAL / DF )
);
CREATE TABLE tb_document (
	docid    integer primary key, -- hash(author + title)
	author   text not null,       -- document author
	title    text not null,       -- document title
	countsum integer              -- COUNTSUM: sum of all token counts
);
CREATE TABLE tb_document_token (
	tokid    integer not null,   -- hash(token)
	docid    integer not null,   -- hash(author + title)
	count    integer,            -- COUNT: token count
	tf       real,               -- TF    = COUNT / COUNTSUM
	tfidf    real,               -- TFIDF = TF * IDF
	ln       real,               -- LN    = LOG (1 + COUNT)
	lnidf    real                -- LNIDF = LN * IDF
);
CREATE UNIQUE INDEX idx_document_token ON tb_document_token(tokid, docid);
```

### Amostras extraídas de um corpus

As amostras exibidas abaixo foram geradas a partir de uma corpus de 223 obras literárias.

Amostras da tabela `tb_token`:

||tokid||token||ng||df||idf||
|52547250513|quincas berro|2|2|4.714025|
|1946607819333|passagem da|2|19|2.462733|
|8400837519913|ilhas salomão|2|1|5.407172|
|22587835753099|naturalizasse|1|1|5.407172|
|31386725336170|se lançada|2|1|5.407172|
|34544116049754|não atingirá o|3|1|5.407172|
|52357328360264|e perturbado|2|3|4.308559|
|52904118997137|existem também|2|1|5.407172|
|60540781295134|brandeburgo|1|3|4.308559|
|67570418119433|goiabal|1|2|4.714025|
|74376093057968|um amigo para|3|1|5.407172|
|78462974031674|chamou baptistin|2|1|5.407172|
|81920552301396|galiani|1|3|4.308559|
|85951629603423|intitulando-se|1|2|4.714025|
|103144800388919|seu cérebro que|3|1|5.407172|

Amostras da tabela `tb_document`:

||docid||author||title||countsum||
|872077297768439|Monteiro Lobato|Contos completos|175750|
|2454032842536215|Lewis Carroll|Alice|134681|
|71937260981337297|Seneca|Sobre a brevidade da vida|9198|
|108495260583527596|Caio Fernando Abreu|Contos completos|320080|
|118314364647261333|Epicteto|Manual de Epicteto|10118|
|534186423037364473|Virginia Woolf|Orlando|107928|
|561367780819544645|C. S. Lewis|Cristianismo puro e simples|81362|
|604725770235478174|Machado de Assis|Memorias postumas de Bras Cubas|72309|
|717129419399034167|Henry David Thoreau|A Desobediencia Civil|9482|
|799616962328782019|Fernando Pessoa|Poesia Completa de Ricardo Reis|8456|
|803940423095354407|Homero|Odisseia|157474|
|807688269992541255|Jose Saramago|As intermitencias da morte|66659|
|856484067375848796|Hermann Hesse|Demian|47032|
|914611506926428287|Edgar Allan Poe|Antologia de contos extraordinarios|87843|
|942864782245759561|Harper Lee|O sol e para todos|116895|

Amostras da tabela `tb_document_token`:

||tokid||docid||count||tf||tfidf||ln||lnidf||
|4300887113479631311|3700917926416630758|14|0.000116312881651643|6.45701657458564e-05|2.70805020110221|1.50335240474028|
|2128437972144812985|3700917926416630758|165|0.00137083039089436|5.00819175009347e-05|5.11198778835654|0.186761361859818|
|343609820321826241|3700917926416630758|2|1.66161259502347e-05|2.38753790553732e-05|1.09861228866811|1.57857402534143|
|885406988480129065|3700917926416630758|1|8.30806297511735e-06|1.32971295642421e-05|0.693147180559945|1.10938830081082|
|2806591476943961253|3700917926416630758|1|8.30806297511735e-06|3.0037070576995e-05|0.693147180559945|2.50601263436259|
|3421407264727284790|3700917926416630758|7|5.81564408258215e-05|6.33056120965397e-06|2.07944154167984|0.226355529578017|
|979524572864747945|3700917926416630758|1|8.30806297511735e-06|1.51510239687617e-05|0.693147180559945|1.26405993526969|
|5246909481818718531|3700917926416630758|9|7.47725667760562e-05|1.3565612927346e-05|2.30258509299405|0.417746500496445|
|3799885114373950314|3700917926416630758|25|0.000207701574377934|3.88019773189881e-05|3.25809653802148|0.608664562847021|
|6174863740756796735|3700917926416630758|50|0.000415403148755868|1.51763386366469e-05|3.93182563272433|0.143645317665951|
|5677475550375849801|3700917926416630758|10|8.30806297511735e-05|2.64969052465418e-06|2.39789527279837|0.0764760739353584|
|8106908528227008933|3700917926416630758|50|0.000415403148755868|4.31466788518257e-05|3.93182563272433|0.408386932994178|
|5680337008210045289|3700917926416630758|34|0.00028247414115399|0.00113579377726083|3.55534806148941|14.2956172474374|
|979297643296043901|3700917926416630758|59|0.000490175715531924|6.63893989116438e-06|4.0943445622221|0.0554538027507361|
|4493781278853348850|3700917926416630758|12|9.96967557014082e-05|3.06373115108213e-05|2.56494935746154|0.788221762294718|

A base de dados de onde foram retiradas essas amostras tem o tamanho de 711,4 MB. A tabela `tb_document` possui 223 linhas, que corresponde à quantidade de livros processados; a tabela `tb_token` possui 1504562 linhas, que são as palavras e combinações de palavras extraídas dos livros; e a tabela `tb_document_token` possui 6412487 registros, que são associações entre os tokens e os livros.




