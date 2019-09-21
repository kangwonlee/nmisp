import platform

import matplotlib.font_manager as fm
import pylab as py
import seaborn as sns


def label_scatter_plot(data_frame, x_field='ROE', y_field='PER', label='종목명', font='Batang'):

    # https://stackoverflow.com/a/1857
    if platform.system() in ('Linux', 'Windows'):
        font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    elif platform.system() in ('Darwin',):
        font_list = fm.OSXInstalledFonts()
    else:
        font_list = []

    # https://code-examples.net/ko/q/13cad76

    b_found = False

    for f in fm.fontManager.ttflist:
        if font in f.name:
            print('using:', repr(f.name), repr(f.fname))
            b_found = True

    if b_found:
        import matplotlib as mpl
        mpl.rcParams['font.family'] = font

    ax = sns.lmplot(
        x_field, 
        y_field,
        data=data_frame,
        fit_reg=False,
    )

    py.title(f'{x_field} vs {y_field}')
    py.xlabel(x_field)
    py.ylabel(y_field)

    for i, row in data_frame.iterrows():
        
        py.gca().text(row[x_field] + 0.2, row[y_field], row[label])
