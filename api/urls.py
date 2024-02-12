from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductsViewSet)
router.register('register', views.AccountViewSet)
router.register('categories', views.CategoryViewSet)
router.register('product/buy', views.OrderViewSet)
router.register('user', views.UserOrdersViewSet)

urlpatterns = router.urls