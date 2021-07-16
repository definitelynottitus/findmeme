async function getData(url = '') {
    const result = await fetch(url);
    return result.json()
}

let ready = (callback) => {
    if (document.readyState != "loading") callback();
    else document.addEventListener("DOMContentLoaded", callback);
}

ready(() => {
    var ctx = document.getElementById("lineChart").getContext("2d");
    const chartDiv = document.querySelector('.flexbox-item-1');
    chartDiv.classList.add('loader')
    lineChart = new Chart(ctx,{
    type: "line",
    data: {
        labels: [],
        datasets: [{
            label: "JPG/PNG Karma Points",
            data: [],
            fill: !1,
            borderColor: "rgb(75, 192, 192)",
            backgroundColor: "rgb(123, 205, 205)",
            borderWiidth: 1,
            radius: 0
        }, {
            label: "GIF Karma Points",
            data: [],
            fill: !1,
            borderColor: "rgb(255, 153, 153)",
            backgroundColor: "rgb(255, 204, 204)",
            borderWiidth: 1,
            radius: 0
        }]
    },
    options: {
        maintainAspectRatio: !1,
        interaction: {
            mode: "nearest",
            intersect: false
        },
        scales: {
            x: {
                type: "time",
                time: {
                    unit: "day"
                },
                title: {
                    display: !0,
                    text: "Date"
                },
                ticks: {
                    source: "auto",
                    maxRotation: 0,
                    autoSkip: !0
                },
                font: function(t) {
                    if (t.tick && t.tick.major)
                        return {
                            weight: "bold"
                        }
                }
            },
            y: {
                display: !0,
                title: {
                    display: !0,
                    text: "Karma Points"
                }
            }
        }
    }
    });
    
    getData('https://api.findmeme.cc/score?imagetype=still')
    .then(t => {
        lineChart.data.datasets[0].data = t.y;
        lineChart.data.labels = t.x.map(x => new Date(x/10**6).toISOString());
        lineChart.update();
    })
    .catch((error)=> {
        console.log(error);
        chartDiv.textContent = 'Sorry Something Went Wrong Please Refresh the Page';
        chartDiv.classList.remove('loader');
    })
    getData('https://api.findmeme.cc/score?imagetype=animated')
    .then(t => {
        lineChart.data.datasets[1].data = t.y;
        lineChart.update();
        chartDiv.classList.remove('loader');
    })
    .catch((error)=> {
        console.log(error);
        chartDiv.textContent = 'Sorry Something Went Wrong Please Refresh the Page';
        chartDiv.classList.remove('loader');
    })
    
});