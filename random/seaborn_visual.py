import seaborn as sns
import matplotlib.pyplot as plt
import time


def seaborn_distplot(df, col):
    sns.distplot(df[col], label=df.index, color='coral')
    return plt.show()


def seaborn_scatter(df, col1, col2):
    sns.scatterplot(x=df[col1], y=df[col2], )
    plt.savefig('new.png')
    return plt.savefig('new.png')
