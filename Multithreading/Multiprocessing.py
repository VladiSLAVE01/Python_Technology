import multiprocessing


def main():
	array_2d = input()

	result = []
	lst = array_2d.replace('[', '').replace(']', '').split(', ')

	for i in lst:
		result.append(list(map(int, i.split())))

	with multiprocessing.Pool() as pool:
		res = pool.map(worker_function, result)

	print(sum(res))


if __name__ == "__main__":
	main()