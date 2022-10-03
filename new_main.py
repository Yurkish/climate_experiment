from traintest import *

# here we set global values that contain names of files in dataset
# month_array = ['june', 'july', 'aug1', 'aug2']
# rooms_array = ['room5', 'room6', 'room7']
month_array = ['july']
rooms_array = ['room7']
# this is train\test ratio
ratio = 0.7

# here the main research starts
for room in rooms_array:
    for month in month_array:
        w, r, t_points, t_days, tt_days = acquisition_step(month, room)
        time_point_amount = len(tt_days)
        plt.plot(tt_days, r, '-', tt_days, w, '-.')
        plt.show()
        #create_cvs_from_our_data(t_points, w, r, month, room)
        w_train, w_test = dividing_lists(w, ratio)
        r_train, r_test = dividing_lists(r, ratio)
        t_train, t_test = dividing_lists(tt_days, ratio)
        # plt.plot(t_train, w_train, '-', t_test, r_test, '-.')
        # plt.show()

        a = search_for_best_shift(w_train, r_train, month, room, t_days)
        t_w_reduced = t_train[:-a[2]]
        r_train_reduced = r_train[:-a[2]]
        print("len(t_train) = ", len(t_train), ', len(t_reduced) = ', len(t_w_reduced))
###########################################################################################
        plt.plot(t_w_reduced, a[0], '-', t_w_reduced, a[1], '-', t_w_reduced, r_train_reduced, '-.')
        plt.show()
###########################################################################################
        slope, intercept, r1, p1, std_err = stats.linregress(a[0], a[1])
###########################################################################################

        def linear_room_weather_prediction(x):
            return slope * x + intercept
        #########################################################################
        # prepareing predicting array ######################################
        mymodel = list(map(linear_room_weather_prediction, w_test[:-a[2]]))
        subtracted_list = np.subtract(mymodel, r_test[a[2]:])
        res = list(map(abs, subtracted_list))
        print('mean of error = ', mean(res))
        plt.plot(t_test[:-a[2]], r_test[a[2]:], '-', t_test[:-a[2]], mymodel, '-', t_test[:-a[2]], subtracted_list, '-.')
        plt.show()
    #    linear_deviation = np.std(subtracted_list)
###########################################################################################


        predict_quality_train = test_linregress_quality(w_train, r_train, slope, intercept)
        print('predict_quality_train ' + month + ' ' + room, predict_quality_train)
        predict_quality_test = test_linregress_quality(w_test, r_test, slope, intercept)
        print('predict_quality_test ' + month + ' ' + room, predict_quality_test)
