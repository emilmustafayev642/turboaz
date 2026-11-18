from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q, Avg
import secrets
from datetime import timedelta
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import ListingForm, RegistrationForm
from django.conf import settings
from django.contrib.auth.models import User
from decimal import Decimal

from .models import (
    Brand,
    CarModel,
    Year,
    Listing,
    ListingPhoto,
    Profile,
    EmailVerification,
    CarModelBodyType,
    PinnedListing,
    Conversation,
    Message,
    CarGeneration,
    ModerationLog,
)


def get_user_role(user):
    if not user.is_authenticated:
        return 'guest'
    if user.is_superuser:
        return 'superadmin'
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile.role


def home(request):
    listings = Listing.objects.filter(is_deleted=False).select_related(
        'car_model__brand'
    ).order_by('-created_at')

    brand = request.GET.get('brand')
    model = request.GET.get('model')
    condition = request.GET.get('condition')
    city = request.GET.get('city')
    fuel_type = request.GET.get('fuel_type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_year = request.GET.get('min_year')
    max_year = request.GET.get('max_year')
    generation_id = request.GET.get('generation')

    if brand:
        listings = listings.filter(car_model__brand__name=brand)
    if model:
        listings = listings.filter(car_model__name=model)
    if condition in ('new', 'used'):
        listings = listings.filter(condition=condition)
    if city:
        listings = listings.filter(city__iexact=city)
    if fuel_type:
        listings = listings.filter(fuel_type=fuel_type)
    if min_price and min_price.isdigit():
        listings = listings.filter(price__gte=min_price)
    if max_price and max_price.isdigit():
        listings = listings.filter(price__lte=max_price)
    if min_year and min_year.isdigit():
        listings = listings.filter(year__gte=min_year)
    if max_year and max_year.isdigit():
        listings = listings.filter(year__lte=max_year)
    if generation_id and generation_id.isdigit():
        listings = listings.filter(generation_id=generation_id)

    brands = Brand.objects.prefetch_related('models').all()
    models_by_brand = {
        item.name: [car_model.name for car_model in item.models.all()]
        for item in brands
    }
    generations = CarGeneration.objects.select_related('car_model__brand').all()

    sort_by = request.GET.get('sort', '-id')
    allowed_sorts = {
        'price': 'price',
        '-price': '-price',
        'mileage': 'mileage',
        '-created_at': '-id',
    }
    if sort_by in allowed_sorts:
        listings = listings.order_by(allowed_sorts[sort_by])

    pinned_ids = []
    if request.user.is_authenticated:
        pinned_ids = list(
            PinnedListing.objects.filter(user=request.user).values_list('listing_id', flat=True)
        )

    return render(request, 'index.html', {
        'brands': brands,
        'models_by_brand': models_by_brand,
        'generations': generations,
        'listings': listings,
        'pinned_ids': pinned_ids,
        'user_role': get_user_role(request.user),
    })


def login_view(request):
    post_data = request.POST.copy() if request.method == 'POST' else None

    if post_data and '@' in post_data.get('username', ''):
        user_model = get_user_model()
        user_obj = user_model.objects.filter(email__iexact=post_data['username'].strip()).first()
        if user_obj:
            post_data['username'] = user_obj.username

    form = AuthenticationForm(request, data=post_data)

    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        next_url = request.POST.get('next') or request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)
        return redirect('home')

    next_url = request.POST.get('next') or request.GET.get('next', '')
    return render(request, 'login.html', {'form': form, 'next': next_url})


def register_view(request):
    form = RegistrationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.email = form.cleaned_data['email']
        user.is_active = False
        user.save()

        Profile.objects.create(
            user=user,
            phone=form.cleaned_data['phone'],
        )

        code = f'{secrets.randbelow(1_000_000):06d}'
        EmailVerification.objects.create(
            user=user,
            code_hash=make_password(code),
        )

        request.session['pending_verification_user_id'] = user.pk

        send_mail(
            'Verify your APEX account',
            f'Your verification code is {code}. It expires in 10 minutes.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return redirect('verify_email')

    return render(request, 'register.html', {'form': form})


def verify_email_view(request):
    user_id = request.session.get('pending_verification_user_id')
    user_model = get_user_model()
    user = user_model.objects.filter(pk=user_id, is_active=False).first()

    if user is None:
        messages.error(request, 'Please register before verifying your email.')
        return redirect('register')

    verification = EmailVerification.objects.filter(user=user).first()
    if verification is None:
        messages.error(request, 'No verification code was found. Please register again.')
        return redirect('register')

    if request.method == 'POST':
        code = request.POST.get('code', '').strip()

        if verification.attempts >= 5:
            messages.error(request, 'Too many incorrect attempts. Request a new code.')
        elif timezone.now() - verification.sent_at > timedelta(minutes=10):
            messages.error(request, 'That code has expired. Request a new one.')
        elif check_password(code, verification.code_hash):
            user.is_active = True
            user.save(update_fields=['is_active'])
            verification.delete()
            request.session.pop('pending_verification_user_id', None)
            messages.success(request, 'Email verified. You can now sign in.')
            return redirect('login')
        else:
            verification.attempts += 1
            verification.save(update_fields=['attempts'])
            messages.error(request, 'That code is incorrect.')

    return render(request, 'verify_email.html')


def resend_verification_view(request):
    user_id = request.session.get('pending_verification_user_id')
    user_model = get_user_model()
    user = user_model.objects.filter(pk=user_id, is_active=False).first()

    if user is None:
        messages.error(request, 'Please register before requesting a code.')
        return redirect('register')

    verification = EmailVerification.objects.filter(user=user).first()
    if verification is None:
        messages.error(request, 'No verification request was found. Please register again.')
        return redirect('register')

    now = timezone.now()

    if verification.resend_count >= 3:
        messages.error(request, 'You have reached the code resend limit.')
    elif now - verification.sent_at < timedelta(seconds=60):
        messages.error(request, 'Wait 60 seconds before requesting another code.')
    else:
        code = f'{secrets.randbelow(1_000_000):06d}'
        verification.code_hash = make_password(code)
        verification.sent_at = now
        verification.attempts = 0
        verification.resend_count += 1
        verification.save(update_fields=[
            'code_hash',
            'sent_at',
            'attempts',
            'resend_count',
        ])

        send_mail(
            'Verify your APEX account',
            f'Your verification code is {code}. It expires in 10 minutes.',
            None,
            [user.email],
            fail_silently=False,
        )
        messages.success(request, 'A new code was sent.')

    return redirect('verify_email')


@login_required(login_url='login')
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {
        'profile': profile,
        'user_role': get_user_role(request.user),
    })


@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')


def detail_view(request, listing_id):
    listing = get_object_or_404(
        Listing.objects.select_related('car_model__brand').prefetch_related('photos'),
        pk=listing_id,
    )

    # 1. BAXIS SAYI (1 User = 1 View)
    if request.user.is_authenticated:
        if not listing.viewed_by.filter(id=request.user.id).exists():
            listing.viewed_by.add(request.user)
            listing.views_count += 1
            listing.save(update_fields=['views_count'])
    else:
        viewed_cars = request.session.get('viewed_cars', [])
        if listing.id not in viewed_cars:
            listing.views_count += 1
            listing.save(update_fields=['views_count'])
            viewed_cars.append(listing.id)
            request.session['viewed_cars'] = viewed_cars

    # 2. LOQIKA QIYMET DUSMEK
    pin_obj = None
    price_drop = None
    if request.user.is_authenticated:
        pin_obj = PinnedListing.objects.filter(user=request.user, listing=listing).first()
        if pin_obj and listing.price < pin_obj.initial_price:
            price_drop = pin_obj.initial_price - listing.price

    # 3. MUQAYISE
    compare_ids = request.session.get('compare_ids', [])
    in_compare = listing.id in compare_ids


    # 4. QIYMET ANALIZI (Market Price Analyzer)
    similar_cars = Listing.objects.filter(
        car_model=listing.car_model,
        is_deleted=False
    ).exclude(pk=listing.pk)
   
    if not similar_cars.exists():
        similar_cars = Listing.objects.filter(
            year__gte=listing.year - 3,
            year__lte=listing.year + 3,
            is_deleted=False
        ).exclude(pk=listing.pk)

    
    if not similar_cars.exists():
        similar_cars = Listing.objects.filter(is_deleted=False).exclude(pk=listing.pk)

    avg_price_data = similar_cars.aggregate(avg_p=Avg('price'))
    avg_price = avg_price_data['avg_p']
    price_status = None
    price_diff = 0

    if avg_price and listing.price:
        avg_price = round(avg_price)
        price_diff = abs(round(listing.price - avg_price))
        if listing.price < avg_price * Decimal('0.92'):
            price_status = 'good'      
        elif listing.price > avg_price * Decimal('1.08'):
            price_status = 'high'      
        else:
            price_status = 'normal'   

    return render(request, 'detail.html', {
        'listing': listing,
        'is_pinned': pin_obj is not None,
        'pin_obj': pin_obj,
        'price_drop': price_drop,
        'in_compare': in_compare,
        'compare_count': len(compare_ids),
        'user_role': get_user_role(request.user),
        'avg_price': avg_price, 'price_status': price_status, 'price_diff': price_diff,
    })


@login_required(login_url='login')
def elan_view(request):
    brands = Brand.objects.prefetch_related('models').all()

    models_by_brand = {
        brand.name: [
            {'id': model.id, 'name': model.name}
            for model in brand.models.all()
        ]
        for brand in brands
    }

    brand_types = {
        brand.name: brand.vehicle_type
        for brand in brands
    }

    body_types_by_model = {}
    for option in CarModelBodyType.objects.select_related('car_model').order_by(
        'car_model_id', 'body_type'
    ):
        body_types_by_model.setdefault(str(option.car_model_id), []).append({
            'value': option.body_type,
            'label': option.get_body_type_display(),
        })

    years = list(
        Year.objects.order_by('-year').values_list('year', flat=True)
    )

    generations = CarGeneration.objects.select_related('car_model__brand').all()

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            photos = form.cleaned_data['photos']
            with transaction.atomic():
                listing = form.save(commit=False)
                listing.owner = request.user
                listing.image = photos[0]
                listing.save()

                for photo in photos[1:]:
                    ListingPhoto.objects.create(listing=listing, image=photo)

            return redirect('home')
    else:
        form = ListingForm()

    context = {
        'form': form,
        'models_by_brand': models_by_brand,
        'brand_types': brand_types,
        'body_types_by_model': body_types_by_model,
        'years': years,
        'selected_vehicle_type': (
            request.POST.get('vehicle-type', 'minik')
            if request.method == 'POST'
            else 'minik'
        ),
        'selected_year': form.data.get('year', '') if form.is_bound else '',
        'generations': generations,
    }
    return render(request, 'elan.html', context)


@login_required(login_url='login')
@require_POST
def toggle_pin_view(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    pin, created = PinnedListing.objects.get_or_create(
        user=request.user,
        listing=listing,
        defaults={'initial_price': listing.price},
    )

    if not created:
        pin.delete()

    return redirect('detail', listing_id=listing.id)


@require_POST
def toggle_compare_view(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    compare_ids = request.session.get('compare_ids', [])

    if listing.id in compare_ids:
        compare_ids.remove(listing.id)
    else:
        if len(compare_ids) >= 2:
            compare_ids.pop(0)
        compare_ids.append(listing.id)

    request.session['compare_ids'] = compare_ids
    return redirect('detail', listing_id=listing.id)


def compare_view(request):
    compare_ids = request.session.get('compare_ids', [])
    listings_to_compare = Listing.objects.select_related('car_model__brand').filter(
        id__in=compare_ids
    )
    return render(request, 'compare.html', {'listings': listings_to_compare})


@login_required(login_url='login')
def edit_listing_view(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if listing.owner != request.user:
        messages.error(request, 'Bu elanı redaktə etməyə icazəniz yoxdur.')
        return redirect('detail', listing_id=listing.id)

    if request.method == 'POST' and 'delete_listing' in request.POST:
        listing.delete()
        return redirect('home')

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Elan uğurla yeniləndi!')
            return redirect('detail', listing_id=listing.id)
    else:
        form = ListingForm(instance=listing)

    context = {
        'form': form,
        'listing': listing,
        'brands': Brand.objects.prefetch_related('models').all(),
        'years': list(Year.objects.order_by('-year').values_list('year', flat=True)),
    }
    return render(request, 'elan.html', context)


@login_required(login_url='login')
def start_or_open_chat(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    storage = get_messages(request)
    storage.used = True

    if not listing.owner:
        messages.error(request, 'Bu elanin saticisi yoxdur.')
        return redirect('detail', listing_id=listing.id)

    if listing.owner == request.user:
        messages.info(request, 'Öz elanınıza mesaj yaza bilməzsiniz.')
        return redirect('detail', listing_id=listing.id)

    conversation, _ = Conversation.objects.get_or_create(
        listing=listing,
        buyer=request.user,
        defaults={'seller': listing.owner},
    )
    return redirect('chat_room', conversation_id=conversation.id)


@login_required(login_url='login')
def chat_room_view(request, conversation_id=None):
    conversations = Conversation.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user)
    ).select_related('listing__car_model__brand', 'buyer', 'seller').order_by('-created_at')

    active_conversation = None
    messages_list = []
    other_user = None

    if conversation_id:
        active_conversation = get_object_or_404(
            Conversation.objects.select_related('listing__car_model__brand', 'buyer', 'seller'),
            pk=conversation_id,
        )

        if request.user not in (active_conversation.buyer, active_conversation.seller):
            return redirect('chat_inbox')

        if request.method == 'POST':
            text = request.POST.get('text', '').strip()
            if text:
                Message.objects.create(
                    conversation=active_conversation,
                    sender=request.user,
                    text=text,
                )
                return redirect('chat_room', conversation_id=active_conversation.id)

        messages_list = active_conversation.messages.select_related('sender').all()
        other_user = (
            active_conversation.seller
            if request.user == active_conversation.buyer
            else active_conversation.buyer
        )
    elif conversations.exists():
        return redirect('chat_room', conversation_id=conversations.first().id)

    return render(request, 'chat.html', {
        'conversations': conversations,
        'active_conversation': active_conversation,
        'messages_list': messages_list,
        'other_user': other_user,
    })


@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        listing.delete()
        return redirect('/')
    return redirect('/')



# indi rollar elvae edirem moderator admin superadmin


@login_required(login_url='login')
@require_POST
def staff_delete_listing(request, listing_id):
    role = get_user_role(request.user)
    if role not in ['moderator', 'admin', 'superadmin']:
        messages.error(request, 'Bu əməliyyat üçün icazəniz yoxdur!')
        return redirect('home')

    listing = get_object_or_404(Listing, pk=listing_id)
    reason = request.POST.get('reason', '').strip()

    if not reason:
        messages.error(request, 'Elanı silmək üçün mütləq səbəb yazmalısınız!')
        return redirect('detail', listing_id=listing.id)

    listing.is_deleted = True
    listing.deleted_by = request.user
    listing.delete_reason = reason
    listing.deleted_at = timezone.now()
    listing.save(update_fields=['is_deleted', 'deleted_by', 'delete_reason', 'deleted_at'])

    owner_name = listing.owner.username if listing.owner else 'Naməlum'
    ModerationLog.objects.create(
        staff_user=request.user,
        action='delete',
        target_info=f"{listing.car_model} ({listing.price} AZN) - Sahibi: {owner_name}",
        reason=reason,
    )

    messages.success(request, 'Elan silindi və Silinmiş Elanlar siyahısına əlavə olundu.')
    return redirect('staff_dashboard')


@login_required(login_url='login')
@require_POST
def staff_restore_listing(request, listing_id):
    role = get_user_role(request.user)
    if role not in ['admin', 'superadmin']:
        messages.error(request, 'Elanı yalnız Admin və ya Superadmin bərpa edə bilər!')
        return redirect('staff_dashboard')

    listing = get_object_or_404(Listing, pk=listing_id)
    listing.is_deleted = False
    listing.deleted_by = None
    listing.delete_reason = ''
    listing.deleted_at = None
    listing.save(update_fields=['is_deleted', 'deleted_by', 'delete_reason', 'deleted_at'])

    messages.success(request, 'Elan yenidən saytda aktiv edildi!')
    return redirect('staff_dashboard')


@login_required(login_url='login')
@require_POST
def staff_verify_listing(request, listing_id):
    role = get_user_role(request.user)
    if role not in ['moderator', 'admin', 'superadmin']:
        return redirect('home')

    listing = get_object_or_404(Listing, pk=listing_id)
    listing.is_verified = not listing.is_verified
    listing.save(update_fields=['is_verified'])

    ModerationLog.objects.create(
        staff_user=request.user,
        action='verify',
        target_info=f"{listing.car_model} (ID: #{listing.id})",
        reason='Elan yoxlanıldı və təsdiqləndi' if listing.is_verified else 'Təsdiq nişanı ləğv edildi',
    )
    return redirect('detail', listing_id=listing.id)


@login_required(login_url='login')
def staff_dashboard(request):
    role = get_user_role(request.user)
    if role not in ['moderator', 'admin', 'superadmin']:
        return redirect('home')

    if request.method == 'POST' and 'change_role' in request.POST and role == 'superadmin':
        target_user = get_object_or_404(User, pk=request.POST.get('user_id'))
        new_role = request.POST.get('new_role')
        profile, _ = Profile.objects.get_or_create(user=target_user)
        profile.role = new_role
        profile.save()
        messages.success(request, f"{target_user.username} istifadəçisinin rolu '{new_role}' olaraq dəyişdirildi!")
        return redirect('staff_dashboard')

    if request.method == 'POST' and 'toggle_ban' in request.POST and role in ['admin', 'superadmin']:
        target_user = get_object_or_404(User, pk=request.POST.get('user_id'))
        if not target_user.is_superuser:
            target_user.is_active = not target_user.is_active
            target_user.save(update_fields=['is_active'])
            ModerationLog.objects.create(
                staff_user=request.user,
                action='ban',
                target_info=target_user.username,
                reason=request.POST.get('ban_reason', 'Qayda pozuntusu'),
            )
            messages.success(request, f"{target_user.username} statusu yeniləndi.")
        return redirect('staff_dashboard')

    deleted_listings = Listing.objects.filter(is_deleted=True).select_related(
        'car_model__brand', 'owner', 'deleted_by'
    ).order_by('-deleted_at')

    logs = ModerationLog.objects.select_related('staff_user').order_by('-created_at')[:50]
    users = User.objects.select_related('profile').all() if role in ['admin', 'superadmin'] else []

    return render(request, 'staff_dashboard.html', {
        'user_role': role,
        'deleted_listings': deleted_listings,
        'logs': logs,
        'users': users,
    })

    # biz nidi seller badge elave iderik 18/11/26

def seller_listings_view(request, username):
    seller = get_object_or_404(User.objects.select_related('profile'), username=username)
    listings = Listing.objects.filter(owner=seller, is_deleted=False).select_related(
        'car_model__brand'
    ).order_by('-created_at')

    return render(request, 'index.html', {
        'listings': listings,
        'brands': Brand.objects.prefetch_related('models').all(),
        'generations': CarGeneration.objects.select_related('car_model__brand').all(),
        'user_role': get_user_role(request.user),
        'selected_seller': seller,
    })