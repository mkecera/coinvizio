var endpoint1 = '/dashboard/chart/dataMarketCap/'
var endpoint2 = '/dashboard/chart/data24hChange/'
var endpoint3 = '/dashboard/chart/dataTopCapChange/'
var labels1 = []
var labels2 = []
var labels3 = []
var defaultData1 = []
var defaultData2 = []
var defaultData3 = []

$.ajax({
    method: "GET",
    url: endpoint1,
    success: function (data) {
        labels1 = data.labels
        defaultData1 = data.default
        setChartMarketCap()
    },
    error: function (error_data) {
        console.log("error")
        console.log(error_data)
    }
})

/*
$.ajax({
    method: "GET",
    url: endpoint2,
    success: function (data) {
        labels2 = data.labels
        defaultData2 = data.default
        setChart24hChange()
    },
    error: function (error_data) {
        console.log("error")
        console.log(error_data)
    }
})
*/

$.ajax({
    method: "GET",
    url: endpoint3,
    success: function (data) {
        labels3 = data.labels
        defaultData3 = data.default
        setChartTopCap24hChange()
    },
    error: function (error_data) {
        console.log("error")
        console.log(error_data)
    }
})


function setChartMarketCap() {
    var ctx2 = document.getElementById("pieMarketCap");
    var myChart = new Chart(ctx2, {
        type: 'doughnut',
        data: {
            labels: labels1,
            datasets: [{
                data: defaultData1,
                borderColor: 'transparent',
                backgroundColor: [
                    '#35a7ff',
                    '#ffbf00',
                    '#e83f6f',
                    '#32936f',
                    '#ffffff',
                    '#1be7ff',
                    '#6eeb83',
                    '#e4ff1a',
                    '#e8aa14',
                    '#ff5714',
                    '#586f7c'
                ],
            }]
        },
        options: {
            tooltips: {
                callbacks: {
                    label: function (tooltipItem, data) {
                        return data.labels[tooltipItem.index] + " $" + Number(data.datasets[0].data[tooltipItem.index]).toFixed(0).replace(/./g, function (c, i, a) {
                            return i > 0 && c !== "." && (a.length - i) % 3 === 0 ? "," + c : c;
                        });
                    }
                }
            },
            title: {
                display: false,
                text: 'Market Capitalisation in $',
                fontSize: 14
            }
        }
    })
}

/*
function setChart24hChange(){
    var ctx = document.getElementById("bar24hChange");
    var myChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: labels2,
            datasets: [{
                data: defaultData2,
                backgroundColor: [
                    'rgba(116,196,147,1)',
                    'rgba(116,196,147,1)',
                    'rgba(116,196,147,1)',
                    'rgba(116,196,147,1)',
                    'rgba(116,196,147,1)',
                    'rgba(116,196,147,1)',
                    'rgba(116,196,147,1)',
                    'rgba(116,196,147,1)',
                    'rgba(116,196,147,1)',
                    'rgba(116,196,147,1)',
                    'rgba(190,81,104,1)',
                    'rgba(190,81,104,1)',
                    'rgba(190,81,104,1)',
                    'rgba(190,81,104,1)',
                    'rgba(190,81,104,1)',
                    'rgba(190,81,104,1)',
                    'rgba(190,81,104,1)',
                    'rgba(190,81,104,1)',
                    'rgba(190,81,104,1)',
                    'rgba(190,81,104,1)',
                ],
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    ticks: {
                        callback: function (value, index, values) {
                            return Math.round(value) +' %';
                        }
                    }
                }]
            },
            tooltips: {
                callbacks: {
                    label: function (tooltipItem, data) {
                        return Math.round(tooltipItem.xLabel) + ' %';
                    }
                }
            },
            title: {
                display: true,
                text: '24h Top Gainers & Losers',
                fontSize: 14
            },
            legend: {
            display: false
            }
        }
    })
}
*/

function setChartTopCap24hChange(){
    var ctx = document.getElementById("barTopCap24hChange");
    var myChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: labels3,
            datasets: [{
                data: defaultData3,
                backgroundColor: [],
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    gridLines:{
                        color: "rgba(171,171,171,0.1)",
                        zeroLineColor: "rgba(171,171,171,0.1)"
                    },
                    ticks: {
                        callback: function (value, index, values) {
                            return Math.round(value*100)/100 +' %';
                        }
                    }                    
                }],
                yAxes:[{
                    gridLines:{
                        color: "rgba(171,171,171,0.3)",
                        zeroLineColor: "rgba(171,171,171,0.3)"
                    }
                }]
            },
            tooltips: {
                callbacks: {
                    label: function (tooltipItem, data) {
                        return Math.round(tooltipItem.xLabel*100)/100 + ' %';
                    }
                }
            },
            title: {
                display: false,
                text: '24h Change - Top Market Cap',
                fontSize: 14
            },
            legend: {
                display: false
            }
        }
    })
    var bars = myChart.data.labels.length;
    for(i=0;i<bars;i++){
       var color="rgba(190,81,104,1)";
       //You can check for bars[i].value and put your conditions here
       if(myChart.data.datasets[0].data[i]<=0){
       	color="rgba(190,81,104,1)";
       }
       else{
       	color="rgba(116,196,147,1)";
       }
       myChart.data.datasets[0].backgroundColor[i] = color;
    }
    myChart.update(); //update the cahrt
}
