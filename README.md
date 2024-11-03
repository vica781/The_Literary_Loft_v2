# The Literary Loft

![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

The Literary Loft is an e-commerce platform designed for book lovers to explore and purchase a curated selection of books. This platform aims to provide an intuitive, user-friendly experience that allows users to browse, search, and buy books seamlessly. The Literary Loft is designed to serve both casual readers and avid book collectors by offering a variety of genres and popular titles.

This project was created as part of my final project with Code Institute and is intended for educational purposes only.

[View the live project here.](https://the-literary-loft-a4b6116b3a17.herokuapp.com/)

![Mockup](readme_files/images/am_i_responsive.png)

## Table of Contents

- [Project Purpose and Objectives](#project-purpose-and-objectives)
- [User Experience (UX)](#user-experience-ux)
  - [Project Goals](#project-goals)
  - [User Stories](#user-stories)
    - [External User Goals](#epic-1-user-management)
    - [Admin User Goals](#admin-user-goals)
- [Features](#features)
  - [Existing Features](#existing-features)
  - [Features to Implement in the Future](#features-to-implement-in-the-future)
- [Design](#design)
  - [Wireframes](#wireframes)
  - [Color Scheme and Typography](#color-scheme-and-typography)
- [Technologies Used](#technologies-used)
- [Testing](#testing)
  - [Manual Testing](#manual-testing)
  - [Validator Testing](#validator-testing)
- [Deployment](#deployment)
- [Credits](#credits)


## Project Purpose and Objectives

The primary goal of The Literary Loft is to simulate a real-world e-commerce application where users can:

- Browse a catalog of books with details and descriptions.
- Search and filter books by title, author, genre, or category.
- Add books to a shopping cart and complete a secure checkout.
- Purchase books either as a guest or as a registered user. While guest users can make purchases, they are encouraged throughout the process to sign in or register, as only registered users can experience the full benefits of the platform, including:
  - Access to order history for easy reference and reorders.
  - The ability to mark books as favorites for quick access.
  - The option to manage their personal account details and saved preferences.
- Subscribe to a newsletter to stay updated with the latest additions and promotions on The Literary Loft.

The project also aims to give site administrators full control over the inventory, enabling them to add, update, or remove books from the catalog without the need for a separate admin panel.

## Disclaimer

**Note**: This project was developed solely for educational purposes and is not intended for real-world use.

## User Experience (UX)

### Project Goals

The main objective of *The Literary Loft* is to create an engaging and seamless e-commerce experience where users can browse, select, and purchase books from a diverse catalog. The platform is designed to cater to both casual readers and dedicated book enthusiasts by offering an intuitive interface, comprehensive user interaction, and personalized account features.

### Strategy

The strategy for *The Literary Loft* focuses on building a user-centric experience that encourages engagement and repeat visits. Key strategies include:

- Ensuring ease of navigation and the ability to search, filter, and browse through books effortlessly.
- Providing an efficient and secure checkout process for both guest users and registered users.
- Encouraging users to sign up and log in to benefit from enhanced features, such as viewing their full order history and managing their favorite books.
- Integrating a newsletter signup feature to keep users informed about new releases and special promotions.
- Incorporating SEO best practices to improve discoverability and audience reach.

### User Stories

#### EPIC 1: User Management

1. **Register for an Account**
   - *Description*: As a Site User, I want to easily register for an account, so that I can have a personal account and be able to view my profile.
   - *Acceptance Criteria*:
     - User can access a registration page.
     - User can fill out a registration form with necessary details.
     - User receives a confirmation email after successful registration.
   - *Tasks*:
     - Create a registration form.
     - Implement form validation.
     - Set up email confirmation for new registrations.

2. **Login or Logout**
   - *Description*: As a Site User, I want to easily login or logout, so that I can access my personal account information.
   - *Acceptance Criteria*:
     - User can access a login page.
     - User can enter credentials to log in.
     - User can easily log out from their account.
   - *Tasks*:
     - Create a login form.
     - Implement login and logout functionality.
     - Ensure session management for logged-in users.

3. **Password Recovery**
   - *Description*: As a Site User, I want to easily recover my password in case I forget it, so that I can recover access to my account.
   - *Acceptance Criteria*:
     - User can request password recovery.
     - User receives a password recovery email.
     - User can reset their password using the link provided.
   - *Tasks*:
     - Create a password recovery form.
     - Set up email functionality for password recovery.
     - Implement password reset functionality.

4. **Email Confirmation**
   - *Description*: As a Site User, I want to receive an email confirmation after registering, so that I can verify that my account registration was successful.
   - *Acceptance Criteria*:
     - User receives an email upon successful registration.
     - Email contains a link to verify the account.
     - Verification link confirms the user account.
   - *Tasks*:
     - Implement email sending functionality for registration.
     - Create verification link handling.
     - Ensure user account activation upon verification.

5. **Manage User Profile**
   - *Description*: As a Site User, I want to manage my user profile, so that I can update my personal information and preferences.
   - *Acceptance Criteria*:
     - User can view their profile page.
     - User can edit and update personal details.
     - Changes to user profile are saved and reflected in the database.
   - *Tasks*:
     - Create a user profile management interface.
     - Implement profile editing and saving functionality.
     - Ensure database updates upon profile changes.

6. **Manage Account Deletion**
   - *Description*: As a Site User, I want to be able to delete my account, so that I can permanently remove my data from the platform.
   - *Acceptance Criteria*:
     - User can access an option to delete their account.
     - User receives a confirmation prompt before deletion.
     - Account is deleted from the database upon confirmation.
   - *Tasks*:
     - Create a delete account option in the user profile.
     - Implement a confirmation prompt for account deletion.
     - Ensure the account is removed from the database upon confirmation.

#### EPIC 2: Product Management

1. **Add a Product**
   - *Description*: As a Store Owner, I want to add a product, so that I can add new items to my store.
   - *Acceptance Criteria*:
     - Admin can access a product addition page.
     - Admin can fill out a form with product details such as name, price, description, and image.
     - Admin can submit the form to add the product to the store.
   - *Tasks*:
     - Create a product addition form.
     - Implement form validation.
     - Ensure the product is added to the database and displayed in the store.

2. **Edit/Update a Product**
   - *Description*: As a Store Owner, I want to edit/update a product, so that I can change product prices, descriptions, images, and other product criteria.
   - *Acceptance Criteria*:
     - Admin can access a product editing page.
     - Admin can edit existing product details.
     - Admin can submit the form to update the product information.
   - *Tasks*:
     - Create a product editing form.
     - Implement form validation.
     - Ensure the updated product details are saved in the database.

3. **Delete a Product**
   - *Description*: As a Store Owner, I want to delete a product, so that I can remove items that are no longer for sale.
   - *Acceptance Criteria*:
     - Admin can access a list of products.
     - Admin can select a product to delete.
     - Admin receives a confirmation prompt before deletion.
     - The product is removed from the store upon confirmation.
   - *Tasks*:
     - Create a product deletion interface.
     - Implement a confirmation prompt for deletions.
     - Ensure the product is removed from the database and the store.

4. **View Product Details**
   - *Description*: As a Site User, I want to view detailed information about a product, so that I can make informed purchasing decisions.
   - *Acceptance Criteria*:
     - User can click on a product to view its details.
     - Product details page shows name, price, description, and images.
     - Additional information like stock availability and reviews is displayed.
   - *Tasks*:
     - Create a product details page.
     - Display product information dynamically from the database.
     - Ensure reviews and ratings are visible (if applicable).

5. **Filter and Sort Products by Category and Subcategory**
   - *Description*: As a Site User, I want to filter and sort products by category and subcategory, so that I can find items that match my interests and preferences.
   - *Acceptance Criteria*:
     - User can filter products based on main categories and subcategories.
     - User can sort products by price, rating, or popularity.
     - Filtered and sorted results are displayed dynamically.
   - *Tasks*:
     - Create filtering and sorting logic.
     - Integrate with the product listing page.
     - Implement UI elements for filter and sort options.

#### EPIC 3: Checkout Process

1. **Add to Bag**
   - *Description*: As a Site User, I want to add products to a shopping bag, so that I can purchase them later.
   - *Acceptance Criteria*:
     - User can add products to their shopping bag.
     - Shopping bag displays added items and total cost.
     - User can continue browsing after adding items to the bag.
   - *Tasks*:
     - Create add to bag functionality.
     - Display bag contents dynamically.
     - Implement a notification system for successful additions.

2. **Review and Edit Bag**
   - *Description*: As a Site User, I want to review and edit my shopping bag, so that I can update quantities or remove items before checkout.
   - *Acceptance Criteria*:
     - User can view their shopping bag.
     - User can update item quantities or remove items.
     - Updated totals are displayed dynamically.
   - *Tasks*:
     - Create a shopping bag review page.
     - Implement editing functionalities for item quantities.
     - Ensure the bag updates in real-time.

3. **Complete Checkout with Payment**
   - *Description*: As a Site User, I want to complete a secure checkout process, so that I can purchase the items in my shopping bag.
   - *Acceptance Criteria*:
     - User can access a checkout page with items, totals, and payment options.
     - User can input payment details and submit for payment.
     - User receives a confirmation of purchase after successful payment.
   - *Tasks*:
     - Create a checkout page.
     - Integrate payment processing (e.g., Stripe).
     - Ensure the user receives feedback on payment status.

4. **Order Confirmation**
   - *Description*: As a Site User, I want to receive an order confirmation, so that I know my purchase was successful.
   - *Acceptance Criteria*:
     - User receives a confirmation message on the site after checkout.
     - Confirmation email is sent with order details.
   - *Tasks*:
     - Implement on-site confirmation message.
     - Set up confirmation email template.
     - Ensure order details are displayed correctly.

5. **Guest Checkout Option**
   - *Description*: As a Site Visitor, I want to make a purchase without registering, so that I can complete an order quickly.
   - *Acceptance Criteria*:
     - Guest users can proceed to checkout without an account.
     - Guest users are encouraged to register or sign in for benefits (e.g., order history).
     - Guest user data is handled securely for checkout.
   - *Tasks*:
     - Enable guest checkout feature.
     - Implement prompts for user registration benefits.
     - Secure guest data during the process.

#### EPIC 4: SEO and Marketing

1. **Implement Meta Tags**
   - *Description*: As a Site Owner, I want to include meta tags on my website, so that it improves SEO and helps with search engine visibility.
   - *Acceptance Criteria*:
     - All pages have meta tags that reflect page content.
     - Meta tags include descriptions, keywords, and author information.
   - *Tasks*:
     - Add meta tags to all main pages.
     - Ensure descriptions and keywords are relevant.
     - Test SEO improvements using validation tools.

2. **Create and Add Sitemap.xml**
   - *Description*: As a Site Owner, I want to create and add a sitemap.xml file, so that search engines can easily crawl my site.
   - *Acceptance Criteria*:
     - A valid sitemap.xml file is present.
     - Sitemap includes links to all pages.
   - *Tasks*:
     - Generate sitemap.xml.
     - Add sitemap.xml to the root directory.
     - Test sitemap with search engine tools.

3. **Add robots.txt**
   - *Description*: As a Site Owner, I want to add a robots.txt file, so that I can control which pages are crawled by search engines.
   - *Acceptance Criteria*:
     - A valid robots.txt file is present.
     - Instructions in robots.txt prevent unwanted pages from being indexed.
   - *Tasks*:
     - Create robots.txt file.
     - Add specific instructions for search engines.
     - Test the file using online tools.

4. **Newsletter Signup Functionality**
   - *Description*: As a Site Owner, I want to add a newsletter signup form, so that I can collect emails for marketing purposes.
   - *Acceptance Criteria*:
     - Users can enter their email to subscribe to the newsletter.
     - Form validates emails and provides success feedback.
     - Data is stored securely for future use.
   - *Tasks*:
     - Create newsletter signup form.
     - Implement email validation.
     - Store email data securely.

5. **Create Facebook Business Page**
   - *Description*: As a Site Owner, I want to create a Facebook Business Page, so that I can increase brand reach and engage with users on social media.
   - *Acceptance Criteria*:
     - Facebook Business Page is set up with appropriate branding.
     - Page includes links to the site and basic business information.
   - *Tasks*:
     - Create Facebook Business Page.
     - Add branding elements (logo, cover photo).
     - Include links and business details.

#### EPIC 5: Site Management & Security

1. **Secure Payment Integration (e.g., Stripe)**
   - *Description*: As a Site Owner, I want to securely integrate payment processing, so that users can make payments safely.
   - *Acceptance Criteria*:
     - Payment processing is securely integrated using Stripe or another service.
     - User data is protected during the transaction.
     - Site shows clear feedback for payment success/failure.
   - *Tasks*:
     - Integrate payment service (e.g., Stripe).
     - Ensure secure data handling.
     - Test payment process for security and functionality.

2. **Role-Based Access Control**
   - *Description*: As a Site Owner, I want to implement role-based access control, so that only authorized users can access certain parts of the site.
   - *Acceptance Criteria*:
     - Admins have access to management pages.
     - Regular users can only access public content.
     - Unauthorized access attempts are blocked.
   - *Tasks*:
     - Implement role-based access control.
     - Secure admin routes.
     - Test user roles for proper access.

3. **Set Up Environment Variables for Security**
   - *Description*: As a Developer, I want to use environment variables, so that sensitive data is not exposed in the code.
   - *Acceptance Criteria*:
     - Environment variables are used for API keys, secret keys, etc.
     - Variables are properly hidden in the .env file and not pushed to the repository.
   - *Tasks*:
     - Set up environment variables in the project.
     - Hide .env file using .gitignore.
     - Ensure sensitive data is not exposed.

4. **Debug Mode Off for Deployment**
   - *Description*: As a Developer, I want to turn off debug mode for deployment, so that the site is secure and users don’t see detailed error information.
   - *Acceptance Criteria*:
     - DEBUG mode is turned off in the deployment settings.
     - Site handles errors gracefully without revealing details.
   - *Tasks*:
     - Ensure debug mode is turned off in the production environment.
     - Test error handling.
     - Confirm site functionality without debug mode.

#### EPIC 6: Testing & Deployment

1. **Unit Testing for User Forms**
   - *Description*: As a Developer, I want to perform unit testing for user forms, so that I can ensure the form functionality works as intended.
   - *Acceptance Criteria*:
     - User forms are tested for input validation.
     - Form submission behavior is verified.
   - *Tasks*:
     - Write test cases for user forms.
     - Ensure test coverage includes form validation.
     - Verify form submissions with test data.

2. **Integration Testing for Checkout**
   - *Description*: As a Developer, I want to perform integration testing for the checkout process, so that I can ensure all components work together seamlessly.
   - *Acceptance Criteria*:
     - Test covers adding items to the cart, reviewing the cart, and completing payment.
     - Edge cases such as empty carts or invalid payment data are tested.
   - *Tasks*:
     - Write integration tests for the checkout process.
     - Test with different scenarios (e.g., guest user, registered user).
     - Validate successful payment and order confirmation.

3. **Validation Testing (HTML, CSS, JS, Python)**
   - *Description*: As a Developer, I want to validate my code, so that I can ensure it meets standards and has no critical issues.
   - *Acceptance Criteria*:
     - Code passes validation checks for HTML, CSS, JS, and Python.
     - Code adheres to PEP8 for Python and linting rules for JavaScript.
   - *Tasks*:
     - Run code through validation tools.
     - Fix any issues identified in the validation report.
     - Re-run validation to confirm issues are resolved.

4. **User Acceptance Testing**
   - *Description*: As a Site Owner, I want to perform user acceptance testing, so that I can ensure the project meets user needs and requirements.
   - *Acceptance Criteria*:
     - Users provide feedback after testing.
     - Any critical issues found during testing are addressed.
   - *Tasks*:
     - Create user testing plan.
     - Collect feedback from test users.
     - Address any major issues discovered.

5. **Bug Fixes and Iterations**
   - *Description*: As a Developer, I want to address bugs and iterate on feedback, so that I can improve the application before final deployment.
   - *Acceptance Criteria*:
     - All major bugs are fixed.
     - Iterations are made based on feedback.
   - *Tasks*:
     - Track bugs found during testing.
     - Implement fixes and test the resolution.
     - Make iterations based on user feedback.

### Wireframes

Wireframes were created at the start of the project to visualize the structure and layout of the key pages, including:

- **Homepage**: A welcoming page with featured books, new arrivals, and a search bar.
- **Product Listing Page**: Displays books in a grid layout with filters and sorting options.
- **Product Detail Page**: Detailed view of each book with options to add to the cart or save as a favorite.
- **Shopping Cart Page**: An overview of the selected books with options to edit quantities or remove items.
- **Checkout Page**: A form-based page to input delivery and payment details securely.
- **User Profile Page**: Allows users to view and manage their account information, past orders, and favorite books.
- **Admin Dashboard**: Provides functionality for adding, updating, and managing products.

These wireframes served as a blueprint for the development and ensured that the final design aligned with the project's goals and user needs.
