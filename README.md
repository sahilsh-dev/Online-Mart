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

### Python Installation

1. Clone this repository to your local machine.
   
2. Navigate to the root directory of the project.

3. Create a virtual environment in python.

3. Install the required packages by running:

    ```bash
    $ pip install -r requirements.text
    ```
3. Create a `.env` file in the root directory of the project.

4. Add the following line to the `.env` file, replacing `YOUR_STRIPE_SECRET_KEY` with your actual Stripe secret key:

    ```
    STRIPE_SECRET_KEY=YOUR_STRIPE_SECRET_KEY
    ```
    
5. Run the following command to start the application:

    ```bash
    $ flask run
    ```

### Docker Installation

1. Make sure you have Docker installed on your machine. If not, you can download and install it from [https://www.docker.com/get-started](https://www.docker.com/get-started).

2. Clone this repository to your local machine.

3. Navigate to the root directory of the project where the Dockerfile is located and add a .env file for storing STRIPE_SECRET_KEY.

4. Build the Docker image by running the following command:

    ```bash
    $ docker build -t homey-app .
    ```

5. Once the image is built, you can run the Docker container using the following command:

    ```bash
    $ docker run -p 5000:5000 homey-app
    ```

Access the application by opening your web browser and navigating to [http://localhost:5000](http://localhost:5000).

## Usage for Other Projects

You can use this project as a template or reference for building your own e-commerce website. Here's how you can adapt it for your needs:

- Customize the product catalog and categories to fit your product offerings.
- Integrate other payment gateways or shipping APIs to expand the payment available.
- Implement additional features such as product reviews or better product recommendation

## Future Todos

- [ ] Make about us and contact us pages.
- [ ] Implement Pagination.
- [ ] Make the application responsive for mobile devices.
- [ ] Implement user reviews and ratings for products.
- [ ] Optimize the application for performance and scalability.


## Contributing

Contributions are super welcome! If you find any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.

Thank you for choosing Homey - Your Online Home Goods Store! Happy shopping! 🏠🛍️
