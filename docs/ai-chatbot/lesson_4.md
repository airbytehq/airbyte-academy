## Configure Stripe

<a href="https://dashboard.stripe.com/test/dashboard" target="_blank">Log into the  Stripe account</a> that you create earlier. make sure that you see the orange Test mode banner at the top. This means you are working with test data and no payment processing will occur. If you do not see this, please click the test mode toggle on the upper right. 

Once you have your Stripe environment in Test mode, tap Developers in the lower left, then select API keys. Copy the Secret key. You will need this in the next step.
![CleanShot 2025-01-14 at 10.06.45@2x](https://hackmd.io/_uploads/rJECw7Ewke.png)


### Load Test Data

A chatbot is pretty boring without data. We will be retrieving data from Stripe for products, customers, and purchases. To save some time, we have created a  <a href="https://colab.research.google.com/drive/1hozY9eZ3g37NtBwBU1hDVujfJtfrpW-5?usp=sharing//" target="_blank">python script</a> to load test data. From within, the Colab notebook. You will see 3 steps in the collab notebook: 
1. Add a secret key (tap on the key icon on the left) ``STRIPE_TEST_KEY`` and use the value from the previous section. 
1. Install the Stripe library
1. Run the script to create and insert test data.
![CleanShot 2025-01-14 at 10.08.32@2x](https://hackmd.io/_uploads/BypNumNDJl.png)

When you run the script, watch for the debug output. Ensure that you see a line which says *Sample data creation complete.* 

