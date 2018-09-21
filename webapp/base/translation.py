from django.utils import translation


class TranslatedField(object):
    def __init__(self, en_field, ca_field, es_field):
        self.en_field = en_field
        self.ca_field = ca_field
        self.es_field = es_field

    def __get__(self, instance, owner):
        en = getattr(instance, self.en_field)
        ca = getattr(instance, self.ca_field)
        es = getattr(instance, self.es_field)
        # TODO molts camps buits tenen '<html><head></head><body></body></html>' i son 39 caracters
        counter = 0
        fieldtype = owner._meta.get_field(self.en_field).get_internal_type()
        # raw_list = c._meta.get_fields_with_model()
        # parsed_list = [item[0].__class__.__name__ for item in raw_list._meta.get_fields_with_model()]
        # print (owner.__subclasses__())
        # print([f.get_internal_type() for f in owner._meta.get_fields()])

        if fieldtype in 'CharField' or fieldtype in 'TextField' and type(ca).__name__ in 'StreamValue':
            counter = 0
        elif fieldtype in 'TextField' and type(ca).__name__ not in 'StreamValue':
            counter = 39

        # print(self.ca_field, ca.__class__.__name__, len(ca), fieldtype, counter)

        if translation.get_language() == 'ca' and ca is not None and len(ca) > counter:
            return ca
        elif translation.get_language() == 'es' and es is not None and len(es) > counter:
            return es
        else:
            return en

    class Meta:
        abstract = True
