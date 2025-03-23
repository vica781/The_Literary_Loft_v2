# Testing

To return to main documentation of 'The Literary Loft' project click here [README.md](README.md).

This contains the testing details for the project 'The Literary Loft'.

## Table of Contents

## User Stories Testing

### Overview

This document details the testing procedures and results for each user story implemented in 'The Literary Loft' project. Each user story has been systematically tested to ensure all acceptance criteria are met and the functionality works as intended.

## EPIC 1: User Management

### 1. Register for an Account

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Access registration page | Navigate to homepage and click "Register" | Registration page loads with form | Registration page loaded successfully | ✅ PASS |
| Complete registration form | Fill in username, email, password and click "Sign Up" | Form submits successfully | Form submitted successfully | ✅ PASS |
| Form validation | Submit form with invalid data (e.g., mismatched passwords) | Form shows appropriate error messages | Error messages displayed correctly | ✅ PASS |
| Email confirmation | Check email after registration | Confirmation email received with verification link | Confirmation email received | ✅ PASS |
| Account verification | Click verification link in email | Account verified and user redirected to login page | Account verified successfully | ✅ PASS |

### 2. Login or Logout

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Access login page | Click "Login" from navigation menu | Login page loads with form | Login page loaded successfully | ✅ PASS |
| Successful login | Enter valid credentials and click "Login" | User logged in and redirected to homepage | Login successful | ✅ PASS |
| Failed login | Enter invalid credentials and click "Login" | Error message displayed | Error message shown correctly | ✅ PASS |
| Logout functionality | Click "Logout" from navigation menu | User logged out and redirected to homepage | Logout successful | ✅ PASS |
| Session persistence | Login and close/reopen browser | User remains logged in | Session maintained correctly | ✅ PASS |

### 3. Password Recovery

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Access password recovery | Click "Forgot Password" on login page | Password recovery page loads | Recovery page loaded successfully | ✅ PASS |
| Request password reset | Enter email address and submit | Confirmation message displayed | Confirmation shown | ✅ PASS |
| Password reset email | Check email for reset link | Password reset email received | Email received with reset link | ✅ PASS |
| Password reset form | Click reset link and enter new password | Form accepts new password | New password saved successfully | ✅ PASS |
| Login with new password | Attempt login with new password | Login successful | Login with new password worked | ✅ PASS |

### 4. Email Confirmation

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Email delivery | Register new account | Confirmation email delivered | Email delivered promptly | ✅ PASS |
| Email content | Open confirmation email | Email contains verification link | Link present and clearly visible | ✅ PASS |
| Verification process | Click verification link | Account verified with success message | Account verified successfully | ✅ PASS |
| Attempt login before verification | Try to login before verifying | Message indicating verification needed | Appropriate message displayed | ✅ PASS |

### 5. Manage User Profile

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Access profile page | Login and click "My Profile" | Profile page loads with user information | Profile page loaded successfully | ✅ PASS |
| Update profile information | Edit profile details and save | Changes saved and confirmation shown | Profile updated successfully | ✅ PASS |
| Profile image upload | Upload profile image | Image uploaded and displayed | Image uploaded correctly | ✅ PASS |
| Validation of form fields | Enter invalid data (e.g., invalid phone number) | Form shows validation errors | Validation errors displayed | ✅ PASS |

### 6. Manage Account Deletion

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Access deletion option | Navigate to profile and click "Delete Account" | Confirmation prompt appears | Prompt displayed correctly | ✅ PASS |
| Cancel deletion | Click "Cancel" on confirmation prompt | Account remains active | Account preserved when canceled | ✅ PASS |
| Confirm deletion | Click "Confirm" on deletion prompt | Account deleted and session ended | Account successfully deleted | ✅ PASS |
| Post-deletion login attempt | Attempt to login with deleted credentials | Error message about non-existent account | Appropriate error shown | ✅ PASS |

## EPIC 2: Product Management

### 1. Add a Product

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Access product addition | Login as admin and navigate to "Product Management" | Product addition form loads | Form loaded successfully | ✅ PASS |
| Complete product form | Fill in all required fields and submit | Product added with confirmation | Product added to database | ✅ PASS |
| Image upload | Upload product image | Image uploaded and associated with product | Image uploaded correctly | ✅ PASS |
| Form validation | Submit with missing required fields | Validation errors shown | Form correctly validated | ✅ PASS |
| Product visibility | Check product appears in store | Product visible to customers | Product displayed in store | ✅ PASS |

### 2. Edit/Update a Product

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Access edit function | Find product and click "Edit" | Edit form loads with current data | Form loaded with product data | ✅ PASS |
| Update information | Change product details and save | Changes saved with confirmation | Product updated successfully | ✅ PASS |
| Update product image | Upload new image | New image replaces old one | Image updated correctly | ✅ PASS |
| Cancel edit | Click "Cancel" during edit | Returns to product without changes | No changes when canceled | ✅ PASS |
| View updated product | Navigate to product page | Updated information displayed | Changes visible to users | ✅ PASS |

### 3. Delete a Product

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Access delete function | Find product and click "Delete" | Confirmation prompt appears | Prompt displayed correctly | ✅ PASS |
| Cancel deletion | Click "Cancel" on prompt | Product remains in store | Product preserved when canceled | ✅ PASS |
| Confirm deletion | Click "Confirm" on prompt | Product removed with confirmation | Product successfully deleted | ✅ PASS |
| Product removal | Search for deleted product | Product not found in store | Product no longer available | ✅ PASS |

### 4. View Product Details

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Access product details | Click on product from listing | Product details page loads | Details page loaded correctly | ✅ PASS |
| Information display | Review product page content | All details displayed correctly | All information visible | ✅ PASS |
| Image display | Check product images | Images load and can be viewed | Images displayed properly | ✅ PASS |
| Stock information | Check availability indicator | Stock status shown accurately | Stock status displayed | ✅ PASS |
| Related products | Scroll to bottom of page | Related products shown | Related items displayed | ✅ PASS |

### 5. Filter and Sort Products

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Category filtering | Select category from menu | Products filtered by category | Category filter worked | ✅ PASS |
| Subcategory filtering | Select subcategory from menu | Products filtered by subcategory | Subcategory filter worked | ✅ PASS |
| Price sorting | Select "Price (low to high)" | Products sorted by ascending price | Price sorting worked | ✅ PASS |
| Rating sorting | Select "Rating (high to low)" | Products sorted by descending rating | Rating sorting worked | ✅ PASS |
| Multiple filters | Apply category and sort option | Products filtered and sorted correctly | Multiple filters worked | ✅ PASS |

## EPIC 3: Checkout Process

### 1. Add to Bag

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Add single item | Click "Add to Bag" on product | Item added with confirmation message | Item added successfully | ✅ PASS |
| Add multiple items | Add multiple products to bag | All items added correctly | Multiple items added | ✅ PASS |
| Add with quantity | Select quantity and add to bag | Correct quantity added | Quantity added correctly | ✅ PASS |
| Bag icon update | Add items to bag | Bag icon updates to show items count | Icon updated correctly | ✅ PASS |
| Continue shopping | Add item and click "Continue Shopping" | User remains on product page | Shopping continued | ✅ PASS |

### 2. Review and Edit Bag

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Access bag | Click bag icon in navigation | Bag page loads with items | Bag page loaded correctly | ✅ PASS |
| Update quantity | Change quantity and click update | Quantity and totals updated | Updates applied correctly | ✅ PASS |
| Remove item | Click "Remove" on item | Item removed and totals updated | Item removed successfully | ✅ PASS |
| Empty bag | Remove all items | Empty bag message displayed | Empty state handled correctly | ✅ PASS |
| Continue shopping | Click "Continue Shopping" | Returns to products page | Returned to products | ✅ PASS |

### 3. Complete Checkout with Payment

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Proceed to checkout | Click "Checkout" from bag | Checkout page loads with form | Checkout page loaded | ✅ PASS |
| Form completion | Fill in delivery and payment details | Form accepts all information | Form completed successfully | ✅ PASS |
| Form validation | Submit with missing required fields | Validation errors shown | Form correctly validated | ✅ PASS |
| Payment processing | Submit valid payment details | Payment processed successfully | Payment completed | ✅ PASS |
| Failed payment | Enter invalid card details | Error message displayed | Payment error handled | ✅ PASS |

### 4. Order Confirmation

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| On-site confirmation | Complete checkout process | Confirmation page with order details | Confirmation displayed | ✅ PASS |
| Confirmation email | Check email after purchase | Order confirmation email received | Email received promptly | ✅ PASS |
| Email content | Open confirmation email | Email contains complete order details | Order details correct | ✅ PASS |
| Order history | Check order history in profile | New order appears in history | Order added to history | ✅ PASS |

### 5. Guest Checkout Option

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Access as guest | Add items to bag and checkout without login | Checkout form available to guest | Guest checkout available | ✅ PASS |
| Complete guest checkout | Fill form and process payment | Order completed successfully | Guest order processed | ✅ PASS |
| Registration prompt | Complete guest checkout | Prompt to register with benefits shown | Registration prompt displayed | ✅ PASS |
| Email confirmation | Check email after guest purchase | Confirmation email received | Email sent to guest | ✅ PASS |

## EPIC 4: SEO and Marketing

### 1. Implement Meta Tags

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Meta tags presence | View page source of homepage | Meta tags present in head section | Meta tags implemented | ✅ PASS |
| Meta tags content | Check meta description and keywords | Tags contain relevant content | Content appropriate | ✅ PASS |
| Social media tags | Check for OpenGraph tags | OG tags present for social sharing | OG tags implemented | ✅ PASS |
| Validator check | Run page through HTML validator | No errors related to meta tags | Validation passed | ✅ PASS |

### 2. Create and Add Sitemap.xml

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| File existence | Navigate to sitemap.xml | File loads in browser | Sitemap accessible | ✅ PASS |
| File validity | Check XML structure | Valid XML with correct schema | Valid sitemap format | ✅ PASS |
| Content completeness | Review sitemap content | All pages included with proper URLs | All pages present | ✅ PASS |
| Google Search Console | Submit to Google Search Console | Sitemap accepted without errors | Sitemap accepted | ✅ PASS |

### 3. Add robots.txt

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| File existence | Navigate to robots.txt | File loads in browser | Robots.txt accessible | ✅ PASS |
| Content validity | Check file content | Proper directives for crawlers | Valid directives | ✅ PASS |
| Sitemap reference | Check for sitemap reference | Sitemap URL included | Sitemap referenced | ✅ PASS |
| Protected paths | Check that admin/private areas are blocked | Admin paths disallowed | Protected areas blocked | ✅ PASS |

### 4. Newsletter Signup Functionality

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Form accessibility | Load homepage | Newsletter signup form visible | Form accessible | ✅ PASS |
| Email validation | Enter invalid email | Error message displayed | Validation worked | ✅ PASS |
| Successful signup | Enter valid email and submit | Success message displayed | Signup successful | ✅ PASS |
| Duplicate prevention | Submit same email twice | Message about existing subscription | Duplicates prevented | ✅ PASS |
| Database storage | Check admin panel after signup | Email stored in subscribers list | Data stored correctly | ✅ PASS |

### 5. Create Facebook Business Page

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Page existence | Navigate to Facebook page link | Facebook page loads | Page accessible | ✅ PASS |
| Branding elements | Check logo and cover photo | Branding consistent with website | Branding consistent | ✅ PASS |
| Website link | Check "About" section | Link to website present | Website linked | ✅ PASS |
| Business information | Review business details | Contact and business info present | Information complete | ✅ PASS |
| Social widgets | Check website for Facebook widgets | Social sharing/follow buttons present | Social integration working | ✅ PASS |

## EPIC 5: Site Management & Security

### 1. Secure Payment Integration

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Stripe integration | Check checkout page source | Stripe scripts loaded securely | Stripe integrated correctly | ✅ PASS |
| HTTPS connection | Check URL during checkout | Secure connection (HTTPS) used | HTTPS implemented | ✅ PASS |
| Test payment | Complete test purchase with Stripe test card | Payment processed in test mode | Test payment successful | ✅ PASS |
| Payment webhooks | Check webhook delivery | Webhooks properly configured | Webhooks functioning | ✅ PASS |
| Failed payment handling | Use testing card for failure | Error handled gracefully | Failures handled correctly | ✅ PASS |

### 2. Role-Based Access Control

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Admin access | Login as admin and access admin areas | Admin can access all areas | Admin access working | ✅ PASS |
| User restrictions | Login as regular user and attempt admin URLs | Access denied with message | User restrictions working | ✅ PASS |
| Unauthenticated restrictions | Logout and attempt protected URLs | Redirected to login page | Authentication required | ✅ PASS |
| Staff permissions | Login as staff and check permissions | Staff can access appropriate areas | Staff roles working | ✅ PASS |
| URL manipulation | Try to access protected pages via URL manipulation | Access denied with appropriate response | URL protection working | ✅ PASS |

### 3. Set Up Environment Variables

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Environment file | Check project files | .env file not in repository | File properly excluded | ✅ PASS |
| Settings configuration | Review Django settings | Sensitive data loaded from env variables | Settings configured correctly | ✅ PASS |
| Local development | Run site locally | Site functions with local env variables | Local environment working | ✅ PASS |
| Production deployment | Deploy to production | Site functions with production variables | Production variables working | ✅ PASS |
| Error handling | Temporarily remove a variable | Appropriate error or fallback | Error handling working | ✅ PASS |

### 4. Debug Mode Off for Deployment

| **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|-----------|---------------------|-------------------|------------|
| Settings configuration | Check production settings | DEBUG set to False | Debug mode disabled | ✅ PASS |
| Error page display | Trigger a 404 error | Custom 404 page displayed | Custom error pages working | ✅ PASS |
| Stack trace hiding | Trigger a 500 error | No detailed error info exposed | Error details hidden | ✅ PASS |
| Log checking | Check error logs | Errors logged but not displayed | Logging working correctly | ✅ PASS |

## External User Goals

| **User Goal** | **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|---------------|-----------|---------------------|-------------------|------------|
| Browse books by genre/title/author | Category navigation | Use navigation menu and filters | Books filtered by selection | Filtering worked correctly | ✅ PASS |
| Add books to bag and see total | Shopping bag functionality | Add multiple books to bag | Items added with running total | Bag worked as expected | ✅ PASS |
| Save favorite books | Wishlist functionality | Add book to wishlist | Book saved to wishlist | Wishlist feature working | ✅ PASS |
| View past orders | Order history | Login and view order history | Past orders displayed | History accessible | ✅ PASS |
| Guest purchase | Guest checkout | Complete purchase without account | Checkout completed successfully | Guest checkout working | ✅ PASS |
| Newsletter signup | Newsletter form | Submit email to newsletter | Confirmation of signup | Newsletter signup working | ✅ PASS |
| Manage account details | Profile management | Edit account information | Changes saved successfully | Profile management working | ✅ PASS |
| Receive order confirmation | Email notifications | Complete purchase | Confirmation email received | Order emails working | ✅ PASS |

## Admin User Goals

| **User Goal** | **Test Case** | **Steps** | **Expected Result** | **Actual Result** | **Status** |
|---------------|---------------|-----------|---------------------|-------------------|------------|
| Manage inventory | Product management | Add, edit, delete products | Changes applied successfully | Inventory management working | ✅ PASS |
| Access store overview | Admin dashboard | Login to admin area | Dashboard with store stats visible | Dashboard accessible | ✅ PASS |
| Purchase notifications | Order alerts | Complete a purchase | Admin notification received | Order alerts working | ✅ PASS |
| Manage user accounts | User management | Access user management section | User accounts viewable/editable | User management working | ✅ PASS |
| Manage newsletter | Subscriber management | View/export subscriber list | List accessible with management tools | Newsletter management working | ✅ PASS |
| Secure access control | Permission testing | Test different user role access | Appropriate restrictions applied | Access control working | ✅ PASS |

## Summary

All user stories have been thoroughly tested against their acceptance criteria, with all tests passing successfully. The implemented features meet the requirements defined in the user stories, providing a comprehensive and functional e-commerce platform for both customers and administrators.

Areas of particularly strong performance include:

- User account management
- Product browsing and filtering
- Secure checkout process
- Admin inventory management

This testing process confirms that 'The Literary Loft' meets all the core requirements outlined in the user stories documentation and provides a solid foundation for future enhancements.

[Back to top ⬆](#table-of-contents)

## Manual Testing

## Validator Testing

- [Manual Testing](#manual-testing)
- [Validator Testing](#validator-testing)
