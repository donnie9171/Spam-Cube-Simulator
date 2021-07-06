import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button
import numpy

total_stirs = 6
no_of_dice = 50
no_of_trails = 50
show_theoretical_val = True
labels = ['1', '2', '3', '4', '5', '6']
x = np.arange(len(labels))  # the label locations
width = 0.45
average_output = [0, 0, 0, 0, 0, 0]
uncertainty_output = [0, 0, 0, 0, 0, 0]
plot_x = [1, 2, 3, 4, 5, 6]
label_text = []
p = [1, 0, 0, 0, 0, 0]
moc = [[1 / 6, 5 / 6, 0, 0, 0, 0], [0, 2 / 6, 4 / 6, 0, 0, 0], [0, 0, 3 / 6, 3 / 6, 0, 0], [0, 0, 0, 4 / 6, 2 / 6, 0],
       [0, 0, 0, 0, 5 / 6, 1 / 6], [0, 0, 0, 0, 0, 1]]


def average(lst):
    return sum(lst) / len(lst)


def uncertainty(lst):
    return (max(lst) - min(lst)) / 2


def format_probability(input_list):
    temp_list = []
    for i in input_list:
        temp_list.append(round(i * 100, 1))
    return temp_list


def calc_theoretical_prob(k):
    if total_stirs == 0:
        return format_probability([1, 0.00, 0.00, 0.00, 0.00, 0.00])
    else:
        p = [1, 0, 0, 0, 0, 0]
        tmp = moc
        for i in range(k - 1):
            tmp = numpy.matmul(tmp, moc)
        return format_probability(numpy.matmul(p, tmp))


def percentage_string_formatter(input_list):
    temp_list = []
    for i in input_list:
        temp_list.append(f"{i}%")
    return temp_list


def update_simulation():
    a = 0
    sides_output_percentage = [0, 0, 0, 0, 0, 0]
    one_output_percentage = []
    two_output_percentage = []
    three_output_percentage = []
    four_output_percentage = []
    five_output_percentage = []
    six_output_percentage = []
    output_percentage_total = [one_output_percentage, two_output_percentage, three_output_percentage,
                               four_output_percentage, five_output_percentage, six_output_percentage]
    global label_text

    # print(f"Number of dice: {no_of_dice}\nNumber of stirs: {total_stirs}\nNumber of trails: {no_of_trails}")
    while a < no_of_trails:
        h = 0
        sides_output = [0, 0, 0, 0, 0, 0]
        while h < no_of_dice:
            single_sides_output = []
            i = 0
            while i < total_stirs + 1:
                dice_output = random.randint(1, 6)
                # print(dice_output)
                if not single_sides_output.__contains__(dice_output):
                    single_sides_output.append(dice_output)

                i += 1
            # print("Sides output (for 1 dice): " + str(len(single_sides_output)))
            sides_output[len(single_sides_output) - 1] += 1
            # print(sides_output)
            h += 1
        i = 0
        for j in sides_output:
            sides_output_percentage[i] = round(j / no_of_dice * 100, 1)
            i += 1
        # print(sides_output_percentage)
        i = 0
        for j in sides_output_percentage:
            output_percentage_total[i].append(j)
            i += 1

        a += 1
    i = 0
    for j in output_percentage_total:
        # print(str(i + 1) + ":" + str(j))
        # print("Average: " + str(round(average(j), 1)))
        average_output[i] = round(average(j), 1)
        # print("Max: " + str(max(j)))
        # print("Min: " + str(min(j)))
        # print("Uncertainty: ±" + str(round(uncertainty(j), 1)))
        uncertainty_output[i] = round(uncertainty(j), 1)
        i += 1

    label_text = []
    i = 0
    # print("--Final output--")
    for j in output_percentage_total:
        # print(str(i + 1) + " side/s: " + str(average_output[i]) + " ±" + str(uncertainty_output[i]) + "%")
        label_text.append(str(average_output[i]) + "%\n±" + str(uncertainty_output[i]) + "%")
        # print(label_text[i])
        i += 1


update_simulation()
# plot graph
fig, ax = plt.subplots()
if show_theoretical_val:
    p1 = ax.bar(x - width / 2, average_output, width, yerr=uncertainty_output, align='center', label='Simulation')
    p2 = ax.bar(x + width / 2, calc_theoretical_prob(total_stirs), width, align='center', label='Theoretical')
    ax.bar_label(p1, labels=label_text, padding=0.5, color='k', fontsize=8)
    ax.bar_label(p2, labels=percentage_string_formatter(calc_theoretical_prob(total_stirs)), padding=0.5, color='k',
                 fontsize=8)
else:
    p1 = ax.bar(x, average_output, width, yerr=uncertainty_output, align='center', label='Simulation')
    ax.bar_label(p1, labels=label_text, padding=0.5, color='k', fontsize=8)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.subplots_adjust(bottom=0.35)
ax.set_ylim(top=max(average_output) + max(uncertainty_output) + 20, bottom=0)

ax.set_xlabel('Number of sides fried/sides')
ax.set_ylabel('Probability/%')

ax.title.set_text('Distribution of ' + str(no_of_dice) + ' cubes stirred ' + str(total_stirs) + " times. (" + str(
    no_of_trails) + " trails total)")


def update_graph():
    ax.cla()
    global p1
    global p2
    global label_text
    # plot graph
    if show_theoretical_val:
        p1 = ax.bar(x - width / 2, average_output, width, yerr=uncertainty_output, align='center', label='Simulation')
        p2 = ax.bar(x + width / 2, calc_theoretical_prob(total_stirs), width, align='center', label='Theoretical')
        ax.bar_label(p1, labels=label_text, padding=0.5, color='k', fontsize=8)
        ax.bar_label(p2, labels=percentage_string_formatter(calc_theoretical_prob(total_stirs)), padding=0.5, color='k',
                     fontsize=8)
    else:
        p1 = ax.bar(x, average_output, width, yerr=uncertainty_output, align='center', label='Simulation')
        ax.bar_label(p1, labels=label_text, padding=0.5, color='k', fontsize=8)
    plt.subplots_adjust(bottom=0.35)
    ax.set_ylim(top=max(average_output) + max(uncertainty_output) + 20, bottom=0)


    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_xlabel('Number of sides fried/sides')
    ax.set_ylabel('Probability/%')
    ax.title.set_text('Distribution of ' + str(no_of_dice) + ' cubes stirred ' + str(total_stirs) + " times. (" + str(
        no_of_trails) + " trails total)")


ax_no_of_dice = plt.axes([0.25, 0.2, 0.6, 0.03])
no_of_dice_slider = Slider(
    ax=ax_no_of_dice,
    label='Number of cubes',
    valmin=1,
    valmax=100,
    valinit=50,
    valstep=1

)

ax_no_of_stirs = plt.axes([0.25, 0.15, 0.6, 0.03])
no_of_stirs_slider = Slider(
    ax=ax_no_of_stirs,
    label='Number of stirs',
    valmin=0,
    valmax=50,
    valinit=6,
    valstep=1

)
ax_no_of_trails = plt.axes([0.25, 0.1, 0.6, 0.03])
no_of_trails_slider = Slider(
    ax=ax_no_of_trails,
    label='Number of trails',
    valmin=1,
    valmax=100,
    valinit=50,
    valstep=1

)


def update_input_values(val):
    global no_of_dice
    no_of_dice = no_of_dice_slider.val
    global no_of_trails
    no_of_trails = no_of_trails_slider.val
    global total_stirs
    total_stirs = no_of_stirs_slider.val
    update_simulation()
    update_graph()


no_of_dice_slider.on_changed(update_input_values)
no_of_stirs_slider.on_changed(update_input_values)
no_of_trails_slider.on_changed(update_input_values)
plt.show()
