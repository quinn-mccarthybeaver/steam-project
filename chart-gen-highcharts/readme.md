# Highcharts chart generator
The files in this folder are responsible for generating a interactive
chart with Highcharts. The `chart-generator.py` file makes use of the card csv file
to plot the real users of each card, and makes use of the peak player data from the `cleaned_data` folder.
## Generating Highcharts chart
* To generate the interactive Highcharts chart, run `Python chart-generator.py`
  * This generates a file called `my_render_target.js`, which contains the Javascript used by
  `render.html`
  * Open `render.html` in a browser
# Known Issues
Since the Python Highcharts library was just updated, some issues may occur with the Javascript generation.
## "new" usage
One such issue is the graph not rendering due to the keyword `new` used in the `my_render_target.js` file.
To fix this issue, delete the keyword in the `my_render_target.js` file and the graph should generate
