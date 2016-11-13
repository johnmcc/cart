Cart
====

To run tests, download the archive, cd into the directory and run "python tests.py".

You can see the API from tests.py, or from the docstring inside each module.

Tested on Python 2.7.10. Requires Python >= 2.7. If you're using a lower version of Python than this, one of the unit tests will fail.

Known issues / possible improvements:
=====================================

* I have assumed that every product is eligible for BOGOF once the discount is applied to the cart. If this is not the case, it would be trivial to add a flag to the Product class and a check in DiscountManager.bogof_discount.
* For Cart.set_total, we are currently rounding off to two decimal places. It would be better to use Locale and currency here, but this works differently across different operating systems etc.
* There is currently no output or GUI; just unit tests.