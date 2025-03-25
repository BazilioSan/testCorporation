from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from e_net.models import Contact, Product, NetworkNode


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "country", "city", "street", "house_number")
    search_fields = ("country", "city", "email")
    list_filter = ("country", "city")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "release_date")
    search_fields = ("name", "model")
    list_filter = ("release_date",)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ("name", "level_display", "supplier_link", "debt", "created_at")
    list_filter = ("contact__city", "level")
    search_fields = ("name", "contact__country", "contact__city")
    actions = ["clear_debt"]
    filter_horizontal = ("products",)

    def level_display(self, obj):
        return obj.get_level_display()

    level_display.short_description = "Уровень"

    def supplier_link(self, obj):
        if obj.supplier:
            url = reverse("admin:e_net_networknode_change", args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier)
        return "-"

    supplier_link.short_description = "Поставщик"
    supplier_link.allow_tags = True

    def clear_debt(self, request, queryset):
        updated = queryset.update(debt=0)
        self.message_user(request, f"Задолженность очищена для {updated} объектов")

    clear_debt.short_description = "Очистить задолженность у выбранных объектов"
