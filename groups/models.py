from django.db import models
from django.contrib.auth import get_user_model
import random
import string
from django.db import transaction


# Utility function to generate group code
def generate_group_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Group(models.Model):
    name = models.CharField(max_length=255)
    admin = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='admin_groups'
    )  # The user who manages the group

    budget_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    group_members_limit = models.IntegerField(default=10)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    secret_santa_assigned = models.BooleanField(default=False)  

    # Join code for group invitations
    join_code = models.CharField(max_length=6, unique=True, blank=True)

    # Members of the group
    members = models.ManyToManyField(get_user_model(), related_name='group_members')
    assigned_member = models.ManyToManyField(
        get_user_model(),
        related_name='assigned_groups',
        blank=True
    )
    
    # Wishlist associated with the group
    wishlists = models.ManyToManyField('wishlists.Wishlist', related_name='groups', blank=True)

    @property
    def is_budget_exceeded(self):
        """
        Checks whether the total price of items in all wishlists exceeds the group's budget limit.
        """
        # Mapping of price ranges to numeric values (you can adjust this mapping if necessary)
        price_range_map = {
            '0_100': 100,
            '101_200': 200,
            '201_300': 300,
            '301_500': 500,
            '501_1000': 1000,
            '1001_2000': 2000,
            '2001_5000': 5000,
            '5001_above': 5001,  # You can adjust this if necessary, e.g., cap it to 5000 or something
        }

        # Calculate total price by summing up the mapped price range values
        total_price = sum(
            price_range_map.get(item.price_range, 0) for wishlist in self.wishlists.all() for item in wishlist.items.all()
        )

        return total_price > self.budget_limit

    def assign_secret_santa(self):
        """
        Randomly assigns Secret Santa members within the group.
        """
        members = list(self.members.all())
        random.shuffle(members)

        profiles_to_update = []
        for i, member in enumerate(members):
            assigned_member = members[(i + 1) % len(members)]  # Next member gets assigned
            profile = member.profile  # Assuming the Profile is already created
            profile.secret_santa_assigned_to = assigned_member
            profiles_to_update.append(profile)

        with transaction.atomic():
            Profile.objects.bulk_update(profiles_to_update, ['secret_santa_assigned_to'])

        self.secret_santa_assigned = False  # Mark as assigned
        self.save()

    def save(self, *args, **kwargs):
        """
        Overridden save method to generate a unique join code if not already set.
        """
        if not self.join_code:
            while True:
                code = generate_group_code()
                if not Group.objects.filter(join_code=code).exists():
                    self.join_code = code
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    pseudoname = models.CharField(max_length=100, blank=True, null=True)
    secret_santa_assigned_to = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='secret_santa'
    )

    def __str__(self):
        return self.user.username
