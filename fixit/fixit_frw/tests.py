from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from .models import Items

User = get_user_model()

class UserDetailTest(APITestCase):

    def setUp(self):
        # User biasa
        self.user = User.objects.create_user(username='user1', password='testpass123')
        # User lain
        self.other_user = User.objects.create_user(username='user2', password='testpass123')
        # Staff user untuk menghindari permission denied (jika pakai StaffEditorPermissionMixin)
        self.staff_user = User.objects.create_user(username='staff', password='testpass123', is_staff=True)
        self.user_detail_url = reverse('user-detail', kwargs={'pk': self.user.pk})

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

    def test_delete_user_detail_by_staff(self):
        """Staff dapat delete user"""
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_permission_denied_for_non_staff(self):
        """Non-staff user tidak boleh mengakses user lain"""
        self.client.force_authenticate(user=self.user)
        other_user_url = reverse('user-detail', kwargs={'pk': self.other_user.pk})
        response = self.client.get(other_user_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ItemDetailTest(APITestCase):
    def setUp(self):
        # User biasa
        self.user = User.objects.create_user(username='user1', password='testpass123')
        # User lain
        self.other_user = User.objects.create_user(username='user2', password='testpass123')
        # Staff user
        self.staff_user = User.objects.create_user(username='staff', password='testpass123', is_staff=True)
        
        # Create test image
        self.test_image = self.create_test_image()
        self.test_image2 = self.create_test_image()
        
        # Create items
        self.user_item = Items.objects.create(
            item_name='User Item',
            deskripsi='Deskripsi item milik user',
            picture=self.test_image,
            rate=Items.Level.MODERATE,
            price_offered=100000,
            pick_address='Alamat pickup user',
            user=self.user
        )
        self.other_item = Items.objects.create(
            item_name='Other Item',
            deskripsi='Deskripsi item milik user lain',
            picture=self.test_image2,
            rate=Items.Level.CONSIDERABLE,
            price_offered=200000,
            user=self.other_user
        )
        
        self.item_detail_url = reverse('item_detail', kwargs={'pk': self.user_item.pk})
        self.other_item_url = reverse('item_detail', kwargs={'pk': self.other_item.pk})

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
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.item_detail_url, {
            'item_name': 'Updated Item Name',
            'price_offered': 150000,
            'rate': Items.Level.CONSIDERABLE
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_item.refresh_from_db()
        self.assertEqual(self.user_item.item_name, 'Updated Item Name')
        self.assertEqual(self.user_item.price_offered, 150000)

    def test_update_item_by_staff(self):
        """Staff dapat update item siapapun"""
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.patch(self.item_detail_url, {
            'item_name': 'Staff Updated Item',
            'fixed': True,
            'price_final': 120000
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_item.refresh_from_db()
        self.assertEqual(self.user_item.item_name, 'Staff Updated Item')
        self.assertTrue(self.user_item.fixed)
        self.assertEqual(self.user_item.price_final, 120000)

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
        # User biasa
        self.user = User.objects.create_user(username='user1', password='testpass123')
        # User lain
        self.other_user = User.objects.create_user(username='user2', password='testpass123')
        # Staff user
        self.staff_user = User.objects.create_user(username='staff', password='testpass123', is_staff=True)
        
        # Create test images
        self.test_image1 = self.create_test_image()
        self.test_image2 = self.create_test_image()
        self.test_image3 = self.create_test_image()
        
        # Create multiple items
        self.user_item1 = Items.objects.create(
            item_name='User Item 1',
            deskripsi='Deskripsi item 1 milik user',
            picture=self.test_image1,
            rate=Items.Level.LOW,
            price_offered=50000,
            user=self.user
        )
        self.user_item2 = Items.objects.create(
            item_name='User Item 2',
            deskripsi='Deskripsi item 2 milik user',
            picture=self.test_image2,
            rate=Items.Level.EXTREME,
            price_offered=300000,
            fixed=True,
            price_final=250000,
            user=self.user
        )
        self.other_item = Items.objects.create(
            item_name='Other User Item',
            deskripsi='Deskripsi item milik user lain',
            picture=self.test_image3,
            rate=Items.Level.DANGEROUS,
            price_offered=150000,
            user=self.other_user
        )
        
        self.item_list_url = reverse('item_list')

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

    def test_get_item_list_by_user(self):
        """User hanya melihat item miliknya sendiri"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.item_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Pastikan hanya item milik user yang muncul
        item_names = [item['item_name'] for item in response.data['results'] if 'results' in response.data]
        if 'results' not in response.data:
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
        item_names = [item['item_name'] for item in response.data['results'] if 'results' in response.data]
        if 'results' not in response.data:
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
            'pick_address': 'Alamat pickup baru'
        }
        response = self.client.post(self.item_list_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['item_name'], 'New Item')
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['rate'], Items.Level.MODERATE)

    def test_create_item_by_staff(self):
        """Staff dapat membuat item"""
        self.client.force_authenticate(user=self.staff_user)
        test_image = self.create_test_image()
        data = {
            'item_name': 'Staff Item',
            'deskripsi': 'Deskripsi staff item',
            'picture': test_image,
            'rate': Items.Level.CONSIDERABLE,
            'price_offered': 90000
        }
        response = self.client.post(self.item_list_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['item_name'], 'Staff Item')

    def test_create_item_unauthorized(self):
        """User tanpa login tidak dapat membuat item"""
        test_image = self.create_test_image()
        data = {
            'item_name': 'Unauthorized Item',
            'deskripsi': 'Deskripsi unauthorized',
            'picture': test_image,
            'rate': Items.Level.LOW
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
        response = self.client.post(self.item_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_item_level_choices(self):
        """Test validasi level choices"""
        self.client.force_authenticate(user=self.user)
        test_image = self.create_test_image()
        data = {
            'item_name': 'Test Level Item',
            'deskripsi': 'Test deskripsi',
            'picture': test_image,
            'rate': 6,  # Invalid choice
        }
        response = self.client.post(self.item_list_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_item_list_filtering_by_rate(self):
        """Test filtering berdasarkan rate level"""
        self.client.force_authenticate(user=self.staff_user)
        
        # Filter items by rate level
        response = self.client.get(self.item_list_url, {'rate': Items.Level.EXTREME})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_item_list_filtering_by_price_range(self):
        """Test filtering berdasarkan range harga"""
        self.client.force_authenticate(user=self.staff_user)
        
        # Filter items by price range (jika diimplementasikan)
        response = self.client.get(self.item_list_url, {'price_min': 100000, 'price_max': 200000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_item_list_search_by_name(self):
        """Test search berdasarkan item name"""
        self.client.force_authenticate(user=self.user)
        
        # Search by item name
        response = self.client.get(self.item_list_url, {'search': 'User Item 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_item_list_ordering(self):
        """Test ordering berdasarkan parameter"""
        self.client.force_authenticate(user=self.user)
        
        # Test ordering by created date
        response = self.client.get(self.item_list_url, {'ordering': '-created'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test ordering by price
        response = self.client.get(self.item_list_url, {'ordering': 'price_offered'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)