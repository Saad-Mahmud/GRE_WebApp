def show_test_stat(status):
    correct = 0
    wrong = 0

    for s in status.items():
        if s[1]==s[0] :
            correct += 1
        else:
            wrong += 1
    return correct, wrong