function CRUDSetting(text, option) {
    this.maxSpan = 3;
    if (typeof option == "object") {
        if (option.colSpan) {
            this.colSpan = option.colSpan;
        }
    }
    this.text_old = text;
    this.parseText = () => {
            var defaults = {
                "sn": "",
                "nm": "",
                "showType": "text",
                "dataType": "String",
                "colSpan": 1,
                "width": 100,
                "fmt": "",
                "hidden": false
            }
            var types = {
                "c": {
                    "showType": "combo",
                    "fmt": "",
                    "dataType": "String",
                },
                "d": {
                    "showType": "datetime",
                    "fmt": "yyyyMMdd",
                    "dataType": "String"
                },
                "a": {
                    "showType": "textarea",
                    "colSpan": 3,
                    "dataType": "String"
                },
                "t": {
                    "showType": "text",
                    "dataType": "String"

                }
            }
            var rows = []
            text.split("\n").forEach(function(r) {
                var row = Object.assign({}, defaults)
                var [sn, dataType, nm, showType, ...optional] = r.split(" ");
                row.sn = sn;
                row.nm = nm;
                if (!nm) {
                    row.nm = row.sn
                }
                row.dataType = dataType || "String";
                row.showType = showType || "t";
                if (["str", "String", "string"].includes(dataType)) {
                    row.dataType = "String";
                }

                Object.keys(types).forEach(function(k) {
                    if (k == row.showType) {
                        Object.assign(row, types[k])
                    }
                })
                // 最后一个字段复制
                if (optional && optional.length > 0) {
                    lastOptional = {};
                    lastA = optional.pop().split(",")
                    lastA.forEach(function(s) {
                        if (s) {
                            var [k, v] = s.split(":")
                            if (k && v) {
                                lastOptional[k] = v
                            }
                        }
                    })
                    Object.assign(row, lastOptional)

                }
                rows.push(row)


            })
            return rows;
        },
        this.transformColumns = () => {
            var cols = []
            this.rows.forEach(function(row) {

                column = `{ "field": "${row.sn}","title": "${row.nm}", "width": ${row.width} }`;
                column = JSON.parse(column);
                if (row.dataType == "combo") {
                    column["binding"] = row.fmt
                } else if (row.dataType == "datetime") {
                    if (row.fmt == "yyyyMMdd" || row.fmt == "yyyy-MM-dd") {
                        column["formatter"] = "DateFormatter"
                    } else if (row.fmt == "yyyyMM" || row.fmt == "yyyy-MM") {
                        column["formatter"] = "MonthFormatter"
                    }

                }
                cols.push(column);
            })
            return cols;
        },
        this.transformInputs = () => {
            var inputs = []
            this.rows.forEach(function(row) {

                var input =
                    `{ "Field": "${row.sn}", "Name": "${row.nm}", "ShowType": "${row.showType}","DataType": "${row.dataType}", "ColSpan": "${row.colSpan}" }`;
                input = JSON.parse(input);
                if (row.dataType == "combo" || row.dataType == "datetime") {
                    input["Ext"] = row.fmt
                }
                inputs.push(input);
            })
            inputs= this.folding(inputs,this.maxSpan)
            return inputs
        },
        this.folding=(a,maxSpan)=>{
            var inputs=[]
            var unitCount=0
            var unit=[]
            a.forEach(function(r){
                unitCount+=(Number(r["ColSpan"]||1))
                if(unitCount<=maxSpan){
                    unit.push(r);
                }else{
                    inputs.push(unit);
                    unitCount=1
                    unit=[r]
                }
            })
            if(unit.length>0){
                inputs.push(unit);
            }

            return inputs 

        }
        this.transformProperties = () => {
            var properties = []
            this.rows.forEach(function(row) {

                var property = `{ "Field": "${row.sn}", "Name": "${row.nm}", "ShowType": "${row.showType}","DataType": "${row.dataType}","FilterEnabled": true }`;
                property = JSON.parse(property);
                if (row.dataType == "combo" || row.dataType == "datetime") {
                    property["Ext"] = row.fmt
                }
                properties.push(property);
            })
            return properties
        },
        this.transformQueries = () => {
            var queries = []
            this.rows.forEach(function(row) {
                if (row.q) {

                    var query = `{ "Field": "${row.sn}", "Label": "${row.nm}", "Type":  "QText"},`
                    query = JSON.parse(query);
                    if (row.dataType == "combo") {
                        row["Type"] = "QCombox";
                        query["Ext"] = row.fmt
                        query["Source"] = row.fmt
                    } else if (row.dataType == "datetime") {
                        row["Type"] = "QDatetime"
                        row["Ext"] = {
                            "Format": row.fmt
                        };
                    }
                    queries.push(query);

                }
            })
            return queries
        },

        this.rows = this.parseText()

    this.get = () => {
        o = {}
        o.columns = this.transformColumns()
        o.inputs = this.transformInputs();
        o.properties = this.transformProperties()
        o.queries = this.transformQueries();
        return o;


    }
};