/*!
* Start Bootstrap - Blog Post v5.0.9 (https://startbootstrap.com/template/blog-post)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-blog-post/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project
document.getElementById("button-search").addEventListener("click", function() {
    // GET 또는 INPUT값을 통해서 받아야함
    var searchTerm = document.getElementById("searchInput").value;
    // 특정 검색어가 넣어야 동작
    if (searchTerm === "만약예 예를 들면 DB를 조회한다던가") {
        // 예시 -> 수정하셈  document.getElementById("elementId").style.color = "red";
    } else {
        // 예시 -> 수정하셈 document.getElementById("elementId").style.color = "black";
    }
});