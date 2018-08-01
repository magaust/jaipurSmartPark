// src: https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
// dynamic dropdown
$("#id_parkinglot").change(function () {
    var url = $("#TicketForm").attr("data-parkingspaces-url");  // get the url of the `load_cities` view
    var parkinglotId = $(this).val();  // get the selected country ID from the HTML input
  // Missin: IF parkinglotID = None -> show standalone parkingticket
    $.ajax({                       // initialize an AJAX request
      url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
      data: {
        'parkinglot': parkinglotId       // add the country id to the GET parameters
      },
      success: function (data) {   // `data` is the return of the `load_cities` view function
        $("#id_parkingspace").html(data);  // replace the contents of the city input with the data that came from the server
      }
    });

  });

  $("#id_parkingspace").change(function() {
      var url = $("#TicketForm").attr("data-vehicles-url");
      var parkingspaceId = $(this).val();
      
      $.ajax({                       
      url: url,                    
      data: {
        'parkingspace': parkingspaceId 
      },
      success: function (data) {   
        $("#id_vehicle").html(data);
      }
    });

  })