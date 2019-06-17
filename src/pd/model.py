
import validate


class Schema:
    ROOT = 'Employees'
    EMP_TAG = "Person"
    EMP_KEY = 'id'

    emp_fields = [
        'name',
        'phone_no',
        'house_no',
        'street',
        'city',
        'postcode',
    ]


def validate_schema(emp_datum):
    """Validate the schema of the source data.

    >>> data = {'000': {
    ...             'name': '', 'phone_no': '',
    ...             'house_no': '', 'street': '', 'city': '', 'postcode': '',
    ...         }}
    >>> failed = validate_schema(data)
    >>> print failed
    False
    """

    field_template = Schema.emp_fields

    failed = {}
    # For each item check each if it's field names follow the schema
    for key, emp_data in emp_datum.iteritems():
        fields = emp_data.keys()
        for field_name in fields[:]:
            if field_name in field_template:
                fields.remove(field_name)

        if fields:
            msg = "Person (id:{0}) has field mismatch: '{1}'.".format(
                    key, fields)
            failed[key] = {
                'type': 'missing_fields',
                'meta': fields,
                'msg': msg,
                }
    if failed:
        return failed
    else:
        return False


@validate.do_ensure
class Employee:
    """ Class to contain data pertaining to a person employeed by the company.

    >>> person_data = {
    ...     'key': '111', 'name': '', 'phone_no': '(11) 1111 1111',
    ...     'house_no': '11', 'street': '', 'city': '', 'postcode': '2000',
    ...         }
    >>> print Employee(**person_data)
    Employee:
        key: 111, name: '', phone_no: '(11) 1111 1111',
        house_no: 11, street: '',
        city: '', postcode: 2000
    """

    key = validate.Ensure(validate.is_valid_key)
    name = validate.Ensure(validate.is_non_empty_str)

    house_no = validate.Ensure(validate.is_non_empty_int)
    street = validate.Ensure(validate.is_non_empty_str)
    city = validate.Ensure(validate.is_non_empty_str)
    postcode = validate.Ensure(validate.is_valid_postcode)

    phone_no = validate.Ensure(validate.is_valid_phone_number)

    def __init__(self, key, name, phone_no,
                 house_no, street, city, postcode):
        self.key = int(key)
        self.name = name
        self.phone_no = phone_no

        self.house_no = int(house_no)
        self.street = street
        self.city = city
        self.postcode = int(postcode)

    def __repr__(self):
        return (
            """Employee:
    key: {0.key!r}, name: {0.name!r}, phone_no: {0.phone_no!r},
    house_no: {0.house_no!r}, street: {0.street!r},
    city: {0.city!r}, postcode: {0.postcode!r}""".format(self)
            )


if __name__ == "__main__":
    import doctest
    doctest.testmod()
