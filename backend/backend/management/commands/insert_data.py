import random

from backend.user.models import User
from system import models
from django.core.management.base import BaseCommand

city = ["Kyiv", "Kharkiv", "Odesa", "Lviv", "Dnipro", "Donetsk"]
district = ["Kyivskiy", "Odeskiy", "Dniprovskiy", "Kharkivskiy", "Donetskiy", "Lvivskiy"]
street = ["Kyivskiya", "Odeskiya", "Dniprovskiya", "Kharkivskiya", "Donetskiya", "Lvivskiya"]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(16):
            username = "username" + str(i)
            password = "Qwedvord123vlad"
            email = str(i) + "@gmail.com"
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()
            first_name = "first_name" + str(i)
            middle_name = "first_name" + str(i)
            last_name = "last_name" + str(i)
            gender_list = ['Male', 'Female']
            phone_number_1 = "+380" + str(random.randint(10000000, 999999999))
            phone_number = "+380" + str(random.randint(10000000, 999999999))
            tenant = models.Tenant.objects.create(first_name=first_name + "00", last_name=last_name + "00",
                                                  middle_name=middle_name + "00",
                                                  gender=random.choice(gender_list), phone_number=phone_number,
                                                  user=user)
            tenant.save()
            landlord = models.Landlord.objects.create(first_name=first_name, last_name=last_name,
                                                      middle_name=middle_name,
                                                      gender=random.choice(gender_list), phone_number=phone_number_1,
                                                      user=user)
            landlord.save()

            city_temp = random.choice(city)
            district_temp = random.choice(district)
            street_temp = random.choice(street)
            house_number = random.randint(1, 100)
            apartment_number = random.randint(1, 100)
            address = models.Address.objects.create(city=city_temp, district=district_temp,
                                                    street=street_temp,
                                                    house_number=house_number, apartment_number=apartment_number)
            address.save()

            cost = random.randint(100, 10000)
            area = random.randint(100, 10000)
            room_count = random.randint(1, 5)
            floor = random.randint(1, 16)
            apartment = models.Apartment.objects.create(cost=cost, area=area, room_count=room_count,
                                                        floor=floor, owner=landlord, tenant=tenant, address=address)
            apartment.save()

            contract = models.Contract.objects.create(is_active=True, owner=landlord, tenant=tenant,
                                                      apartment=apartment)

            contract.save()
            contractfile = models.ContractFile.objects.create(url="https://stackoverflow.com/questions"
                                                                  "/18834636/random-word-generator-python" + str(i),
                                                              file_hash="kdjsfkdjb", file_name="file" + str(i),
                                                              contract=contract)
            contractfile.save()
            ap_hidden_photo = models.ApartmentHiddenPhoto.objects.create(url="https://stackoverflow.com/questions"
                                                                             "/18834636/random-word-generator-python"
                                                                             + str(i), image_name="djklgfnlds",
                                                                         contract=contract)
            ap_hidden_photo.save()
            ap_photo = models.ApartmentPhoto.objects.create(url="https://stackoverflow.com/questions"
                                                                "/18834636/random-word-generator-python"
                                                                + str(i), image_name="djklgfnlds",
                                                            apartment=apartment)
            ap_photo.save()
            u_bills = models.UtilityBills.objects.create(gas_supply=random.randint(1, 100),
                                                         water_supply=random.randint(1, 100),
                                                         electricity=random.randint(1, 100),
                                                         apartment=apartment)
            u_bills.save()
