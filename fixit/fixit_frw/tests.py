from django.test import TestCase

from django.utils import timezone
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from PIL import Image
import io
from .models import Items, User, Address, Payments
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
import uuid

User = get_user_model()


class SignupTest(APITestCase):

    def setUp(self):
        self.signup_url = reverse('fixit_frw:SignUpView')
        # Create a test address for signup
        self.test_address = Address.objects.create(
            province='Jawa Tengah',
            city='Semarang',
            street='Jalan Test'
        )

    def create_test_image(self):
        """Create a valid test JPEG image"""
        return SimpleUploadedFile(
            name='test_profile.jpg',
            content=b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xff\xd9',
            content_type='image/jpeg'
        )

    def test_signup_success(self):
        """Test successful user signup with all fields"""
        test_image = self.create_test_image()
        unique_email = f'user{uuid.uuid4()}@gmail.com'
        unique_username = f'User_{uuid.uuid4().hex[:8]}'

        data = {
            'username': unique_username,
            'email': unique_email,
            'phone': '0889343987',
            'address_id': self.test_address.address_id,
            'profile_pict': test_image,
            'password1': 'userpekok123',
            'password2': 'userpekok123',
        }

        response = self.client.post(self.signup_url, data, format='multipart')

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], unique_username)
        self.assertEqual(response.data['email'], unique_email)
        self.assertEqual(response.data['phone'], '0889343987')
        self.assertEqual(response.data['address_id'], self.test_address.address_id)

        # Verify user was created in database
        user_exists = User.objects.filter(username=unique_username).exists()
        self.assertTrue(user_exists)

        # Verify user can authenticate with the password
        user = User.objects.get(username=unique_username)
        self.assertTrue(user.check_password('userpekok123'))

    def test_signup_password_mismatch(self):
        """Test signup fails when passwords don't match"""
        test_image = self.create_test_image()
        unique_email = f'user{uuid.uuid4()}@gmail.com'

        data = {
            'username': f'User_{uuid.uuid4().hex[:8]}',
            'email': unique_email,
            'phone': '0889343987',
            'address_id': self.test_address.address_id,
            'profile_pict': test_image,
            'password1': 'userpekok123',
            'password2': 'differentpassword',
        }

        response = self.client.post(self.signup_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_duplicate_email(self):
        """Test signup fails with duplicate email"""
        # Create first user
        User.objects.create_user(
            username='existing_user',
            email='duplicate@gmail.com',
            password='password123',
            address_id=self.test_address,
            profile_pict=self.create_test_image()
        )

        test_image = self.create_test_image()
        data = {
            'username': 'new_user',
            'email': 'duplicate@gmail.com',  # Same email
            'phone': '0889343987',
            'address_id': self.test_address.address_id,
            'profile_pict': test_image,
            'password1': 'userpekok123',
            'password2': 'userpekok123',
        }

        response = self.client.post(self.signup_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_duplicate_phone(self):
        """Test signup fails with duplicate email"""
        # Create first user
        User.objects.create_user(
            username='existing_user',
            email='user1@gmail.com',
            phone='0889343987',
            password='password123',
            address_id=self.test_address,
            profile_pict=self.create_test_image()
        )

        test_image = self.create_test_image()
        data = {
            'username': 'new_user',
            'email': 'newuser@gmail.com',  # Same email
            'phone': '0889343987',
            'address_id': self.test_address.address_id,
            'profile_pict': test_image,
            'password1': 'userpekok123',
            'password2': 'userpekok123',
        }

        response = self.client.post(self.signup_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalid_file_type(self):
        """Test signup fails with invalid file type"""
        invalid_file = SimpleUploadedFile(
            name='test.txt',
            content=b'This is not an image',
            content_type='text/plain'
        )

        data = {
            'username': f'User_{uuid.uuid4().hex[:8]}',
            'email': f'user{uuid.uuid4()}@gmail.com',
            'phone': '0889343987',
            'address_id': self.test_address.address_id,
            'profile_pict': invalid_file,
            'password1': 'userpekok123',
            'password2': 'userpekok123',
        }

        response = self.client.post(self.signup_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_missing_required_fields(self):
        """Test signup fails when required fields are missing"""
        data = {
            'username': 'incomplete_user',
            # Missing email, phone, address_id, profile_pict
            'password1': 'userpekok123',
            'password2': 'userpekok123',
        }

        response = self.client.post(self.signup_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        """Clean up after tests"""
        # Clean up uploaded files and test data
        pass

class UserDetailTest(APITestCase):

    def setUp(self):
        # Create test addresses
        self.test_address1 = Address.objects.create(
            province='Jawa Tengah',
            city='Solo',
            street='Jalan User1'
        )
        self.test_address2 = Address.objects.create(
            province='Jawa Timur',
            city='Surabaya',
            street='Jalan User2'
        )

        # Create test image
        test_image = self.create_test_image()

        # User biasa
        self.user = User.objects.create_user(
            username='user1',
            password='testpass123',
            email='user1@test.com',
            address_id=self.test_address1,
            profile_pict=test_image
        )
        # User lain
        self.other_user = User.objects.create_user(
            username='user2',
            password='testpass123',
            email='user2@test.com',
            address_id=self.test_address2,
            profile_pict=self.create_test_image()
        )
        # Staff user
        self.staff_user = User.objects.create_user(
            username='staff',
            password='testpass123',
            email='staff@test.com',
            is_staff=True,
            address_id=self.test_address1,
            profile_pict=self.create_test_image()
        )
        self.user_detail_url = reverse('fixit_frw:user-detail', kwargs={'pk': self.user.pk})

    def create_test_image(self):
        """Helper method to create test image"""
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        return SimpleUploadedFile(
            name='test_image.jpg',
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )

    def test_get_user_detail_unauthorized(self):
        """Test akses tanpa login"""
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_detail_with_staff(self):
        """Test akses dengan user staff"""
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_get_own_user_detail(self):
        """Test user dapat melihat detail dirinya sendiri"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_permission_denied_for_other_user(self):
        """User lain tidak boleh mengakses detail user"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_detail_by_staff(self):
        """Staff dapat update data user"""
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.patch(self.user_detail_url, {
            'username': 'updated_user1',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updated_user1')

    def test_update_own_user_detail(self):
        """User dapat update data dirinya sendiri"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.user_detail_url, {
            'username': 'self_updated_user1',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'self_updated_user1')

    def test_permission_denied_for_non_staff(self):
        """Non-staff user tidak boleh mengakses user lain"""
        self.client.force_authenticate(user=self.user)
        # other_user_url = reverse('user-detail', kwargs={'pk': self.other_user.pk})
        other_user_url = f"/user/{self.other_user.pk}"
        response = self.client.get(other_user_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ItemDetailTest(APITestCase):
    def setUp(self):
        # Create test addresses
        self.test_address1 = Address.objects.create(
            province='Jawa Tengah',
            city='Yogyakarta',
            street='Jalan Malioboro'
        )
        self.test_address2 = Address.objects.create(
            province='Jawa Barat',
            city='Bandung',
            street='Jalan Asia Afrika'
        )

        # User biasa
        self.user = User.objects.create_user(
            username='user1',
            password='testpass123',
            email='user1@test.com',
            address_id=self.test_address1,
            profile_pict=self.create_test_image()
        )
        # User lain
        self.other_user = User.objects.create_user(
            username='user2',
            password='testpass123',
            email='user2@test.com',
            address_id=self.test_address2,
            profile_pict=self.create_test_image()
        )
        # Staff user
        self.staff_user = User.objects.create_user(
            username='staff',
            password='testpass123',
            email='staff@test.com',
            is_staff=True,
            address_id=self.test_address1,
            profile_pict=self.create_test_image()
        )

        # Create items
        self.user_item = Items.objects.create(
            item_name='User Item',
            deskripsi='Deskripsi item milik user',
            picture=self.create_test_image(),
            rate=Items.Level.MODERATE,
            price_offered=100000,
            address_id=self.test_address1,
            user=self.user
        )
        self.other_item = Items.objects.create(
            item_name='Other Item',
            deskripsi='Deskripsi item milik user lain',
            picture=self.create_test_image(),
            rate=Items.Level.CONSIDERABLE,
            price_offered=200000,
            address_id=self.test_address2,
            user=self.other_user
        )

        self.item_detail_url = reverse('fixit_frw:item_detail', kwargs={'pk': self.user_item.pk})
        self.other_item_url = reverse('fixit_frw:item_detail', kwargs={'pk': self.other_item.pk})

    def create_test_image(self):
        """Helper method untuk membuat test image"""
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        return SimpleUploadedFile(
            name='test_image.jpg',
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )

    def test_get_item_detail_unauthorized(self):
        """Test akses tanpa login"""
        response = self.client.get(self.item_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_item_detail_by_owner(self):
        """Owner dapat melihat item miliknya"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.item_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['item_name'], self.user_item.item_name)
        self.assertEqual(response.data['rate'], self.user_item.rate)

    def test_get_item_detail_by_staff(self):
        """Staff dapat melihat item siapapun"""
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(self.item_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['item_name'], self.user_item.item_name)

    def test_permission_denied_for_other_user(self):
        """User lain tidak boleh mengakses item"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.item_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_item_by_owner(self):
        """Owner dapat update item miliknya"""
        test_image = SimpleUploadedFile(
            name='test.jpg',
            content=b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xff\xd9',
            content_type='image/jpeg'
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            self.item_detail_url,
            {
                'item_name': 'Updated Item Name',
                'picture': test_image,
                'price_offered': 150000,
                'rate': Items.Level.CONSIDERABLE
            },
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_item.refresh_from_db()
        self.assertEqual(self.user_item.item_name, 'Updated Item Name')
        self.assertEqual(self.user_item.price_offered, 150000)

    def test_update_item_by_staff(self):
        """Staff dapat update item miliknya"""
        test_image = SimpleUploadedFile(
            name='test.jpg',
            content=b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xff\xd9',
            content_type='image/jpeg'
        )

        self.client.force_authenticate(user=self.staff_user)
        response = self.client.patch(
            self.item_detail_url,
            {
                'item_name': 'Barang Bobrok',
                'picture': test_image,
                'deskripsi': 'wis dadi lo',
                'price_final': 40000
            },
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_item.refresh_from_db()
        self.assertEqual(self.user_item.item_name, 'Barang Bobrok')
        self.assertEqual(self.user_item.deskripsi, 'wis dadi lo')
        self.assertEqual(self.user_item.price_final, 40000)

    def test_update_item_with_image(self):
        """Test update item dengan gambar baru"""
        self.client.force_authenticate(user=self.user)
        new_image = self.create_test_image()
        response = self.client.patch(self.item_detail_url, {
            'item_name': 'Item with New Image',
            'picture': new_image
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_item.refresh_from_db()
        self.assertEqual(self.user_item.item_name, 'Item with New Image')

    def test_delete_item_by_owner(self):
        """Owner dapat delete item miliknya"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.item_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Items.objects.filter(pk=self.user_item.pk).exists())

    def test_delete_item_by_staff(self):
        """Staff dapat delete item siapapun"""
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(self.other_item_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Items.objects.filter(pk=self.other_item.pk).exists())


class ItemListTest(APITestCase):
    def setUp(self):
        # Create test addresses
        self.test_address1 = Address.objects.create(
            province='Jawa Tengah',
            city='Semarang',
            street='Jalan Pemuda'
        )
        self.test_address2 = Address.objects.create(
            province='Jawa Timur',
            city='Malang',
            street='Jalan Ijen'
        )

        # User biasa
        self.user = User.objects.create_user(
            username='user1',
            password='testpass123',
            email='user1@test.com',
            address=self.test_address1,
            profile_pict=self.create_test_image()
        )
        # User lain
        self.other_user = User.objects.create_user(
            username='user2',
            password='testpass123',
            email='user2@test.com',
            address=self.test_address2,
            profile_pict=self.create_test_image()
        )
        # Staff user
        self.staff_user = User.objects.create_user(
            username='staff',
            password='testpass123',
            email='staff@test.com',
            is_staff=True,
            address=self.test_address1,
            profile_pict=self.create_test_image()
        )

        # Create multiple items
        self.user_item1 = Items.objects.create(
            item_name='User Item 1',
            deskripsi='Deskripsi item 1 milik user',
            picture=self.create_test_image(),
            rate=Items.Level.LOW,
            price_offered=50000,
            address=self.test_address1,
            user=self.user
        )
        self.user_item2 = Items.objects.create(
            item_name='User Item 2',
            deskripsi='Deskripsi item 2 milik user',
            picture=self.create_test_image(),
            rate=Items.Level.EXTREME,
            price_offered=300000,
            fixed=True,
            price_final=250000,
            address=self.test_address1,
            user=self.user
        )
        self.other_item = Items.objects.create(
            item_name='Other User Item',
            deskripsi='Deskripsi item milik user lain',
            picture=self.create_test_image(),
            rate=Items.Level.DANGEROUS,
            price_offered=150000,
            address=self.test_address2,
            user=self.other_user
        )

        self.item_list_url = reverse('fixit_frw:item_list')

    def create_test_image(self):
        """Helper method untuk membuat test image"""
        image = Image.new('RGB', (100, 100), color='blue')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        return SimpleUploadedFile(
            name='test_image.jpg',
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )

    def test_get_item_list_unauthorized(self):
        """Test akses list tanpa login"""
        response = self.client.get(self.item_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_item_idx_unauthorized(self):
        """Test akses index item tanpa login harus redirect ke login"""
        response = self.client.get(reverse('fixit_frw:item_idx'))
        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse('fixit_frw:item_idx')}"
        )

    def test_get_item_list_by_user(self):
        """User hanya melihat item miliknya sendiri"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.item_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Pastikan hanya item milik user yang muncul
        if 'results' in response.data:
            item_names = [item['item_name'] for item in response.data['results']]
        else:
            item_names = [item['item_name'] for item in response.data]

        self.assertIn('User Item 1', item_names)
        self.assertIn('User Item 2', item_names)
        self.assertNotIn('Other User Item', item_names)

    def test_get_item_list_by_staff(self):
        """Staff dapat melihat semua item"""
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(self.item_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Staff melihat semua item

        # item_names = [item['item_name'] for item in response.data['results'] if 'results' in response.data]
        # if 'results' not in response.data:
        #     item_names = [item['item_name'] for item in response.data]

        if 'results' in response.data:
            item_names = [item['item_name'] for item in response.data['results']]
        else:
            item_names = [item['item_name'] for item in response.data]

        self.assertIn('User Item 1', item_names)
        self.assertIn('User Item 2', item_names)
        self.assertIn('Other User Item', item_names)

    def test_create_item_by_user(self):
        """User dapat membuat item baru"""
        self.client.force_authenticate(user=self.user)
        test_image = self.create_test_image()
        data = {
            'item_name': 'New Item',
            'deskripsi': 'Deskripsi item baru',
            'picture': test_image,
            'rate': Items.Level.MODERATE,
            'price_offered': 75000,
            'address': self.test_address1
        }
        response = self.client.post(self.item_list_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['item_name'], 'New Item')
        self.assertEqual(response.data['rate'], Items.Level.MODERATE)
        self.assertEqual(response.data['address']['street'],  "Jalan Pemuda")

    def test_create_item_by_staff(self):
        """Staff dapat membuat item"""
        self.client.force_authenticate(user=self.staff_user)
        test_image = self.create_test_image()
        data = {
            'item_name': 'Staff Item',
            'deskripsi': 'Deskripsi staff item',
            'picture': test_image,
            'rate': Items.Level.CONSIDERABLE,
            'price_offered': 90000,
            'address': self.test_address1
        }
        response = self.client.post(self.item_list_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['item_name'], 'Staff Item')
        self.assertEqual(response.data['address']['street'], "Jalan Pemuda")

    def test_create_item_unauthorized(self):
        """User tanpa login tidak dapat membuat item"""
        test_image = self.create_test_image()
        data = {
            'item_name': 'Unauthorized Item',
            'deskripsi': 'Deskripsi unauthorized',
            'picture': test_image,
            'rate': Items.Level.LOW,
            'address': self.test_address1
        }
        response = self.client.post(self.item_list_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_item_without_required_fields(self):
        """Test validasi field yang required"""
        self.client.force_authenticate(user=self.user)
        # Missing required fields: picture and deskripsi
        data = {
            'item_name': 'Incomplete Item',
            'rate': Items.Level.LOW
        }
        response = self.client.post(self.item_list_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_input(self):
        self.client.force_authenticate(user=self.user)
        test_image = self.create_test_image()
        data = {
            'item_name': 'Unauthorized Item',
            'deskripsi': 'Deskripsi unauthorized',
            'picture': test_image,
            'rate': Items.Level.LOW,
            'address_id': self.test_address1.address_id,
            'price_offered': -9,
        }
        response = self.client.post(self.item_list_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Cek field dan pesan error-nya
        self.assertIn('price_offered', response.data)
        self.assertEqual(
            str(response.data['price_offered'][0]),
            "price offered must be greater than 0"
        )

    def test_item_with_payment_address(self):
        self.client.force_authenticate(user=self.user)
        test_image = self.create_test_image()
        data = {
            'item_name': 'Payment Item',
            'deskripsi': 'Deskripsi item payment',
            'picture': test_image,
            'rate': Items.Level.LOW,
            'address_data.province': 'Jawa Utara',
            'address_data.city': 'Semarang',
            'address_data.street': 'Jalan Terboyo 45',
            'payment_data.method' : "GOPAY",
            'payment_data.amount' : 150000
        }

        response = self.client.post(self.item_list_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Ambil item yang baru dibuat
        item = Items.objects.get(item_name='Payment Item')

        # Pastikan item punya relasi payment
        self.assertIsNotNone(item.payment)
        self.assertIsNotNone(item.address)

        # Cek isi payment terkait
        payment = Payments.objects.get(payment_id=item.payment_id)

        self.assertEqual(item.payment.method, payment.method)
        self.assertEqual(item.payment.amount, payment.amount)
        self.assertEqual(item.payment.amount, 150000)
        self.assertEqual(item.payment.method, "GOPAY")

        # Cek Alamat
        address = Address.objects.get(address_id=item.address_id)

        self.assertEqual(address.province, "Jawa Utara")
        self.assertEqual(address.city, "Semarang")
        self.assertEqual(address.street, "Jalan Terboyo 45")
        self.assertEqual(address.street, item.address.street)

        # Cek bahwa user adalah pemilik item
        self.assertEqual(item.user, self.user)

    def test_item_with_payment_address_invalid(self):
        self.client.force_authenticate(user=self.user)
        test_image = self.create_test_image()
        data = {
            'item_name': 'Payment Item',
            'deskripsi': 'Deskripsi item payment',
            'picture': test_image,
            'rate': Items.Level.LOW,
            'price_offered' : 200000,
            'address_data.province': 'Jawa Utara',
            'address_data.city': 'Semarang',
            'address_data.street': 'Jalan Terboyo 45',
            'payment_data.method' : "GOPAY",
            'payment_data.amount' : 150000
        }

        response = self.client.post(self.item_list_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Ambil item yang baru dibuat
        item = Items.objects.get(item_name='Payment Item')

        # mengeset price final
        item.price_final = item.price_offered
        item.save()

        # Test error price final dan amount

        # Cek bahwa user adalah pemilik item
        self.assertEqual(item.user, self.user)


class PaymentTest(APITestCase):

    def setUp(self):
        self.time_before_create = timezone.now()
        self.payment1 = Payments.objects.create(
            method='GOPAY',
            amount=30000
        )

    def test_get_first_payment(self):
        payment = Payments.objects.first()

        self.assertIsNotNone(payment.payment_id)
        self.assertEqual(payment, self.payment1)
        self.assertEqual(payment.amount, 30000)
        self.assertEqual(payment.method, 'GOPAY')

    def test_auto_date(self):
        """Test auto generate time"""
        payment = Payments.objects.first()
        after_create = timezone.now()

        self.assertLessEqual(payment.date, after_create)
        self.assertGreaterEqual(payment.date, self.time_before_create)
        self.assertIsNotNone(payment.date)

    def test_method_choices(self):
        """Test semua pilihan method payment"""
        # Test GOPAY
        payment_gopay = Payments.objects.create(
            method=Payments.Method.GOPAY,
            amount=50000
        )
        self.assertEqual(payment_gopay.method, "GOPAY")

        # Test COD
        payment_cod = Payments.objects.create(
            method=Payments.Method.COD,
            amount=25000
        )
        self.assertEqual(payment_cod.method, "COD")

    def test_invalid_method_choice(self):
            """Test error ketika menggunakan method yang tidak valid"""
            with self.assertRaises(ValidationError):
                payment = Payments(method="INVALID_METHOD", amount=100000)
                payment.full_clean()

    def test_multiple_payments_creation(self):
        """Test membuat beberapa payment sekaligus"""
        payments_data = [
            {'method': Payments.Method.GOPAY, 'amount': 50000},
            {'method': Payments.Method.TRANSFER, 'amount': 75000},
            {'method': Payments.Method.COD, 'amount': 100000},
        ]

        for data in payments_data:
            Payments.objects.create(**data)

        self.assertEqual(Payments.objects.count(), 4)

        # Pastikan semua payment_id unik
        payment_ids = list(Payments.objects.values_list('payment_id', flat=True))
        self.assertEqual(len(payment_ids), len(set(payment_ids)))

class MathTest(APITestCase):
    def test_kuadrat(self):
        response = self.client.post(reverse('fixit_frw:kuadrat'), {'value': 100}, format='json')
        self.assertEqual(response.data['kuadrat'], 10000)

    def test_kuadrat_invalid(self):
        response = self.client.post(reverse('fixit_frw:kuadrat'), {'value': 'abc'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'value harus berupa angka'})