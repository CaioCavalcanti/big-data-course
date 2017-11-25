# Mongo Shell

## Starting the service
Just execute ```mongodb``` and let it open to keep it running
```
$ mongod
```

## Connecting to MongoDB
```
$ mongo
MongoDB shell version: 3.2.4
connecting to: test
Welcome to the MongoDB shell.
>
```

## Inserting a document (~~row~~)
```
> db.things.save({ a:1, b:2, c:3 })
WriteResult({ "nInserted" : 1 })

> db.things.save({ a:3, b:4, c:6, c:200 })
WriteResult({ "nInserted" : 1 })
```

In this case we're adding documents to ```things``` collection (~~table~~). You don't need to worry about the collection, if it exists or not, column definitions, etc. It will automatically create the collection, if it doesn't exist.

```
> db.things.save({ a:10, b:15, fruits:['apple', 'orange', 'pear']})
WriteResult({ "nInserted" : 1 })
```

**References**
- [save() definition](https://docs.mongodb.com/manual/reference/method/db.collection.save/)

### Getting documents
```
> db.things.find()
{ "_id" : ObjectId("5a195f13f4476b3b48738df6"), "a" : 1, "b" : 2, "c" : 3 }
{ "_id" : ObjectId("5a19603cf4476b3b48738df7"), "a" : 3, "b" : 4, "c" : 200 }
```
As you can see, the ObjectId was automatically generated. You can format the results using ```pretty()```

```
> db.things.find().pretty()
{ "_id" : ObjectId("5a195f13f4476b3b48738df6"), "a" : 1, "b" : 2, "c" : 3 }
{
        "_id" : ObjectId("5a19603cf4476b3b48738df7"),
        "a" : 3,
        "b" : 4,
        "c" : 200
}
{
        "_id" : ObjectId("5a196195f4476b3b48738df8"),
        "a" : 10,
        "b" : 15,
        "fruits" : [
                "apple",
                "orange",
                "pear"
        ]
}
```

The ```find()``` will return all results from the table, but you can use a where clause:

```
> db.things.find({a:1})
{ "_id" : ObjectId("5a195f13f4476b3b48738df6"), "a" : 1, "b" : 2, "c" : 3 }

> db.things.find({a: { $lt:2 }})
{ "_id" : ObjectId("5a195f13f4476b3b48738df6"), "a" : 1, "b" : 2, "c" : 3 }
>
```

You can also return a single document as result, using ```findOne()```.

```
> db.things.findOne({a:10})
{
        "_id" : ObjectId("5a196195f4476b3b48738df8"),
        "a" : 10,
        "b" : 15,
        "fruits" : [
                "apple",
                "orange",
                "pear"
        ]
}
```

**References**
- [Comparison query operators](https://docs.mongodb.com/manual/reference/operator/query-comparison/)
- [find() definition](https://docs.mongodb.com/manual/reference/method/db.collection.find/)

## Updating documents
```
TODO
```

## Working with variables
```
> var obj = db.things.findOne({a:10})
> obj
{
        "_id" : ObjectId("5a196195f4476b3b48738df8"),
        "a" : 10,
        "b" : 15,
        "fruits" : [
                "apple",
                "orange",
                "pear"
        ]
}
> obj.a
> 10
```

You can change the object properties, but it won't replicate to the database until you save the changes.

```
> obj.colors = ["blue", "red"]
[ "blue", "red" ]

> db.things.save(obj)
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
```