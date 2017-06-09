<%@ page contentType="text/html;charset=UTF-8" language="java" pageEncoding="UTF-8" %>
<%@include file="common/tag.jsp" %>
<!DOCTYPE html>
<html>
<head>
    <title>列表页</title>
    <%@include file="common/head.jsp" %>
</head>
<body>
<div class="container">
    <div class="panel panel-default">
        <div class="panel-heading text-center">
            <h2>列表</h2>
        </div>
        <div class="panel-body">
            <table class="table table-hover">
                <thead>
                <tr>
                    <th>名称</th>
                    <th>库存</th>
                    
                    <th>详情页</th>
                    <th>预定</th>
                </tr>
                </thead>
                <tbody>
                <c:forEach var="sk" items="${list}">
                    <tr>
                        <td>${sk.name},${sk.bookId}</td>
                        <td>${sk.number}</td>
                        
                        <td>
                            <a class="btn btn-info" href="/ssm-simple/book/${sk.bookId}/detail" target="_blank">详情</a>
                        </td>
                        <td>
                            <button id="appoint_btn" type="button" class="btn btn-success" onclick="reserve('${sk.bookId}')">预定</button>
                        </td>
                    </tr>
                </c:forEach>
                </tbody>
            </table>
        </div>
    </div>

</div>
<!-- jQuery文件。务必在bootstrap.min.js 之前引入 -->

<script src="http://apps.bdimg.com/libs/jquery/2.0.0/jquery.min.js"></script>
<!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
<script src="http://apps.bdimg.com/libs/bootstrap/3.3.0/js/bootstrap.min.js"></script>
<script type="text/javascript">
  $(function () {
	  
    });
 function reserve(i){
	 
	 $.post("/ssm-simple/book/"+i+"/appoint",{
			studentId:123			
		},
		function(data,status){
	        alert("数据: \n" + data.success + "\n状态: " + status);
	    }
		);
 }
</script>
</body>
</html>