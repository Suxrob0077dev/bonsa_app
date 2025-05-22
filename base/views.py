from django.shortcuts import render, redirect
from .models import *
from django.views.generic import TemplateView, ListView, DetailView
from .forms import *
from pyexpat.errors import messages

# Create your views here.

class HomePageView(ListView):
    model = Pricing
    template_name = 'pages/home.html'
    context_object_name = 'price'

class AboutPageView(ListView):
    model = Pricing
    template_name = 'pages/about.html'
    context_object_name = 'price'

class MembersPageView(TemplateView):
    template_name = 'pages/members.html'

class PortfolioPageView(TemplateView):
    template_name = 'pages/portfolio.html'

class PricingPageView(TemplateView):
    template_name = 'pages/pricing.html'
    
class Error404PageView(TemplateView):
    template_name ='pages/error404.html'

class FaqPageView(TemplateView):
    template_name = 'pages/faq.html'

class TermsConditionPageView(TemplateView):
    template_name = 'pages/terms-condition.html'

class PrivacyPolicyPageView(TemplateView):
    template_name = 'pages/privacy-policy.html'

class ServicesPageView(ListView):
    model = Service
    template_name = 'pages/services.html'
    context_object_name = 'services'
    paginate_by = 6

class ServiceDetailsPageView(DetailView):
    model = Service
    template_name = 'pages/service-details.html'
    context_object_name = 'service'

class TestimonialPageView(TemplateView):
    template_name = 'pages/testimonial.html'

class BlogPageView(ListView):
    model = Blog
    template_name = 'pages/blog.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(
            post_count=Count('blogs')
        )
        return context

class BlogDetailPageView(DetailView):
    model = Blog
    template_name = 'pages/blog-details.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        context['categories'] = Category.objects.annotate(
            post_count=Count('blogs')
        )
        context['last_posts'] = Blog.objects.order_by('-created_at')
        context["prev_post"] = Blog.objects.filter(
            created_at__lt=post.created_at
        ).order_by('-created_at').first()
        context["next_post"] = Blog.objects.filter(
            created_at__gt=post.created_at
        ).order_by('created_at').first()

        context['form'] = CommentForm()
        context['comments'] = post.comments.order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            messages.error(request, "Kamentariya yozish uchun oldin login qiling!")
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.user = request.user
            comment.save()
            return redirect('blog_details', slug=self.object.slug)
        return self.render_to_response(self.get_context_data(form=form))

class ContactPageView(ListView):
    model = Contact
    template_name = 'pages/contact.html'
    context_object_name = 'contacts'

class Sign_inPageView(TemplateView):
    template_name = 'pages/sign-in.html'

class Sign_upPageView(TemplateView):
    template_name = 'pages/sign-up.html'

class Recover_passwordPageView(TemplateView):
    template_name = 'pages/recover-password.html'

class FooterPageView(ListView):
    model = Service
    template_name = 'pages/layouts/footer.html'
    context_object_name = 'services'
    paginate_by = 6