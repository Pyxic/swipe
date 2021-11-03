import io

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from account.models import User
from building.models import ResidentialComplex, Announcement


class ResidentialComplexTests(APITestCase):
    def setUp(self) -> None:
        user_test1 = User.objects.create_user(email="test@user.com", password="@sdfw3dfg", role_id=1)
        user_test_client = User.objects.create_user(email="test@client.com", password="Zaqqwe123", role_id=2)
        admin = User.objects.create_superuser(email='test@admin.com', password='pass12345')
        user_test1.save()
        user_test_client.save()
        admin.save()
        self.first_complex = ResidentialComplex.objects.create(
            name='House', district='district', microdistrict='microdistrict', price_for_meter=14,
            min_area=14, max_area=60, frame_quantity=4, level_quantity=5, section_quantity=3, riser_quantity=10,
            status=ResidentialComplex.StatusComplex.flats, house_type=ResidentialComplex.HouseType.apartment_house,
            house_class=ResidentialComplex.HouseClass.new, house_territory=ResidentialComplex.HouseTerritory.closed,
            user=user_test1
        )

        self.data = {
            'name': 'House',
            'district': 'district',
            'microdistrict': 'microdistrict',
            'min_area': 14,
            'max_area': 18,
            'level_quantity': 2,
            'section_quantity': 4,
            'riser_quantity': 10,
            'price_for_meter': 14,
            'frame_quantity': 5,
        }

        image = io.BytesIO()
        Image.new('RGB', (1152, 2048)).save(image, 'JPEG')
        image.seek(0)
        image_file = SimpleUploadedFile('image.jpg', image.getvalue())
        self.announcement_data = {
            'address': 'address',
            'foundation_document': Announcement.FoundationDocument.own,
            'room_quantity': 1,
            'layout': Announcement.AnnouncementLayout.studio,
            'living_condition': Announcement.LivingCondition.new,
            'area': 50,
            'kitchen_area': 20,
            'agent_commission': 10,
            'communication_method': Announcement.CommunicationMethod.message,
            'description': 'test',
            'price': 100000,
            'user': user_test_client,
        }
        self.first_announcement = Announcement.objects.create(**self.announcement_data)
        self.announcement_data['user'] = user_test_client.id
        self.announcement_data['photo'] = image_file
        self.user_test1_token = Token.objects.create(user=user_test1)
        self.user_test_client = Token.objects.create(user=user_test_client)
        self.admin_token = Token.objects.create(user=admin)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user_test1_token.key}'
        )

    def test_residential_complex_list(self):
        response = self.client.get(reverse('list-complex'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_fail_complex_detail(self):
        response = self.client.get(reverse('detail-complex', kwargs={'pk': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_complex_detail(self):
        response = self.client.get(reverse('detail-complex', kwargs={'pk': self.first_complex.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invalid_complex(self):
        self.client.logout()
        response = self.client.post(reverse('create-complex'), self.data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_valid_complex(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.post(reverse('create-complex'), self.data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_valid_announcement(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test_client.key)
        response = self.client.post(reverse('create-announcement'), self.announcement_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_approve_announcement(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        response = self.client.put(reverse('approve-announcement', kwargs={'pk': self.first_announcement.id}),
                                   format='multipart')
        announcement = Announcement.objects.get(id=self.first_announcement.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(announcement.is_draft, True)

    def test_announcement_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test_client.key)
        response = self.client.get(reverse('list-announcement'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_invalid_announcement_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test_client.key)
        response = self.client.get(reverse('detail-announcement', kwargs={'pk': self.first_announcement.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_announcement_moderation_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        response = self.client.get(reverse('list-announcement-moderation'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_announcement_moderation_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        response = self.client.get(reverse('detail-announcement-moderation', kwargs={'pk': self.first_announcement.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_announcement_reject(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        response = self.client.patch(reverse('reject-announcement', kwargs={'pk': self.first_announcement.id}),
                                     format='multipart')
        announcement = Announcement.objects.get(id=self.first_announcement.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(announcement.reject, True)

    def test_request_to_chest_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_test1_token}')
        response = self.client.get(reverse('request-to-chest-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_request_to_chest_approve(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_test1_token}')
        create_response = self.client.post(reverse('request-to-chest-create'), data={
            'announcement': self.first_announcement.id,
            'residential_complex': self.first_complex.id
        }, format='multipart')
        response = self.client.put(reverse('request-to-chest-approve', kwargs={'pk': create_response.json().get('id')}))
        announcement = Announcement.objects.get(id=self.first_announcement.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(announcement.residential_complex, None)
