/**
 * Created by mesogene on 16-5-7.
 */
var id = 0;
console.log(classify);
$('#indexTalbe').bootstrapTable({
    columns: [{
        field: 'state',
        checkbox: "true",
        align: 'center',
        valign: 'middle'
    }, {
        field: 'kid',
        formatter: 'nameFormatter',
        sortable: 'true',
        visible: false,
        title: 'Id编号',
        align: 'center',
        valign: 'middle'
    }, {
        field: 'dataName',
        title: '数据集名称',
        align: 'center',
        valign: 'middle'
    }, {
        field: 'clusterNum',
        title: '簇数',
        align: 'center',
        valign: 'middle'
    }, {
        field: 'description',
        title: '描述',
        align: 'center',
        valign: 'middle'
    }, {
        field: 'file_path',
        // visible: false,
        title: '数据集下载',
        formatter: operateFormatter,
        align: 'center',
        valign: 'middle'
    }, {
        field: 'pngPath',
        // visible: false,
        title: '聚类后ＰＮＧ展示',
        formatter: operateTreePngDown,
        align: 'center',
        valign: 'middle'
    }],
    striped: true,
    checkbox: true,
    // search: true,
    showRefresh: true,
    showColumns: true,
    pagination: true,
    pageSize: 10,
    pageNumber: 1,
    pageList:"[5,10,20]",
    locale:"zh-CN",
    // clickToSelect: true,
    smartDisplay: true,
    showToggle: true,
    singleSelect: true,
    url: "/api/twok/",
    sidePagination: 'client'
}).on('uncheck.bs.table', function (e, row) {
    temp = 0;
}).on('check.bs.table', function (e, row) {
    temp = 1;
    rowContent = JSON.stringify(row);  //把json对象解析成string对象
});

function searchEvent(){
    var letter=$("#search").val();
    alert(letter);
    $("#docTable").bootstrapTable('refresh',{url:"/api/twok/?dataName="+letter});
}

function operateFormatter(value, row, index) {
    return [
        '<a title="下载" download href='+ value + '>',
        '<i class="am-icon-btn-sm am-primary am-icon-download am-icon-sm"></i>',
        '</a>'
    ].join('');
}


function operateTreePngDown(value, row, index) {
    return [
        '<a title="下载" download href='+ value + '>',
        '<i class="am-icon-download am-icon-sm"></i>',
        '</a>&nbsp;&nbsp;&nbsp;',
        '<a title="查看" target="view_window" href='+value+'>',
        '<i class="am-icon-eye am-icon-sm"></i>',
        '</a>'
    ].join('');
}


$("#dataSetInput").fileinput({
    uploadUrl: "/k_view/", // server upload action
    uploadAsync: false,
    showPreview: true,
    maxFileCount: 1,
    previewFileType: 'any',
    // showRemove: false,
    // removeClass: "btn btn-danger",
    // removeLabel: "Delete",
    // removeIcon: "<i class=\"glyphicon glyphicon-trash\"></i>",
    // uploadClass: "btn btn-info",
    // uploadLabel: "Upload",
    // uploadIcon: "<i class=\"glyphicon glyphicon-upload\"></i>",
    // allowedFileExtensions: ["jpg"],
    // previewClass: "bg-warning",
    maxFileSize: 1000000,
    // allowedFileTypes: ["video"],
    elErrorContainer: '#kv-error-2',
    uploadExtraData: function() {
        return {
            dataName: $("#dataName").val(),
            clusterNum: $("#clusterNum option:selected").val(),
            description: $("#dataDescribe").val()
        };
    }
    // layoutTemplates: {
    //         main1: "{preview}\n" +
    //         "<div class=\'input-group {class}\'>\n" +
    //         "   <div class=\'input-group-btn\'>\n" +
    //         "       {browse}\n" +
    //         "       {upload}\n" +
    //         "       {remove}\n" +
    //         "   </div>\n" +
    //         "   {caption}\n" +
    //         "</div>"
    // }
}).on('filebatchpreupload', function (event, data, id, index) {
    $('#kv-success-2').html('<h4>Train Status</h4><ul></ul>');
    $('#kv-success-2').fadeIn('slow');
    $('#kv-success-2 ul').html('<h5 id="loading_h5">training...</h5><img id="loading_bar" src="../../../templates/assets/img/bar.gif" width="300px" height="27px">');
}).on('filebatchuploadsuccess', function (event, data) {
    console.log(data);
    var out = '';
    out = data.response['success'];
    // $.each(data.files, function (key, file) {
    //     var fname = file.name;
    //     out = out + '<li>' + 'Uploaded file # ' + (key + 1) + ' - ' + fname + ' successfully.' + '</li>';
    // });
    $('#loading_bar').remove();
    $('#loading_h5').remove();
    $('#kv-success-2 ul').append(out);

});


$('#addDoc').click(function () {
    $('#dataInputFooter').css('display', 'none');
    $('#table').css('display', 'none');
    $('#docPanel').css('display', 'block');
});

$('#cancel').click(function () {
    turnPage('/k/');
});

$('#create').click(function () {
    if ($("#dataDescribe").val() == "") {
        sweetAlert("请填写描述", '', 'error');
    }else{
        var jsonObjectEdit = eval('(' + rowContent + ')');
        var kid = jsonObjectEdit.kid;
        $.ajax({
                async:false,
                type: "patch",
                dataType: 'json',
                // contentType: 'application/json',
                data: {'description': $("#dataDescribe").val()},
                url: '/api/twok/'+kid+'/',
                success: function (data) {
                    // swal({
                    //     title:'修改成功',
                    //     type:'success',
                    //     timer:1000
                    // },function () {
                    //     turnPage('/a/');
                    // });
                    // // // sweetAlert("修改成功",'','success', {timer:2000});
                    turnPage('/k/');
                },
                error: function (json) {
                    sweetAlert("修改失败", '', 'error');
                    $('#table').css('display', 'none');
                    $('#docPanel').css('display', 'block');
                }
            });
    }
});


$("#dataName").blur(function () {
    var msg = '';
    var data_name = $('#dataName').val();
    msg = restful('get', '/api/twok/', {'dataName': data_name});
    if(msg.length > 0 && data_name.length != ''){
        $('#kv-error-1').css('display', 'block');
        $('#kv-error-1-li').text('该数据集已被存储，请更改！！！');
        msg = '';
    }else{
        $('#kv-error-1').css('display', 'none');
        $('#kv-error-1-li').text("");
    }
});

$('#editDoc').click(function () {
    if(typeof(temp) == "undefined"){
        sweetAlert("请选择编辑行", '', 'error');
    }
    else if (temp == 1) {
        var jsonObjectEdit = eval('(' + rowContent + ')');

        $('#dataName').val(jsonObjectEdit.dataName);
        $('#dataDescribe').val(jsonObjectEdit.description);
        $('#clusterNum').val(jsonObjectEdit.clusterNum);
        $('#table').css('display', 'none');

        $('#docPanel').css('display', 'block');

        $('#dataName').attr("disabled","disabled");
        $('#clusterNum').attr("disabled","disabled");
        $('#dataInputDiv').css('display', 'none');
        $('#dataEdit').css('display', 'block');
    }
    else {
        sweetAlert("请选择编辑行", '', 'error');
    }
});

$('#deleteDoc').click(function () {
    if (temp == 1) {
        var jsonObjectDelete = eval('(' + rowContent + ')');
        swal(
            {
                title: "Are you sure?",
                text: "Your will not be able to recover this data!",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Yes, delete it!",
                closeOnConfirm: false
            },
            function(isConfirm){
                if(isConfirm){
                    restful('post', '/cleanK/', {'id': jsonObjectDelete.kid});
                    $.ajax({
                        async: false,
                        type: 'delete',
                        url: "/api/twok/" + jsonObjectDelete.kid + "/",
                        success: function (json) {
                            swal("Deleted!", "Your data has been deleted.", "success");
                            turnPage('/k/');
                        }
                    })
                }else {     
                    swal("Cancelled", "Your imaginary file is safe :)", "error");  
                }
            }
        );
    }
    else {
        alert("请选择删除行");
    }
});

