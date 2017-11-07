""" Main application API written in Restless with Django """
# pylint: disable=no-member
from datetime import datetime
from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from django.http import HttpResponse
from django.conf.urls import url
from django.contrib.auth.models import User
from boxer.models import Delivery,Profile,Offer,Picture,Schedule

CLIENT = 1
FREIGHTER = 2

class BaseResource(DjangoResource):

    def serialize_list(self, d):
        if d is None: return ''
        # Check for a ``Data``-like object. We should assume ``True`` (all
        # data gets prepared) unless it's explicitly marked as not.
        f = d.value if not getattr(d, 'should_prepare', True) else [self.prepare(i) for i in d]
        return self.serializer.serialize(f)

    def is_authenticated(self):
        """ Verifies authorization of modification of API objects """
        # Open everything wide!
        # DANGEROUS, DO NOT DO IN PRODUCTION.
        return True
        # An OAuth provider will be integrated.

        # Alternatively, if the user is logged into the site...
        # return self.request.user.is_authenticated()

        # Alternatively, you could check an API key. (Need a model for this...)
        # from myapp.models import ApiKey
        # try:
        #     key = ApiKey.objects.get(key=self.request.GET.get('api_key'))
        #     return True
        # except ApiKey.DoesNotExist:
        #     return False


class FreighterResource(BaseResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'address': 'address_line_1',
        'city': 'city',
        'state': 'state',
        'region': 'region',
        'postalcode': 'zipcode',
        'phone': 'phone',
        'ranking': 'ranking',
        'description': 'description',
        'photo': 'logo',
    })

    def list(self):
        return Profile.objects.filter(side=2)

    def detail(self, pk, **kwargs):
        return Profile.objects.get(side=2,id=pk)

    def create(self):
        freighter = Profile(
            address_line_1=self.data['address'],
            city=self.data['city'],
            state=self.data['state'],
            region=self.data['region'],
            zipcode=self.data['postalcode'],
            phone=self.data['phone'],
            ranking=self.data['ranking'],
            description=self.data['description'],
            logo=self.data['logo'],
            side=2
        )
        return freighter.save()

    def update(self, pk, **kwargs):
        try:
            freighter = Profile.objects.get(side=2,id=pk)
        except Profile.DoesNotExist:
            freighter = Profile()
        freighter.address_line_1 = self.data['address'],
        freighter.city = self.data['city'],
        freighter.state = self.data['state'],
        freighter.region = self.data['region'],
        freighter.zipcode = self.data['postalcode'],
        freighter.phone = self.data['phone'],
        freighter.ranking = self.data['ranking'],
        freighter.description = self.data['description'],
        freighter.logo = self.data['logo'],
        freighter.side = 1
        return freighter.save()

    def delete(self, pk, **kwargs):
        Profile.objects.get(side=2,id=pk)

class ClientResource(BaseResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'address': 'address_line_1',
        'city': 'city',
        'state': 'state',
        'region': 'region',
        'postalcode': 'zipcode',
        'phone': 'phone',
        'ranking': 'ranking',
        'description': 'description',
        'photo': 'logo',
    })

    def list(self):
        return Profile.objects.filter(side=1)

    def detail(self, pk, **kwargs):
        return Profile.objects.get(side=1,id=pk)

    def create(self):
        client = Profile(
            address_line_1=self.data['address'],
            city=self.data['city'],
            state=self.data['state'],
            region=self.data['region'],
            zipcode=self.data['postalcode'],
            phone=self.data['phone'],
            ranking=self.data['ranking'],
            description=self.data['description'],
            logo=self.data['logo'],
            side=1
        )
        return client.save()

    def update(self, pk, **kwargs):
        try:
            client = Profile.objects.get(side=1,id=pk)
        except Profile.DoesNotExist:
            client = Profile()
        client.address_line_1 = self.data['address'],
        client.city = self.data['city'],
        client.state = self.data['state'],
        client.region = self.data['region'],
        client.zipcode = self.data['postalcode'],
        client.phone = self.data['phone'],
        client.ranking = self.data['ranking'],
        client.description = self.data['description'],
        client.logo = self.data['logo'],
        client.side = 1
        return client.save()

    def delete(self, pk, **kwargs):
        Profile.objects.get(side=1,id=pk)

class ScheduleResource(BaseResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'delivery': 'delivery_id',
        'detail': 'schedule_detail',
        'payment': 'payment_detail',
        'start': 'start_time',
        'end': 'end_time'
    })

    def list(self):
        return Schedule.objects.all()

    def detail(self, pk, **kwargs):
        return Schedule.objects.get(id=pk)

    def create(self):
        sched = Schedule(
            delivery=Delivery.objects.get(id=self.data['delivery']),
            schedule_detail=self.data['detail'],
            payment_detail=self.data['payment'],
            start_time=datetime.strptime(self.data['start'], '%d-%m-%Y %H:%M'),
            end_time=datetime.strptime(self.data['end'], '%d-%m-%Y %H:%M')
        )
        return sched.save()

    def update(self, pk, **kwargs):
        try:
            sched = Schedule.objects.get(id=pk)
        except Schedule.DoesNotExist:
            sched = Schedule()
        sched.delivery = Delivery.objects.get(id=self.data['delivery'])
        sched.schedule_detail = self.data['detail']
        sched.payment_detail = self.data['payment']
        sched.start_time = datetime.strptime(self.data['start_time'], '%d-%m-%Y %H:%M')
        sched.end_time = datetime.strptime(self.data['end_time'], '%d-%m-%Y %H:%M')

    def delete(self, pk, **kwargs):
        return Schedule.objects.get(id=pk).delete()

class DeliveryResource(BaseResource):
    """ Prepares the Delivery Model as API Resource """
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'title': 'title',
        'deadline': 'deadline',
        'volume': 'volume',
        'weight': 'weight',
        'description': 'description'
    })

    # GET /kombi/deliveries/
    def list(self):
        """ Lists all delivery intances """
        return Delivery.objects.all()

    # GET /kombi/deliveries/<pk>/
    def detail(self, pk, **kwargs):
        """ Lists one specific delivery intances """
        return Delivery.objects.get(id=pk)

    # POST /kombi/deliveries/
    def create(self):
        delivery = Delivery(
            title=self.data['title'],
            departure_lat=self.data['departure_lat'],
            departure_lon=self.data['departure_lon'],
            arrival_lat=self.data['arrival_lat'],
            arrival_lon=self.data['arrival_lon'],
            deadline=datetime.strptime(self.data['deadline'], '%d-%m-%Y %H:%M'),
            volume=float(self.data['volume']),
            weight=float(self.data['weight']),
            description=self.data['description']
        )
        if 'freighter' in self.data.keys():
            delivery.freighter = Profile.objects.get(side=FREIGHTER, id=self.data['freighter'])
        return delivery.save()

    # PUT /kombi/deliveries/<pk>/
    def update(self, pk, **kwargs):
        try:
            delivery = Delivery.objects.get(id=pk)
        except Delivery.DoesNotExist:
            delivery = Delivery()
        delivery.title = self.data['title'],
        delivery.freighter = int(self.data['freighter'])
        delivery.departure = self.data['departure']
        delivery.arrival = self.data['arrival']
        delivery.deadline = datetime.strptime(self.data['deadline'], '%d-%m-%Y %H:%M')
        delivery.volume = float(self.data['volume'])
        delivery.weight = float(self.data['weight'])
        delivery.description = self.data['description']
        return delivery.save()

    # DELETE /kombi/deliveries/<pk>/
    def delete(self, pk, **kwargs):
        Delivery.objects.get(id=pk).delete()

    @classmethod
    def urls(cls, name_prefix=None):
        urlpatterns = super(DeliveryResource, cls).urls(name_prefix=name_prefix)
        return [
            url(r'^(?P<pk>\d+)/offers/(?P<i>\d+)', OfferResource.as_detail(), name='offer'),
            url(r'^(?P<pk>\d+)/offers', OfferResource.as_list(), name='offers'),
            url(r'^(?P<pk>\d+)/photos/(?P<i>\d+)', PhotoResource.as_detail(), name='photo'),
            url(r'^(?P<pk>\d+)/photos', PhotoResource.as_list(), name='photos'),
        ] + urlpatterns

class OfferResource(BaseResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'bidder': 'bidder_id',
        'delivery': 'delivery_id',
        'amount': 'amount'
    })

    def list(self, pk):
        return Offer.objects.filter(delivery=pk)

    def detail(self, pk, i, **kwargs):
        return Offer.objects.get(delivery=pk,id=i)

    def update(self, pk, i, **kwargs):
        try:
            offer = Offer.objects.get(delivery=pk,id=i)
        except Delivery.DoesNotExist:
            offer = Offer()
        offer.bidder = User.objects.get(id=self.data['bidder'])
        offer.delivery = Delivery.objects.get(id=pk)
        offer.amount = self.data['amount']
        return offer.save()

    def create(self, pk):
        offer = Offer(
            delivery=Delivery.objects.get(id=pk),
            bidder=User.objects.get(id=int(self.data['bidder'])),
            amount=float(self.data['amount'])
        )
        return offer.save()

    def delete(self, pk, i, **kwargs):
        Offer.objects.get(delivery=pk,id=i).delete()

class PhotoResource(BaseResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'owner': 'bidder_id',
        'delivery': 'delivery_id',
        'image': 'image'
    })

    def list(self, pk):
        return Picture.objects.filter(delivery=pk)

    def detail(self, pk, i, **kwargs):
        return Picture.objects.get(delivery=pk,id=i)

    def create(self):
        photo = Picture(
            delivery=Delivery.objects.get(id=pk),
            owner=User.objects.get(id=self.data['owner']),
            image=self.data('image')
        )
        return photo.save()

    def update(self, pk, i, **kwargs):
        try:
            photo = Picture.objects.get(delivery=pk,id=i)
        except Delivery.DoesNotExist:
            photo = Picture()
        photo.owner = User.objects.get(id=self.data['owner'])
        photo.delivery = Delivery.objects.get(id=pk)
        photo.image = self.data['image']
        return offer.save()

    def delete(self, pk, i, **kwargs):
        Picture.objects.get(delivery=pk,id=i).delete()
