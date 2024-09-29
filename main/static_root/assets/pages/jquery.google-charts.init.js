/**
 * Theme: Zircos Admin Template
 * Author: Coderthemes
 * Module/App: Flot-Chart
 */

! function($) {
    "use strict";

    var GoogleChart = function() {
        this.$body = $("body")
    };

       
    //creates pie chart
    GoogleChart.prototype.createPieChart = function(selector, data, colors, is3D, issliced) {
        var options = {
            fontName: 'Hind Madurai',
            fontSize: 13,
            height: 300,
            width: 500,
            chartArea: {
                left: 50,
                width: '90%',
                height: '90%'
            },
            colors: colors
        };

        if(is3D) {
            options['is3D'] = true;
        }

        if(issliced) {
            options['is3D'] = true;
            options['pieSliceText'] = 'label';
            options['slices'] = {
                2: {offset: 0.15},
                5: {offset: 0.1}
            };
        }

        var google_chart_data = google.visualization.arrayToDataTable(data);
        var pie_chart = new google.visualization.PieChart(selector);
        pie_chart.draw(google_chart_data, options);
        return pie_chart;
    },

   
    //init
    GoogleChart.prototype.init = function () {
        var $this = this;
 
        //creating pie chart
        var pie_data = [
            ['Task', 'overall percentage'],
            ['In-Progress',     11],
            ['Completed',      7],
            ['Error',  2], 
        ];
   
        //creating 3d pie chart
        $this.createPieChart($('#pie-3d-chart')[0], pie_data, ['#188ae2', '#4bd396', '#f9c851'], true, false);

      
        //on window resize - redrawing all charts
        $(window).on('resize', function() {
          $this.createPieChart($('#pie-3d-chart')[0], pie_data, ['#188ae2', '#4bd396', '#f9c851'], true, false);
        });
    },
    //init GoogleChart
    $.GoogleChart = new GoogleChart, $.GoogleChart.Constructor = GoogleChart
}(window.jQuery),

//initializing GoogleChart
function($) {
    "use strict";
    //loading visualization lib - don't forget to include this
    google.load("visualization", "1", {packages:["corechart"]});
    //after finished load, calling init method
    google.setOnLoadCallback(function() {$.GoogleChart.init();});
}(window.jQuery);