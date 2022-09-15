$(document).ready(()=>{
    const countryForm = $('#country-form'),
        stateForm = $('#state-form')

    $.ajax({
        url: 'https://api.countrystatecity.in/v1/countries',
        method: 'GET',
        headers: {
            'X-CSCAPI-KEY': 'API_KEY'
          },
        success: function(data){
            console.log(data);
        }
    });


    var settings = {
        "url": "https://api.countrystatecity.in/v1/countries",
        "method": "GET",
        "headers": {
          "X-CSCAPI-KEY": "API_KEY"
        },
      };
      
      $.ajax(settings).done(function (response) {
        console.log(response);
      });


})