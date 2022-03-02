# Simple TFIDF

### Como usar

1. incluir arquivos em texto puro, no formato TXT, dentro do diretório `corpus`;
2. iniciar o processamento, executando o arquivo bash `run.sh`.

No final do processamento, haverá um arquivo com o nome `database.db` que conterá todos os tokens extraídos do corpus. O arquivo é uma base de dados SQLite3. Os tokens são n-gramas até 3. Cada token conterá os valores calculados de TF, IDF e TFIDF.

### Schema da base de dados

Definição do schema da base `database.db`:

```sql
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
	tfidf    real                -- TFIDF = TF * IDF
);
CREATE UNIQUE INDEX idx_document_token ON tb_document_token(tokid, docid);
```

### Amostras extraídas de um corpus

As amostras exibidas abaixo foram geradas a partir de uma corpus de 223 obras literárias.

Amostras da tabela `tb_token`:
|tokid|token| ng| df|idf|
|-----|-----|---|---|---|
|1840136470791495|daquele que eu|3|1|2.348305|
|2931500323374330|aída não|2|1|2.348305|
|13702393451447370|análogas|1|26|0.933332|
|25767776797066056|depender|1|84|0.424026|
|30215640691573632|primo era|2|1|2.348305|
|37621775049098355|mundão de|2|1|2.348305|
|67963017270264600|teve uma|2|85|0.418886|
|81021474727593312|sedições|1|8|1.445215|
|100143751288062837|odette na|2|1|2.348305|
|102941720628954015|sonhos ou|2|3|1.871184|
|105177113536824000|acabava|1|144|0.189942|
|110841879156949881|neve mais|2|1|2.348305|
|110906853526733814|ao filho do|3|1|2.348305|
|115422986070263064|aquele desejo|2|4|1.746245|
|116728299705795891|ordem do banho|3|1|2.348305|
|146361675758503482|puseram então|2|1|2.348305|
|156342939061847349|protestativo|1|1|2.348305|
|183293614534231824|da província das|3|1|2.348305|
|202342039216785216|veio abraçá-lo|2|1|2.348305|
|202845301755413913|purificaram-se|1|2|2.047275|
|208827258748011408|o torneio|2|1|2.348305|
|210980708434904406|bastos voltou|2|2|2.047275|
|234405666642396921|fizera progressos|2|1|2.348305|
|234745616972907591|a hesitante|2|1|2.348305|
|236618957012468610|murzelos|1|1|2.348305|

Amostras da tabela `tb_document`:

|docid|author|title|countsum|
|-----|------|-----|--------|
|4599410278996316604|Alexandre Dumas|A mulher da gargantilha de veludo|123844|
|2002214003974934280|Arthur C. Clarke|2001_ uma odisseia no espaco|64002|
|6040563740601422364|Arthur Conan Doyle|As aventuras de Sherlock Holmes|97253|
|5412829502169157044|C. S. Lewis|Cristianismo puro e simples|76580|
|8585721594460245588|Charles Darwin|Viagem de um naturalista|227994|
|5374806420848183652|Charlotte Bronte|Jane Eyre|196924|
|5416514216564295864|Eca de Queiros|A reliquia|82732|
|3593078514968889300|Esopo|Fabulas de Esopo|28783|
|7302110749345647672|F. Scott Fitzgerald|O grande Gatsby|61384|
|1635915704993450592|Giovanni Boccaccio|Decameron|25175|
|7917616467944868072|Herman Melville|Moby Dick|244119|
|4121653044533266224|Hermann Hesse|Demian|44832|
|5409149175546119580|Homero|Odisseia|148058|
|5988698015774411532|Isaac Asimov|Fundacao e Imperio|76766|
|5423309478507317952|Jorge Amado|Tenda dos milagres|113500|
|433379578201116348|Jose Saramago|As intermitencias da morte|63133|
|1221040864867258584|Jose Saramago|O evangelho segundo Jesus Cristo|144571|
|7288184424339999360|Olavo Bilac|Antologia Poetica|6295|
|4943105971880136216|Rachel de Queiroz|A casa do morro branco|25003|
|829192832218500192|Robert Musil|O Homem Sem Qualidades|544799|
|272429951391567204|Santo Agostinho|Contra os academicos|32627|
|4458238110063791004|Seneca|Tratado sobre a clemencia|23805|
|5994250083749594664|Seneca|Sobre a ira|88742|
|630268896103107528|Thomas Paine|Os Direitos do homem|73950|
|8845063824200042544|Virginia Woolf|Orlando|102202|

Amostras da tabela `tb_document_token`:

|tokid|docid|count| tf|tfidf|
|-----|-----|-----|---|-----|
|1719728510461673518|272429951391567204|66|0.00202286449872805|0.000233254482483832|
|6734340121257247147|272429951391567204|22|0.000674288166242682|0.000339306525270482|
|7870899372499731065|272429951391567204|3|9.19483863058203e-05|3.75872130444111e-05|
|3758152231500906813|272429951391567204|45|0.00137922579458731|2.69224875103442e-06|
|5392486776358961802|272429951391567204|11|0.000337144083121341|0.000247976553161492|
|1010087513902088557|272429951391567204|404|0.0123823826891838|0.0|
|5411216986956890646|272429951391567204|26|0.000796886014650443|7.03116437306525e-05|
|9124239703635526527|272429951391567204|27|0.000827535476752383|5.7555919943605e-05|
|1117798623902958653|272429951391567204|19|0.000582339779936862|6.42082017960585e-05|
|1383220391278805413|272429951391567204|66|0.00202286449872805|0.0|
|1840292507463123483|272429951391567204|57|0.00174701933981059|3.83802678762988e-05|
|1957982625939260276|272429951391567204|16|0.000490391393631042|0.000394390903239648|
|484664102759956580|272429951391567204|2|6.12989242038802e-05|1.10943696938119e-05|
|2413511002044826539|272429951391567204|195|0.00597664510987832|0.000766187973151071|
|2032997644178883363|272429951391567204|58|0.00177766880191253|1.39742544518344e-05|
|1210751156661585064|272429951391567204|2|6.12989242038802e-05|9.62487510344194e-05|
|4969201849419563775|272429951391567204|6|0.000183896772611641|4.94910350323352e-05|
|8175763680291455712|272429951391567204|29|0.000888834400956263|5.22812394642474e-06|
|2543983784740520689|272429951391567204|3|9.19483863058203e-05|2.6793759769516e-05|
|5303359569275454122|272429951391567204|6|0.000183896772611641|6.5665675667392e-05|
|5280926860616270588|272429951391567204|12|0.000367793545223281|0.000207058571122077|
|8111542554649690658|272429951391567204|102|0.00312624513439789|6.10243050234468e-06|
|336639072875315623|272429951391567204|3|9.19483863058203e-05|6.18545989517884e-06|
|8583771507274809776|272429951391567204|102|0.00312624513439789|1.22329972108989e-05|
|1684889707444896725|272429951391567204|86|0.00263585374076685|0.000270944677720906|

A base de dados de onde foram retiradas essas amostras tem o tamanho de 470 MB. A tabela `tb_document` possui 223 linhas, que corresponde à quantidade de livros processados; a tabela `tb_token` possui 1097434 linhas, que são as palavras e combinações de palavras extraídas dos livros; e a tabela `tb_document_token` possui 5633081 registros, que são associações entre os tokens e os livros.

Os itens do corpus não serão fornecidos sob nenhuma hipótese por estarem protegidos por direitos autorais.

