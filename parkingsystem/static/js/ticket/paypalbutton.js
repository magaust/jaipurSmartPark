var form = document.getElementById("TicketForm");
print(price)


paypal.Button.render({
    // Configure environment
    env: 'sandbox',
    client: {
      sandbox: 'demo_sandbox_client_id',
    },
    // Customize button (optional)
    locale: 'en_GB',
    style: {
      size: 'small',
      color: 'gold',
      shape: 'pill',
    },
    // Set up a payment
    payment: function (data, actions) {
      return actions.payment.create({
        transactions: [{
          amount: {
            total: price.toString(),
            currency: 'USD'
          }
        }]
      });
    },
    // Execute the payment
    onAuthorize: function (data, actions) {
      return actions.payment.execute()
        .then(function () {
          // Show a confirmation message to the buyer
          form.submit();
        });
    }
  }, '#paypal-button');