export default {
   
    tooltip: {
        trigger: 'item',
        formatter: function(params){
            let one=params.data[3]
            let a=""+one.address+"<br/>"
            a=a+"avg:"+one.avg+"<br/>"
            a=a+"count:"+one.c+"<br/>"
            return a
        }
    },
    bmap: {
        center: [120.79200448509146, 30.74407593469307],
        // 万达广场
        zoom: 13,
        roam: true,
        mapStyle: {
            
        }
    },
    series: [
        {
            name: '均价',
            type: 'effectScatter',
            coordinateSystem: 'bmap',
            data: [
             
              ],
            symbolSize: function (val) {
                return val[2] / 1000;
            },
            showEffectOn: 'emphasis',
            rippleEffect: {
                brushType: 'stroke'
            },
            hoverAnimation: true,
            label: {
                normal: {
                    formatter: '{b}',
                    position: 'right',
                    show: true
                }
            },
            itemStyle: {
                normal: {
                    color: '#f4e925',
                    shadowBlur: 10,
                    shadowColor: '#333'
                }
            },
            zlevel: 100,
            z:100
        }
    ]
}