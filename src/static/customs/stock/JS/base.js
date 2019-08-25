// 获取词典key

function GetBindCode({
    Code,
    Bindings,
    Basic
}) {
    Bindings = Bindings || GBindings || [];


    oBinding = Bindings.find(function (v) {
        return v.Relation == Code && v.Effect && v.Effect.includes(Basic)
    });
    if (!oBinding) {
        oBinding = Bindings.find(function (v) {
            return v.Code == Code && ((v.Effect && v.Effect.includes(Basic)) || !v.Effect)
        });
    }
    if (oBinding) {
        return oBinding.Code
    }
    return null
}




GBindings.push({
    Code: 'SF',
    Desc: "是否",
    Records: [{
        name: '是',
        value: '1'
    }, {
        name: '否',
        value: '0'
    }, ]
});