from traintest import *
month_array = ['june', 'july', 'aug1', 'aug2']
rooms_array = ['room5', 'room6', 'room7']
ratio = 0.7
for room in rooms_array:
    for month in month_array:
        w, r, t_days = acquisition_step(month, room)
        w_train = dividing_lists(w, ratio)[0]
        w_test = dividing_lists(w, ratio)[1]
        r_train = dividing_lists(r, ratio)[0]
        r_test = dividing_lists(r, ratio)[1]
        a = search_for_best_shift(w_train, r_train, month, room, t_days)
        slope, intercept, r1, p1, std_err = stats.linregress(a[0], a[1])
        predict_quality_train = test_linregress_quality(w_train, r_train, slope, intercept)
        print('predict_quality_train ' + month + ' ' + room, predict_quality_train)
        predict_quality_test = test_linregress_quality(w_test, r_test, slope, intercept)
        print('predict_quality_test ' + month + ' ' + room, predict_quality_test)
