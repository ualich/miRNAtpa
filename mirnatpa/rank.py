import csv

import utils


def reformat_data(interaction_data, expression_data, genes):
	"""
	Combine interaction and expression data into the dictionary `all_data`.
	:param interaction_data:
	:param expression_data:
	:param genes:
	:return:
	"""
	all_data = dict()
	# Process interaction data
	for interaction_profile in interaction_data[1:]:
		mirna = interaction_profile[0]
		all_data_row = interaction_profile[1:] + (0,)
		if mirna in all_data:
			merged_row = utils.merge_rows(all_data[mirna], all_data_row)
			all_data[mirna] = merged_row
		else:
			all_data[mirna] = all_data_row

	# Process expression data
	for expression_profile in expression_data:
		mirna = expression_profile[0]
		default_tuple = tuple()
		for i in range(len(genes)*len(utils.BIO_DATABASES)):
			default_tuple += (0,)
		all_data_row = default_tuple + (float(expression_profile[1]),)
		if mirna in all_data:
			merged_row = utils.merge_rows(all_data[mirna], all_data_row)
			all_data[mirna] = merged_row
		else:
			all_data[mirna] = all_data_row

	return all_data


def save_all_data(all_data, genes, analysis_name):
	rows = list()
	for mirna, values in all_data.items():
		rows.append((mirna,) + values)
	data_path = utils.get_path(f"analyses/{analysis_name}/results/all-data.csv")
	header = ("mirna",)
	for db in utils.BIO_DATABASES:
		for gene in genes:
			header_value = f"{db}-{gene}"
			header += (header_value,)
	header += ("expression",)
	rows.insert(0, header)
	with open(data_path, mode="w+") as f:
		csv_writer = csv.writer(f)
		csv_writer.writerows(rows)


def save_ranked_data(ranked_mirnas, genes, analysis_name):
	data_path = utils.get_path(f"analyses/{analysis_name}/results/ranked-mirnas.csv")
	header = ("mirna",) + tuple(genes) + ("expression", "total")
	ranked_mirnas.insert(0, header)
	with open(data_path, "w+") as f:
		csv_writer = csv.writer(f)
		csv_writer.writerows(ranked_mirnas)


def rank_mirnas(all_data, genes):
	condensed_rows = list()
	for mirna, row in all_data.items():
		mirna_score = 0
		mirna_row = tuple()
		for i in range(len(genes)):
			gene_score = round(sum(list(row[i*5:i*5+5])), 5)
			mirna_score += gene_score
			mirna_row += (gene_score,)
		expression = row[-1]
		total_score = round(expression * len(genes) + mirna_score, 5)
		condensed_row = mirna, *mirna_row, row[-1], total_score
		condensed_rows.append(condensed_row)

	# Sort by total score
	condensed_rows = sorted(condensed_rows, key=lambda x: x[len(genes)+2], reverse=True)

	return condensed_rows


def rank(interaction_data, expression_data, genes, analysis_name):
	all_data = reformat_data(interaction_data, expression_data, genes)
	save_all_data(all_data, genes, analysis_name)
	ranked_mirnas = rank_mirnas(all_data, genes)
	save_ranked_data(ranked_mirnas, genes, analysis_name)
