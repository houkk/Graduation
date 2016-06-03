/**
 * Created by mesogene on 16-5-7.
 */
/* 点击切换中间content */
function turnPage(res) {    //url:请求的url  res：存放网页的地址，使用相对地址，django会在自动搜索app的templates文件夹，子目录要自己写  url和res参数格式是 String
    $.ajax({
        type: "get",
        url: res,
        cache: false,
        dateType: "html",
        data: {area: res},
        success: function (html) {
            $('#content').empty();    //首先清空centent区
            $('#content').html(html);  //把下载的html文件添加到centent区中
        },
        error: function () {
            $('#content').empty();
            $('#content').html('<p>出了一些差错，请耐心等待修复：）</p>');
        }
    });
}

function restful(typeInfo, urlInfo, dataInfo) {
    /**typeInfo:操作类型；
     * urlInfo:地址；
     * dataInfo:json数据；
     * 操作类型：
     * get：获取（dataInfo为空时，查询所有；dataInfo不为空，条件查询）；
     * 查询(数据分页，暂时每页是十条数据，可后台更改)
     * post：上传；
     * put：更新(按照id)；
     * delete：删除数据（id）；
     * */

    var result = null;
    $.ajax({
        async: false,
        type: typeInfo,
        url: urlInfo,
        dataType: "json",
        //contentType:"application/json",
        data: dataInfo,
        // traditional: true,
        success: function (json) {
            result = json;
        },
        error: function () {
            result = "fail";
        }
    });
    return result;
}

