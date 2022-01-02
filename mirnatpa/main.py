import glob
import os
import sys

import expression
import rank
import standard
import utils


def get_data(analysis_name):
	# Validate the name
	if not analysis_name.isalnum():
		print(f"Invalid analysis_name: {analysis_name}")
		print_help()
		sys.exit()

	# Validate directory structure
	input_data_path = os.path.abspath(f"analyses/{analysis_name}/input")  # NOTE
	if not os.path.isdir(input_data_path):
		print(f"Input data directory was not found: {input_data_path}")
		sys.exit()
	subdirs = glob.glob(input_data_path + "/*")
	data_found = dict()
	for subdir in subdirs:
		subdir_name = subdir.rsplit("/", 1)[1]
		if subdir_name in utils.BIO_DATABASES and os.listdir(subdir):
			data_found[subdir_name] = subdir
	if data_found:
		print(f"Input data from {len(data_found)} databases found: {', '.join(data_found.keys())}\n")
		return data_found
	else:
		print(f"No valid input data found.")
		sys.exit()


def print_help():
	print("\nUse syntax:\n\t\033[1mpython3 mirnatpa/run.py <analysis_name>\033[0m\n")
	print("\tanalysis_name - the name of the folder, where input\n\tdata is stored, only use alphanumerical characters")


def run_analysis(analysis_name, regions):
	# Prepare result folder
	folder_name = utils.get_path(f"analyses/{analysis_name}/results")
	os.makedirs(folder_name, exist_ok=True)

	data_found = get_data(analysis_name)
	interaction_data, genes = standard.run(analysis_name, data_found)
	expression_data = expression.run(analysis_name, regions)
	rank.rank(interaction_data, expression_data, genes, analysis_name)


if __name__ == "__main__":
	# Parse arguments
	if len(sys.argv) == 1:
		print("No analysis_name given.")
		print_help()
	else:
		analysis_name = sys.argv[1]
		if len(sys.argv) > 2:
			regions = sys.argv[2:]
		else:
			# Default regions - frontal cortex miRNA expression
			regions = ["brain_1", "brain_cerebral_cortex_frontal_2"]
		run_analysis(analysis_name, regions)
