
/* global $, window */

$(function () {
    'use strict';
    
    $("#rotateBtn").click(function(e) {
    
        $('#filemergeupload').addClass('fileupload-processing');
        var url = "rotate"; // the script where you handle the form input.
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

    $("#translateBtn").click(function(e) {
    
        $('#filemergeupload').addClass('fileupload-processing');
        var url = "translate"; // the script where you handle the form input.
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
