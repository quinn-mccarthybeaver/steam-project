import pandas
import pandas as pd
from highcharts_core import highcharts
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import LineSeries, StreamGraphSeries, AreaRangeSeries
from highcharts_core.options.series.bar import BarSeries, ColumnSeries
from highcharts_core.options.series.histogram import HistogramSeries
from highcharts_core.options.series.scatter import ScatterSeries
from highcharts_core.options.series.spline import SplineSeries
import os

df = pd.DataFrame()
df = pandas.read_csv("./steamdb/card_users_real.csv", index_col=0)
folder_path = './steamdb/cards'
# df = df.dropna(subset=['shading_units'])
print(df.head())
template_options = HighchartsOptions.from_js_literal(
    'template.js'
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
                                           'name': filename
                                       })

        my_chart.add_series(series)

as_js_literal = my_chart.to_js_literal()


# my_png_image = my_chart.download_chart(
#     format = 'png',
#     filename = '/images/my-chart-file.png'
# )

with open('my_target_file.js', 'w') as file:
    file.write(as_js_literal)
    file.close()

