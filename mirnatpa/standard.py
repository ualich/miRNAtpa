"""
Standardize all input data to equivalent JSON format.
"""
import csv
import glob
import os
import re

import bs4

import utils


def get_genes(interaction_data):
	genes = set()
	for row in interaction_data:
		gene = row[1]
		genes.add(gene)
	return genes


def read_csv(file_path, conn):
	f = open(file_path)
	csv_reader = csv.reader(f)
	conn.send(csv_reader)


class Diana:
	"""
	DIANA microT
	"""
	def __init__(self, input_path):
		self.input = input_path
		self.name = "diana"

	@staticmethod
	def filter_rows(csv_reader):
		for row in csv_reader:
			if len(row) == 4:
				yield row

	def extract_data(self, row_stream):
		for row in row_stream:
			mirna = row[2]
			score = round(float(row[3]), 5)
			gene = re.findall(r"\(([^()]+)\)", row[1])[0]
			yield mirna, gene, score, self.name

	def standardize(self):
		standardized_data = list()
		for file_path in glob.glob(f"{self.input}/*"):
			with open(file_path) as f:
				csv_reader = csv.reader(f)
				next(csv_reader)  # Skip header
				data_extract = self.extract_data(self.filter_rows(csv_reader))
				for i in data_extract:
					standardized_data.append(i)

		return standardized_data


class Mirdb:
	"""
	miRDB
	"""
	def __init__(self, input_path):
		self.input = input_path
		self.normalization_factor = 0.01
		self.name = "mirdb"

	@staticmethod
	def parse_html(html_path):
		with open(html_path) as f:
			soup = bs4.BeautifulSoup(f, "html.parser")
			return soup

	def extract_data(self, soup):
		table = soup.find(id="table1")
		table_rows = table.tbody.children
		table_rows = [row for row in table_rows if hasattr(row, "text")]
		for row in table_rows[1:]:
			data_objects = row.findAll("td")
			mirna = data_objects[3].text.strip()
			score = round(float(data_objects[2].text) * self.normalization_factor, 5)
			gene = data_objects[4].text.strip()
			yield mirna, gene, score, self.name

	def standardize(self):
		standardized_data = list()
		for file_path in glob.glob(f"{self.input}/*"):
			soup = self.parse_html(file_path)
			data_extract = self.extract_data(soup)
			for i in data_extract:
				standardized_data.append(i)
		return standardized_data


class Mirmap:
	def __init__(self, input_path):
		self.input = input_path
		self.name = "mirmap"
		self.normalization_factor = 0.01

	def extract_data(self, csv_reader):
		for row in csv_reader:
			mirna = row[0]
			gene = row[1]
			score = round(float(row[5]) * self.normalization_factor, 5)
			yield mirna, gene, score, self.name

	def standardize(self):
		standardized_data = list()
		for file_path in glob.glob(f"{self.input}/*"):
			with open(file_path) as f:
				csv_reader = csv.reader(f)
				next(csv_reader)  # Skipping header
				data_extract = self.extract_data(csv_reader)
				for i in data_extract:
					standardized_data.append(i)

		return standardized_data


class Mirwalk:
	def __init__(self, input_path):
		self.input = input_path
		self.name = "mirwalk"

	@staticmethod
	def filter_rows(csv_reader):
		mirna_list = list()
		for row in csv_reader:
			if row[0] not in mirna_list and len(row) == 21:
				mirna_list.append(row[0])
				yield row

	def extract_data(self, row_stream):
		for row in row_stream:
			mirna = row[0]
			gene = row[2]
			score = 1
			yield mirna, gene, score, self.name

	def standardize(self):
		standardized_data = list()
		for file_path in glob.glob(f"{self.input}/*"):
			with open(file_path) as f:
				csv_reader = csv.reader(f)
				next(csv_reader)  # Skipping header
				data_extract = self.extract_data(self.filter_rows(csv_reader))
				for i in data_extract:
					standardized_data.append(i)
		return standardized_data


class Targetscan:
	def __init__(self, input_path):
		self.input = input_path
		self.name = "targetscan"

	@staticmethod
	def get_gene_name(file_path):
		gene_name = os.path.splitext(os.path.basename(file_path))[0]
		return gene_name

	def extract_data(self, row_stream, file_path):
		gene = self.get_gene_name(file_path)
		for row in row_stream:
			if row == ["Conserved sites"] or row == ["Poorly conserved sites"]:
				continue
			mirna = row[0]
			score = 1
			yield mirna, gene, score, self.name

	def standardize(self):
		standardized_data = list()
		for file_path in glob.glob(f"{self.input}/*"):
			with open(file_path) as f:
				csv_reader = csv.reader(f, delimiter="\t")
				next(csv_reader)  # Skipping header
				data_extract = self.extract_data(csv_reader, file_path)
				for i in data_extract:
					standardized_data.append(i)
		return standardized_data


def get_rows(all_rows, mirna):
	rows = list()
	for row in all_rows:
		if row[0] == mirna:
			rows.append(row)
	return rows


def save_interaction_data(interaction_data, analysis_name):
	data_path = utils.get_path(f"analyses/{analysis_name}/results/interaction-data.csv")
	with open(data_path, "w+") as f:
		csv_writer = csv.writer(f)
		csv_writer.writerows([("miRNA", "gene", "score", "database")] + interaction_data)


def get_interaction_data(analysis_name, input_data_index):
	index = {
		"diana": Diana,
		"mirdb": Mirdb,
		"mirmap": Mirmap,
		"mirwalk": Mirwalk,
		"targetscan": Targetscan
	}

	interaction_data = list()
	for database, input_path in input_data_index.items():
		print(f"Preparing {database} data...", end="")
		standardized_data = index[database](input_path).standardize()

		try:
			print(f"obtained {len(standardized_data)} entries...", end="")
			interaction_data.extend(standardized_data)
		except BaseException as e:
			print(e)
		print("DONE")
	return interaction_data


def order_by_mirna(interaction_data, genes):

	header = ("mirna",)
	for db in utils.BIO_DATABASES:
		for gene in genes:
			header_value = f"{db}-{gene}"
			header += (header_value,)

	ordered_data = dict()
	for interaction_value in interaction_data:
		mirna, gene, score, db = interaction_value
		ordered_row = [mirna]
		for i in range(len(genes)*len(utils.BIO_DATABASES)):
			ordered_row.append(0)
		index = header.index(f"{db}-{gene}")
		ordered_row[index] = float(score)
		ordered_row = tuple(ordered_row)
		if mirna in ordered_data:
			merged_row = utils.merge_rows(ordered_data[mirna][1:], ordered_row[1:])
			ordered_data[mirna] = (mirna, *merged_row)
		else:
			ordered_data[mirna] = ordered_row

	rows = [header]
	for mirna in ordered_data:
		rows.append(ordered_data[mirna])
	return rows


def run(analysis_name, input_data_index):
	"""
	Standardize all the input data and assemble a list of tuples
	named `interaction_data`:
		[0] - miRNA
		[1] - gene
		[2] - score
		[3] - database

	:param analysis_name:
	:param input_data_index:
	:return:
	"""
	interaction_data = get_interaction_data(analysis_name, input_data_index)
	save_interaction_data(interaction_data, analysis_name)
	genes = get_genes(interaction_data)
	interaction_data = order_by_mirna(interaction_data, genes)
	return interaction_data, genes
