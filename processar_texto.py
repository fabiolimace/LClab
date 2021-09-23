#!/usr/bin/python3

import os
import sys
import math
import zlib
import sqlite3
import tempfile

# parameters
document = sys.argv[1]

# variables
database_file = "database.db"

# n-grams
ngram1 = {}
ngram2 = {}
ngram3 = {}

# black list
stopwords = []

print("Processando o arquivo '%s'" % document)

# expected file name format: "TITLE - AUTHOR.txt"
filename = document.split("/")[::-1][0]
title =  filename.split("-")[0].strip()
author = filename.split("-")[1].replace('.txt.preparado','').strip()

f = open(document, 'r')

def get_stopwords():
	stopwords = []
	f = open('stopwords.txt', 'r')
	for line in f:
		word = line.strip()
		# ignore empty lines and commented lines
		if len(word) > 0 and word[0] != '#':
			stopwords.append(word)
	f.close()
	return stopwords;

def insert_tokens(ngrams, ng):
	con = sqlite3.connect(database_file)
	cur = con.cursor()
	
	for k in ngrams.keys():
		token = k
		tokid = get_hash(token)
		cur.execute('SELECT token FROM tb_token WHERE tokid = %d;' % (tokid));
		if cur.fetchone() is None:
			cur.execute("INSERT INTO tb_token (tokid, token, ng) VALUES (%d, '%s', %d);" % (tokid, token, ng))

	con.commit()
	con.close()
	
def insert_document(author, title, countsum):
	docid = get_hash(author + title)
	con = sqlite3.connect(database_file)
	cur = con.cursor()
	cur.execute("INSERT INTO tb_document (docid, author, title, countsum) VALUES (%d, '%s', '%s', %d);" % (docid, author, title, countsum))
	con.commit()
	con.close()
	
def insert_document_tokens(author, title, ngrams, countsum):
	con = sqlite3.connect(database_file)
	cur = con.cursor()
	
	records = []
	
	for k in ngrams.keys():
		token = k
		tokid = get_hash(token)
		docid = get_hash(author + title)
		count = ngrams[k]
		tf = count / countsum
		records.append((tokid, docid, count, tf))
	
	cur.executemany("INSERT INTO tb_document_token (tokid, docid, count, tf) VALUES (?, ?, ?, ?);", records)

	con.commit()
	con.close()

def get_hash(text):
	# [Compare hashes in Python](https://gist.github.com/fabiolimace/507eac3d35900050eeb9772e5b1871ba)
	return (zlib.crc32(text.encode('utf-8')) << 32 | zlib.adler32(text.encode('utf-8'))) & 0x7fffffffffffffff # 2^63-1

def get_count_sum(ngram):
	sum = 0;
	for i in ngram:
		sum = sum + ngram[i]

# ngram 1
def get_unigrams(itens):
	unigrams = {}
	for i in itens:
		if i in unigrams:
			unigrams[i] = unigrams[i] + 1
		else:
			unigrams[i] = 1
	return unigrams

def get_bigrams(itens):
	bigrams = {}
	temp = []
	for i in itens:
		temp.append(i)
		if len(temp) == 2:
			s = ' '.join(temp)
			if s in bigrams:
				bigrams[s] = bigrams[s] + 1
			else:
				bigrams[s] = 1
			temp = temp[1:]
	return bigrams

for line in f:
	itens = line.split()
	
	## ngram 1
	unigrams = get_unigrams(itens)
	ngram1.update(unigrams)

	## ngram 2
	bigrams = get_bigrams(itens)
	ngram2.update(bigrams)

	## ngram 3
	temp = []
	for i in itens:
		temp.append(i)
		if len(temp) == 3:
			s = ' '.join(temp)
			if s in ngram3:
				ngram3[s] = ngram3[s] + 1
			else:
				ngram3[s] = 1
			temp = temp[1:]
f.close()

# carregar as stop words
stopwords = get_stopwords()

# remover as stop words
ngram1 = { k:v for (k,v) in ngram1.items() if k not in stopwords}

# remover 2-grams que so ocorrem 1x
ngram2 = { k:v for (k,v) in ngram2.items() if not ngram2[k] < 2}

# remover 3-grams que so ocorrem 2x ou menos
ngram3 = { k:v for (k,v) in ngram3.items() if not ngram3[k] < 3}

# juntar os ngramas
ngrams = dict()
ngrams.update(ngram1)
ngrams.update(ngram2)
ngrams.update(ngram3)

# somando as quantidades absolutas de ngramas
countsum = sum(ngrams.values())

# inserir os tokens no banco
insert_tokens(ngram1, 1)
insert_tokens(ngram2, 2)
insert_tokens(ngram3, 3)
insert_document(author, title, countsum)
insert_document_tokens(author, title, ngrams, countsum)


