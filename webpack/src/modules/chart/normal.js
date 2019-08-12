//可以选择的图表
// 1 setRemark   :  "可选择分类": 属性

var remarks = {
    simpleBar: {
        "desc": "简单的barDemo",
        "option": "optionSimpleBar",

    },
    dataSet: {
        "desc": "简单的dataSet",
        "option": "optionDataSet",
        // "default":true 
    },
    dataSetDimensions: {
        desc: "dataSet维度",
        "option": "optionDataSetDimensions"
    },
    graphic: {
        desc: "画网元组图标",
        // "default":true 
    },
    graphic1: {
        desc: "项目中应用",
        "default": true
    }

}

var optionGraphic = {
    graphic: [{
        type: 'group',
        rotation: Math.PI / 4,
        bounding: 'raw',
        right: 110,
        bottom: 110,
        z: 100,
        children: [{
                type: 'rect',
                left: 'center',
                top: 'center',
                z: 100,
                shape: {
                    width: 400,
                    height: 50
                },
                style: {
                    fill: 'rgba(0,0,0,0.3)'
                }
            },
            {
                type: 'text',
                left: 'center',
                top: 'center',
                z: 100,
                style: {
                    fill: '#fff',
                    text: 'ECHARTS BAR CHART',
                    font: 'bold 26px Microsoft YaHei'
                }
            }
        ]
    }, ]
}


var  optionGraphic1 = {
    graphic: [{
        type: 'group',
        position: [100, 100],
        children: [{
            type: 'group',
            draggable: true, // echarts bug 不能被整体拖动
            children: [{
                    // draggable: true,
                    type: 'circle',
                    position: [0, 0],
                    shape: {
                        cx: 10,
                        cy: 10,
                        r: 10
                    },
                    style: {
                        stroke: '#BEBEBE',
                        strokeWidth: 2,
                        fill: "#FFFFFF"
                    }
                },
                {
                    // draggable: true,
                    type: 'text',
                    style: {
                        x: 24,
                        y: 4,
                        text: "我的老家1111"
                    }
                }

            ]
        }, {
            type: 'text',
            style: {
                x: 24,
                y: 4,
                text: "我的老家"
            }
        }]
    }, ]
}

var  optionSimpleBar = {
    xAxis: {
        type: 'category',
        data: ['Matcha Latte', 'Milk Tea', 'Cheese Cocoa', 'Walnut Brownie']
    },
    yAxis: {},
    series: [{
            type: 'bar',
            name: '2015',
            data: [89.3, 92.1, 94.4, 85.4]
        },
        {
            type: 'bar',
            name: '2016',
            data: [95.8, 89.4, 91.2, 76.9]
        },
        {
            type: 'bar',
            name: '2017',
            data: [97.7, 83.1, 92.5, 78.1]
        }
    ]
};



var  optionDataSet = {
    legend: {},
    tooltip: {},
    dataset: {
        // 提供一份数据。 'column': 默认值。 列模式，
        source: [
            ['product', '2015', '2016', '2017'],
            ['Matcha Latte', 43.3, 85.8, 93.7],
            ['Milk Tea', 83.1, 73.4, 55.1],
            ['Cheese Cocoa', 86.4, 65.2, 82.5],
            ['Walnut Brownie', 72.4, 53.9, 39.1]
        ]
    },
    // 声明一个 X 轴，类目轴（category）。默认情况下，类目轴对应到 dataset 第一列。
    xAxis: { type: 'category' },
    // 声明一个 Y 轴，数值轴。
    yAxis: {},
    // 声明多个 bar 系列，默认情况下，每个系列会自动对应到 dataset 的每一列。
    series: [
        { type: 'bar' },
        { type: 'bar' },
        { type: 'bar' }
    ]
}



var optionDataSetDimensions = { // dimension 维度
    legend: {},
    tooltip: {},
    dataset: {
        // 这里指定了维度名的顺序，从而可以利用默认的维度到坐标轴的映射。
        // 如果不指定 dimensions，也可以通过指定 series.encode 完成映射，参见后文。
        dimensions: ['product', '2015', '2016', '2017'],
        source: [
            { product: 'Matcha Latte', '2015': 43.3, '2016': 85.8, '2017': 93.7 },
            { product: 'Milk Tea', '2015': 83.1, '2016': 73.4, '2017': 55.1 },
            { product: 'Cheese Cocoa', '2015': 86.4, '2016': 65.2, '2017': 82.5 },
            { product: 'Walnut Brownie', '2015': 72.4, '2016': 53.9, '2017': 39.1 }
        ]
    },
    xAxis: { type: 'category' },
    yAxis: {},
    series: [
        { type: 'bar' },
        { type: 'bar' },
        { type: 'bar' }
    ]
}




var toFirstUpperCase=function(str,lowerOther){
    return str.replace(/\b(\w)(\w*)/g, function($0, $1, $2) {
        if(lowerOther){
            return  $1.toUpperCase() + $2.toLowerCase();
        }
        return $1.toUpperCase() + $2;
    })
}


Object.keys(remarks).forEach(function(k){
    let remark=remarks[k];
    let dom="option"+toFirstUpperCase(k||"")
    if (dom!="option"){
        remark["setting"]=eval(dom);
    }
})
export function getRemarks(){
    return  remarks;
}  