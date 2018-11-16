odoo.define('sales_dashboard', function (require) {
    'use strict';

    var AbstractField = require('web.AbstractField');
    var field_registry = require('web.field_registry');

    var SalesDashboardGraph = AbstractField.extend({
        className: "o_dashboard_graph", // TODO: Revisar si es la mejor opción
        cssLibs: [
            '/web/static/lib/nvd3/nv.d3.css'
        ],

        jsLibs: [
            '/web/static/lib/nvd3/d3.v3.js',
            '/web/static/lib/nvd3/nv.d3.js',
            '/web/static/src/js/libs/nvd3.js'
        ],
        start: function() {
            this.graph_type = this.attrs.graph_type;
            this.data = JSON.parse(this.value);
            this.display_graph();
            return this._super();
        },
        display_graph : function() {
            var self = this; // Objeto con atributos del campo a graficar
            nv.addGraph(function () {
                self.$svg = self.$el.append('<svg>');
                // TODO: Dependiendo del cliente se puede hacer más gráficas
                switch(self.graph_type) {
                    case "bar":
                        self.$svg.addClass('o_graph_barchart');
                        self.chart = nv.models.discreteBarChart()
                            .x(function(d) { return d.label })
                            .y(function(d) { return d.value })
                            .showValues(true)
                            .showYAxis(false)
                            .wrapLabels(true)
                            .margin({'left': 0, 'right': 0, 'top': 20, 'bottom': 20});
                        self.chart.xAxis.
                            axisLabel(self.data[0].title);
                        self.chart.yAxis.
                            tickFormat(d3.format(',.2f'));
                        break;
                }
                d3.select(self.$el.find('svg')[0])
                    .datum(self.data)
                    .call(self.chart);

                self.customize_chart();

                nv.utils.windowResize(self.on_resize);

                d3.selectAll('.nv-legend')[0].forEach(function(d) {
                    positionY += verticalOffset;
                    d3.select(d).attr('transform', 'translate(' + positionX + ',' + positionY + ')');
                });
            });
        },

        // Al cambiar tamaño de pantalla actualizó gráficas
        on_resize: function(){
            this.chart.update();
            this.customize_chart();
        },

        customize_chart: function(){
            // Personalización para gráfica de barra
            if (this.graph_type === 'bar') {
                var bar_classes = _.map(this.data[0].values, function (v, k) {return v.type});
                _.each(this.$('.nv-bar'), function(v, k){
                    $(v).attr('class', $(v).attr('class') + ' ' + bar_classes[k]);
                });
            }
        },

        destroy: function(){
            nv.utils.offWindowResize(this.on_resize);
            this._super();
        },

    });

    field_registry.add("sales_dashboard_graph", SalesDashboardGraph);

    return SalesDashboardGraph;
});