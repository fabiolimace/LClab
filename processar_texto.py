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
ngrams1 = {}
ngrams2 = {}
ngrams3 = {}

# black list
stopwords = []

print("Processando o arquivo '%s'" % document)

# expected file name format: "TITLE - AUTHOR.txt"
filename = document.split("/")[::-1][0]
title =  filename.split("-")[0].strip()
author = filename.split("-")[1].replace('.txt.preparado','').strip()

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

def get_ngrams1(itens):
	unigrams = {}
	for i in itens:
		if i in unigrams:
			unigrams[i] = unigrams[i] + 1
		else:
			unigrams[i] = 1
	return unigrams

def get_ngrams2(itens):
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

def get_ngrams3(itens):
	trigrams = {}
	temp = []
	for i in itens:
		temp.append(i)
		if len(temp) == 3:
			s = ' '.join(temp)
			if s in trigrams:
				trigrams[s] = trigrams[s] + 1
			else:
				trigrams[s] = 1
			temp = temp[1:]
	return trigrams

# carregar n-gramas
f = open(document, 'r')
itens = f.read().split()
ngrams1 = get_ngrams1(itens)
ngrams2 = get_ngrams2(itens)
ngrams3 = get_ngrams3(itens)
f.close()

# carregar as stop words
stopwords = get_stopwords()

# remover as stop words
ngrams1 = { k:v for (k,v) in ngrams1.items() if k not in stopwords}

# remover 2-grams que so ocorrem 1x
ngrams2 = { k:v for (k,v) in ngrams2.items() if not ngrams2[k] < 2}

# remover 3-grams que so ocorrem 2x ou menos
ngrams3 = { k:v for (k,v) in ngrams3.items() if not ngrams3[k] < 3}

# juntar os ngramas
ngrams = dict()
ngrams.update(ngrams1)
ngrams.update(ngrams2)
ngrams.update(ngrams3)

# somando as quantidades absolutas de ngramas
countsum = sum(ngrams.values())

# inserir os tokens no banco
insert_tokens(ngrams1, 1)
insert_tokens(ngrams2, 2)
insert_tokens(ngrams3, 3)
insert_document(author, title, countsum)
insert_document_tokens(author, title, ngrams, countsum)


