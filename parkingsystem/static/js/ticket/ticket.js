var now = new Date();
console.log(now);


var year, month, day, hour, minute;
var valid_to_date, price, minutes;
var price_html = document.getElementById("ticket-price");

var parkinglot = document.getElementById("id_parkinglot");
parkinglot.required = false;

var valid_to = document.getElementById("id_valid_to");
function timeCalculator() {
    year = valid_to.value.slice(0,4);
    month = valid_to.value.slice(5,7);
    month = (parseInt(month)-1).toString();
    day = valid_to.value.slice(8,10);
    hour = valid_to.value.slice(11,13);
    minute = valid_to.value.slice(14,16);

    if((!isNaN(year)) && (!isNaN(month)) && (!isNaN(day))) {
        valid_to_date = new Date(year,month,day, hour, minute);
        if(valid_to_date > now) {
            minutes=parseInt((valid_to_date-now)/60000);
            price = (price*minutes);
            console.log("pris: " + price);
        }
    } ;
}

valid_to.setAttribute("onchange", 'timeCalculator()');

$("#id_parkinglot").change(function() {
    var url = $("#TicketForm").attr("data-parkinglot-price-url");
    var parkinglotId = $(this).val();
    
    $.ajax({                       
    url: url,
    data: {
      'parkinglot': parkinglotId 
    },
    success: function (data) {
        price = parseInt(data['price']);
        price_html.innerHTML = price + " INR";
    }
  });

})

$("#id_parkingspace").change(function() {
    var url = $("#TicketForm").attr("data-parkingspace-price-url");
    var parkingspaceId = $(this).val();
    
    $.ajax({                       
    url: url,
    data: {
      'parkingspace': parkingspaceId 
    },
    success: function (data) {
        price = parseInt(data['price']);
        price_html.innerHTML = price + " INR";
    }
  });

})