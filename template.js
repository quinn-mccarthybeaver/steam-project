{
    xAxis: {
            type: 'datetime',
        labels: {
    format: '{value:%Y-%b-%e}'
  }
  },
    yAxis: {
            scrollbar: {
                enabled: true,
                showFull: false
            }
        },
    chart: {
        scrollablePlotArea: {
            minWidth: 700,
            scrollPositionX: 1
        },
    zoomType: 'xy'
},
      tooltip: {
    shared: true,
    crosshairs: true,
  },
    plotOptions: {
        pointInterval: 3600000, // one hour
            pointStart: Date.UTC(2015, 4, 31, 0, 0, 0),
        panning: true,

    bar: {
      borderRadius: 8,
      negativeColor: '#FF0000'
    },
        column:{
            zoomType: 'x'
        },
    series: {
            boost: true,
            cursor: 'pointer',
            className: 'popup-on-click',
            marker: {
                lineWidth: 1
            },
          turboThreshold: 0
    }
  }
}