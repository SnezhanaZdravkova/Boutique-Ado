from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """
#  Now that we've got the full product list in product detail view complete.
# We'll spend this video and the next making sure that users can view specific categories of products.
# I've added another user story for this since it didn't really fit any of the others.
# And before we can allow sorting within a specific category
# we need to first filter to the specific categories we want to sort.
# So this user story will allow shoppers to quickly find products they're interested in
# without having to search through all the products.
# We'll also take care of these two stories related to search queries.
# We've actually got most of the infrastructure needed to accomplish this already setup.
# Let's begin with search queries.
# You'll recall that we have a search form in the main site header
# which uses request.get to submit a search query.
# We didn't give it an action url when we created it.
# Because we didn't have a url to handle it at that time.
# But now we have the products url. So let's change the action url to products which
# will submit this form to the all_products view.
# And let's not forget we also need to do this in the mobile version of the header
# So I'll do that here in mobile top header.html
# This change means that when we submit a search query.
# It'll end up in the url as a get parameter.
# We can access those url parameters in the all_products view by checking whether request.get exists.
# Since we named the text input in the form q. We can just check if q is in request.get
# If it is I'll set it equal to a variable called query.
# If the query is blank it's not going to return any results. So if that's the case let's use
# the Django messages framework to attach an error message to the request.
# And then redirect back to the products url.
# We'll also need to import messages, redirect, and reverse up here.
# In order for that to work and we'll talk more about this later.
# If the query isn't blank.
# I'm going to use a special object from Jango.db.models called Q to generate a search query.
# This deserves a bit of an explanation.
# In Jango if you use something like product.objects.filter
# In order to filter a list of products. Everything will be ended together.
# In the case of our queries that would mean that when a user submits a query.
# In order for it to match the term would have to appear in both the product name and the product description.
# Instead, we want to return results where the query was matched in either
# the product name or the description.
# In order to accomplish this or logic, we need to use Q
# This is worth knowing because in real-world database operations.
# Queries can become quite complex and using Q is often the only way to handle them.
# Because of that, I'd strongly recommend that you become familiar with this
# and the other complex database functionality.
# By reading through the queries portion of the Django documentation.
# Getting back to the code using Q is actually quite simple.
# I'll set a variable equal to a Q object. Where the name contains the query.
# Or the description contains the query.
# The pipe here is what generates the or statement.
# And the i in front of contains makes the queries case insensitive.
# With those queries constructed.
# Now I can pass them to the filter method in order to actually filter the products.
# Now I'll add the query to the context. And in the template call it search term.
# And we'll start with it as none at the top of this view to ensure we don't get an error
# when loading the products page without a search term.
# Let's save that and test whether it works.
# I'll run a search for jeans, which as you can see returns all the jeans in our store.
# Now let's run a search for soft. To verify that we're also searching in descriptions.
# Looking at these items none of these first four contain the term soft in the product name.
# But they do in fact contain it in the product description.
# We'll add some of the finer details to this in a bit.
# But, for now, let's commit our changes and move on to filtering products by categories.
# We'll take care of that in the next video.


    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)

# With search queries working let's give our users the ability to show specific
# categories of products.
# This will handle the clothing home wear and special offers dropdowns in the main navigation menu.
# Let's start in main_nav.html,
# In order to handle filtering by category, I'm gonna pass a category parameter to the
# products URL just like we're doing with q for search queries.
# These parameters will use the name field from the category model so we have
# a programmatic way to access them.
# Of course we could also use the category id.
# But this makes the URLs a little more semantic which is nice for the user.
# So for the first drop-down menu clothing. This top link here will point to the products URL.
# Followed by a question mark to indicate we're about to pass the category parameter.
# Followed by activewear and essentials separated by a comma.
# This syntax ensures we end up with a comma-separated string in the view.
# The other three links are pretty self-explanatory.
# I'll simply use the same syntax with the appropriate categories for jeans shirts and then all clothing.
# Now heading to the all_products view we need to capture this category parameter.
# Again we'll start with it as none at the top of the view.
# And then we'll check whether it exists in requests.get.
# If it does I'm gonna split it into a list at the commas.
# And then use that list to filter the current
# query set of all products down to only products whose category name is in the list.
# It's worth noting by the way, that this double underscore syntax is common when making queries in django.
# Using it here means we're looking for the name field of the category model.
# And we're able to do this because category and product are related with a foreign key.
# An alternative way to do this would be to filter all categories down to those contained in this list
# and then filter products based on the category ID instead of the name.
# But this would take more queries and add unnecessary complexity.
# It's faster and easier to just drill into the related model using this double underscore syntax.
# Actually, though we should grab those categories anyway
# so we can display for the user which categories they currently have selected.
# For that, we need to import category here at the top.
# And then we'll filter all categories down to the ones whose name is in the list from the URL.
# This might seem redundant but remember that by doing this
# we're converting the list of strings of category names passed through the URL
# into a list of actual category objects, so that we can access all their fields in the template.
# Let's call that list of category objects, current_categories.
# and return it to the context so we can use it in the template later on.
# If we head back to the site now you'll see that all our filtering is working for the clothing category.
# Now all we need to do is copy the same syntax into the rest of the menu items in main_nav.html
# You can see now why the programmatic and friendly names in this model are nice
# since we can use the programmatic name in the URLs here
# and we'll be able to render the friendly name in our templates.
# Let's check one more time to make sure all of our menu items are working.
# And looks like we've got a small bug here so let's go and check out what's going on with that.
# It looks like there's a typo in our category's variable here at the top on line 13.
# So that should take care of that.
# And this all looks good now.
# So I'm gonna head back and commit my changes before moving on.
# But this takes care of almost the entire navigation menu.
# Our store is really starting to take shape now
# with users having the ability to search product names and descriptions
# and filter the product list down to specific categories.
# In the next video well tidy this up a bit and start working on the ability to
# sort products in various ways.
