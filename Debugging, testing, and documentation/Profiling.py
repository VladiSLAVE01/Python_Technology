import cProfile
import pstats
import io
from functions_to_profile import load_files, read_database, get_id, get_user_data, generate_words

TASK_FUNCTIONS_ORDER = ['load_files', 'read_database', 'get_id', 'get_user_data', 'generate_words']
FUNCTION_MAP = {
	'load_files': load_files,
	'read_database': read_database,
	'get_id': get_id,
	'get_user_data': get_user_data,
	'generate_words': generate_words,
}


def run_all_tasks():
	for func_name in TASK_FUNCTIONS_ORDER:
		FUNCTION_MAP[func_name]()


def get_function_stat_key(stats, func_name):
	for k in stats.stats.keys():
		if k[2] == func_name:
			return k
	return None


def process_profiling_results():
	profiler = cProfile.Profile()

	profiler.enable()
	run_all_tasks()
	profiler.disable()

	dummy_stream = io.StringIO()
	stats = pstats.Stats(profiler, stream=dummy_stream)
	stats.strip_dirs()

	total_profiling_time = stats.total_tt

	for func_name in TASK_FUNCTIONS_ORDER:
		func_cumtime = 0.0
		percentage = 0.0

		func_stat_key = get_function_stat_key(stats, func_name)

		if func_stat_key:
			func_cumtime = stats.stats[func_stat_key][3]

			if total_profiling_time > 0:
				percentage = (func_cumtime / total_profiling_time) * 100
			else:
				percentage = 0.0

		print(f"{func_cumtime:.4f}: {int(round(percentage))}%")


def main():
	process_profiling_results()


if __name__ == "__main__":
	main()
