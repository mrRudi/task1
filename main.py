from pprint import pprint


def update(data, new_service, count):
    if not data:
        data['default'] = {}

    def add_count(host, service, values):
        if service in data[host]:
            data[host][service] += values
        else:
            data[host][service] = values

    def sum_counts_in_host(host):
        return sum(data[host].values())

    def sum_all_numbers_in_host():
        return sum( sum(services.values()) for services in data.values())

    number_host = len(data)
    all_working = sum_all_numbers_in_host()

    max_number = 0
    for host in data:
        sum_number = sum_counts_in_host(host)
        if sum_number > max_number:
            max_number = sum_number

    # скільки залишилося вільного місця
    remain = max_number * number_host - all_working

    # якщо нових сервісів достатньо шоб урівняти значення у всіх хостах
    if count >= remain:
        # add_every_host - на скільки ще можна збільшити кожен хост
        # remainders - остача шо лишилась при поділ порівну
        add_every_host, remainders = divmod(count - remain, number_host)
        final_number = add_every_host + max_number
        for host , services in data.items():
            counts_in_host = sum_counts_in_host(host)
            if add_every_host == 0 and counts_in_host == max_number:
                continue
            else:
                add_count(host, new_service, final_number - counts_in_host)
        #   розподілити дані з остачі
        for _,host in zip(range(remainders),data.keys()):
            add_count(host,new_service,1)

    else:
        def min_len(array, value):
            length = 0
            for el in array:
                if el[1] != value:
                    break
                length += 1
            return length

        def next_minimum(array, value):
            for el in array:
                if el[1] == value:
                    continue
                return el[1]
        tabl = [[host,sum_counts_in_host(host)] for host in data.keys()]    #[[<service>, <number>], ...]

        #
        #   *      __*
        #   *     |20*
        #   *_    |##*
        #   *_|_ _|##*      спочатку заповниться прямокутник між 2 і 8
        #   *_ _ _|##*      далі заповниться прямокутник між 8 і 12
        #   * |8|8|##*      далі заповняться елементи з остачі
        #   *_|#|#|##*
        #   *2|#|#|##*
        #   **********
        #
        tabl = sorted(tabl, key=lambda i:i[1])
        while (True):
            minimum = tabl[0][1]
            line_min = min_len(tabl, minimum)
            next_min = next_minimum(tabl, minimum)
            add_every, remainders = divmod(count, line_min)
            if add_every >= next_min - minimum:
                count -= line_min * (next_min - minimum)
                for i in range(line_min):
                    tabl[i][1] = next_min
            else:
                for i in range(line_min):
                    tabl[i][1] += add_every
                for i in range(remainders):
                    tabl[i][1] += 1
                break

        for host_number in range(len(tabl) - 1):
            counts_in_host = sum_counts_in_host(tabl[host_number][0])
            if tabl[host_number][1] > counts_in_host:
                add_count(tabl[host_number][0], new_service, tabl[host_number][1] - counts_in_host)


def main():
    example_data = {
    }

    print("Configuration before:")
    pprint(example_data)

    update(example_data, 'pylons', 12)

    print("Configuration after:")
    pprint(example_data)

if __name__ == '__main__':
    main()