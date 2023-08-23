from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Outlet

class OutletForm(ModelForm):
    class Meta:
        # merelasikan form dengan model
        model = Outlet
        # mengeset field apa saja yang akan ditampilkan pada form
        fields = ('name', 'address')
        # mengatur teks label untuk setiap field
        labels = {
            'name': _('Nama Outlet'),
            'address': _('Alamat Outlet'),
        }
        # mengatur teks pesan error untuk setiap validasi fieldnya
        error_messages = {
            'name': {
                'required': _("Nama outlet harus diisi."),
            },
            'address': {
                'required': _("Alamat outlet harus diisi."),
            },
        }
