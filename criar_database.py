#!/usr/bin/python3

import sys
import sqlite3

database_file = sys.argv[1]

token = '''
CREATE TABLE tb_token (
	tokid   integer primary key, -- hash(token)
	token   text not null,       -- 1, 2 or 3 words
	ng      integer,             -- NGRAM: 1, 2 or 3
	dc      integer,             -- DC: document count                     // select x.tokid, count(1) from tb_document_token x join tb_token y on y.tokid = x.tokid group by x.tokid;
	idf     real                 -- IDF = LOG ( DOCUMENTS_TOTAL / DC )
);
'''

document = '''
create table tb_document (
	docid    integer primary key, -- hash(author + title)
	author   text not null,       -- document author
	title    text not null,       -- document title
	countsum integer              -- COUNTSUM: sum of all token counts
);
'''

document_token = '''
CREATE TABLE tb_document_token (
	tokid    integer not null,   -- hash(token)
	docid    integer not null,   -- hash(author + title)
	count    integer,            -- COUNT: token count
	tf       real,               -- TF    = COUNT / COUNTSUM
	tfidf    real,               -- TFIDF = TF * IDF
	ln       real,               -- LN    = LOG (1 + COUNT)
	lnidf    real                -- LNIDF = LN * IDF
);
'''

document_token_index = 'CREATE UNIQUE INDEX idx_document_token ON tb_document_token(tokid, docid);'

def create_database(filename):
	con = sqlite3.connect(filename)
	cur = con.cursor()
	cur.execute(token)
	cur.execute(document)
	cur.execute(document_token)
	cur.execute(document_token_index)
	con.commit()
	con.close()

create_database(database_file)

print("Criada a base de dados '%s'" % database_file)

