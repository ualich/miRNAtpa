BIO_DATABASES = [
	"diana",
	"mirdb",
	"mirmap",
	"mirwalk",
	"targetscan"
]


def get_path(subpath):
	return __file__.replace("mirnatpa/utils.py", subpath)


def merge_rows(*rows):
	max_len = max([len(row) for row in rows])
	merged_row = tuple()
	for i in range(max_len):
		max_value = max([row[i] for row in rows])
		merged_row += (max_value,)
	return merged_row
