import pandas
import pandas as pd
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.bar import BarSeries, ColumnSeries
from highcharts_core.options.series.scatter import ScatterSeries
import os

folder_path = '../TechSpider/cards'
template_options = HighchartsOptions.from_js_literal(
    '../template.js'
)
my_chart = Chart.from_options(template_options,
                              chart_kwargs={
                                  'container': 'chart',
                                  'variable_name': 'myChart',
                                  'zoomType': 'xy'

                              })
for filename in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, filename)):
        series = ColumnSeries.from_csv(os.path.join(folder_path, filename),
                                       property_column_map={
                                           'x': 'date',
                                           'y': 'real_users',
                                           'name': 'date'
                                       },
                                       series_kwargs={
                                           'name': filename,
                                       })

        my_chart.add_series(series)

game_series = ScatterSeries.from_csv("./data/playerdata/test.csv",
                                     property_column_map={
                                         'x': 'all-time date',
                                         'y': 'all-time peak',
                                         'name': 'id'
                                     },
                                     series_kwargs={
                                         'tooltip': {
                                             'pointFormat': '<b>'
                                                            'players:{point.y}'
                                                            'time:{point.x}'
                                                            'id:{point.name}</b>'
                                         }
                                     })


# Add the game series to the chart
my_chart.add_series(game_series)

as_js_literal = my_chart.to_js_literal()

with open('my_target_file.js', 'w') as file:
    file.write(as_js_literal)
    file.close()
