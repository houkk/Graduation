/**
 * Created by mesogene on 16-5-13.
 */
var id = 0;
var classify = 'C4.5';
console.log(classify);
$('#indexTalbe').bootstrapTable({
    columns: [{
        field: 'state',
        checkbox: "true",
        align: 'center',
        valign: 'middle'
    }, {
        field: 'tree_id',
        formatter: 'nameFormatter',
        sortable: 'true',
        visible: false,
        title: 'Id编号',
        align: 'center',
        valign: 'middle'
    }, {
        field: 'tree_name',
        title: '数据集名称',
        align: 'center',
        valign: 'middle'
    }, {
        field: 'description',
        title: '描述',
        align: 'center',
        valign: 'middle'
    }, {
        field: 'file_status',
        title: '数据集状态',
        formatter: dataStatus,
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
        field: 'status',
        title: '决策树状态',
        formatter: treeStatus,
        align: 'center',
        valign: 'middle'
    }, {
        field: 'tree_path',
        // visible: false,
        title: '决策树TXT下载',
        formatter: operateTreeTxtDown,
        align: 'center',
        valign: 'middle'
    }, {
        field: 'png_path',
        // visible: false,
        title: '决策树ＰＮＧ下载',
        formatter: operateTreePngDown,
        align: 'center',
        valign: 'middle'
    }, {
        field: 'classify',
        // visible: false,
        title: '类别',
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
    url: "/api/tree/?classify="+classify,
    sidePagination: 'client'
}).on('uncheck.bs.table', function (e, row) {
    temp = 0;
}).on('check.bs.table', function (e, row) {
    temp = 1;
    rowContent = JSON.stringify(row);  //把json对象解析成string对象
});


function searchEvent(){
    var letter=$("#search").val();
    $("#indexTalbe").bootstrapTable('refresh',{url:"/api/tree/?classify=C4.5&&tree_name__contains="+letter});
}

function operateFormatter(value, row, index) {
    return [
        '<a title="下载" download href='+ value + '>',
        '<i class="am-icon-btn-sm am-primary am-icon-download am-icon-sm"></i>',
        '</a>'
    ].join('');
}

function operateTreeTxtDown(value, row, index) {
    return [
        '<a title="下载" download href='+ value + '>',
        '<i class="am-icon-btn-sm am-primary am-icon-download am-icon-sm"></i>',
        '</a>'
    ].join('');
}

function dataStatus(value, row, index) {
    if(value == true){
         return [
             '<span class="am-badge am-round am-badge-success am-text-sm">True</span>'
         ].join('');
    }else if(value == false){
         return [
              '<span class="am-badge am-round am-badge-danger am-text-sm">False</span>'
         ].join('');
    }
}

function treeStatus(value, row, index) {
    if(value == true){
         return [
             '<span class="am-badge am-round am-badge-success am-text-sm">True</span>'
         ].join('');
    }else if(value == false){
         return [
              '<span class="am-badge am-round am-badge-danger am-text-sm">False</span>'
         ].join('');
    }
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
    uploadUrl: "/tree_ID3/", // server upload action
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
            tree_name: $("#dataName").val(),
            description: $("#dataDescribe").val(),
            classify: classify
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

$('#cancel, #cancel2').click(function () {
    turnPage('/c4dot5/');
});

$('#create').click(function () {
    if ($("#dataDescribe").val() == "") {
        sweetAlert("请填写描述", '', 'error');
    }else{
        var jsonObjectEdit = eval('(' + rowContent + ')');
        var tree_id = jsonObjectEdit.tree_id;
        $.ajax({
                async:false,
                type: "patch",
                dataType: 'json',
                // contentType: 'application/json',
                data: {'description': $("#dataDescribe").val()},
                url: '/api/tree/'+tree_id+'/',
                success: function (data) {
                    // swal({
                    //     title:'修改成功',
                    //     type:'success',
                    //     timer:1000
                    // },function () {
                    //     turnPage('/a/');
                    // });
                    // // // sweetAlert("修改成功",'','success', {timer:2000});
                    turnPage('/c4dot5/');
                },
                error: function (json) {
                    sweetAlert("修改失败", '', 'error');
                    $('#table').css('display', 'none');
                    $('#docPanel').css('display', 'block');
                }
            });
    }
});

$('#create2').click(function () {
    var classify_data = [];
    var count = 0;
    $("#data3 :input").each(function () {
        count++;
        if($(this).val() == ''){
            sweetAlert("请填写完整", '', 'warning');
        }else{
            classify_data.push($(this).val());
        }
    });
    if(classify_data.length == count){
        var jsonObjectEdit = eval('(' + rowContent + ')');
        apply_data = {'file_path': jsonObjectEdit.file_path, 'tree_path': jsonObjectEdit.tree_path, 'data': classify_data};
        // result = restful('post', '/tree_classify/', apply_data);
        console.log(apply_data);
        $.ajax({
            async: false,
            type: 'post',
            url: '/tree_classify/',
            dataType: "json",
            // contentType:"application/json",
            data: apply_data,
            traditional: true,
            success: function (result) {
                console.log(result['result']);
                sweetAlert(result['label']+':'+result['result'], '', 'success');
            },
            error: function () {
                sweetAlert('输入错误，请重新输入！！！', '', 'error');
            }
        });
    }
});


$("#dataName").blur(function () {
    var msg = '';
    var data_name = $('#dataName').val();
    msg = restful('get', '/api/tree/', {'tree_name': data_name});
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

        $('#dataName').val(jsonObjectEdit.tree_name);
        $('#dataDescribe').val(jsonObjectEdit.description);
        $('#table').css('display', 'none');

        $('#docPanel').css('display', 'block');

        $('#dataName').attr("disabled","disabled");
        $('#dataInputDiv').css('display', 'none');
        $('#dataEdit').css('display', 'block');
    }
    else {
        sweetAlert("请选择编辑行", '', 'error');
    }
});

$('#applyTree').click(function () {
    if(typeof(temp) == "undefined"){
        sweetAlert("请选择编辑行", '', 'error');
    }
    else if (temp == 1) {
        var jsonObjectEdit = eval('(' + rowContent + ')');
        $('#table').css('display', 'none');
        $('#docPanel').css('display', 'block');

        $('#data1').css("display","none");
        $('#data2').css("display","none");
        $('#dataInputDiv').css('display', 'none');
        $('#dataEdit2').css('display', 'block');

        result = restful('get', '/tree_labels/', {'file_path': jsonObjectEdit.file_path});
        for(var value in result['labels']){
            $('#data3').append(
                '<div class="am-input-group am-input-group-secondary am-form-group">' +
                '<span class="am-input-group-label">'+result['labels'][value]+'</span>' +
                '<input required class="am-form-field" placeholder='+result['labels'][value]+'>' +
                '</div>'
            );
        }
    }
    else {
        sweetAlert("请选择编辑行", '', 'error');
    }
});

$('#deleteDoc').click(function () {
    if (temp == 1) {
        var jsonObjectDelete = eval('(' + rowContent + ')');
        //确认是否删除
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
                    restful('post', '/cleanTree/', {'id': jsonObjectDelete.tree_id});
                    $.ajax({
                        async: false,
                        type: 'delete',
                        url: "/api/tree/" + jsonObjectDelete.tree_id + "/",
                        success: function (json) {
                            swal("Deleted!", "Your data has been deleted.", "success");
                            turnPage('/c4dot5/');
                        }
                    });
                    
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
