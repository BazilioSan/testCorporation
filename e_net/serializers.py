from rest_framework import serializers
from e_net.models import NetworkNode, Product, Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class NetworkNodeSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    products = ProductSerializer(many=True)
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=NetworkNode.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = NetworkNode
        fields = "__all__"
        read_only_fields = ("debt", "created_at")

    def validate(self, data):
        supplier = data.get("supplier")
        level = data.get("level")

        if supplier and level is not None:
            if level != supplier.level + 1:
                raise serializers.ValidationError(
                    "Уровень должен быть на 1 выше уровня поставщика"
                )
        return data

    def create(self, validated_data):
        contact_data = validated_data.pop("contact")
        products_data = validated_data.pop("products")

        contact = Contact.objects.create(**contact_data)
        network_node = NetworkNode.objects.create(contact=contact, **validated_data)

        for product_data in products_data:
            product, _ = Product.objects.get_or_create(**product_data)
            network_node.products.add(product)

        return network_node
