
/* global $, window */

$(function () {
    'use strict';
    
    $("#merge2img").click(function(e) {
    
        $('#filemergeupload').addClass('fileupload-processing');
        var url = "stitch"; // the script where you handle the form input.
        $("#merged_result").empty();
        $.ajax({
               type: "POST",
               url: url,
               data: $("#filemergeupload").serialize(), // serializes the form's elements.
               success: function(data)
               {
                   var dataJson = JSON.parse(data);
                   if(dataJson.result == '0') {
                        $('#merged_result').html('<p><b>' + dataJson.msg + '</b></p>'); 
                   } else {
                    $('#merged_result').html('<img src="' + dataJson.imgPath + '" />');
                   }
                   $("#filemergeupload").removeClass('fileupload-processing');
               }
             });
    
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });

    $("#threshold_btn").click(function(e) {
    
        $('#filemergeupload').addClass('fileupload-processing');
        var url = "threshold"; // the script where you handle the form input.
        $("#merged_result").empty();
        $.ajax({
               type: "POST",
               url: url,
               data: $("#filemergeupload").serialize(), // serializes the form's elements.
               success: function(data)
               {
                   var dataJson = JSON.parse(data);
                   if(dataJson.result == '0') {
                        $('#merged_result').html('<p><b>' + dataJson.msg + '</b></p>'); 
                   } else {
                    $('#merged_result').html('<img src="' + dataJson.imgPath + '" />');
                   }
                   $("#filemergeupload").removeClass('fileupload-processing');
               }
             });
    
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });

});
