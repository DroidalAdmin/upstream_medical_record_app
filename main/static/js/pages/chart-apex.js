document.addEventListener('DOMContentLoaded', function () {
    let chartData = {};

    function fetchDataAndUpdateCharts(fromDate, toDate) {
        console.log('Fetching data from', fromDate, 'to', toDate);
        fetch('/daterange/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken // Ensure CSRF token is included
            },
            body: JSON.stringify({
                fromdate: fromDate,
                todate: toDate
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Fetched data:', data);
            chartData = data;
            updateCharts(data);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while fetching the data.');
        });
    }

    function updateCharts(data) {
        const { new_requests, assigned_requests, completed_requests, months } = data;

        // Reverse the months and data arrays
        const reversedMonths = months.slice().reverse();
        const reversedNewRequests = new_requests.slice().reverse();
        const reversedAssignedRequests = assigned_requests.slice().reverse();
        const reversedCompletedRequests = completed_requests.slice().reverse();

        // Calculate the sum for the line chart
        const summedRequests = reversedNewRequests.map((val, index) => 
            val + reversedAssignedRequests[index] + reversedCompletedRequests[index]
        );

        console.log('Updating charts with:', reversedNewRequests, reversedMonths);

        chart_bar_chart_1.updateSeries([
            { name: 'New Requests', data: reversedNewRequests },
            { name: 'Assigned Requests', data: reversedAssignedRequests },
            { name: 'Requests Completed', data: reversedCompletedRequests }
        ]);

        chart_bar_chart_1.updateOptions({
            xaxis: {
                categories: reversedMonths  // Reversed months
            }
        });

        chart_pie_chart_1.updateSeries([
            new_requests.reduce((a, b) => a + b, 0),
            assigned_requests.reduce((a, b) => a + b, 0),
            completed_requests.reduce((a, b) => a + b, 0)
        ]);

        chart_line_chart_1.updateSeries([
            { name: 'Total Requests', data: summedRequests }
        ]);

        chart_line_chart_1.updateOptions({
            xaxis: {
                categories: reversedMonths  // Reversed months
            }
        });
    }

    // Initialize Bar and Pie Charts
    var chart_bar_chart_1 = new ApexCharts(document.querySelector('#bar-chart-1'), {
        chart: { height: 350, type: 'bar' },
        plotOptions: { bar: { horizontal: false, columnWidth: '55%', endingShape: 'rounded' } },
        dataLabels: { enabled: false },
        colors: ['#2CA87F', '#4680FF', '#13c2c2'],
        stroke: { show: true, width: 2, colors: ['transparent'] },
        series: [
            { name: 'New Requests', data: [] },
            { name: 'Assigned Requests', data: [] },
            { name: 'Requests Completed', data: [] }
        ],
        xaxis: { categories: [] },
        fill: { opacity: 1 },
        tooltip: { y: { formatter: function (val) { return `${val} requests`; } } }
    });
    chart_bar_chart_1.render();

    var chart_pie_chart_1 = new ApexCharts(document.querySelector('#pie-chart-1'), {
        chart: { height: 320, type: 'pie' },
        labels: ['New Requests', 'Assigned Requests', 'Requests Completed'],
        series: [],
        colors: ['#4680FF', '#2CA87F', '#13c2c2'],
        legend: { show: true, position: 'bottom' },
        dataLabels: { enabled: true, dropShadow: { enabled: false } },
        responsive: [{ breakpoint: 480, options: { legend: { position: 'bottom' } } }]
    });
    chart_pie_chart_1.render();

    // Initialize Line Chart
    var chart_line_chart_1 = new ApexCharts(document.querySelector('#line-chart-1'), {
        chart: {
            height: 300,
            type: 'line',
            zoom: {
                enabled: false
            }
        },
        dataLabels: {
            enabled: false,
            width: 2
        },
        stroke: {
            curve: 'straight'
        },
        colors: ['#4680FF'],
        series: [
            {
                name: 'Total Requests',
                data: [] // Initialize with empty data
            }
        ],
        grid: {
            row: {
                colors: ['#f3f6ff', 'transparent'],
                opacity: 0.5
            }
        },
        xaxis: {
            categories: [] // Initialize with empty categories
        }
    });
    chart_line_chart_1.render();

    // Fetch data for the default date range (last 4 months)
    const toDate = new Date().toISOString().split('T')[0];
    const fromDate = new Date(new Date().setDate(new Date().getDate() - 120)).toISOString().split('T')[0];
    fetchDataAndUpdateCharts(fromDate, toDate);

    // Event listener for the date range form submission
    document.getElementById('daterange-form').addEventListener('submit', function (e) {
        e.preventDefault();
        const fromDate = document.getElementById('from-date').value;
        const toDate = document.getElementById('to-date').value;

        fetchDataAndUpdateCharts(fromDate, toDate);
    });
});
