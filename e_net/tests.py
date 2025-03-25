from django.test import TestCase
from django.core.exceptions import ValidationError
from e_net.models import Contact, Product, NetworkNode

"1. Тесты моделей"


class ContactModelTest(TestCase):
    """Тестирование модели Contact (контактная информация)"""

    def setUp(self):
        """Подготовка тестовых данных для контактов"""
        self.contact_data = {
            "email": "test@example.com",
            "country": "Россия",
            "city": "Москва",
            "street": "Ленина",
            "house_number": "10",
        }

    def test_contact_creation(self):
        """Проверка корректного создания контакта и строкового представления"""
        contact = Contact.objects.create(**self.contact_data)
        self.assertEqual(contact.email, "test@example.com")
        self.assertEqual(str(contact), "Россия, Москва, Ленина, 10")


class ProductModelTest(TestCase):
    """Тестирование модели Product (продукты)"""

    def setUp(self):
        """Подготовка тестовых данных для продуктов"""
        self.product_data = {
            "name": "Смартфон",
            "model": "X100",
            "release_date": "2023-01-01",
        }

    def test_product_creation(self):
        """Проверка создания продукта и его строкового представления"""
        product = Product.objects.create(**self.product_data)
        self.assertEqual(product.name, "Смартфон")
        self.assertEqual(str(product), "Смартфон (X100)")


class NetworkNodeModelTest(TestCase):
    """Тестирование модели NetworkNode (звено сети)"""

    def setUp(self):
        """Подготовка тестовых данных для звеньев сети"""
        # Создаем уникальные контакты для разных уровней сети
        self.factory_contact = Contact.objects.create(
            email="factory@example.com",
            country="Россия",
            city="Москва",
            street="Ленина",
            house_number="1",
        )
        self.retail_contact = Contact.objects.create(
            email="retail@example.com",
            country="Россия",
            city="Санкт-Петербург",
            street="Невский",
            house_number="10",
        )
        self.entrepreneur_contact = Contact.objects.create(
            email="entrepreneur@example.com",
            country="Россия",
            city="Казань",
            street="Баумана",
            house_number="5",
        )

        # Создаем тестовые продукты
        self.product1 = Product.objects.create(
            name="Ноутбук", model="N200", release_date="2023-01-01"
        )
        self.product2 = Product.objects.create(
            name="Смартфон", model="S300", release_date="2023-02-01"
        )

    def test_factory_creation(self):
        """Проверка создания завода (уровень 0) без поставщика"""
        factory = NetworkNode.objects.create(
            name="Завод 1", level=0, contact=self.factory_contact
        )
        factory.products.add(self.product1)

        self.assertEqual(factory.level, 0, "Завод должен иметь уровень 0")
        self.assertEqual(factory.get_level_display(), "Завод")
        self.assertEqual(factory.products.count(), 1, "Завод должен иметь продукты")
        self.assertIsNone(factory.supplier, "У завода не должно быть поставщика")

    def test_retail_network_creation(self):
        """Проверка создания розничной сети (уровень 1) с поставщиком-заводом"""
        factory = NetworkNode.objects.create(
            name="Завод 1", level=0, contact=self.factory_contact
        )

        retail = NetworkNode.objects.create(
            name="Розничная сеть 1",
            level=1,
            contact=self.retail_contact,
            supplier=factory,
        )

        self.assertEqual(retail.level, 1, "Розничная сеть должна иметь уровень 1")
        self.assertEqual(retail.supplier, factory, "Поставщик должен быть заводом")

    def test_level_auto_assignment(self):
        """Проверка автоматического определения уровня при создании"""
        factory = NetworkNode.objects.create(
            name="Завод 1", level=0, contact=self.factory_contact
        )

        retail = NetworkNode.objects.create(
            name="Розничная сеть 1",
            contact=self.retail_contact,
            supplier=factory,  # Уровень должен установиться автоматически
        )

        self.assertEqual(retail.level, 1, "Уровень должен быть на 1 выше поставщика")

    def test_debt_precision(self):
        """Проверка точности хранения задолженности (до копеек)"""
        factory = NetworkNode.objects.create(
            name="Завод 1", level=0, contact=self.factory_contact, debt=123.45
        )
        self.assertEqual(
            factory.debt, 123.45, "Должен сохраняться точный размер задолженности"
        )

    def test_unique_contact_per_node(self):
        """Проверка, что один контакт может принадлежать только одному звену сети"""
        NetworkNode.objects.create(
            name="Завод 1", level=0, contact=self.factory_contact
        )

        with self.assertRaises(
            Exception, msg="Нельзя создать два звена с одним контактом"
        ):
            NetworkNode.objects.create(
                name="Завод 2", level=0, contact=self.factory_contact  # Тот же контакт
            )
