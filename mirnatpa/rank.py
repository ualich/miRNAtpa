import csv
import utils


def reformat_data(interaction_data, expression_data, genes):
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

	rows = list()
	for mirna in all_data:
		rows.append(all_data[mirna])
	return rows


def save_data(all_data, genes, analysis_name):
	data_path = utils.get_path(f"analyses/{analysis_name}/results/all_data.csv")
	header = ("mirna",)
	for db in utils.BIO_DATABASES:
		for gene in genes:
			header_value = f"{db}-{gene}"
			header += (header_value,)
	header += ("expression",)
	all_data.insert(0, header)
	with open(data_path, mode="w+") as f:
		csv_writer = csv.writer(f)
		csv_writer.writerows(all_data)


def rank(interaction_data, expression_data, genes, analysis_name):
	all_data = reformat_data(interaction_data, expression_data, genes)
	save_data(all_data, genes, analysis_name)
