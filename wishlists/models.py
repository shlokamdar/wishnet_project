from django.db import models
from django.contrib.auth import get_user_model




from groups.models import Group  # Import your Group model if it's in a separate app
class Wishlist(models.Model):
    CATEGORY_CHOICES = [
        ('hobby', 'Hobby'),
        ('gifts', 'Gifts'),
        ('home-decor', 'Home Decor'),
        ('books', 'Books'),
        ('health', 'Health'),
        ('electronics', 'Electronics'),
        ('clothing&accesories', 'Clothing & Accessories'),
        ('kitchen', 'Kitchen'),
        ('beauty', 'Beauty'),
        ('stationery', 'Stationery'),
        ('sports', 'Sports'),
        ('travel', 'Travel'),
        ('tech', 'Tech'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('events', 'Events'),
        ('charity', 'Charity'),
        ('services', 'Services'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100, default='new list')
    description = models.TextField()

    def get_color_code(self):
        category_colors = {
            'hobby': '#FF5733',
            'gifts': '#FFBD33',
            'home-decor': '#33FF57',
            'books': '#3377FF',
            'health': '#FF33A8',
            'electronics': '#33FFBD',
            'clothing&accesories': '#9933FF',
            'kitchen': '#FF8C00',
            'beauty': '#FFC0CB',
            'stationery': '#6A5ACD',
            'sports': '#FF6347',
            'travel': '#4682B4',
            'tech': '#00BFFF',
            'finance': '#4CAF50',
            'education': '#FFD700',
            'events': '#8A2BE2',
            'charity': '#C71585',
            'services': '#20B2AA',
            'other': '#808080', 
        }
        # Check if the category exists in the dictionary and return the corresponding color
        return category_colors.get(self.category, '#808080')  # Default to gray if not found
    
    VISIBILITY_CHOICES = [
        ('private', 'Private (Only Me)'),
        ('public', 'Public (My Friends)'),
    ]
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='wishlists')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='private')
    group = models.ForeignKey('groups.Group', related_name='wishlist_set', on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title




class WishlistItem(models.Model):
    RANGE_CHOICES = [
        ('0_100', '0 to 100'),
        ('101_200', '101 to 200'),
        ('201_300', '201 to 300'),
        ('301_500', '301 to 500'),
        ('501_1000', '501 to 1000'),
        ('1001_2000', '1001 to 2000'),
        ('2001_5000', '2001 to 5000'),
        ('5001_above', '5001 and above'),
    ]

    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_range = models.CharField(max_length=10, choices=RANGE_CHOICES)  # Using price range choices
    url = models.URLField()
    image = models.ImageField(upload_to='wishlist_items/', null=True, blank=True)
    bought = models.BooleanField(default=False)

    def __str__(self):
        return self.name