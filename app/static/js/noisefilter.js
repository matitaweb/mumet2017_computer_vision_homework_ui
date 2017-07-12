
/* global $, window */

$(function () {
    'use strict';
    
    $("#medianFilterBtn").click(function(e) {
    
        $('#filemergeupload').addClass('fileupload-processing');
        var url = "medianfilter"; // the script where you handle the form input.
        $("#merged_result").empty();
        callAjax(url)
    
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });
    
    $("#meanFilterBtn").click(function(e) {
    
        $('#filemergeupload').addClass('fileupload-processing');
        var url = "meanfilter"; // the script where you handle the form input.
        $("#merged_result").empty();
        callAjax(url)
    
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });
    
    $("#gaussianFilterBtn").click(function(e) {
    
        $('#filemergeupload').addClass('fileupload-processing');
        var url = "gaussianFilter"; // the script where you handle the form input.
        $("#merged_result").empty();
        callAjax(url)
    
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });
    
    $("#bilateralFilterBtn").click(function(e) {
    
        $('#filemergeupload').addClass('fileupload-processing');
        var url = "bilateralFilter"; // the script where you handle the form input.
        $("#merged_result").empty();
        callAjax(url)
    
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });
    
    $("#otsuFilterBtn").click(function(e) {
    
        $('#filemergeupload').addClass('fileupload-processing');
        var url = "otsuFilter"; // the script where you handle the form input.
        $("#merged_result").empty();
        callAjax(url)
    
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });
    
    
    $("#adaptiveGaussianFilterBtn").click(function(e) {
    
        $('#filemergeupload').addClass('fileupload-processing');
        var url = "adaptiveGaussianFilter"; // the script where you handle the form input.
        $("#merged_result").empty();
        callAjax(url)
    
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });
    
    
    function callAjax(url){
        $.ajax({
           type: "POST",
           url: url,
           data: $("#filemergeupload").serialize(), // serializes the form's elements.
           success: function(data)
           {
               var dataJson = JSON.parse(data);
               console.log(dataJson)
               if(dataJson.result == '0') {
                    $('#merged_result').html('<p><b>' + dataJson.msg + '</b></p>'); 
               } else {
                $('#merged_result').html('<img width="800px" src="' + dataJson.imgPath + '" />');
               }
               $("#filemergeupload").removeClass('fileupload-processing');
           }
         });
    }

});
