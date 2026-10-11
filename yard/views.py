import csv
from django.http import HttpResponse
from django.http import request
from django.utils import timezone
from django.contrib import messages
from django.db.models import Count, Q
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Inquiry, Yard, Reference, Container, Invoice, InvoiceItem
from .forms import RegisterForm, LoginForm, YardForm, ReferenceForm, ContainerForm, InvoiceForm, InvoiceItemFormSet, InquiryForm


# =========================================================
# AUTHENTICATION VIEWS
# =========================================================

def register_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            # Automatically log the new user in
            login(request, user)

            messages.success(
                request,
                'Account created successfully.'
            )

            return redirect('dashboard')

    else:

        form = RegisterForm()

    context = {
        'form': form
    }

    return render(
        request,
        'accounts/register.html',
        context
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                messages.success(
                    request,
                    f'Welcome back, {user.username}.'
                )

                # Return user to the page they originally requested
                next_url = request.GET.get('next')

                if next_url:
                    return redirect(next_url)

                return redirect('dashboard')

            else:

                form.add_error(
                    None,
                    'Invalid username or password.'
                )

    else:

        form = LoginForm()

    context = {
        'form': form
    }

    return render(
        request,
        'accounts/login.html',
        context
    )


def logout_view(request):

    logout(request)

    messages.success(
        request,
        'You have been logged out successfully.'
    )

    return redirect('login')


@login_required
def dashboard(request):

    yards = Yard.objects.annotate(
        total=Count('references__containers', distinct=True),
        stock_out=Count(
            'references__containers',
            filter=Q(references__containers__status='Out of Yard'),
            distinct=True
        ),
        reserved=Count(
            'references__containers',
            filter=Q(references__containers__status='Reserved'),
            distinct=True
        ),
    )

    recent_stock_out = Container.objects.filter(
        status='Out of Yard'
    ).select_related(
        'reference',
        'reference__yard'
    ).order_by('-date')[:10]

    recent_containers = Container.objects.select_related( 
            'reference', 'reference__yard' ).order_by('-id')[:5] 

    total_references = Reference.objects.count() 
    total_containers = Container.objects.count()
    out_containers = Container.objects.filter( status='Out of Yard' ).count()

    context = {
        'yards': yards,
        'recent_stock_out': recent_stock_out,
        'total_references': total_references,
        'total_containers': total_containers,
        'out_containers': out_containers,
        'recent_containers': recent_containers
    }

    return render(request, 'dashboard.html', context)


def export_container_csv(request):

    status = request.GET.get('status', 'total')

    containers = Container.objects.select_related(
        'reference',
        'reference__yard'
    )

    if status != 'total':
        containers = containers.filter(status=status)

    response = HttpResponse(
        content_type='text/csv'
    )

    response['Content-Disposition'] = (
        'attachment; filename="container_summary.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Container No',
        'Size',
        'Yard',
        'Reference',
        'Status',
        'Client',
        'Date',
    ])

    for container in containers:
        writer.writerow([
            container.container_no,
            container.size,
            container.reference.yard.name,
            container.reference.reference_no,
            container.status,
            container.client_name,
            container.date,
        ])

    return response

# =========================================================
# YARD VIEWS
# =========================================================

def create_yard(request):
    if request.method == 'POST':
        form = YardForm(request.POST)

        if form.is_valid():
            yard = form.save()
            messages.success(request, 'Yard created successfully.')
            return redirect('yard_detail', slug=yard.slug)

    else:
        form = YardForm()

    context = {
        'form': form
    }

    return render(request, 'yards/create_yard.html', context)


def yard_list(request):
    yards = Yard.objects.all().order_by('name')

    context = {
        'yards': yards
    }

    return render(request, 'yards/yard_list.html', context)


def yard_detail(request, slug):
    yard = get_object_or_404(Yard, slug=slug)

    # Because related_name='references'
    references = yard.references.all().order_by('reference_no')

    context = {
        'yard': yard,
        'references': references
    }

    return render(request, 'yards/yard_detail.html', context)


def delete_yard(request, slug):
    yard = get_object_or_404(Yard, slug=slug)

    if request.method == 'POST':
        yard.delete()
        messages.success(request, 'Yard deleted successfully.')
        return redirect('yard_list')

    context = {
        'yard': yard
    }

    return render(request, 'yards/delete_yard.html', context)


# =========================================================
# REFERENCE VIEWS
# =========================================================

def create_reference(request):
    if request.method == 'POST':
        form = ReferenceForm(request.POST)

        if form.is_valid():
            reference = form.save()
            messages.success(request, 'Reference created successfully.')
            return redirect('reference_detail', slug=reference.slug)

    else:
        form = ReferenceForm()

    context = {
        'form': form
    }

    return render(request, 'references/create_reference.html', context)


def reference_list(request):
    query = request.GET.get('q', '')
    references = Reference.objects.select_related('yard').all().order_by(
        'reference_no'
    )

    if query:
        references = references.filter(
            Q(reference_no__icontains=query) |
            Q(yard__name__icontains=query)
        )

    context = {
        'references': references,
        'query': query
    }

    return render(request, 'references/reference_list.html', context)


def reference_detail(request, slug):
    reference = get_object_or_404(
        Reference.objects.select_related('yard'),
        slug=slug
    )

    # Because related_name='containers'
    containers = reference.containers.all().order_by('container_no')

    context = {
        'reference': reference,
        'containers': containers
    }

    return render(
        request,
        'references/reference_detail.html',
        context
    )


def delete_reference(request, slug):
    reference = get_object_or_404(Reference, slug=slug)

    if request.method == 'POST':
        reference.delete()
        messages.success(request, 'Reference deleted successfully.')
        return redirect('reference_list')

    context = {
        'reference': reference
    }

    return render(
        request,
        'references/delete_reference.html',
        context
    )


# =========================================================
# CONTAINER VIEWS
# =========================================================

def create_container(request):
    if request.method == 'POST':
        form = ContainerForm(request.POST)

        if form.is_valid():
            container = form.save()
            messages.success(request, 'Container created successfully.')
            return redirect('container_detail', slug=container.slug)

    else:
        form = ContainerForm()

    context = {
        'form': form
    }

    return render(request, 'containers/create_container.html', context)


def container_list(request):
    query = request.GET.get('q', '')
    containers = Container.objects.select_related(
        'reference',
        'reference__yard'
    ).all().order_by('container_no')

    if query:
        containers = containers.filter(
            Q(container_no__icontains=query) |
            Q(client_name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(reference__reference_no__icontains=query) |
            Q(reference__yard__name__icontains=query)
        )

    context = {
        'containers': containers,
        'query': query
    }

    return render(request, 'containers/container_list.html', context)


def container_detail(request, slug):
    container = get_object_or_404(
        Container.objects.select_related(
            'reference',
            'reference__yard'
        ),
        slug=slug
    )

    context = {
        'container': container
    }

    return render(
        request,
        'containers/container_detail.html',
        context
    )


def delete_container(request, slug):
    container = get_object_or_404(Container, slug=slug)

    if request.method == 'POST':
        container.delete()
        messages.success(request, 'Container deleted successfully.')
        return redirect('container_list')

    context = {
        'container': container
    }

    return render(
        request,
        'containers/delete_container.html',
        context
    )


@login_required
def create_invoice(request):

    if request.method == 'POST':

        invoice_form = InvoiceForm(request.POST)

        if invoice_form.is_valid():

            invoice = invoice_form.save(commit=False)
            invoice.date = timezone.localdate()

            formset = InvoiceItemFormSet(
                request.POST,
                instance=invoice
            )

            if formset.is_valid():

                
                invoice.save()

                # Save invoice product rows
                formset.instance = invoice
                formset.save()

                # Calculate and save grand total
                invoice.calculate_grand_total()
                invoice.save()

                messages.success(
                    request,
                    'Invoice created successfully.'
                )

                return redirect(
                    'invoice_detail',
                    pk=invoice.pk
                )

        else:
            formset = InvoiceItemFormSet(
                request.POST
            )

    else:
        invoice_form = InvoiceForm()
        formset = InvoiceItemFormSet()

    context = {
        'invoice_form': invoice_form,
        'formset': formset,
    }

    return render(
        request,
        'invoices/create_invoice.html',
        context
    )


@login_required
def invoice_detail(request, pk):

    invoice = get_object_or_404(
        Invoice.objects.prefetch_related('items'),
        pk=pk
    )

    context = {
        'invoice': invoice,
        'items': invoice.items.all(),
    }

    return render(
        request,
        'invoices/invoice_detail.html',
        context
    )


@login_required
def invoice_list(request):

    invoices = Invoice.objects.all().order_by('-date', '-id')

    context = {
        'invoices': invoices
    }

    return render(
        request,
        'invoices/invoice_list.html',
        context
    )



def submit_inquiry(request):
    """Handles the contact/quote form on the public homepage."""
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thank you — your quote request has been received."
                "Our team will be in touch."
            )
            return redirect('homepage')
        messages.error(request, "Please correct the errors below and try again.")
        print(form.errors)
    else:
        form = InquiryForm()

    return render(request, 'index.html', {'form': form})


# --- Admin side ---

@login_required
def inquiry_list(request):
    """
    Inquiries list. Newest first (Meta.ordering handles it).
    ?status=new|read|archived filters; default hides archived.
    """
    status = request.GET.get('status', 'active')

    inquiries = Inquiry.objects.all()
    if status == 'archived':
        inquiries = inquiries.filter(status=Inquiry.Status.ARCHIVED)
    elif status in (Inquiry.Status.NEW, Inquiry.Status.READ):
        inquiries = inquiries.filter(status=status)
    else:
        status = 'active'
        inquiries = inquiries.exclude(status=Inquiry.Status.ARCHIVED)

    context = {
        'inquiries': inquiries,
        'active_filter': status,
        'unread_count': Inquiry.objects.filter(status=Inquiry.Status.NEW).count(),
        'archived_count': Inquiry.objects.filter(status=Inquiry.Status.ARCHIVED).count(),
    }
    return render(request, 'inquiries/inquiry_list.html', context)


@login_required
def inquiry_detail(request, pk):
    """Viewing an inquiry marks it as read automatically."""
    inquiry = get_object_or_404(Inquiry, pk=pk)
    inquiry.mark_read()
    return render(request, 'inquiries/inquiry_detail.html', {'inquiry': inquiry})


@login_required
@require_POST
def mark_inquiry_read(request, pk):
    inquiry = get_object_or_404(Inquiry, pk=pk)
    inquiry.mark_read()
    messages.success(request, f"Inquiry from {inquiry.full_name} marked as read.")
    return redirect(request.POST.get('next') or 'inquiry_list')


@login_required
@require_POST
def archive_inquiry(request, pk):
    inquiry = get_object_or_404(Inquiry, pk=pk)
    inquiry.status = Inquiry.Status.ARCHIVED
    inquiry.save(update_fields=['status'])
    messages.success(request, f"Inquiry from {inquiry.full_name} archived.")
    return redirect('inquiry_list')


@login_required
@require_POST
def unarchive_inquiry(request, pk):
    inquiry = get_object_or_404(Inquiry, pk=pk)
    inquiry.status = Inquiry.Status.READ
    inquiry.save(update_fields=['status'])
    messages.success(request, f"Inquiry from {inquiry.full_name} restored.")
    return redirect('inquiry_list')


@login_required
def delete_inquiry(request, pk):
    """GET shows the confirmation page; POST performs the delete."""
    inquiry = get_object_or_404(Inquiry, pk=pk)

    if request.method == 'POST':
        name = inquiry.full_name
        inquiry.delete()
        messages.success(request, f"Inquiry from {name} deleted.")
        return redirect('inquiry_list')

    return render(request, 'inquiries/delete_inquiry.html', {'inquiry': inquiry})

