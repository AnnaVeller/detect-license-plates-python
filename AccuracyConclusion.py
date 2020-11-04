import logging.config

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
log = logging.getLogger(__name__)

file = 'car_numbers/fin_file.txt'

if __name__ == '__main__':
    file = open(file)
    line = file.readline()
    state_array = []
    w, h, name_video, fps = line.split()
    line = file.readline()
    while line:
        try:
            count, number, state = line.split()
            state = int(state)
            state_array.append([number, state])
            line = file.readline()
        except ValueError:
            log.error('\nIn your file a few videos.\nYou should edit your file.\nNow we took only first video values')
            break
    file.close()

    count_true = 0
    count_unknown = 0
    count_false = 0
    for one_number in state_array:
        log.debug(one_number)
        if one_number[1] == 1:
            count_true += 1
        elif one_number[1] == -1:
            count_unknown += 1
        elif one_number[1] == 0:
            count_false += 1

    log.info(
        """ 
        All numbers          | %d
        -------------------------
        Clear numbers        | %d
        -------------------------
        Correctly recognized | %d
        -------------------------
        Not correctly        | %d
        -------------------------
        Numbers is not clear | %d
        -------------------------
        Precision            | %f %%
        """
        % (
            len(state_array),
            count_false + count_true,
            count_true,
            count_false,
            count_unknown,
            count_true / (count_false + count_true) * 100
        ))
