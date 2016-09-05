
import matplotlib.pyplot as plt
from novainstrumentation import smooth
import numpy as np
import os


def EMG_diferential(data, patient):
    fig1 = plt.figure(1)
    fig2 = plt.figure(2)

    fig3 = plt.figure(3)
    fig4 = plt.figure(4)

    maxs = [0, 0, 0, 0]

    max_range = [0, 0]

    for i in range(0, len(data)):
        Acc_ = data[i].get_variable('open_signals_data_filtered')[5:8]
        EMGs = data[i].get_variable('open_signals_data_filtered')[1:5]
        wii = data[i].get_variable("wii_data")

        Acc = []
        Acc.append(Acc_[2][100:-100])
        Acc.append(Acc_[0][100:-100])

        Acc[0] = list(np.array(Acc[0]))
        Acc[1] = list(np.array(Acc[1]))

        FR = list(smooth(np.abs(np.array(EMGs[0])), 500))[100:-100]
        FL = list(smooth(np.abs(np.array(EMGs[1])), 500))[100:-100]
        BL = list(smooth(np.abs(np.array(EMGs[2])), 500))[100:-100]
        BR = list(smooth(np.abs(np.array(EMGs[3])), 500))[100:-100]

        if max(FR)>maxs[0]:
            maxs[0] = max(FR)

        if max(FL) > maxs[1]:
            maxs[1] = max(FL)

        if max(BL) > maxs[2]:
            maxs[2] = max(BL)

        if max(BR) > maxs[3]:
            maxs[3] = max(BR)

        [FR, FL, BL, BR] = normalize([FR, FL, BL, BR])

        Front = (np.array(FR) + np.array(FL))
        Back = (np.array(BL) + np.array(BR))
        Left = (np.array(FL) + np.array(BL))
        Right = (np.array(FR) + np.array(BR))

        x = list(np.array(Left)/2.0 - np.array(Right)/2.0)
        y = list(np.array(Front)/2.0 - np.array(Back)/2.0)

        [x, y] = normalize([x, y], zero_out=True)

        Acc = normalize(Acc)

        Cops=[]
        Cops.append(wii[6][0][10:-10])
        Cops.append(wii[6][1][10:-10])

        if (max(Cops[0]) - min(Cops[0])) > max_range[0]:
            max_range[0] = (max(Cops[0]) - min(Cops[0]))

        if (max(Cops[1]) - min(Cops[1])) > max_range[1]:
            max_range[1] = (max(Cops[1]) - min(Cops[1]))

        Cops = normalize(Cops)

        #SEPARAR
        plt.figure(1)
        t1 = np.linspace(0, len(Acc[1]), len(Cops[0]))

        plt.subplot(3, 4, i + 1)
        l1, = plt.plot(x, y, color='red')
        l2, = plt.plot(Cops[0], Cops[1], color='blue')
        l3, = plt.plot(Acc[0], Acc[1], color='black', alpha=0.2)
        plt.xlabel("Norm x")
        plt.ylabel("Norm y")

        plt.subplot(3, 4, i + 5)
        plt.plot(x, color='red')
        plt.plot(t1, Cops[0], color='blue')
        l4, = plt.plot(np.array(Left)/2.0, color='black', alpha=0.7)
        l5, = plt.plot(np.array(Right)/2.0, color='green', alpha=0.7)
        plt.xlim([0, len(Acc[0])])
        plt.xlabel("Samples")
        plt.ylabel("Norm x")
        plt.title("X Axis")

        plt.subplot(3, 4, i + 9)
        plt.plot(y, color='red')
        plt.plot(t1, Cops[1], color='blue')
        l6, = plt.plot(np.array(Front)/2.0, color='black', alpha=0.7)
        l7, = plt.plot(np.array(Back)/2.0, color='green', alpha=0.7)
        plt.xlim([0, len(Acc[0])])
        plt.xlabel("Samples")
        plt.ylabel("Norm y")
        plt.title("Y Axis")

        Acc[0] = list(smooth(np.array(Acc[0]), 1000))[100:-100]
        Acc[1] = list(smooth(np.array(Acc[1]), 1000))[100:-100]
        Cops[0] = list(smooth(np.array(Cops[0]), 100))[10:-10]
        Cops[1] = list(smooth(np.array(Cops[1]), 100))[10:-10]
        x = list(smooth(np.array(x), 1000))[100:-100]
        y = list(smooth(np.array(y), 1000))[100:-100]

        Left = list(smooth(np.array(Left), 1000))[100:-100]
        Right = list(smooth(np.array(Right), 1000))[100:-100]
        Front = list(smooth(np.array(Front), 1000))[100:-100]
        Back = list(smooth(np.array(Back), 1000))[100:-100]

        plt.figure(2)
        t1 = np.linspace(0, len(Acc[1]), len(Cops[0]))

        plt.subplot(3, 4, i + 1)
        l1, = plt.plot(x, y, color='red')
        l2, = plt.plot(Cops[0], Cops[1], color='blue')

        plt.xlabel("Norm x")
        plt.ylabel("Norm y")

        plt.subplot(3, 4, i + 5)
        plt.plot(x, color='red')
        plt.plot(t1, Cops[0], color='blue')
        plt.plot(np.array(Left)/2.0, color='black', alpha=0.7)
        plt.plot(np.array(Right)/2.0, color='green', alpha=0.7)
        plt.xlabel("Samples")
        plt.ylabel("Norm x")
        plt.title("X Axis")

        plt.subplot(3, 4, i + 9)
        plt.plot(y, color='red')
        plt.plot(t1, Cops[1], color='blue')
        plt.plot(np.array(Front)/2.0, color='black', alpha=0.7)
        plt.plot(np.array(Back)/2.0, color='green', alpha=0.7)
        plt.xlabel("Samples")
        plt.ylabel("Norm y")
        plt.title("Y Axis")

    for i in range(0, len(data)):
        Acc_ = data[i].get_variable('open_signals_data_filtered')[5:8]
        EMGs = data[i].get_variable('open_signals_data_filtered')[1:5]
        wii = data[i].get_variable("wii_data")

        Acc = []
        Acc.append(Acc_[2][100:-100])
        Acc.append(Acc_[0][100:-100])

        Acc[0] = list(np.array(Acc[0]))
        Acc[1] = list(np.array(Acc[1]))

        FR = list(smooth(np.abs(np.array(EMGs[0])), 500))[100:-100]
        FL = list(smooth(np.abs(np.array(EMGs[1])), 500))[100:-100]
        BL = list(smooth(np.abs(np.array(EMGs[2])), 500))[100:-100]
        BR = list(smooth(np.abs(np.array(EMGs[3])), 500))[100:-100]

        [FR, FL, BL, BR] = normalize([FR, FL, BL, BR], currentMax=False, globalMax=maxs)

        Front = (np.array(FR) + np.array(FL))
        Back = (np.array(BL) + np.array(BR))
        Left = (np.array(FL) + np.array(BL))
        Right = (np.array(FR) + np.array(BR))

        x = list(np.array(Left)/2.0 - np.array(Right)/2.0)
        y = list(np.array(Front)/2.0 - np.array(Back)/2.0)

        [x, y] = normalize([x, y], zero_out=True)

        Acc = normalize(Acc)

        Cops = []
        Cops.append(wii[6][0][10:-10])
        Cops.append(wii[6][1][10:-10])

        Cops = normalize(Cops, cop=True, cop_range=max_range, currentMax=False)

        # SEPARAR
        plt.figure(3)
        t1 = np.linspace(0, len(Acc[1]), len(Cops[0]))

        plt.subplot(3, 4, i + 1)
        l1, = plt.plot(x, y, color='red')
        l2, = plt.plot(Cops[0], Cops[1], color='blue')
        l3, = plt.plot(Acc[0], Acc[1], color='black', alpha=0.2)
        plt.xlabel("Norm x")
        plt.ylabel("Norm y")

        plt.subplot(3, 4, i + 5)
        plt.plot(x, color='red')
        plt.plot(t1, Cops[0], color='blue')
        l4, = plt.plot(np.array(Left)/2.0, color='black', alpha=0.7)
        l5, = plt.plot(np.array(Right)/2.0, color='green', alpha=0.7)
        plt.xlim([0, len(Acc[0])])
        plt.xlabel("Samples")
        plt.ylabel("Norm x")
        plt.title("X Axis")

        plt.subplot(3, 4, i + 9)
        plt.plot(y, color='red')
        plt.plot(t1, Cops[1], color='blue')
        l6, = plt.plot(np.array(Front)/2.0, color='black', alpha=0.7)
        l7, = plt.plot(np.array(Back)/2.0, color='green', alpha=0.7)
        plt.xlim([0, len(Acc[0])])
        plt.xlabel("Samples")
        plt.ylabel("Norm y")
        plt.title("Y Axis")

        Acc[0] = list(smooth(np.array(Acc[0]), 1000))[100:-100]
        Acc[1] = list(smooth(np.array(Acc[1]), 1000))[100:-100]
        Cops[0] = list(smooth(np.array(Cops[0]), 100))[10:-10]
        Cops[1] = list(smooth(np.array(Cops[1]), 100))[10:-10]
        x = list(smooth(np.array(x), 1000))[100:-100]
        y = list(smooth(np.array(y), 1000))[100:-100]

        Left = list(smooth(np.array(Left), 1000))[100:-100]
        Right = list(smooth(np.array(Right), 1000))[100:-100]
        Front = list(smooth(np.array(Front), 1000))[100:-100]
        Back = list(smooth(np.array(Back), 1000))[100:-100]

        plt.figure(4)
        t1 = np.linspace(0, len(Acc[1]), len(Cops[0]))

        plt.subplot(3, 4, i + 1)
        l1, = plt.plot(x, y, color='red')
        l2, = plt.plot(Cops[0], Cops[1], color='blue')

        plt.xlabel("Norm x")
        plt.ylabel("Norm y")

        plt.subplot(3, 4, i + 5)
        plt.plot(x, color='red')
        plt.plot(t1, Cops[0], color='blue')
        plt.plot(np.array(Left)/2.0, color='black', alpha=0.7)
        plt.plot(np.array(Right)/2.0, color='green', alpha=0.7)
        plt.xlabel("Samples")
        plt.ylabel("Norm x")
        plt.title("X Axis")

        plt.subplot(3, 4, i + 9)
        plt.plot(y, color='red')
        plt.plot(t1, Cops[1], color='blue')
        plt.plot(np.array(Front)/2.0, color='black', alpha=0.7)
        plt.plot(np.array(Back)/2.0, color='green', alpha=0.7)
        plt.xlabel("Samples")
        plt.ylabel("Norm y")
        plt.title("Y Axis")

    plt.figure(1)
    fig1.suptitle(patient, fontsize=20)

    plt.subplots_adjust(hspace=0.45, wspace=0.24, top=0.94, bottom=0.11, left=0.04, right=0.98)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()

    fig1.legend((l1,l2, l3), ('Emg', 'Cop', 'Acc'), bbox_to_anchor=[0.5, 0.06], loc='center', ncol=3, labelspacing=0.,
                fontsize=14)
    fig1.legend([l6, l7], ['Front', 'Back'], bbox_to_anchor=[0.5, 0.03], loc='center', ncol=2, labelspacing=0.,
                fontsize=14)
    fig1.legend([l4, l5], ['Left', 'Right'], bbox_to_anchor=[0.5, 0.365], loc='center', ncol=2, labelspacing=0.,
                fontsize=14)

    plt.figure(2)
    fig2.suptitle(patient, fontsize=20)
    fig2.legend((l1, l6, l2, l7), ('Emg', 'Front', 'Cop', 'Back'), loc='lower center', ncol=2, labelspacing=1., fontsize=14)
    fig2.legend([l4, l5], ['Left', 'Right'], bbox_to_anchor=[0.5, 0.365], loc='center', ncol=2, labelspacing=0.,
                fontsize=14)
    plt.subplots_adjust(hspace=0.45, wspace=0.24, top=0.94, bottom=0.11, left=0.04, right=0.98)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()

    plt.figure(3)
    fig3.suptitle(patient, fontsize=20)

    plt.subplots_adjust(hspace=0.45, wspace=0.24, top=0.94, bottom=0.11, left=0.04, right=0.98)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()

    fig3.legend((l1, l2, l3), ('Emg', 'Cop', 'Acc'), bbox_to_anchor=[0.5, 0.06], loc='center', ncol=3, labelspacing=0.,
                fontsize=14)
    fig3.legend([l6, l7], ['Front', 'Back'], bbox_to_anchor=[0.5, 0.03], loc='center', ncol=2, labelspacing=0.,
                fontsize=14)
    fig3.legend([l4, l5], ['Left', 'Right'], bbox_to_anchor=[0.5, 0.365], loc='center', ncol=2, labelspacing=0.,
                fontsize=14)

    plt.figure(4)
    fig4.suptitle(patient, fontsize=20)
    fig4.legend((l1, l6, l2, l7), ('Emg', 'Front', 'Cop', 'Back'), loc='lower center', ncol=2, labelspacing=1.,
                fontsize=14)
    fig4.legend([l4, l5], ['Left', 'Right'], bbox_to_anchor=[0.5, 0.365], loc='center', ncol=2, labelspacing=0.,
                fontsize=14)
    plt.subplots_adjust(hspace=0.45, wspace=0.24, top=0.94, bottom=0.11, left=0.04, right=0.98)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()


    if not os.path.exists('../WiiBoard/DataProcessor/Images/Cops_gen_4/' + patient+'/'):
        os.makedirs('../WiiBoard/DataProcessor/Images/Cops_gen_4/'+ patient+'/')
    fig1.set_size_inches(20, 11.25)
    plt.figure(1)
    plt.savefig('../WiiBoard/DataProcessor/Images/Cops_gen_4/' + patient +'/cops1.png', dpi=300)
    fig2.set_size_inches(20, 11.25)
    plt.figure(2)
    plt.savefig('../WiiBoard/DataProcessor/Images/Cops_gen_4/' + patient + '/cops2.png', dpi=300)
    fig3.set_size_inches(20, 11.25)
    plt.figure(3)
    plt.savefig('../WiiBoard/DataProcessor/Images/Cops_gen_4/' + patient + '/cops3.png', dpi=300)
    fig4.set_size_inches(20, 11.25)
    plt.figure(4)
    plt.savefig('../WiiBoard/DataProcessor/Images/Cops_gen_4/' + patient + '/cops4.png', dpi=300)
    plt.show()


def normalize(EMG_data, currentMax = True, globalMax = (1), cop = False, cop_range=(0), zero_out=False):
    for i in range(0, len(EMG_data)):
        if zero_out:
            EMG_data[i] = list((np.array(EMG_data[i]) - min(EMG_data[i])))
        elif currentMax:
            EMG_data[i] = list((np.array(EMG_data[i])-min(EMG_data[i]))/(max(EMG_data[i])-min(EMG_data[i])))
        elif cop:

            EMG_data[i] = list((np.array(EMG_data[i])-min(EMG_data[i]))/(cop_range[i]))
        else:
            EMG_data[i] = list((np.array(EMG_data[i]) - min(EMG_data[i])) / (globalMax[i] - min(EMG_data[i])))
    return EMG_data

