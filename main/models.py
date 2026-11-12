from django.db import models

from django.conf import settings

from django.utils import timezone

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    VEHICLE_TYPE_CHOICES = [
        ('minik', 'Minik'),
        ('kommersiya', 'Kommersiya'),
        ('moto', 'Moto'),
    ]

    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPE_CHOICES,
        default='minik',
    )

    def __str__(self):
        return self.name

class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.brand.name} {self.name}"

class CarGeneration(models.Model):
    car_model = models.ForeignKey(
        'CarModel',
        on_delete=models.CASCADE,
        related_name='generation',
    )
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='generations/', blank=True, null=True)


    def __str__(self):
        return f'{self.car_model.name} - {self.name}'

class Year(models.Model):
    year = models.IntegerField(unique=True)
    
    def __str__(self):
        return str(self.year)

class Listing(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Yeni'),
        ('used', 'İşlənmiş'),
    ]

    BODY_TYPE_CHOICES = [
        # Для Minik (Легковые)
        ('sedan', 'Sedan'),
        ('hatchback', 'Hetçbek'),
        ('suv', 'SUV / Offroader'),
        ('coupe', 'Kupe'),
        ('universal', 'Universal'),
        ('crossover', 'Krossover'),
        ('minivan', 'Minivan'),
        ('cabriolet', 'Kabriolet'),
        
        # Для Kommersiya (Коммерческие — точь-в-точь как на твоем скриншоте)
        ('avtokran', 'Avtokran'),
        ('soyuduculu_furqon', 'Soyuduculu furqon'),
        ('qolfkar', 'Qolfkar'),
        ('karvan', 'Karvan'),
        ('avtobus', 'Avtobus'),
        ('dartqi', 'Dartqı'),
        ('yuk_masini', 'Yük maşını'),
        ('furqon', 'Furqon'),
        
        # Для Moto
        ('sport', 'Sportbike'),
        ('cruiser', 'Kruizer'),
        ('scooter', 'Skuter'),
        
        ('other', 'Digər'),
    ]

    FUEL_TYPE_CHOICES = [
        ('petrol', 'Benzin'),
        ('diesel', 'Dizel'),
        ('hybrid', 'Hibrid'),
        ('electric', 'Elektro'),
        ('gas', 'Qaz'),
    ]

    generation = models.ForeignKey(
        'CarGeneration',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='listing',
    )

    car_model = models.ForeignKey(
        CarModel,
        on_delete=models.PROTECT,
        related_name='listings',
    )

    # MEN INDI PROFILE EMAIL VERIFICATION YARATMAQA BASLAYIRAM 27/10/26  21:03

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='listings',
    )

    year = models.PositiveSmallIntegerField()
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES, default='petrol')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    mileage = models.PositiveIntegerField()
    city = models.CharField(max_length=100)
    description = models.TextField()
    phone_number = models.CharField(max_length=30, default='')
    image = models.ImageField(upload_to='listing_photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_damaged = models.BooleanField(default=False, verbose_name='Vurugu var')
    is_repainted = models.BooleanField(default=False, verbose_name="Rənglənib")
    


    def __str__(self):
        return f'{self.car_model} {self.year}'



class ListingPhoto(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='photos',
    )
    image = models.ImageField(upload_to='listing_photos/')

    def __str__(self):
        return f'Photo for {self.listing}'



class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    phone = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.user.username} profile'

class EmailVerification(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='email_verification',
    )

    code_hash = models.CharField(max_length=128)
    sent_at = models.DateTimeField(default=timezone.now)
    attempts = models.PositiveSmallIntegerField(default=0)
    resend_count = models.PositiveSmallIntegerField(default=0)


class CarModelBodyType(models.Model):
    car_model = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        related_name='body_type_options',
    )

    body_type = models.CharField(
        max_length=20,
        choices=Listing.BODY_TYPE_CHOICES,
    )


    class Meta:
        constraints = [ 
            models.UniqueConstraint(
                fields=['car_model', 'body_type'],
                name='unique_body_type_per_car_model'
            ),
        ]

    def __str__(self):
        return f'{self.car_model} - {self.get_body_type_display()}'

class PinnedListing(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pinned_listings',
    )
    
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='pins',
    )

    # Burda masinin qiymeti saxlayiriq 67 pin knopkasina basanda!!

    initial_price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'listing'],
                name='unique_user_pinned_listing',
            ),
        ]

    def __str__(self):
        return f'{self.user.username} pinned {self.listing}'

 # bura benim 04/11/26 seller and user danisma seyifesidi

class Conversation(models.Model):
    listing = models.ForeignKey(
        'Listing',
        on_delete=models.CASCADE,
        related_name='conversations',
    )

    # buyer modeli conversation

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='buying_conversations',
    )

    # seller burda
 
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='selling_conversations',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
       constraints = [ 
            models.UniqueConstraint(
                fields=['listing', 'buyer'],
                name='unique_buyer_listing_conversation'
            ),
        ]

    def __str__(self):
        return f'{self.buyer.username} -> {self.seller.username} ({self.listing})'

class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
    )

    # mesaji ginderen

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
    )

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender.username}: {self.text[:30]}'



