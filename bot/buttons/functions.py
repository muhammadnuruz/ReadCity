import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def create_statistic_image(data: dict, chat_id: int, name=None, date=None):
    df = pd.DataFrame(list(data.items()), columns=['names', 'values'])
    df = df.sort_values('values', ascending=False)
    names = df['names'].tolist()
    values = df['values'].tolist()
    colors = plt.cm.viridis_r(np.linspace(0, 1, len(names)))  # ranglarni yorqinligi bo'yicha tartiblash
    plt.figure(figsize=(10, 8))
    bars = plt.barh(names, values, color=colors)
    for i, bar in enumerate(bars):
        if int(bar.get_width()) == 0:
            alignment = 'left'
            padding = 5
        else:
            alignment = 'right'
            padding = -5
        plt.text(bar.get_width() + padding, bar.get_y() + bar.get_height() / 2,
                 '%s, %d%%' % (names[i], int(bar.get_width())), ha=alignment, va='center', color='black', fontsize=15)
    plt.gca().invert_yaxis()
    plt.tick_params(labelleft=False, top=False)
    plt.xlim([0, 100])
    if name and date:
        plt.title(f"{name} - {date}", fontsize="large", fontweight="bold", color="black")
    plt.savefig(f'images/{chat_id}.png')
