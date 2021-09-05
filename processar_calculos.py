#!/usr/bin/python3

import math
import sqlite3

# variables
database_file = "database.db"

def gravar_calculos_tfidf():

	print("Processando calculos de TF, IDF e TFIDF")

	con = sqlite3.connect(database_file)
	cur = con.cursor()

	cur.execute("select count(distinct docid) from tb_document;")
	total_documents = cur.fetchone()[0]

	# Update tb_token.df // DF: document frequence
	cur.execute("update tb_token as t set df = (select count(x.docid) from tb_document_token x where x.tokid = t.tokid);")

	# IDF = LOG ( DOCUMENTS_TOTAL / DF )
	cur.execute("select tokid, df from tb_token;")
	for i in cur.fetchall():
		cur.execute("update tb_token set idf = %f where tokid = %d;" % (math.log10(total_documents / i[1]), i[0]))

	# TFIDF = TF * IDF
	cur.execute("update tb_document_token as d set tfidf = (tf * (select x.idf from tb_token x where x.tokid = d.tokid));")

	con.commit()
	con.close()
	

gravar_calculos_tfidf()


