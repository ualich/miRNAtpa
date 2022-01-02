import csv
import numpy

import utils


def extract_expression_data(regions):
	expression_data_path = utils.get_path("expression/expression-data.csv")
	with open(expression_data_path) as f:
		csv_reader = csv.reader(f)
		header = next(csv_reader)

		# Validate region names
		for region in regions:
			if region not in header:
				regions.remove(region)

		# Determine regions indexes
		region_indexes = list()
		for region in regions:
			region_index = header.index(region)
			region_indexes.append(region_index)

		# Extracting data from csv
		expression_data = list()
		for row in csv_reader:
			mirna = row[0]

			expression_values = tuple()
			for region_index in region_indexes:
				expression_values += (float(row[region_index]),)
			expression_level = sum(expression_values) / len(expression_values)

			expression_row = mirna, expression_level
			expression_data.append(expression_row)

	return expression_data


def save_expression_data(analysis_name, expression_data):
	analysis_expression_data_path = utils.get_path(f"analyses/{analysis_name}/results/expression-data.csv")
	with open(analysis_expression_data_path, mode="w+") as f:
		csv_writer = csv.writer(f)
		csv_writer.writerows(expression_data)


def run(analysis_name, regions):
	expression_data = extract_expression_data(regions)
	save_expression_data(analysis_name, expression_data)
	return expression_data
