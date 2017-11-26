from pymongo.write_concern import WriteConcern

class Category():
    id = fields.IntegerField(primary_key=True)
    name = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'pf'