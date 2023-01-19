# mm_auto
Automation system I developed for Mutual Mobile.  This is the "testing side."  The "infrastructure side" called MATS is not included here.

Typical UI automation for web and mobile apps uses a Page-Object model along with tests.  I find this insufficient and inextensible.
* Layer 1: I first wrap the automation tool, which encapsulates UI-handing
* Layer 2: Then I create flow classes, which encapsulate UI element attributes (similar to page-object model) and (unlike page-object model)
encapsulates business rules.  This avoids things like "clicking a button," instead focusing on user-centric actions like "buying a product."
* Layer 3: Then writing tests with business-level actions is a breeze!

A typical test might look like

    flow.login(user01)
    flow.add_to_cart(item01)
    checkout_total = flow.checkout()
    flow.verify_cart_is_empty()
    flow.verify_receipt_total_equals(checkout_total)

Of course, methods like add_to_cart() are made up of methods like search_for_item() and checkout() is made up of go_to_cart() and add_payment()
etc., so if tests need to be finer-grained, that's no problem.

See more:
* Automation strategy blog posts: https://jws-testing-blog.blogspot.com/search/label/test%20automation
* Page-object model vs Flow: https://jws-testing-blog.blogspot.com/2018/01/automation-strategy-flow-vs-page.html
* 3 Layer architecture: https://docs.google.com/presentation/d/1pmP-7xCt0i-IAIWFrfwQHNTBTPiagcD0v8BxR_wLmsg/edit?usp=sharing
