from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Item, Claim
from .forms import ItemForm, ClaimForm, UserProfileForm


# ---------- STATIC PAGES ----------


def about(request):
    return render(request, 'about.html')

#---------Home Page----------
def home(request):
    recent_lost = Item.objects.filter(status='lost').order_by('-created_at')[:5]
    recent_found = Item.objects.filter(status='found').order_by('-created_at')[:5]
    return render(request, 'home.html', {
        'recent_lost': recent_lost,
        'recent_found': recent_found
    })

# ---------- ITEM LISTING ----------
def lost_items(request):
    items = Item.objects.filter(status='lost').order_by('-created_at')
    return render(request, 'lost_items.html', {'items': items})


def found_items(request):
    items = Item.objects.filter(status='found').order_by('-created_at')
    return render(request, 'found.html', {'items': items})


# ---------- ADD ITEM ----------
@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.posted_by = request.user
            item.save()
            return redirect('item_detail', item_id=item.id)
    else:
        form = ItemForm()

    return render(request, 'add_item.html', {'form': form})


# ---------- MY ITEMS ----------
@login_required
def my_items(request):
    items = Item.objects.filter(posted_by=request.user).order_by('-created_at')
    return render(request, 'my_items.html', {'items': items})


# ---------- ITEM DETAIL + MATCHING ----------
def get_matching_items(item):
    opposite_status = 'found' if item.status == 'lost' else 'lost'

    return Item.objects.filter(
        status=opposite_status,
        location__icontains=item.location[:5]  # simple area-based match
    ).exclude(
        posted_by=item.posted_by
    )


def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    matches = get_matching_items(item)
    return render(request, 'item_detail.html', {
        'item': item,
        'matches': matches
    })


# ---------- EDIT ITEM ----------
@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, posted_by=request.user)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('my_items')
    else:
        form = ItemForm(instance=item)

    return render(request, 'edit_item.html', {'form': form})


# ---------- DELETE ITEM ----------
@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, posted_by=request.user)

    if request.method == 'POST':
        item.delete()
        return redirect('my_items')

    return render(request, 'delete_item.html', {'item': item})


# ---------- CLAIM ITEM ----------
@login_required
def claim_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    # Prevent self-claim
    if item.posted_by == request.user:
        messages.error(request, "You cannot claim your own item.")
        return redirect('home')

    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.item = item
            claim.claimant = request.user
            claim.save()
            return redirect('my_claims')
    else:
        form = ClaimForm()

    return render(request, 'claim_item.html', {
        'form': form,
        'item': item
    })


# ---------- MY CLAIMS ----------
@login_required
def my_claims(request):
    claims = Claim.objects.filter(claimant=request.user).order_by('-created_at')
    return render(request, 'my_claims.html', {'claims': claims})


# ---------- MANAGE CLAIMS (ITEM OWNER) ----------
@login_required
def manage_claims(request):
    claims = Claim.objects.filter(
        item__posted_by=request.user
    ).order_by('-created_at')

    return render(request, 'manage_claims.html', {'claims': claims})


# ---------- UPDATE CLAIM STATUS ----------
@login_required
def update_claim_status(request, claim_id, status):
    claim = get_object_or_404(
        Claim,
        id=claim_id,
        item__posted_by=request.user
    )

    if status in ['approved', 'rejected']:
        claim.status = status
        claim.save()

    return redirect('manage_claims')


# ---------- MARK ITEM AS RETURNED ----------
@login_required
def mark_as_returned(request, claim_id):
    claim = get_object_or_404(
        Claim,
        id=claim_id,
        item__posted_by=request.user
    )

    claim.status = 'returned'
    claim.save()

    claim.item.status = 'returned'
    claim.item.save()

    messages.success(request, "Item marked as returned.")
    return redirect('manage_claims')


# ---------- USER PROFILE ----------
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})
