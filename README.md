# Homey - Your online store for all home items

Welcome to Homey - your ultimate destination for purchasing home items online, leveraging Flask, SQLAlchemy, Bootstrap, and HTMX to deliver an efficient e-commerce solution.
<br>
<br>
![image](https://github.com/Sam6900/Online-Mart/assets/85671637/47c629fe-7c79-4d20-8e37-3d601bb77d63)

## Features:

- **User Authentication:** Secure sign-up, login, and logout functionalities.
- **Product Catalog:** Explore and purchase various home items and categories effortlessly.
- **Shopping Cart:** Add items, manage quantities, and proceed to checkout seamlessly.
- **Order Management:** Track order history and manage account details with ease.
- **Stripe Payments:** Secure integration with Stripe for smooth transactions.
- **htmx Integration:** Enhances user experience with dynamic HTML content updates.

## Installation

1. Clone this repository to your local machine.
   
2. Navigate to the root directory of the project.

3. Create a virtual environment in python.

3. Install the required packages by running:

    ```bash
    pip install -r requirements.text
    ```

4. Set up your Stripe API keys in envrionment variable or create a .env file to store the key to enable payment processing.

5. Run the following command to start the application:

    ```bash
    flask run
    ```

6. Access the application by opening your web browser and navigating to [http://localhost:5000](http://localhost:5000).

## Usage for Other Projects

You can use this project as a template or reference for building your own e-commerce website. Here's how you can adapt it for your needs:

- Customize the product catalog and categories to fit your product offerings.
- Extend the user authentication system to include additional features such as social login or two-factor authentication.
- Integrate other payment gateways or shipping APIs to expand the payment and shipping options available to your customers.
- Implement additional features such as product reviews, better product recommendation or live chat support to enhance the shopping experience.

## Future Todos

- [ ] Implement user reviews and ratings for products.
- [ ] Add support for multiple languages and currencies.
- [ ] Enhance the admin panel with more advanced product and order management features.
- [ ] Optimize the application for performance and scalability to handle a larger number of users and transactions.
- [ ] Integrate with third-party analytics tools to gain insights into user behavior and sales performance.

## Contributing

Contributions are super welcome! If you find any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.

Thank you for choosing Homey - Your Online Home Goods Store! Happy shopping! 🏠🛍️
